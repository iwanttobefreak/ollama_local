# API Ollama Server

Servidor Flask que proporciona una API REST para interactuar con Ollama usando contextos de personajes y historial de conversaciones.

## 🚀 Inicio Rápido

### 1. Ejecutar el contenedor Docker
```bash
docker run --rm -d --name ollama \
  -p 11434:11434 -p 5000:5000 \
  --memory="16g" \
  -v /Users/T054810/ollama_local/scrics:/scrics \
  -v /Users/T054810/ia/ollama/usr_local_lib:/usr/local/lib \
  -v /Users/T054810/ia/ollama/root_ollama:/root/.ollama \
  -ti ollama
```

### 2. Ejecutar la API
```bash
docker exec -it ollama bash
cd /app/scrics/chats
python api_ollama_server.py
```

### 3. Probar la API
```bash
# Desde otra terminal
curl -X POST http://localhost:5000/preguntar \
     -H "Content-Type: application/json" \
     -d '{"persona":"jandro", "pregunta":"¿Como se llama mi padre"}'
```

## 📁 Estructura de Archivos

```
/scrics/chats/
├── api_ollama_server.py    # Servidor Flask principal
├── test_api.sh             # Script de prueba
├── historial/              # Historiales de conversación
│   └── {persona}_history.txt
└── contextos/              # Contextos de personajes
    └── {persona}.json
```

## 🔧 Endpoints

### POST /preguntar
Hace una pregunta a un personaje específico usando Ollama.

**Parámetros:**
- `persona` (string): Nombre del personaje
- `pregunta` (string): Pregunta a hacer

**Ejemplo:**
```bash
curl -X POST http://localhost:5000/preguntar \
     -H "Content-Type: application/json" \
     -d '{"persona":"jandro", "pregunta":"¿Qué tiempo hace?"}'
```

**Respuesta exitosa:**
```json
{
  "persona": "jandro",
  "pregunta": "¿Qué tiempo hace?",
  "respuesta": "Hace un día soleado..."
}
```

### POST /resumir
Resume el historial de conversación de un personaje.

**Parámetros:**
- `persona` (string): Nombre del personaje

**Ejemplo:**
```bash
curl -X POST http://localhost:5000/resumir \
     -H "Content-Type: application/json" \
     -d '{"persona":"jandro"}'
```

## 📋 Formato de Contextos

Los archivos de contexto deben estar en `/scrics/chats/contextos/{persona}.json`:

```json
{
  "nombre": "Jandro",
  "relacion": "amigo cercano",
  "personalidad": "amigable, sarcástico, le gusta la tecnología",
  "proyectos": [
    "Desarrollo de APIs",
    "Machine Learning",
    "Desarrollo web"
  ]
}
```

## 🔍 Solución de Problemas

### Error 404 en Ollama
- Verificar que Ollama esté corriendo: `curl http://localhost:11434/api/tags`
- Verificar que el modelo esté disponible: `ollama list`

### Error de conexión
- Asegurarse de que los puertos 11434 y 5000 estén mapeados
- Verificar que el contenedor esté corriendo: `docker ps`

### Modelo no encontrado
- Cambiar `MODEL_NAME` en el código por un modelo disponible
- O instalar el modelo: `ollama pull llama3.1:8b`

## 🧪 Pruebas

Ejecutar el script de prueba:
```bash
./test_api.sh
```

Esto verificará que:
- El contenedor esté corriendo
- La API responda correctamente
- Ollama esté disponible