import json
import os
import requests

# -----------------------------
# Configuración
# -----------------------------
CONTEXT_PATH = "./contextos"
HISTORIAL_PATH = "./historial"
OLLAMA_URL = "http://localhost:11434/v1/chat/completions"
MODEL = "llama3.1:latest"

# -----------------------------
# Funciones de contexto
# -----------------------------
def cargar_contexto(nombre_persona):
    """Carga el JSON de contexto de la persona"""
    archivo = os.path.join(CONTEXT_PATH, f"{nombre_persona}.json")
    if not os.path.exists(archivo):
        raise FileNotFoundError(f"No se encontró el contexto: {archivo}")
    with open(archivo, "r") as f:
        return json.load(f)

# -----------------------------
# Funciones de historial
# -----------------------------
def cargar_historial(nombre_persona):
    """Carga historial previo de conversaciones"""
    archivo = os.path.join(HISTORIAL_PATH, f"{nombre_persona}_history.txt")
    if os.path.exists(archivo):
        with open(archivo, "r") as f:
            lines = f.readlines()
        historial = []
        for i in range(0, len(lines), 2):
            user_line = lines[i].strip().replace("Usuario: ", "")
            assistant_line = lines[i+1].strip().replace(f"{nombre_persona.capitalize()}: ", "")
            historial.append({"role": "user", "content": user_line})
            historial.append({"role": "assistant", "content": assistant_line})
        return historial
    return []

def guardar_historial(nombre_persona, pregunta, respuesta):
    """Guarda pregunta y respuesta en historial"""
    archivo = os.path.join(HISTORIAL_PATH, f"{nombre_persona}_history.txt")
    with open(archivo, "a") as f:
        f.write(f"Usuario: {pregunta}\n{nombre_persona.capitalize()}: {respuesta}\n")

# -----------------------------
# Generar mensajes para la API
# -----------------------------
def generar_mensajes(contexto, historial, pregunta):
    """Crea la lista de mensajes para chat completions, incluyendo contexto"""
    system_msg = {
        "role": "system",
        "content": (
            f"Contexto de la persona:\n"
            f"Nombre: {contexto['nombre']}\n"
            f"Relación: {contexto['relacion']}\n"
            f"Personalidad: {contexto['personalidad']}\n"
            f"Proyectos: {'; '.join(contexto['proyectos'])}\n\n"
            "Instrucciones:\n"
            "1. Actúa como esta persona en la conversación.\n"
            "2. Responde de forma natural y coherente.\n"
            "3. Mantén memoria del contexto y del historial.\n"
            "4. Si no sabes algo, responde educadamente sin inventar."
        )
    }
    messages = [system_msg] + historial
    messages.append({"role": "user", "content": pregunta})
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
            headers={"Content-Type": "application/json"},
            json={
                "model": MODEL,
                "messages": messages,
                "n": 1
            },
            timeout=30
        )
        response.raise_for_status()  # Detecta errores HTTP
        data = response.json()
        salida = data['choices'][0]['message']['content']

        # Guardar en historial
        guardar_historial(nombre_persona, pregunta, salida)

        return salida

    except requests.RequestException as e:
        print("Error al conectar con Ollama:", e)
        return None
    except (KeyError, IndexError, json.JSONDecodeError) as e:
        print("Error procesando la respuesta de Ollama:", e)
        print("Texto crudo devuelto:")
        print(response.text)
        return None

# -----------------------------
# Ejemplo de uso
# -----------------------------
if __name__ == "__main__":
    persona = "jandro"
    pregunta = "¿Dónde vamos a llevar las cajas?"

    respuesta = preguntar_a_ollama(persona, pregunta)
    if respuesta:
        print(f"{persona.capitalize()}: {respuesta}")

