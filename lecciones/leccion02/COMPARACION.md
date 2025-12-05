# Comparación: Lección 1 vs Lección 2

## Arquitectura Visual

### Lección 1: Tools Directas

```
┌─────────────────────────────────────────────────────┐
│                  Script Python                      │
│  ┌─────────────────────────────────────────────┐   │
│  │           Ollama Client                     │   │
│  │  ┌────────────────────────────────────┐     │   │
│  │  │  LLM (llama3.2:3b)                 │     │   │
│  │  │  - Recibe pregunta                 │     │   │
│  │  │  - Decide usar tool                │     │   │
│  │  │  - Extrae parámetros               │     │   │
│  │  └────────────────────────────────────┘     │   │
│  │                    ↓                         │   │
│  │  ┌────────────────────────────────────┐     │   │
│  │  │  Tool Definition                   │     │   │
│  │  │  - Función Python local            │     │   │
│  │  │  - subprocess.run()                │     │   │
│  │  └────────────────────────────────────┘     │   │
│  └─────────────────────────────────────────────┘   │
│                    ↓                                │
│  ┌─────────────────────────────────────────────┐   │
│  │  Script Externo (script_temperatura.py)     │   │
│  │  - Llama a API Open-Meteo                   │   │
│  │  - Devuelve resultado                       │   │
│  └─────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────┘
```

**Características:**
- ✅ Simple y directo
- ✅ Todo en un solo proceso
- ❌ Difícil de reutilizar
- ❌ Acoplamiento fuerte

---

### Lección 2: MCP Servers

```
┌──────────────────────┐         ┌──────────────────────┐
│   Cliente Python     │         │   Servidor MCP       │
│                      │         │                      │
│  ┌────────────────┐  │         │  ┌────────────────┐  │
│  │ Ollama Client  │  │  MCP    │  │  MCP Server    │  │
│  │ - LLM decide   │◄─┼────────►│  │  - Registra    │  │
│  │ - Usa tools    │  │Protocol │  │    tools       │  │
│  └────────────────┘  │         │  │  - Ejecuta     │  │
│         ↓            │         │  │    lógica      │  │
│  ┌────────────────┐  │         │  └────────────────┘  │
│  │ MCP Client     │  │         │         ↓            │
│  │ - Conecta      │◄─┼─────────┤  ┌────────────────┐  │
│  │ - Lista tools  │  │         │  │ Script Externo │  │
│  │ - Llama tools  │  │         │  │ - API calls    │  │
│  └────────────────┘  │         │  └────────────────┘  │
└──────────────────────┘         └──────────────────────┘
     Proceso 1                        Proceso 2
```

**Características:**
- ✅ Arquitectura desacoplada
- ✅ Múltiples clientes pueden conectarse
- ✅ Protocolo estandarizado
- ✅ Escalable y distribuible
- ⚠️  Más complejo de configurar

---

## Comparación Código

### Lección 1: Tool Definition

```python
# Todo en un archivo
TOOL_DEFINITION = {
    'type': 'function',
    'function': {
        'name': 'obtener_temperatura',
        'description': '...',
        'parameters': {...}
    }
}

def ejecutar_script_temperatura(ciudad):
    resultado = subprocess.run(['python3', 'script.py', ciudad])
    return resultado.stdout

# Chat loop
respuesta = ollama.chat(model='llama3.2:3b', messages=mensajes, tools=[TOOL_DEFINITION])
if respuesta['message'].get('tool_calls'):
    resultado = ejecutar_script_temperatura(ciudad)
    # Continuar con el resultado...
```

### Lección 2: MCP Server + Client

**Servidor (mcp_server_temperatura.py):**
```python
from mcp.server import Server
import mcp.types as types

server = Server("temperatura-server")

@server.list_tools()
async def handle_list_tools() -> list[types.Tool]:
    return [types.Tool(name="obtener_temperatura", ...)]

@server.call_tool()
async def handle_call_tool(name: str, arguments: dict):
    # Ejecutar lógica
    resultado = subprocess.run(['python3', 'script.py', ciudad])
    return [types.TextContent(text=resultado.stdout)]
```

**Cliente (mcp_client_temperatura.py):**
```python
from mcp import ClientSession
from mcp.client.stdio import stdio_client

async with stdio_client(server_params) as (read, write):
    async with ClientSession(read, write) as session:
        await session.initialize()
        tools = await session.list_tools()
        
        # Usar con Ollama
        respuesta = ollama.chat(model='llama3.2:3b', tools=tools)
        if respuesta['message'].get('tool_calls'):
            resultado = await session.call_tool(tool_name, tool_args)
```

---

## Casos de Uso

### Usa Lección 1 (Tools Directas) cuando:
- 🎯 Proyecto simple y personal
- 🎯 Prototipado rápido
- 🎯 No necesitas reutilización
- 🎯 Todo corre en la misma máquina

### Usa Lección 2 (MCP Servers) cuando:
- 🎯 Múltiples clientes/aplicaciones
- 🎯 Herramientas reutilizables
- 🎯 Arquitectura distribuida
- 🎯 Quieres seguir estándares de la industria
- 🎯 Necesitas escalar

---

## Ejemplo Práctico

**Escenario:** Asistente meteorológico para toda España

### Con Tools Directas (Lección 1):
```
app_web.py     → Copia de tool_temperatura.py
app_mobile.py  → Copia de tool_temperatura.py
app_cli.py     → Copia de tool_temperatura.py
```
❌ Código duplicado en cada aplicación

### Con MCP Server (Lección 2):
```
mcp_server_temperatura.py  (Corre una vez)
         ↑           ↑           ↑
    app_web.py  app_mobile.py  app_cli.py
```
✅ Un servidor, múltiples clientes

---

## Próximos Pasos

1. ✅ Completar Lección 1 (entender tools básicas)
2. ✅ Completar Lección 2 (entender MCP)
3. 🔜 Lección 3: Crear tu propio servidor MCP con múltiples tools
4. 🔜 Lección 4: Desplegar MCP servers en producción
5. 🔜 Lección 5: Integrar con servicios reales (bases de datos, APIs)

---

**Recursos adicionales:**
- [MCP Official Docs](https://modelcontextprotocol.io/)
- [Ollama Tools Documentation](https://ollama.ai/docs)
- [Examples Repository](https://github.com/modelcontextprotocol/servers)
