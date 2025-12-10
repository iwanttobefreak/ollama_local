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

