# Lección 2: MCP Servers (Model Context Protocol)

## 🚀 Inicio Rápido

```bash
cd lecciones/leccion02

# Opción 1: Usar el script interactivo
./test_leccion02.sh

# Opción 2: Instalar y probar manualmente
pip install mcp ollama
python3 mcp_client_minimo.py
```

> 📖 **Guía completa de instalación:** Ver [INSTALACION.md](INSTALACION.md)

---

## Contenido

1. [¿Qué es MCP?](#qué-es-mcp)
2. [Ejemplo Mínimo (sin Ollama)](#ejemplo-mínimo-sin-ollama)
3. [Ejemplo Completo con Temperatura](#ejemplo-completo-con-temperatura)
4. [Instalación](#instalación-de-dependencias)
5. [Cómo Ejecutar](#cómo-ejecutar)
6. [Usando Docker con Ollama](#usando-ollama-con-docker)
7. [Ventajas de MCP](#ventajas-de-mcp-sobre-tools-directas)
8. [Comparación con Lección 1](#comparación-con-lección-1)

**📚 Documentación adicional:**
- [INSTALACION.md](INSTALACION.md) - Guía completa de instalación y troubleshooting
- [COMPARACION.md](COMPARACION.md) - Comparación detallada Lección 1 vs Lección 2
- [RESUMEN.md](RESUMEN.md) - Resumen visual y conceptos clave
- [MODELOS.md](MODELOS.md) - Comparación de modelos Ollama (llama3.1:8b vs llama3.2:3b)
- [TROUBLESHOOTING.md](TROUBLESHOOTING.md) - Solución de problemas comunes
- [VALIDACION_TIPOS.md](VALIDACION_TIPOS.md) - ⚠️ Importante: Cómo validar tipos de parámetros en MCP

---

## ¿Qué es MCP?

MCP (Model Context Protocol) es un protocolo estándar creado por Anthropic que permite a los modelos de lenguaje conectarse con **servidores externos** que proporcionan datos y herramientas de forma estandarizada.

### Diferencia con Tools (Lección 1):

- **Tools (Lección 1)**: El script Python ejecuta directamente comandos locales
- **MCP Servers (Lección 2)**: Un servidor externo proporciona las herramientas y el LLM se conecta a él

## Arquitectura MCP

```
┌─────────────┐         ┌─────────────┐         ┌──────────────┐
│   Cliente   │ ◄─────► │ MCP Server  │ ◄─────► │   Recursos   │
│  (Ollama)   │   MCP   │  (Python)   │         │  (APIs, DB)  │
└─────────────┘         └─────────────┘         └──────────────┘
```

---

## Ejemplo Mínimo (sin Ollama)

Antes de integrar con Ollama, veamos un ejemplo **súper simple** de MCP:

### Servidor Mínimo: `mcp_server_minimo.py`

```python
#!/usr/bin/env python3
import asyncio
from mcp.server import Server, NotificationOptions
from mcp.server.models import InitializationOptions
import mcp.server.stdio
import mcp.types as types

server = Server("ejemplo-minimo")

@server.list_tools()
async def handle_list_tools() -> list[types.Tool]:
    return [
        types.Tool(
            name="saludar",
            description="Devuelve un saludo personalizado",
            inputSchema={
                "type": "object",
                "properties": {
                    "nombre": {"type": "string", "description": "Nombre de la persona"}
                },
                "required": ["nombre"]
            }
        )
    ]

@server.call_tool()
async def handle_call_tool(name: str, arguments: dict | None) -> list[types.TextContent]:
    if name != "saludar":
        raise ValueError(f"Herramienta desconocida: {name}")
    nombre = arguments.get("nombre", "desconocido")
    return [types.TextContent(type="text", text=f"¡Hola {nombre}! Bienvenido al servidor MCP.")]

async def main():
    async with mcp.server.stdio.stdio_server() as (read_stream, write_stream):
        await server.run(read_stream, write_stream, 
            InitializationOptions(server_name="ejemplo-minimo", server_version="1.0.0",
                capabilities=server.get_capabilities(notification_options=NotificationOptions(), 
                    experimental_capabilities={})))

if __name__ == "__main__":
    asyncio.run(main())
```

### Cliente Mínimo: `mcp_client_minimo.py`

```python
#!/usr/bin/env python3
import asyncio
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

async def main():
    print("🧪 PRUEBA MÍNIMA DE MCP\n")
    
    server_params = StdioServerParameters(command="python3", args=["mcp_server_minimo.py"])
    
    async with stdio_client(server_params) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()
            
            tools = await session.list_tools()
            print(f"✅ Herramientas: {tools.tools[0].name}")
            
            resultado = await session.call_tool("saludar", {"nombre": "María"})
            print(f"📨 Respuesta: {resultado.content[0].text}")

if __name__ == "__main__":
    asyncio.run(main())
```

### Ejecutar el ejemplo mínimo:

```bash
cd lecciones/leccion02
pip install mcp
python3 mcp_client_minimo.py
```

Salida esperada:
```
🧪 PRUEBA MÍNIMA DE MCP

✅ Herramientas: saludar
📨 Respuesta: ¡Hola María! Bienvenido al servidor MCP.
```

---

## Ejemplo Completo con Temperatura

Ahora integramos MCP con Ollama para crear un asistente meteorológico inteligente.

### 1. Arquitectura

### 1. Arquitectura

```
Usuario → Cliente Python → Ollama (LLM) ⟷ MCP Server → Script Temperatura → API Open-Meteo
```

El servidor MCP básico necesita:
- Definir las herramientas (tools) que ofrece
- Implementar la lógica de cada herramienta
- Ejecutarse y esperar conexiones

### 2. Código del Servidor: `mcp_server_temperatura.py`

Este servidor expone una herramienta para obtener temperatura de ciudades españolas:

```python
#!/usr/bin/env python3
"""
Servidor MCP simple para consultar temperatura
"""
import asyncio
import subprocess
from mcp.server import Server, NotificationOptions
from mcp.server.models import InitializationOptions
import mcp.server.stdio
import mcp.types as types

# Crear el servidor MCP
server = Server("temperatura-server")

@server.list_tools()
async def handle_list_tools() -> list[types.Tool]:
    """Lista las herramientas disponibles"""
    return [
        types.Tool(
            name="obtener_temperatura",
            description="Obtiene el pronóstico de temperatura para ciudades españolas",
            inputSchema={
                "type": "object",
                "properties": {
                    "ciudad": {
                        "type": "string",
                        "description": "Nombre de la ciudad española"
                    },
                    "dias": {
                        "type": "integer",
                        "description": "Número de días de pronóstico (1-16)",
                        "default": 3
                    }
                },
                "required": ["ciudad"]
            }
        )
    ]

@server.call_tool()
async def handle_call_tool(
    name: str, arguments: dict | None
) -> list[types.TextContent]:
    """Ejecuta la herramienta solicitada"""
    
    if name != "obtener_temperatura":
        raise ValueError(f"Herramienta desconocida: {name}")
    
    ciudad = arguments.get("ciudad")
    dias = arguments.get("dias", 3)
    
    # Ejecutar el script de temperatura
    try:
        resultado = subprocess.run(
            ['python3', 'script_pronostico_temperatura.py', ciudad, str(dias)],
            capture_output=True,
            text=True,
            timeout=30,
            cwd="/Users/T054810/ollama_local/lecciones/leccion01"
        )
        
        if resultado.returncode == 0:
            return [types.TextContent(
                type="text",
                text=resultado.stdout
            )]
        else:
            return [types.TextContent(
                type="text",
                text=f"Error: {resultado.stderr}"
            )]
    except Exception as e:
        return [types.TextContent(
            type="text",
            text=f"Error ejecutando script: {str(e)}"
        )]

async def main():
    """Punto de entrada del servidor"""
    async with mcp.server.stdio.stdio_server() as (read_stream, write_stream):
        await server.run(
            read_stream,
            write_stream,
            InitializationOptions(
                server_name="temperatura-server",
                server_version="1.0.0",
                capabilities=server.get_capabilities(
                    notification_options=NotificationOptions(),
                    experimental_capabilities={},
                )
            )
        )

if __name__ == "__main__":
    asyncio.run(main())
```

### 3. Cliente para Conectar con el Servidor MCP: `mcp_client_temperatura.py`

```python
#!/usr/bin/env python3
"""
Cliente simple que se conecta al servidor MCP de temperatura
"""
import asyncio
import ollama
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

async def main():
    print("="*60)
    print("🌐 CLIENTE MCP - Conexión con Servidor de Temperatura")
    print("="*60)
    
    # Parámetros del servidor MCP
    server_params = StdioServerParameters(
        command="python3",
        args=["mcp_server_temperatura.py"],
        env=None
    )
    
    # Conectar al servidor MCP
    async with stdio_client(server_params) as (read, write):
        async with ClientSession(read, write) as session:
            # Inicializar sesión
            await session.initialize()
            
            # Listar herramientas disponibles
            tools = await session.list_tools()
            print(f"\n✅ Conectado al servidor MCP")
            print(f"📋 Herramientas disponibles: {len(tools.tools)}")
            
            for tool in tools.tools:
                print(f"   - {tool.name}: {tool.description}")
            
            print("\n" + "="*60)
            print("Escribe 'salir' para terminar\n")
            
            # Chat con el usuario
            mensajes = [
                {
                    'role': 'system',
                    'content': 'Eres un asistente meteorológico. Usa las herramientas disponibles para responder preguntas sobre el tiempo.'
                }
            ]
            
            while True:
                pregunta = input("\n👤 Tú: ").strip()
                
                if pregunta.lower() in ['salir', 'exit', 'quit']:
                    print("👋 ¡Hasta luego!")
                    break
                
                if not pregunta:
                    continue
                
                mensajes.append({'role': 'user', 'content': pregunta})
                
                # Convertir tools MCP a formato Ollama
                tools_ollama = []
                for tool in tools.tools:
                    tools_ollama.append({
                        'type': 'function',
                        'function': {
                            'name': tool.name,
                            'description': tool.description,
                            'parameters': tool.inputSchema
                        }
                    })
                
                # Primera llamada: LLM decide
                print("\n🤔 Pensando...")
                respuesta = ollama.chat(
                    model='llama3.1:8b',
                    messages=mensajes,
                    tools=tools_ollama
                )
                
                # ¿El LLM quiere usar una herramienta?
                if respuesta['message'].get('tool_calls'):
                    print("✅ Usando herramienta MCP...")
                    
                    tool_call = respuesta['message']['tool_calls'][0]
                    tool_name = tool_call['function']['name']
                    tool_args = tool_call['function']['arguments']
                    
                    print(f"🔧 Herramienta: {tool_name}")
                    print(f"📝 Argumentos: {tool_args}")
                    
                    # Llamar a la herramienta en el servidor MCP
                    resultado = await session.call_tool(tool_name, tool_args)
                    
                    resultado_texto = resultado.content[0].text
                    
                    # Añadir resultado al historial
                    mensajes.append(respuesta['message'])
                    mensajes.append({
                        'role': 'tool',
                        'content': resultado_texto
                    })
                    
                    # Segunda llamada: LLM procesa el resultado
                    respuesta = ollama.chat(
                        model='llama3.1:8b',
                        messages=mensajes
                    )
                
                # Mostrar respuesta
                print(f"\n🤖 Asistente: {respuesta['message']['content']}")
                mensajes.append(respuesta['message'])

if __name__ == "__main__":
    asyncio.run(main())
```

## Instalación de Dependencias

Para ejecutar los ejemplos de MCP necesitas instalar el SDK de MCP:

```bash
pip install mcp
pip install ollama
```

## Cómo Ejecutar

### Opción 1: Ejecutar el Servidor Manualmente (para debugging)

En una terminal, ejecuta el servidor:
```bash
cd lecciones/leccion02
python3 mcp_server_temperatura.py
```

El servidor se quedará esperando conexiones.

### Opción 2: Ejecutar el Cliente (automático)

El cliente inicia el servidor automáticamente:
```bash
cd lecciones/leccion02
python3 mcp_client_temperatura.py
```

## Usando Ollama con Docker

Si tienes Ollama en Docker (contenedor llamado "ollama"), asegúrate de que esté corriendo:

```bash
# Ver si está corriendo
docker ps | grep ollama

# Si no está corriendo, iniciarlo
docker start ollama

# Verificar que el modelo esté disponible
docker exec ollama ollama list
```

Para ejecutar los scripts con Ollama en Docker, el cliente Python se conecta al API de Ollama (por defecto en `http://localhost:11434`).

## Ejemplo de Uso

```
👤 Tú: ¿Qué temperatura hará mañana en Madrid?

🤔 Pensando...
✅ Usando herramienta MCP...
🔧 Herramienta: obtener_temperatura
📝 Argumentos: {'ciudad': 'Madrid', 'dias': 3}

🤖 Asistente: Según el pronóstico para Madrid:

Mañana (Sábado 06/12/2025):
- Temperatura: Entre 9.8°C y 19.1°C
- Clima: Nublado
- Probabilidad de lluvia: 8%
- Viento: 12.5 km/h
```

## Ventajas de MCP sobre Tools Directas

1. **Separación de responsabilidades**: El servidor MCP puede ejecutarse en otra máquina
2. **Reutilización**: Múltiples clientes pueden conectarse al mismo servidor
3. **Estándares**: MCP es un protocolo estándar compatible con múltiples LLMs
4. **Escalabilidad**: Fácil de escalar y distribuir

## Comparación con Lección 1

| Aspecto | Lección 1 (Tools) | Lección 2 (MCP) |
|---------|-------------------|-----------------|
| Arquitectura | Monolítica | Cliente-Servidor |
| Reutilización | Baja | Alta |
| Complejidad | Simple | Moderada |
| Escalabilidad | Limitada | Excelente |
| Estándar | Específico | Protocolo MCP |

## Próximos Pasos

- Crear servidores MCP con múltiples herramientas
- Conectar con APIs externas reales
- Implementar autenticación en servidores MCP
- Desplegar servidores MCP en la nube

---

**Recursos**:
- [Documentación MCP](https://modelcontextprotocol.io/)
- [MCP GitHub](https://github.com/modelcontextprotocol)
- [Ollama Docs](https://ollama.ai/docs)
