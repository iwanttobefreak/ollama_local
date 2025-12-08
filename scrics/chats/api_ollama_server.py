from flask import Flask, request, Response
import json
import os
import shutil
from datetime import datetime
import requests

# -----------------------------
# Configuración Ollama
# -----------------------------
OLLAMA_URL = "http://localhost:11434/api/chat"
MODEL_NAME = "llama3.1:8b"
HISTORIAL_DIR = "historial"
CONTEXTOS_DIR = "contextos"

# -----------------------------
# Funciones de contexto
# -----------------------------
def cargar_contexto(nombre_persona):
    archivo = os.path.join(CONTEXTOS_DIR, f"{nombre_persona}.json")
    if not os.path.exists(archivo):
        return ""
    with open(archivo, "r", encoding="utf-8") as f:
        data = json.load(f)

    contexto = f"Nombre: {data.get('nombre', '')}\n"
    contexto += f"Relación con el usuario: {data.get('relacion', '')}\n"
    contexto += f"Personalidad: {data.get('personalidad', '')}\n"
    proyectos = data.get("proyectos", [])
    if proyectos:
        contexto += "Proyectos y actividades:\n"
        for p in proyectos:
            contexto += f"- {p}\n"
    return contexto.strip()

# -----------------------------
# Funciones de historial
# -----------------------------
def cargar_historial(nombre_persona):
    archivo = os.path.join(HISTORIAL_DIR, f"{nombre_persona}_history.txt")
    if not os.path.exists(archivo):
        return []
    with open(archivo, "r", encoding="utf-8") as f:
        lines = f.readlines()

    historial = []
    i = 0
    while i < len(lines):
        line = lines[i].strip()
        if line.startswith("Usuario: "):
            user_line = line.replace("Usuario: ", "")
            if i + 1 < len(lines):
                assistant_line = lines[i + 1].strip()
                if ": " in assistant_line:
                    assistant_line = assistant_line.split(": ", 1)[1]
                historial.append({"role": "user", "content": str(user_line)})
                historial.append({"role": "assistant", "content": str(assistant_line)})
            i += 2
        else:
            i += 1
    return historial

def guardar_historial(nombre_persona, user_msg, assistant_msg):
    archivo = os.path.join(HISTORIAL_DIR, f"{nombre_persona}_history.txt")
    with open(archivo, "a", encoding="utf-8") as f:
        f.write(f"Usuario: {user_msg}\n")
        f.write(f"{nombre_persona.capitalize()}: {assistant_msg}\n")

def generar_mensajes(contexto, historial, pregunta):
    messages = []
    if contexto:
        messages.append({"role": "system", "content": str(contexto)})
    if historial:
        for m in historial:
            messages.append({"role": m["role"], "content": str(m["content"])})
    messages.append({"role": "user", "content": str(pregunta)})
    return messages

# -----------------------------
# Función principal
# -----------------------------
def preguntar_a_ollama(nombre_persona, pregunta):
    contexto = cargar_contexto(nombre_persona)
    historial = cargar_historial(nombre_persona)
    messages = generar_mensajes(contexto, historial, pregunta)

    try:
        response = requests.post(
            OLLAMA_URL,
            json={
                "model": MODEL_NAME,
                "messages": messages,
                "stream": False
            }
        )
        response.raise_for_status()
        data = response.json()
        assistant_msg = data["message"]["content"]

        # Guardar en historial
        guardar_historial(nombre_persona, pregunta, assistant_msg)

        return assistant_msg
    except Exception as e:
        print("Error al preguntar a Ollama:", e)
        return None

# -----------------------------
# Función para verificar Ollama
# -----------------------------
def verificar_ollama():
    try:
        response = requests.get("http://localhost:11434/api/tags", timeout=5)
        if response.status_code == 200:
            models = response.json().get("models", [])
            model_names = [model["name"] for model in models]
            if MODEL_NAME in model_names:
                print(f"✅ Modelo {MODEL_NAME} disponible")
                return True
            else:
                print(f"❌ Modelo {MODEL_NAME} no encontrado. Modelos disponibles: {model_names}")
                return False
        else:
            print("❌ Ollama no responde correctamente")
            return False
    except Exception as e:
        print(f"❌ Error conectando con Ollama: {e}")
        return False
def resumir_historial(nombre_persona):
    archivo = os.path.join(HISTORIAL_DIR, f"{nombre_persona}_history.txt")
    if not os.path.exists(archivo):
        return False

    # Backup del historial antiguo
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_file = f"{archivo}_{timestamp}"
    shutil.copy2(archivo, backup_file)

    # Cargar historial completo
    historial = cargar_historial(nombre_persona)
    if not historial:
        return False

    # Generar resumen como string manteniendo formato Usuario/Asistente
    resumen_texto = "\n".join([f"{m['role'].capitalize()}: {m['content']}" for m in historial])

    prompt_resumen = (
        "Usuario: Resumen del historial previo\n"
        f"{nombre_persona.capitalize()}: Resume la conversación anterior de forma concisa, "
        "manteniendo el formato Usuario/Asistente para que pueda seguir siendo leído por la API:\n\n"
        f"{resumen_texto}"
    )

    contexto = cargar_contexto(nombre_persona)

    try:
        response = requests.post(
            OLLAMA_URL,
            json={
                "model": MODEL_NAME,
                "messages": [
                    {"role":"system", "content": contexto if contexto else "Eres un asistente útil que resume conversaciones."},
                    {"role":"user","content": prompt_resumen}
                ],
                "stream": False
            }
        )
        response.raise_for_status()
        data = response.json()
        resumen = data["message"]["content"]

        # Guardar resumen en el historial
        with open(archivo, "w", encoding="utf-8") as f:
            f.write(resumen)

        return True
    except Exception as e:
        print("Error al resumir historial:", e)
        return False

# -----------------------------
# API Flask
# -----------------------------
app = Flask(__name__)

@app.route("/preguntar", methods=["POST"])
def preguntar():
    data = request.get_json()
    if not data or "persona" not in data or "pregunta" not in data:
        return Response(
            json.dumps({"error": "Faltan parámetros 'persona' y 'pregunta'"}, ensure_ascii=False),
            mimetype="application/json",
            status=400
        )

    persona = data["persona"]
    pregunta = data["pregunta"]

    respuesta = preguntar_a_ollama(persona, pregunta)
    if respuesta is None:
        return Response(
            json.dumps({"error": "No se pudo obtener respuesta de Ollama"}, ensure_ascii=False),
            mimetype="application/json",
            status=500
        )

    return Response(
        json.dumps({"persona": persona, "pregunta": pregunta, "respuesta": respuesta}, ensure_ascii=False),
        mimetype="application/json"
    )

@app.route("/resumir", methods=["POST"])
def resumir():
    data = request.get_json()
    if not data or "persona" not in data:
        return Response(
            json.dumps({"error": "Falta parámetro 'persona'"}, ensure_ascii=False),
            mimetype="application/json",
            status=400
        )
    persona = data["persona"]
    exito = resumir_historial(persona)
    if not exito:
        return Response(
            json.dumps({"error": f"No se pudo resumir historial de {persona}"}, ensure_ascii=False),
            mimetype="application/json",
            status=500
        )
    return Response(
        json.dumps({"mensaje": f"Historial de {persona} resumido correctamente"}, ensure_ascii=False),
        mimetype="application/json"
    )

if __name__ == "__main__":
    print("🚀 Iniciando API Ollama Server...")
    print(f"📡 Ollama URL: {OLLAMA_URL}")
    print(f"🤖 Modelo: {MODEL_NAME}")

    # Verificar que Ollama esté disponible
    if not verificar_ollama():
        print("❌ No se puede iniciar la API sin Ollama funcionando correctamente")
        exit(1)

    print("🌐 Iniciando servidor Flask en puerto 5000...")
    app.run(host="0.0.0.0", port=5000, debug=True)

