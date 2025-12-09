from flask import Flask, request, Response
import json
import os
import shutil
from datetime import datetime
import requests

# ...existing code...

app = Flask(__name__)

# --- Endpoint para añadir eventos ---
@app.route("/anadir_evento", methods=["POST"])
def anadir_evento():
    logger.info("🔄 Endpoint /anadir_evento llamado")
    try:
        data = request.get_json()
        logger.debug(f"📥 Datos recibidos: {data}")

        required = ["persona", "tipo", "nombre", "lugar", "fecha"]
        if not data or not all(k in data for k in required):
            logger.warning("❌ Faltan parámetros obligatorios: persona, tipo, nombre, lugar, fecha")
            return Response(
                json.dumps({"error": "Faltan parámetros obligatorios: persona, tipo, nombre, lugar, fecha"}, ensure_ascii=False),
                mimetype="application/json",
                status=400
            )

        persona = data["persona"]
        evento = {
            "tipo": data["tipo"],
            "nombre": data["nombre"],
            "lugar": data["lugar"],
            "fecha": data["fecha"]
        }
        if "notas" in data:
            evento["notas"] = data["notas"]

        archivo = os.path.join(CONTEXTOS_DIR, f"{persona}.json")
        if os.path.exists(archivo):
            with open(archivo, "r", encoding="utf-8") as f:
                datos = json.load(f)
        else:
            datos = {"nombre": persona, "eventos": []}

        if "eventos" not in datos or not isinstance(datos["eventos"], list):
            datos["eventos"] = []
        datos["eventos"].append(evento)

        with open(archivo, "w", encoding="utf-8") as f:
            json.dump(datos, f, ensure_ascii=False, indent=2)

        logger.info(f"✅ Evento añadido para {persona}")
        return Response(
            json.dumps({"mensaje": f"Evento añadido para {persona}"}, ensure_ascii=False),
            mimetype="application/json"
        )

    except Exception as e:
        logger.error(f"❌ Error inesperado en endpoint /anadir_evento: {e}")
        logger.error(f"   Traceback: {traceback.format_exc()}")
        return Response(
            json.dumps({"error": "Error interno del servidor"}, ensure_ascii=False),
            mimetype="application/json",
            status=500
        )
from flask import Flask, request, Response
import json
import os
import shutil
from datetime import datetime
import requests
import logging
import traceback

# Configurar logging detallado
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('/app/chats/api_ollama_server.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# -----------------------------
# Configuración Ollama
# -----------------------------
OLLAMA_URL = "http://localhost:11434/api/chat"
MODEL_NAME = "llama3.2:1b"
HISTORIAL_DIR = "/app/chats/historial"
CONTEXTOS_DIR = "/app/chats/contextos"

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

    eventos = data.get("eventos", [])
    if eventos:
        contexto += "Eventos importantes:\n"
        for e in eventos:
            tipo = e.get('tipo', '')
            nombre = e.get('nombre', '')
            lugar = e.get('lugar', '')  
            fecha = e.get('fecha', '')
            notas = e.get('notas', '')
            contexto += f"- {tipo}: {nombre} en {lugar} el {fecha}"
            if notas:
                contexto += f" | Notas: {notas}"
            contexto += "\n"

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

def procesar_resumen_formato(resumen_completo, nombre_persona):
    """
    Procesa el resumen generado por Ollama para asegurar que tenga el formato correcto
    Usuario: [mensaje] \n Persona: [respuesta]
    """
    logger.debug("🔧 Procesando formato del resumen...")

    # Limpiar y dividir el resumen en líneas
    lineas = [line.strip() for line in resumen_completo.split('\n') if line.strip()]

    # Buscar líneas que empiecen con "Usuario:" o el nombre de la persona
    usuario_line = None
    persona_line = None

    for linea in lineas:
        if linea.lower().startswith('usuario:'):
            usuario_line = linea
        elif linea.lower().startswith(f'{nombre_persona.lower()}:'):
            persona_line = linea

    # Si no encontramos el formato esperado, crear uno básico
    if not usuario_line or not persona_line:
        logger.warning("⚠️ Resumen no tiene formato esperado, creando formato básico")

        # Crear un resumen consolidado
        resumen_limpio = resumen_completo.replace('\n', ' ').strip()

        usuario_line = f"Usuario: Conversación resumida con {nombre_persona}"
        persona_line = f"{nombre_persona.capitalize()}: {resumen_limpio}"

    # Asegurar que las líneas terminen correctamente
    if not usuario_line.endswith('\n'):
        usuario_line += '\n'
    if not persona_line.endswith('\n'):
        persona_line += '\n'

    resumen_formateado = usuario_line + persona_line
    logger.debug(f"✅ Resumen formateado: {len(resumen_formateado)} caracteres")
    return resumen_formateado

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
    logger.debug(f"🤖 Preguntando a Ollama para {nombre_persona}")

    try:
        contexto = cargar_contexto(nombre_persona)
        logger.debug(f"🎭 Contexto cargado, longitud: {len(contexto) if contexto else 0}")

        historial = cargar_historial(nombre_persona)
        logger.debug(f"📚 Historial cargado con {len(historial)} mensajes")

        messages = generar_mensajes(contexto, historial, pregunta)
        logger.debug(f"📝 Mensajes preparados: {len(messages)} mensajes")

        logger.info("📤 Enviando petición a Ollama...")
        response = requests.post(
            OLLAMA_URL,
            json={
                "model": MODEL_NAME,
                "messages": messages,
                "stream": False
            },
            timeout=60
        )

        logger.debug(f"📥 Respuesta de Ollama: status={response.status_code}")

        if response.status_code != 200:
            logger.error(f"❌ Error HTTP de Ollama: {response.status_code} - {response.text}")
            return None

        response.raise_for_status()
        data = response.json()

        if "message" not in data or "content" not in data["message"]:
            logger.error(f"❌ Respuesta de Ollama malformada: {data}")
            return None

        assistant_msg = data["message"]["content"]
        logger.info(f"✅ Respuesta generada, longitud: {len(assistant_msg)} caracteres")

        # Guardar en historial
        logger.debug("💾 Guardando en historial...")
        guardar_historial(nombre_persona, pregunta, assistant_msg)
        logger.debug("💾 Historial guardado")

        return assistant_msg

    except requests.exceptions.Timeout:
        logger.error("❌ Timeout conectando con Ollama")
        return None
    except requests.exceptions.ConnectionError:
        logger.error("❌ Error de conexión con Ollama")
        return None
    except requests.exceptions.RequestException as e:
        logger.error(f"❌ Error en petición HTTP a Ollama: {e}")
        return None
    except json.JSONDecodeError as e:
        logger.error(f"❌ Error decodificando JSON de Ollama: {e}")
        return None
    except Exception as e:
        logger.error(f"❌ Error inesperado en preguntar_a_ollama: {e}")
        logger.error(f"   Traceback: {traceback.format_exc()}")
        return None

# -----------------------------
# Función para verificar Ollama
# -----------------------------
def verificar_ollama():
    logger.info("🔍 Verificando conectividad con Ollama...")
    try:
        response = requests.get("http://localhost:11434/api/tags", timeout=10)
        logger.debug(f"📥 Respuesta de /api/tags: status={response.status_code}")

        if response.status_code == 200:
            data = response.json()
            models = data.get("models", [])
            model_names = [model["name"] for model in models]
            logger.info(f"📋 Modelos disponibles: {model_names}")

            if MODEL_NAME in model_names:
                logger.info(f"✅ Modelo {MODEL_NAME} disponible")
                return True
            else:
                logger.error(f"❌ Modelo {MODEL_NAME} no encontrado. Modelos disponibles: {model_names}")
                return False
        else:
            logger.error(f"❌ Ollama no responde correctamente: {response.status_code} - {response.text}")
            return False

    except requests.exceptions.Timeout:
        logger.error("❌ Timeout conectando con Ollama")
        return False
    except requests.exceptions.ConnectionError:
        logger.error("❌ Error de conexión con Ollama")
        return False
    except Exception as e:
        logger.error(f"❌ Error inesperado verificando Ollama: {e}")
        logger.error(f"   Traceback: {traceback.format_exc()}")
        return False
def resumir_historial(nombre_persona):
    logger.info(f"🔍 Iniciando resumen para persona: {nombre_persona}")
    logger.debug(f"📍 Directorio de trabajo actual: {os.getcwd()}")
    logger.debug(f"📂 HISTORIAL_DIR configurado como: {HISTORIAL_DIR}")
    logger.debug(f"📂 Ruta completa del historial: {os.path.abspath(HISTORIAL_DIR)}")

    try:
        # Verificar que el directorio existe
        if not os.path.exists(HISTORIAL_DIR):
            logger.error(f"❌ Directorio HISTORIAL_DIR no existe: {HISTORIAL_DIR}")
            return False

        # Buscar archivo de historial (case-insensitive)
        nombre_persona_lower = nombre_persona.lower()
        logger.debug(f"🔍 Buscando archivo para: {nombre_persona_lower}_history.txt")

        historial_files = [f for f in os.listdir(HISTORIAL_DIR) if f.endswith('_history.txt')]
        logger.debug(f"📋 Archivos encontrados en {HISTORIAL_DIR}: {historial_files}")

        archivo = None
        for hist_file in historial_files:
            logger.debug(f"🔍 Comparando '{hist_file.lower()}' con '{nombre_persona_lower}_history.txt'")
            if hist_file.lower() == f"{nombre_persona_lower}_history.txt":
                archivo = os.path.join(HISTORIAL_DIR, hist_file)
                logger.info(f"✅ Archivo encontrado: {archivo}")
                break

        if not archivo or not os.path.exists(archivo):
            logger.error(f"❌ No se encontró archivo de historial para {nombre_persona}")
            return False

        # Verificar permisos de lectura
        if not os.access(archivo, os.R_OK):
            logger.error(f"❌ No hay permisos de lectura para: {archivo}")
            return False

        # Leer contenido del archivo
        logger.debug(f"📖 Leyendo archivo: {archivo}")
        with open(archivo, 'r', encoding='utf-8') as f:
            contenido = f.read()

        logger.debug(f"📖 Archivo leído exitosamente. Longitud: {len(contenido)} caracteres")

        # Verificar que hay contenido
        if not contenido.strip():
            logger.warning("⚠️ El archivo está vacío")
            return False

        # Backup del historial antiguo
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_file = f"{archivo}_{timestamp}"
        logger.debug(f"💾 Creando backup: {backup_file}")
        shutil.copy2(archivo, backup_file)

        # Cargar historial completo
        logger.debug("📚 Cargando historial completo...")
        historial = cargar_historial(nombre_persona)
        if not historial:
            logger.warning("⚠️ No se pudo cargar el historial")
            return False

        logger.debug(f"📚 Historial cargado con {len(historial)} mensajes")

        # Generar resumen como string manteniendo formato Usuario/Asistente
        resumen_texto = "\n".join([f"{m['role'].capitalize()}: {m['content']}" for m in historial])
        logger.debug(f"📝 Texto a resumir generado, longitud: {len(resumen_texto)}")

        # Preparar prompt para Ollama - MODIFICADO para mantener formato
        contexto = cargar_contexto(nombre_persona)
        logger.debug(f"🎭 Contexto cargado, longitud: {len(contexto) if contexto else 0}")

        prompt_resumen = (
            f"Eres {nombre_persona}. Has tenido una conversación larga con un usuario. "
            "Necesito que resumes toda la conversación anterior de manera concisa pero completa.\n\n"
            f"CONVERSACIÓN ANTERIOR:\n{resumen_texto}\n\n"
            "INSTRUCCIONES IMPORTANTES:\n"
            "1. Resume la conversación manteniendo los puntos clave y decisiones importantes\n"
            "2. DEBES responder EXACTAMENTE en este formato:\n"
            "Usuario: [resumen de lo que preguntó el usuario en la conversación]\n"
            f"{nombre_persona.capitalize()}: [tu respuesta resumida como asistente]\n"
            "3. Si hay múltiples temas, consolídalos en una sola interacción Usuario/Asistente\n"
            "4. No agregues texto adicional, solo estas dos líneas\n\n"
            "Ejemplo:\n"
            "Usuario: El usuario preguntó sobre mis proyectos, personalidad y actividades\n"
            f"{nombre_persona.capitalize()}: Soy una persona creativa con varios proyectos en marcha, incluyendo desarrollo de software y escritura técnica.\n\n"
            "Ahora resume la conversación anterior:"
        )

        logger.info("🤖 Enviando petición a Ollama para resumir historial...")

        response = requests.post(
            OLLAMA_URL,
            json={
                "model": MODEL_NAME,
                "messages": [
                    {"role": "system", "content": contexto if contexto else "Eres un asistente útil que resume conversaciones."},
                    {"role": "user", "content": prompt_resumen}
                ],
                "stream": False
            },
            timeout=120  # Aumentar timeout
        )

        logger.debug(f"📥 Respuesta de Ollama: status={response.status_code}")

        if response.status_code != 200:
            logger.error(f"❌ Error HTTP de Ollama: {response.status_code} - {response.text}")
            return False

        response.raise_for_status()
        data = response.json()

        if "message" not in data or "content" not in data["message"]:
            logger.error(f"❌ Respuesta de Ollama malformada: {data}")
            return False

        resumen_completo = data["message"]["content"]
        logger.info(f"✅ Resumen generado exitosamente, longitud: {len(resumen_completo)} caracteres")

        # Procesar el resumen para asegurar formato correcto
        resumen_formateado = procesar_resumen_formato(resumen_completo, nombre_persona)
        logger.debug(f"📝 Resumen formateado, longitud: {len(resumen_formateado)}")

        # Verificar permisos de escritura
        if not os.access(archivo, os.W_OK):
            logger.error(f"❌ No hay permisos de escritura para: {archivo}")
            return False

        # Guardar resumen formateado en el historial
        logger.debug(f"💾 Guardando resumen formateado en: {archivo}")
        with open(archivo, "w", encoding="utf-8") as f:
            f.write(resumen_formateado)

        logger.info(f"💾 Resumen guardado exitosamente en {archivo}")
        return True

    except FileNotFoundError as e:
        logger.error(f"❌ Archivo no encontrado: {e}")
        logger.error(f"   Traceback: {traceback.format_exc()}")
        return False
    except PermissionError as e:
        logger.error(f"❌ Error de permisos: {e}")
        logger.error(f"   Traceback: {traceback.format_exc()}")
        return False
    except requests.exceptions.RequestException as e:
        logger.error(f"❌ Error de conexión con Ollama: {e}")
        logger.error(f"   Traceback: {traceback.format_exc()}")
        return False
    except json.JSONDecodeError as e:
        logger.error(f"❌ Error decodificando JSON de Ollama: {e}")
        logger.error(f"   Traceback: {traceback.format_exc()}")
        return False
    except Exception as e:
        logger.error(f"❌ Error inesperado en resumir_historial: {e}")
        logger.error(f"   Tipo de error: {type(e).__name__}")
        logger.error(f"   Traceback completo: {traceback.format_exc()}")
        return False

# -----------------------------
# API Flask
# -----------------------------
app = Flask(__name__)


# --- Endpoint para añadir eventos con texto coloquial ---
@app.route("/anadir_evento_colloquial", methods=["POST"])
def anadir_evento_colloquial():
    logger.info("🔄 Endpoint /anadir_evento_colloquial llamado")
    try:
        data = request.get_json()
        logger.debug(f"📥 Datos recibidos: {data}")
        if not data or "texto" not in data:
            logger.warning("❌ Falta parámetro 'texto'")
            return Response(
                json.dumps({"error": "Falta parámetro 'texto'"}, ensure_ascii=False),
                mimetype="application/json",
                status=400
            )
        texto = data["texto"]
        # Prompt aún más detallado para extracción
        prompt = (
            "Extrae los siguientes campos de evento de este texto y devuélvelos en JSON válido con las claves: persona, tipo, nombre, lugar, fecha, notas.\n"
            "- Si aparece 'con [nombre]' en el texto, pon ese nombre en el campo 'persona'.\n"
            "- El campo 'tipo' debe ser la actividad principal (por ejemplo: cena, comida, concierto).\n"
            "- El campo 'nombre' debe ser el nombre del restaurante, artista, lugar, etc.\n"
            "- El campo 'lugar' es la ciudad o localización.\n"
            "- El campo 'fecha' es la fecha del evento.\n"
            "- El campo 'notas' es cualquier detalle adicional.\n"
            "No inventes datos, pero usa la información que encuentres en el texto. Si algún campo no está, déjalo vacío.\n"
            "\nEjemplo 1:\n"
            "TEXTO: he ido con Laia a cenar al restaurante Coque de Madrid el 8 de diciembre de 2025 y me gustó mucho la comida\n"
            "JSON:\n"
            "{\n  \"persona\": \"Laia\",\n  \"tipo\": \"cena\",\n  \"nombre\": \"Coque\",\n  \"lugar\": \"Madrid\",\n  \"fecha\": \"8 de diciembre de 2025\",\n  \"notas\": \"Me gustó mucho la comida\"\n}\n"
            "\nEjemplo 2:\n"
            "TEXTO: fuimos con Jandro al concierto de Vetusta Morla en WiZink Center el 5 de mayo de 2024, fue espectacular\n"
            "JSON:\n"
            "{\n  \"persona\": \"Jandro\",\n  \"tipo\": \"concierto\",\n  \"nombre\": \"Vetusta Morla\",\n  \"lugar\": \"WiZink Center\",\n  \"fecha\": \"5 de mayo de 2024\",\n  \"notas\": \"fue espectacular\"\n}\n"
            f"\nTEXTO: {texto}\nJSON:"
        )
        messages = [{"role": "user", "content": prompt}]
        response = requests.post(
            OLLAMA_URL,
            json={
                "model": MODEL_NAME,
                "messages": messages,
                "stream": False
            },
            timeout=60
        )
        logger.debug(f"📥 Respuesta de Ollama: status={response.status_code}")
        if response.status_code != 200:
            logger.error(f"❌ Error HTTP de Ollama: {response.status_code} - {response.text}")
            return Response(
                json.dumps({"error": "No se pudo obtener respuesta de Ollama"}, ensure_ascii=False),
                mimetype="application/json",
                status=500
            )
        data_ollama = response.json()
        if "message" not in data_ollama or "content" not in data_ollama["message"]:
            logger.error(f"❌ Respuesta de Ollama malformada: {data_ollama}")
            return Response(
                json.dumps({"error": "Respuesta de Ollama malformada"}, ensure_ascii=False),
                mimetype="application/json",
                status=500
            )
        # Intentar extraer el primer bloque JSON de la respuesta
        import re
        import json as pyjson
        respuesta_llm = data_ollama["message"]["content"]
        logger.debug(f"📝 Respuesta LLM: {respuesta_llm}")
        # Buscar todos los bloques JSON válidos
        matches = re.findall(r'\{[\s\S]*?\}', respuesta_llm)
        if not matches:
            logger.error("❌ No se encontró JSON en la respuesta de Ollama")
            return Response(
                json.dumps({"error": "No se encontró JSON en la respuesta de Ollama"}, ensure_ascii=False),
                mimetype="application/json",
                status=500
            )
        evento = None
        for bloque in matches:
            try:
                posible = pyjson.loads(bloque)
            except Exception as e:
                continue
            # Si es un dict con campos relevantes y no todos vacíos
            campos = ["persona", "tipo", "nombre", "lugar", "fecha"]
            if all(k in posible for k in campos) and any(posible.get(k) for k in campos):
                evento = posible
                break
            # Si es un dict con 'eventos' como lista, usar el primer evento válido
            if "eventos" in posible and isinstance(posible["eventos"], list):
                for ev in posible["eventos"]:
                    if all(k in ev for k in campos) and any(ev.get(k) for k in campos):
                        # Prompt mejorado para extracción robusta
                        break
                if evento:
                    break
        if not evento:
            logger.error("❌ No se encontró ningún evento válido en los bloques JSON")
            return Response(
                json.dumps({"error": "No se encontró ningún evento válido en los bloques JSON"}, ensure_ascii=False),
                mimetype="application/json",
                status=500
            )
        # Si el campo persona está vacío, intentar inferirlo del texto original
        persona = evento.get("persona")
        if not persona:
            texto_original = data["texto"]
            persona_match = re.search(r"con ([A-ZÁÉÍÓÚÑ][a-záéíóúñ]+)", texto_original)
            if persona_match:
                persona = persona_match.group(1)
                logger.info(f"🔎 Persona inferida del texto: {persona}")
            else:
                logger.warning("❌ No se pudo extraer el campo 'persona' del texto")
                return Response(
                    json.dumps({"error": "No se pudo extraer el campo 'persona' del texto"}, ensure_ascii=False),
                    mimetype="application/json",
                    status=400
                )
        archivo = os.path.join(CONTEXTOS_DIR, f"{persona}.json")
        if os.path.exists(archivo):
            with open(archivo, "r", encoding="utf-8") as f:
                datos = json.load(f)
        else:
            datos = {"nombre": persona, "eventos": []}
        if "eventos" not in datos or not isinstance(datos["eventos"], list):
            datos["eventos"] = []
        evento_guardar = {k: v for k, v in evento.items() if k != "persona"}
        datos["eventos"].append(evento_guardar)
        with open(archivo, "w", encoding="utf-8") as f:
            json.dump(datos, f, ensure_ascii=False, indent=2)
        logger.info(f"✅ Evento añadido para {persona} (colloquial)")
        return Response(
            json.dumps({"mensaje": f"Evento añadido para {persona}"}, ensure_ascii=False),
            mimetype="application/json"
        )
    except Exception as e:
        logger.error(f"❌ Error inesperado en endpoint /anadir_evento_colloquial: {e}")
        logger.error(f"   Traceback: {traceback.format_exc()}")
        return Response(
            json.dumps({"error": "Error interno del servidor"}, ensure_ascii=False),
            mimetype="application/json",
            status=500
        )

@app.route("/preguntar", methods=["POST"])
def preguntar():
    logger.info("🔄 Endpoint /preguntar llamado")
    try:
        data = request.get_json()
        logger.debug(f"📥 Datos recibidos: {data}")


        if not data or "pregunta" not in data:
            logger.warning("❌ Falta parámetro 'pregunta'")
            return Response(
                json.dumps({"error": "Falta parámetro 'pregunta'"}, ensure_ascii=False),
                mimetype="application/json",
                status=400
            )

        pregunta = data["pregunta"]
        persona = data.get("persona")
        logger.debug(f"❓ Pregunta recibida: {pregunta}")
        if persona:
            logger.info(f"👤 Procesando pregunta para persona: {persona}")
            contexto = cargar_contexto(persona)
            logger.debug(f"🧩 Contexto usado: {contexto}")
            historial = cargar_historial(persona)
            logger.debug(f"📚 Historial usado: {historial}")
            messages = generar_mensajes(contexto, historial, pregunta)
            logger.debug(f"📝 Mensajes enviados a Ollama: {messages}")
            try:
                response = requests.post(
                    OLLAMA_URL,
                    json={
                        "model": MODEL_NAME,
                        "messages": messages,
                        "stream": False
                    },
                    timeout=60
                )
                logger.debug(f"📥 Respuesta de Ollama: status={response.status_code}")
                if response.status_code != 200:
                    logger.error(f"❌ Error HTTP de Ollama: {response.status_code} - {response.text}")
                    return Response(
                        json.dumps({"error": "No se pudo obtener respuesta de Ollama"}, ensure_ascii=False),
                        mimetype="application/json",
                        status=500
                    )
                data_ollama = response.json()
                if "message" not in data_ollama or "content" not in data_ollama["message"]:
                    logger.error(f"❌ Respuesta de Ollama malformada: {data_ollama}")
                    return Response(
                        json.dumps({"error": "Respuesta de Ollama malformada"}, ensure_ascii=False),
                        mimetype="application/json",
                        status=500
                    )
                respuesta = data_ollama["message"]["content"]
                # Guardar en historial
                guardar_historial(persona, pregunta, respuesta)
            except Exception as e:
                logger.error(f"❌ Error inesperado en pregunta persona: {e}")
                logger.error(f"   Traceback: {traceback.format_exc()}")
                return Response(
                    json.dumps({"error": "Error interno del servidor"}, ensure_ascii=False),
                    mimetype="application/json",
                    status=500
                )
        else:
            logger.info("🤖 Procesando pregunta general (sin persona)")
            # Prompt general sin contexto ni historial
            messages = [{"role": "user", "content": str(pregunta)}]
            logger.debug(f"📝 Mensaje enviado a Ollama: {messages}")
            try:
                response = requests.post(
                    OLLAMA_URL,
                    json={
                        "model": MODEL_NAME,
                        "messages": messages,
                        "stream": False
                    },
                    timeout=60
                )
                logger.debug(f"📥 Respuesta de Ollama: status={response.status_code}")
                if response.status_code != 200:
                    logger.error(f"❌ Error HTTP de Ollama: {response.status_code} - {response.text}")
                    return Response(
                        json.dumps({"error": "No se pudo obtener respuesta de Ollama"}, ensure_ascii=False),
                        mimetype="application/json",
                        status=500
                    )
                data_ollama = response.json()
                if "message" not in data_ollama or "content" not in data_ollama["message"]:
                    logger.error(f"❌ Respuesta de Ollama malformada: {data_ollama}")
                    return Response(
                        json.dumps({"error": "Respuesta de Ollama malformada"}, ensure_ascii=False),
                        mimetype="application/json",
                        status=500
                    )
                respuesta = data_ollama["message"]["content"]
            except Exception as e:
                logger.error(f"❌ Error inesperado en pregunta general: {e}")
                logger.error(f"   Traceback: {traceback.format_exc()}")
                return Response(
                    json.dumps({"error": "Error interno del servidor"}, ensure_ascii=False),
                    mimetype="application/json",
                    status=500
                )

        if respuesta is None:
            logger.error("❌ No se pudo obtener respuesta de Ollama")
            return Response(
                json.dumps({"error": "No se pudo obtener respuesta de Ollama"}, ensure_ascii=False),
                mimetype="application/json",
                status=500
            )

        logger.info("✅ Respuesta generada exitosamente")
        return Response(
            json.dumps({"pregunta": pregunta, "respuesta": respuesta, "persona": persona}, ensure_ascii=False),
            mimetype="application/json"
        )

    except json.JSONDecodeError as e:
        logger.error(f"❌ Error decodificando JSON de la petición: {e}")
        return Response(
            json.dumps({"error": "JSON malformado en la petición"}, ensure_ascii=False),
            mimetype="application/json",
            status=400
        )
    except Exception as e:
        logger.error(f"❌ Error inesperado en endpoint /preguntar: {e}")
        logger.error(f"   Traceback: {traceback.format_exc()}")
        return Response(
            json.dumps({"error": "Error interno del servidor"}, ensure_ascii=False),
            mimetype="application/json",
            status=500
        )

@app.route("/resumir", methods=["POST"])
def resumir():
    logger.info("🔄 Endpoint /resumir llamado")
    try:
        data = request.get_json()
        logger.debug(f"📥 Datos recibidos: {data}")

        if not data or "persona" not in data:
            logger.warning("❌ Falta parámetro 'persona'")
            return Response(
                json.dumps({"error": "Falta parámetro 'persona'"}, ensure_ascii=False),
                mimetype="application/json",
                status=400
            )

        persona = data["persona"]
        logger.info(f"👤 Procesando resumen para persona: {persona}")

        exito = resumir_historial(persona)
        logger.info(f"📊 Resultado de resumir_historial: {exito}")

        if not exito:
            logger.error(f"❌ No se pudo resumir historial de {persona}")
            return Response(
                json.dumps({"error": f"No se pudo resumir historial de {persona}"}, ensure_ascii=False),
                mimetype="application/json",
                status=500
            )

        logger.info(f"✅ Historial de {persona} resumido correctamente")
        return Response(
            json.dumps({"mensaje": f"Historial de {persona} resumido correctamente"}, ensure_ascii=False),
            mimetype="application/json"
        )

    except json.JSONDecodeError as e:
        logger.error(f"❌ Error decodificando JSON de la petición: {e}")
        return Response(
            json.dumps({"error": "JSON malformado en la petición"}, ensure_ascii=False),
            mimetype="application/json",
            status=400
        )
    except Exception as e:
        logger.error(f"❌ Error inesperado en endpoint /resumir: {e}")
        logger.error(f"   Traceback: {traceback.format_exc()}")
        return Response(
            json.dumps({"error": "Error interno del servidor"}, ensure_ascii=False),
            mimetype="application/json",
            status=500
        )

if __name__ == "__main__":
    logger.info("🚀 Iniciando API Ollama Server...")
    logger.info(f"📡 Ollama URL: {OLLAMA_URL}")
    logger.info(f"🤖 Modelo: {MODEL_NAME}")
    logger.info(f"📂 Directorio historial: {HISTORIAL_DIR}")
    logger.info(f"📂 Directorio contextos: {CONTEXTOS_DIR}")

    # Verificar que Ollama esté disponible
    if not verificar_ollama():
        logger.error("❌ No se puede iniciar la API sin Ollama funcionando correctamente")
        exit(1)

    # Verificar directorios
    for directorio in [HISTORIAL_DIR, CONTEXTOS_DIR]:
        if not os.path.exists(directorio):
            logger.warning(f"⚠️ Directorio no existe, creándolo: {directorio}")
            try:
                os.makedirs(directorio, exist_ok=True)
                logger.info(f"✅ Directorio creado: {directorio}")
            except Exception as e:
                logger.error(f"❌ Error creando directorio {directorio}: {e}")
                exit(1)

    logger.info("🌐 Iniciando servidor Flask en puerto 5000...")
    try:
        app.run(host="0.0.0.0", port=5000, debug=False)
    except Exception as e:
        logger.error(f"❌ Error iniciando servidor Flask: {e}")
        logger.error(f"   Traceback: {traceback.format_exc()}")
        exit(1)

 
