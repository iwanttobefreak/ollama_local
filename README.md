## Tabla de Contenidos

1. [Introducción](#introducción)
2. [Creación imágen de docker de Ollama](#creación-imágen-de-docker-de-ollama)
3. [Lección 1: Tools con Ollama](#lección-1)
4. [Lección 2: MCP Servers](#lección-2)

---

## Introducción
Ejecución de modelos de APIs y agentes de IA 100% en local sin usar tokens ni servicios externos.

## Creación imágen de docker de Ollama
Descarga el repositorio. Dentro del repositorio hay un Dockerfile para usar ollama (modelo de LLM). Crearemos una imagen que se llame **ollama**
```bash
git clone https://github.com/iwanttobefreak/ollama_local.git
cd ollama_local
docker build -t ollama .
```
Nos crea una imagen con ollama y algunas bibliotecas necesarias que ocupa unos 4.71Gb
```
REPOSITORY                                   TAG              IMAGE ID      CREATED        SIZE
localhost/ollama                             latest           5869e52488df  2 minutes ago  4.71 GB
```
### Parámetros Docker
- Puertos
  - $PUERTO_OLLAMA: Api ollama
  - $PUERTO_FLASK: Api Flask
- Volumenes
  - $DIR_DATOS: volúmen fuera del repositorio de GIT para mapear datos locales como BBDD, txt con contextos, etc...
  - $DIR_LLM: volúmen donde guarda los LLMs. Ocupan mucho, mejor guardar fuera del contenedor también para poder reaprovechar
  - $DIR_SCRIPTS: volúmen donde se guardan los scripts. Recomendable mapear con el repositorio de GIT
- Otros
  - $MEMORIA: memoria del docker. Si no tienes GPU, recomendado poner bastante

Ejemplo:
```bash
PUERTO_OLLAMA=11434
PUERTO_FLASK=5000
DIR_LLM=/ollama/llm
DIR_SCRIPTS=/ollama/scripts
DIR_DATOS=/ollama/datos
MEMORIA=16g
```

```bash
docker run --rm -d --name ollama \
  -p $PUERTO_OLLAMA:11434 \
  -p $PUERTO_FLASK:5000 \
  --memory="$MEMORIA" \
  -v $DIR_SCRIPTS:/app/scrics \
  -v $DIR_LLM:/root/.ollama \
  -v $DIR_DATOS:/app/datos \
  ollama
```

Ahora si entramos en el docker, vemos que no tiene descargado ningun LLM
```bash
docker exec -ti ollama bash
```
Mostrar LLMs cargados, no tenemos ninguno:
```bash
ollama list
NAME    ID    SIZE    MODIFIED
```
Descargamos el modelo llama3.2:1b
```bash
ollama push llama3.2:1b
```

Podemos descargar también otros modelos depende de lo que queramos usar:
```bash
NAME                       ID              SIZE      MODIFIED
nomic-embed-text:latest    0a109f422b47    274 MB    34 hours ago
llama3.2:1b                baf6a787fdff    1.3 GB    37 hours ago
codellama:13b              9f438cb9cd58    7.4 GB    5 days ago
llama3.1:8b                46e0c10c039e    4.9 GB    6 weeks ago
```

## Lección 1
Contenido de la lección...

## Lección 2

**MCP Servers (Model Context Protocol)**

Aprende a crear servidores MCP que exponen herramientas de forma estandarizada.

### ¿Qué aprenderás?

- Diferencia entre Tools directas (Lección 1) y MCP Servers
- Crear un servidor MCP básico
- Conectar Ollama con servidores MCP
- Arquitectura cliente-servidor para LLMs

### Archivos principales:

- `mcp_server_minimo.py` - Ejemplo mínimo de servidor MCP
- `mcp_client_minimo.py` - Cliente básico para probar MCP
- `mcp_server_temperatura.py` - Servidor que usa el script de temperatura
- `mcp_client_temperatura.py` - Cliente completo con Ollama
- `test_leccion02.sh` - Script interactivo para probar todo

### Inicio rápido:

```bash
cd lecciones/leccion02
./test_leccion02.sh
```

O ejecuta directamente:

```bash
cd lecciones/leccion02
pip install mcp ollama
python3 mcp_client_minimo.py  # Ejemplo simple
python3 mcp_client_temperatura.py  # Ejemplo completo
```

### Conceptos clave:

**Arquitectura MCP:**
```
Usuario → Cliente → Ollama ⟷ MCP Server → Recursos externos
```

**Ventajas sobre Tools directas:**
- ✅ Separación de responsabilidades
- ✅ Reutilización entre múltiples clientes
- ✅ Protocolo estandarizado
- ✅ Escalabilidad mejorada

Ver documentación completa: [lecciones/leccion02/README.md](lecciones/leccion02/README.md)

