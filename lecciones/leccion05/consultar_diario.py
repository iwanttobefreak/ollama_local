# Importaciones necesarias (utilizando la ruta 'classic' y las demás modernas)
from langchain_chroma import Chroma
from langchain_classic.chains import RetrievalQA # ¡Tu solución!
from langchain_ollama import OllamaLLM
from langchain_ollama import OllamaEmbeddings

# --- 1. CONFIGURACIÓN ---
OLLAMA_EMBED_MODEL = "nomic-embed-text"
OLLAMA_LLM_MODEL = "llama3.1:8b" # Usamos el modelo que indicaste
PERSIST_DIR = "/app/datos/diario/diario_chroma_db"

# --- 2. CARGAR LA BASE DE DATOS (BD) PERSISTIDA ---
print(f"Cargando el modelo de embeddings: {OLLAMA_EMBED_MODEL}...")
embeddings = OllamaEmbeddings(model=OLLAMA_EMBED_MODEL)

print(f"Cargando la Base de Datos Vectorial desde {PERSIST_DIR}...")
# Cargar la BD existente, usando el mismo modelo de embeddings que se usó para crearla
vectorstore = Chroma(
    persist_directory=PERSIST_DIR,
    embedding_function=embeddings
)
print("Base de datos cargada correctamente.")

# --- 3. CONFIGURAR EL LLM Y LA CADENA RAG ---
# Inicializar el LLM de Ollama
llm = OllamaLLM(model=OLLAMA_LLM_MODEL)

# Configurar el RetrievalQA Chain (el corazón del RAG)
# Esto crea un 'Retriever' que sabe cómo buscar en tu BD
qa_chain = RetrievalQA.from_chain_type(
    llm=llm,
    chain_type="stuff", 
    retriever=vectorstore.as_retriever(k=3) # Recupera los 3 fragmentos más relevantes
)

import sys
if len(sys.argv) < 2:
    print("ERROR: Debes proporcionar la consulta como parámetro.")
    print(f"Uso: python {sys.argv[0]} '¿Que tal fue el concierto de Rosalía?'\n")
    sys.exit(1)

user_query = sys.argv[1]

# El método .run(query) o .invoke(query) en LangChain realiza el siguiente proceso:
# 1. Convierte 'user_query' en vector (embedding).
# 2. Busca los 3 fragmentos más similares en la base de datos.
# 3. Construye el prompt final: [System Prompt por defecto + Fragmentos Recuperados + user_query].
# 4. Envía el prompt al modelo.
response = qa_chain.invoke(user_query)

print(f"\n--- CONSULTA ---\n{user_query}")
print("\n--- RESPUESTA DEL DIARIO ---\n")
print(response['result'])
