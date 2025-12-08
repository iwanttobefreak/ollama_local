# Servidor MCP - Consulta de Población INE

Este servidor MCP expone la funcionalidad de consulta de población del INE como una herramienta para modelos de lenguaje (Ollama, Claude, etc).

## ¿Qué es MCP?

MCP (Model Context Protocol) es un protocolo que permite a los modelos de lenguaje usar herramientas externas de forma segura y estandarizada.

## Instalación

### 1. Instalar dependencias

```powershell
pip install mcp requests
```

### 2. Configurar en Claude Desktop (opcional)

Si usas Claude Desktop, edita el archivo de configuración:

**Ubicación:** `%APPDATA%\Claude\claude_desktop_config.json`

Añade esta configuración:

```json
{
  "mcpServers": {
    "ine-poblacion": {
      "command": "python",
      "args": [
        "C:\\Users\\joseantonio.legidoma\\copilot\\apis\\mcp_ine_server.py"
      ]
    }
  }
}
```

### 3. Configurar para Ollama

#### Opción A: Usar con Ollama + Open WebUI

1. Instala Open WebUI:
```powershell
pip install open-webui
```

2. Configura el servidor MCP en Open WebUI:
   - Abre la configuración de funciones (Functions)
   - Añade una nueva función personalizada
   - Usa el script `mcp_ine_server.py`

#### Opción B: Usar directamente con API

Puedes ejecutar el servidor MCP manualmente y conectarlo a través de stdio:

```powershell
python apis/mcp_ine_server.py
```

## Uso

### Herramienta disponible: `consultar_poblacion_ine`

**Parámetros:**
- `lugar` (string): Nombre de la provincia o municipio (ej: Madrid, Barcelona, Murcia)
- `año` (integer): Año de consulta (entre 1996 y 2021)

**Ejemplo de uso desde un modelo:**

```
Usuario: "¿Cuántos habitantes tenía Madrid en 2021?"

Modelo: [Llama a la herramienta consultar_poblacion_ine]
  - lugar: "Madrid"
  - año: 2021

Respuesta: "Población obtenida del INE:
Lugar: Madrid. Total. Total habitantes. Personas.
Codigo INE: DPOP12922
Año: 2021
Poblacion: 6,751,251 habitantes"
```

## Probar el servidor

### Prueba manual:

```powershell
# Ejecutar el servidor
python apis/mcp_ine_server.py
```

El servidor quedará esperando comandos MCP en formato JSON por stdin/stdout.

### Prueba con script de ejemplo:

```python
import asyncio
import json

async def test_mcp():
    # Simular llamada a la herramienta
    proceso = await asyncio.create_subprocess_exec(
        'python', 'apis/mcp_ine_server.py',
        stdin=asyncio.subprocess.PIPE,
        stdout=asyncio.subprocess.PIPE
    )
    
    # Enviar comando
    comando = {
        "jsonrpc": "2.0",
        "id": 1,
        "method": "tools/call",
        "params": {
            "name": "consultar_poblacion_ine",
            "arguments": {
                "lugar": "Madrid",
                "año": 2021
            }
        }
    }
    
    proceso.stdin.write(json.dumps(comando).encode() + b'\n')
    await proceso.stdin.drain()
    
    # Leer respuesta
    respuesta = await proceso.stdout.readline()
    print(json.loads(respuesta))

asyncio.run(test_mcp())
```

## Características

✅ **Sin datos hardcodeados** - Todo se consulta en tiempo real desde www.ine.es
✅ **Datos oficiales** - Directamente del Instituto Nacional de Estadística
✅ **Cobertura completa** - Provincias y capitales de provincia de España
✅ **Histórico amplio** - Datos desde 1996 hasta 2021
✅ **Formato estándar MCP** - Compatible con múltiples clientes

## Limitaciones

- Solo incluye provincias y municipios principales (capitales)
- Datos disponibles hasta 2021
- Requiere conexión a internet

## Ejemplo completo con Ollama

```python
# Ejemplo de integración con Ollama usando MCP

from ollama import chat
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

# Configurar servidor MCP
server_params = StdioServerParameters(
    command="python",
    args=["C:\\Users\\joseantonio.legidoma\\copilot\\apis\\mcp_ine_server.py"]
)

async def chat_with_tools():
    async with stdio_client(server_params) as (read, write):
        async with ClientSession(read, write) as session:
            # Inicializar
            await session.initialize()
            
            # Listar herramientas
            tools = await session.list_tools()
            print(f"Herramientas disponibles: {[t.name for t in tools.tools]}")
            
            # Hacer pregunta a Ollama
            response = chat(
                model='llama3.2',
                messages=[{
                    'role': 'user',
                    'content': '¿Cuántos habitantes tenía Barcelona en 2020?'
                }],
                tools=tools.tools
            )
            
            # Si el modelo decide usar la herramienta
            if response.message.tool_calls:
                for tool_call in response.message.tool_calls:
                    result = await session.call_tool(
                        tool_call.function.name,
                        tool_call.function.arguments
                    )
                    print(f"Resultado: {result.content[0].text}")

# Ejecutar
asyncio.run(chat_with_tools())
```

## Soporte

Para más información sobre MCP:
- Documentación oficial: https://modelcontextprotocol.io
- Repositorio: https://github.com/modelcontextprotocol

Para más información sobre el INE:
- Web oficial: https://www.ine.es
- Tabla de población: https://www.ine.es/jaxiT3/Tabla.htm?t=2852
