## Creación imágen de docker de Ollama
Descarga el repositorio. Dentro del repositorio hay un Dockerfile para usar ollama (modelo de LLM). Crearemos una imagen que se llame **ollama**
```bash
git clone https://github.com/iwanttobefreak/ollama_local.git
cd ollama_local
docker build -t ollama .
```

### Parámetros Docker

- **Puertos:**
  - `PUERTO_OLLAMA`: Puerto de la API Ollama (ejemplo: 11434)
  - `PUERTO_FLASK`: Puerto de la API Flask (ejemplo: 5000)

- **Volúmenes:**
  - `DIR_DATOS`: Volumen externo para datos locales (BBDD, txt de contextos, etc.)
  - `DIR_LLM`: Volumen para los modelos LLM (recomendado fuera del contenedor para reutilizar y ahorrar espacio)

- **Otros:**
  - `MEMORIA`: Memoria asignada al contenedor Docker (si no tienes GPU, pon suficiente RAM)

Creamos los directorios para DIR_LLM y DIR_DATOS y los otros parámetros podrían ser:
```bash
DIR_LLM=/ollama/llm
DIR_DATOS=/ollama/datos
DIR_LECCIONES=${PWD}/lecciones
PUERTO_OLLAMA=11434
PUERTO_FLASK=5000
MEMORIA=16g
```

Descargarmos el repositorio y desde dentro del repositorio construimos la imagen del repositorio:
```
git clone https://github.com/iwanttobefreak/ollama_local.git
cd ollama_local
docker build -t ollama .
```

Una vez construida la imagen, levantamos el contenedor de docker

```bash
docker run --rm -d --name ollama \
  -p $PUERTO_OLLAMA:11434 \
  -p $PUERTO_FLASK:5000 \
  --memory="$MEMORIA" \
  -v ${PWD}/scrics:/app/scrics \
  -v ${PWD}/lecciones:/app/lecciones \
  -v $DIR_LLM:/root/.ollama \
  -v $DIR_DATOS:/app/datos \
  ollama
```

Mostrar LLMs cargados, esperamos 30 segundos que arranque y tiene por defecto llama3.2:1b que es ligero (en el momento de esta documentación, supongo que cambiará con el tiempo porque esto va muy rápido):
```bash
docker exec -ti ollama bash -c "ollama list"

NAME    ID    SIZE    MODIFIED
llama3.2:1b    baf6a787fdff    1.3 GB    9 seconds ago
```

También los podemos mostrar por la API:
```bash
curl http://localhost:11434/api/tags
```

```json
{
  "models": [
    {
      "name": "llama3.2:1b",
      "model": "llama3.2:1b",
      "modified_at": "2025-12-10T10:54:58.961147297+01:00",
      "size": 1321098329,
      "digest": "baf6a787fdffd633537aa2eb51cfd54cb93ff08e28040095462bb63daf552878",
      "details": {
        "parent_model": "",
        "format": "gguf",
        "family": "llama",
        "families": [
          "llama"
        ],
        "parameter_size": "1.2B",
        "quantization_level": "Q8_0"
      }
    }
  ]
}
```

Podemos descargar también otros modelos depende de lo que queramos usar. Lista de modelos disponibles: https://ollama.com/library

Por ejemplo descargamos llama3.1:8b

```bash
docker exec -ti ollama bash -c "ollama pull llama3.1:8b"
```
o con la API:
```bash
curl -X POST http://localhost:11434/api/pull \
  -H "Content-Type: application/json" \
  -d '{"name": "llama3.1:8b"}'
```
Ejemplo de LLMs y tamaños
```bash
NAME                       ID              SIZE      MODIFIED
nomic-embed-text:latest    0a109f422b47    274 MB    34 hours ago
llama3.2:1b                baf6a787fdff    1.3 GB    37 hours ago
codellama:13b              9f438cb9cd58    7.4 GB    5 days ago
llama3.1:8b                46e0c10c039e    4.9 GB    6 weeks ago
```

También podemos abrir un prompt tipo ChatGPT e interactura con él:
```bash
docker exec -ti ollama bash -c "ollama run llama3.1:8b"
>>> Send a message (/? for help)
```
```
>>> ¿Cual es la capital de China?
La respuesta a esta pregunta depende del contexto. Si se está refiriendo a la República Popular China (RPC), su
capital es Pekín. Sin embargo, si nos referimos a la República de China (ROC), su capital es Taiwán.

Pekín o Beijing, tiene una población de 21,544,000 habitantes y ocupa el puesto número 17 en términos de población
global, y en cuanto al tamaño territorial, tiene un área de 16,800 kilómetros cuadrados.
```


También lo podemos probar por la API

```bash
curl -X POST http://localhost:11434/api/chat \
    -H "Content-Type: application/json" \
    -d '{
        "model": "llama3.2:1b",
        "messages": [
            {"role": "user", "content": "¿Cuál es la capital de Francia?"}
        ],
        "stream": false
    }'
```
Respuesta:
```json
{
  "model": "llama3.2:1b",
  "created_at": "2025-12-10T10:10:03.99293422Z",
  "message": {
    "role": "assistant",
    "content": "La capital de Francia es París."
  },
  "done": true,
  "done_reason": "stop",
  "total_duration": 225175942,
  "load_duration": 108852053,
  "prompt_eval_count": 35,
  "prompt_eval_duration": 9316088,
  "eval_count": 10,
  "eval_duration": 103798175
}
```