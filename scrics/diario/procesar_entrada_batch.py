import json
import os
import sys
from langchain_ollama import OllamaLLM, OllamaEmbeddings
from langchain_chroma import Chroma
from langchain_text_splitters import CharacterTextSplitter

# --- CONFIGURACIÓN ---
OLLAMA_LLM_MODEL = "llama3.1:8b" 
OLLAMA_EMBED_MODEL = "nomic-embed-text" 
DIARY_FILE = "/app/chats/diario/diario_personal_vida.txt" # El fichero consolidado del RAG
PERSIST_DIR = "/app/chats/diario/diario_chroma_db"
SEPARADOR = "\n---\n" # El delimitador atómico

# --- 1. CONFIGURACIÓN DEL LLM EXTRACTOR ---

EXTRACTION_PROMPT = """
Eres un asistente experto en estructuración de diarios personales. 
Tu tarea es analizar cada entrada de texto y extraer los siguientes campos:
- FECHA (formato AAAA-MM-DD, si no hay fecha explícita, déjala vacía)
- TIPO (una palabra o frase corta que resuma el evento: ejemplo: Cena, Viaje, Concierto, Trabajo, Médico, etc.)
- LUGAR (ciudad, local, país, o sitio relevante; si no hay, déjalo vacío)

Devuelve SOLO un objeto JSON válido con las claves 'FECHA', 'TIPO' y 'LUGAR'.

Ejemplo:
Entrada: "Hoy he ido a cenar con Ana al restaurante Coque de Madrid. La comida espectacular."
JSON:
{"FECHA": "", "TIPO": "Cena", "LUGAR": "Madrid"}

NO respondas nada más. Devuelve SOLO el objeto JSON solicitado, sin explicaciones ni contexto adicional.
"""

# Inicializar el LLM para la extracción (solo una vez)
llm_extractor = OllamaLLM(model=OLLAMA_LLM_MODEL, system=EXTRACTION_PROMPT)

# --- 2. FUNCIONES ---

def reindex_rag(): 
    """Carga todo el archivo del diario y re-indexa la Base de Datos Vectorial."""
    print("-> 4. Re-indexando RAG...")
    if not os.path.exists(DIARY_FILE) or os.path.getsize(DIARY_FILE) == 0:
        print("El archivo del diario está vacío. No hay nada que indexar.")
        return

    try:
        # Cargar todo el texto
        with open(DIARY_FILE, 'r', encoding='utf-8') as f:
            document_text = f.read()

        # Usar el splitter atómico para dividir por el separador '---'
        text_splitter = CharacterTextSplitter(
            separator=SEPARADOR, 
            chunk_size=4000, 
            chunk_overlap=0,
            length_function=len
        )
        # Se necesita un documento dummy si el splitter no soporta directamente el texto
        # Usamos create_documents sobre el texto completo
        texts = text_splitter.create_documents([document_text])
        
        # Crear/Actualizar la Base de Datos Vectorial
        embeddings = OllamaEmbeddings(model=OLLAMA_EMBED_MODEL)
        
        # Esto sobrescribe o crea la base de datos con el nuevo contenido
        vectorstore = Chroma.from_documents(
            documents=texts,
            embedding=embeddings,
            persist_directory=PERSIST_DIR
        )
        # Persist solo si existe el método
        if hasattr(vectorstore, "persist"):
            vectorstore.persist()
        print(f"Base de datos RAG actualizada con {len(texts)} fragmentos.")
    
    except Exception as e:
        print(f"Error durante la re-indexación: {e}")

def process_single_entry(texto_nota_voz: str): 
    """Procesa una sola entrada, extrae etiquetas y la escribe en el archivo."""
    
    if not texto_nota_voz.strip():
        return
        
    print(f"\nProcesando: '{texto_nota_voz[:50]}...'")

    # --- A. Extracción de Etiquetas ---

    try:
        messages = [
            {"role": "system", "content": EXTRACTION_PROMPT},
            {"role": "user", "content": texto_nota_voz}
        ]
        json_output_str = llm_extractor.invoke(messages).strip()
        json_output_str = json_output_str.strip()
        if json_output_str.startswith("```json"):
            json_output_str = json_output_str[7:]
        if json_output_str.endswith("```"):
            json_output_str = json_output_str[:-3]
        json_output_str = json_output_str.strip()
        import re
        matches = re.findall(r'\{[\s\S]*?\}', json_output_str)
        metadata = None
        for bloque in matches:
            try:
                metadata = json.loads(bloque)
                break
            except Exception as ex_json:
                print(f"[DEBUG] Fallo al parsear bloque JSON: {bloque}\nError: {ex_json}")
                continue
        if not metadata:
            print(f"[DEBUG] No se pudo extraer JSON válido de la respuesta: {json_output_str}")
            raise ValueError("No se pudo extraer JSON válido")
        fecha = metadata.get('FECHA', 'FECHA_DESCONOCIDA')
        tipo = metadata.get('TIPO', 'EVENTO_DESCONOCIDO')
        lugar = metadata.get('LUGAR', 'LUGAR_DESCONOCIDO')
        # --- B. Formato Final RAG ---
        etiquetas = f"[FECHA: {fecha}] [TIPO: {tipo}] [LUGAR: {lugar}]"
        entrada_rag = f"{etiquetas}\n{texto_nota_voz}\n{SEPARADOR}"
        # --- C. Guardar en el Archivo de Texto ---
        with open(DIARY_FILE, 'a', encoding='utf-8') as f:
            f.write(entrada_rag)
        print(f"-> Entrada guardada con etiquetas: {etiquetas}")
    except Exception as e:
        print(f"--- ERROR: No se pudo extraer la metadata. Saltando entrada. ---")
        print(f"[DEBUG] Motivo: {e}")
        return
    # print fuera del bloque try/except eliminado para evitar error de sintaxis


# --- 3. EJECUCIÓN PRINCIPAL ---

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("ERROR: Por favor, proporciona la ruta del archivo de texto como argumento.")
        print(f"Uso: python {sys.argv[0]} <ruta_al_fichero.txt>")
        sys.exit(1)

    input_file_path = sys.argv[1]
    
    if not os.path.exists(input_file_path):
        print(f"ERROR: El archivo de entrada '{input_file_path}' no fue encontrado.")
        sys.exit(1)

    print(f"--- INICIANDO PROCESAMIENTO DE: {input_file_path} ---")

    try:
        with open(input_file_path, 'r', encoding='utf-8') as f:
            diary_entries = f.readlines()
        
        # Procesar cada línea del archivo de entrada
        for line in diary_entries:
            process_single_entry(line.strip())
            
        print("\n--- PROCESAMIENTO DE ARCHIVO FINALIZADO ---")
        reindex_rag()
        
        print("\n¡El archivo RAG ha sido actualizado y está listo para ser consultado!")

    except Exception as e:
        print(f"Ocurrió un error inesperado: {e}")
        sys.exit(1)
