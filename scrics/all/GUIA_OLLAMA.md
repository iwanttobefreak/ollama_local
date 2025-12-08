# Integración del Servidor MCP INE con Ollama

## Guía paso a paso para usar el script de población INE como herramienta en Ollama

### Requisitos previos

```powershell
# Verificar instalación de Python
python --version

# Verificar instalación de Ollama
ollama --version
```

---

## Opción 1: Usar con Ollama mediante Python SDK (RECOMENDADO)

### 1. Instalar dependencias

```powershell
pip install ollama mcp requests
```

### 2. Crear script de integración

Guarda este código como `ollama_con_ine.py`:

```python
#!/usr/bin/env python3
"""
Cliente Ollama con herramienta MCP para consultar poblacion INE
"""

import asyncio
from ollama import chat
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client


async def chat_con_herramientas():
    """
    Chat con Ollama usando la herramienta de consulta INE
    """
    # Configurar servidor MCP
    server_params = StdioServerParameters(
        command="python",
        args=["C:\\Users\\joseantonio.legidoma\\copilot\\apis\\mcp_ine_server.py"]
    )
    
    print("Iniciando servidor MCP...")
    
    async with stdio_client(server_params) as (read, write):
        async with ClientSession(read, write) as session:
            # Inicializar
            await session.initialize()
            
            # Obtener herramientas
            tools_response = await session.list_tools()
            tools_list = tools_response.tools
            
            print(f"Herramientas disponibles: {[t.name for t in tools_list]}")
            print()
            
            # Convertir herramientas MCP a formato Ollama
            ollama_tools = []
            for tool in tools_list:
                ollama_tools.append({
                    'type': 'function',
                    'function': {
                        'name': tool.name,
                        'description': tool.description,
                        'parameters': tool.inputSchema
                    }
                })
            
            # Loop de conversación
            messages = []
            
            print("Chat con Ollama (escribe 'salir' para terminar)")
            print("=" * 60)
            
            while True:
                # Obtener pregunta del usuario
                user_input = input("\nTu: ")
                
                if user_input.lower() in ['salir', 'exit', 'quit']:
                    print("Adios!")
                    break
                
                # Agregar mensaje del usuario
                messages.append({
                    'role': 'user',
                    'content': user_input
                })
                
                # Llamar a Ollama
                response = chat(
                    model='llama3.2',  # o el modelo que prefieras
                    messages=messages,
                    tools=ollama_tools
                )
                
                # Procesar respuesta
                if response.message.tool_calls:
                    # El modelo quiere usar una herramienta
                    for tool_call in response.message.tool_calls:
                        print(f"\n[Ollama llama a: {tool_call.function.name}]")
                        print(f"[Argumentos: {tool_call.function.arguments}]")
                        
                        # Ejecutar herramienta en el servidor MCP
                        result = await session.call_tool(
                            tool_call.function.name,
                            tool_call.function.arguments
                        )
                        
                        tool_result = result.content[0].text
                        print(f"\n[Resultado de la herramienta:]")
                        print(tool_result)
                        
                        # Agregar resultado al historial
                        messages.append(response.message)
                        messages.append({
                            'role': 'tool',
                            'content': tool_result
                        })
                        
                        # Obtener respuesta final del modelo
                        final_response = chat(
                            model='llama3.2',
                            messages=messages
                        )
                        
                        print(f"\nOllama: {final_response.message.content}")
                        messages.append(final_response.message)
                else:
                    # Respuesta normal sin herramientas
                    print(f"\nOllama: {response.message.content}")
                    messages.append(response.message)


if __name__ == "__main__":
    asyncio.run(chat_con_herramientas())
```

### 3. Ejecutar

```powershell
python ollama_con_ine.py
```

### 4. Ejemplos de uso

```
Tu: ¿Cuántos habitantes tenía Madrid en 2021?
[Ollama llama a: consultar_poblacion_ine]
[Argumentos: {'lugar': 'Madrid', 'año': 2021}]

[Resultado de la herramienta:]
Poblacion obtenida del INE:
Lugar: Madrid. Total. Total habitantes. Personas.
Poblacion: 6,751,251 habitantes

Ollama: Según los datos del INE, Madrid tenía 6,751,251 habitantes en 2021.

---

Tu: Compara la población de Barcelona y Sevilla en 2020
[Ollama llama a: consultar_poblacion_ine]
[Argumentos: {'lugar': 'Barcelona', 'año': 2020}]
...
[Ollama llama a: consultar_poblacion_ine]
[Argumentos: {'lugar': 'Sevilla', 'año': 2020}]
...

Ollama: En 2020, Barcelona tenía 5,743,402 habitantes mientras que 
Sevilla tenía 1,950,219 habitantes. Barcelona tenía aproximadamente 
3.8 millones más de habitantes que Sevilla.
```

---

## Opción 2: Usar con Open WebUI (Interfaz web para Ollama)

### 1. Instalar Open WebUI

```powershell
pip install open-webui
```

### 2. Ejecutar Open WebUI

```powershell
open-webui serve
```

### 3. Configurar la herramienta

1. Abre http://localhost:8080
2. Ve a **Settings** → **Functions**
3. Crea una nueva función
4. Pega el código del servidor MCP adaptado

### 4. Usar en el chat

Ahora puedes hacer preguntas y Open WebUI automáticamente usará la herramienta cuando sea necesario.

---

## Opción 3: Usar como función standalone para Ollama

Si prefieres una integración más simple sin MCP:

```python
#!/usr/bin/env python3
"""
Ollama con función de consulta INE (sin MCP)
"""

import requests
from ollama import chat


def consultar_poblacion_ine(lugar: str, año: int) -> str:
    """Consulta población en el INE"""
    try:
        url = "https://servicios.ine.es/wstempus/js/ES/DATOS_TABLA/2852?tip=AM&"
        response = requests.get(url, timeout=30)
        datos = response.json()
        
        nombre_buscar = lugar.lower().strip()
        
        for registro in datos:
            if not isinstance(registro, dict):
                continue
            
            nombre_registro = registro.get('Nombre', '').lower()
            
            if (nombre_buscar in nombre_registro and 
                'total' in nombre_registro and 
                'hombres' not in nombre_registro and 
                'mujeres' not in nombre_registro):
                
                for dato in registro.get('Data', []):
                    if dato.get('Anyo') == año:
                        return f"{lugar}: {int(dato['Valor']):,} habitantes en {año}"
        
        return f"No se encontraron datos para {lugar} en {año}"
    
    except Exception as e:
        return f"Error: {str(e)}"


# Definir herramientas para Ollama
tools = [{
    'type': 'function',
    'function': {
        'name': 'consultar_poblacion_ine',
        'description': 'Consulta la población de provincias y ciudades españolas en el INE',
        'parameters': {
            'type': 'object',
            'properties': {
                'lugar': {
                    'type': 'string',
                    'description': 'Nombre de la provincia o ciudad'
                },
                'año': {
                    'type': 'integer',
                    'description': 'Año (entre 1996 y 2021)'
                }
            },
            'required': ['lugar', 'año']
        }
    }
}]

# Chat
messages = [{'role': 'user', 'content': '¿Cuántos habitantes tenía Murcia en 2021?'}]

response = chat(
    model='llama3.2',
    messages=messages,
    tools=tools
)

# Si usa la herramienta
if response.message.tool_calls:
    for tool_call in response.message.tool_calls:
        args = tool_call.function.arguments
        result = consultar_poblacion_ine(args['lugar'], args['año'])
        print(f"Resultado: {result}")
        
        # Segunda llamada con el resultado
        messages.append(response.message)
        messages.append({'role': 'tool', 'content': result})
        
        final = chat(model='llama3.2', messages=messages)
        print(f"Respuesta: {final.message.content}")
else:
    print(response.message.content)
```

---

## Verificación

Para verificar que todo funciona:

```powershell
# 1. Probar el servidor MCP
cd C:\Users\joseantonio.legidoma\copilot\apis
python test_mcp_ine.py --direct

# 2. Probar con Ollama
python ollama_con_ine.py
```

---

## Troubleshooting

### Error: "mcp module not found"
```powershell
pip install mcp
```

### Error: "ollama module not found"
```powershell
pip install ollama
```

### Error: "Ollama not running"
```powershell
# Iniciar Ollama
ollama serve

# En otra terminal, descargar un modelo
ollama pull llama3.2
```

### El modelo no usa la herramienta

Algunos modelos de Ollama no soportan function calling. Modelos recomendados:
- `llama3.2` (mejor soporte)
- `mistral`
- `qwen2.5`

---

## Recursos adicionales

- **Documentación MCP:** https://modelcontextprotocol.io
- **Ollama Python SDK:** https://github.com/ollama/ollama-python
- **Open WebUI:** https://github.com/open-webui/open-webui
- **INE:** https://www.ine.es
