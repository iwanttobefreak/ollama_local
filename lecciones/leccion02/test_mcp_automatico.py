#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script de prueba automatizada del cliente MCP
Simula la interacción con el usuario enviando preguntas automáticamente
"""
import asyncio
import ollama
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

async def test_mcp():
    print("="*60)
    print("🧪 PRUEBA AUTOMATIZADA - Cliente MCP Temperatura")
    print("="*60)
    
    # Parámetros para iniciar el servidor MCP
    server_params = StdioServerParameters(
        command="python3",
        args=["mcp_server_temperatura.py"],
        env=None
    )
    
    try:
        # Conectar al servidor MCP
        print("🔌 Conectando al servidor MCP...")
        async with stdio_client(server_params) as (read, write):
            async with ClientSession(read, write) as session:
                # Inicializar sesión
                await session.initialize()
                
                # Listar herramientas disponibles
                tools = await session.list_tools()
                print(f"✅ Conectado al servidor MCP")
                print(f"📋 Herramientas disponibles: {len(tools.tools)}\n")
                
                for tool in tools.tools:
                    print(f"   🔧 {tool.name}")
                    print(f"      └─ {tool.description}\n")
                
                # Preparar historial de mensajes
                mensajes = [
                    {
                        'role': 'system',
                        'content': 'Eres un asistente meteorológico. Usa las herramientas disponibles para responder preguntas sobre el tiempo en ciudades españolas. Sé amable y conciso.'
                    }
                ]
                
                # Pregunta de prueba
                pregunta = "¿Qué temperatura va a hacer mañana en Madrid?"
                print("="*60)
                print(f"👤 Pregunta de prueba: {pregunta}\n")
                
                mensajes.append({'role': 'user', 'content': pregunta})
                
                # Convertir herramientas MCP a formato Ollama
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
                
                # Primera llamada: LLM decide si usar herramienta
                print("🤔 Procesando pregunta con Ollama...")
                respuesta = ollama.chat(
                    model='llama3.1:8b',
                    messages=mensajes,
                    tools=tools_ollama
                )
                
                # ¿El LLM quiere usar una herramienta?
                if respuesta['message'].get('tool_calls'):
                    print("✅ Ollama decidió usar la herramienta MCP\n")
                    
                    tool_call = respuesta['message']['tool_calls'][0]
                    tool_name = tool_call['function']['name']
                    tool_args = tool_call['function']['arguments']
                    
                    print(f"📊 ANTES de la conversión:")
                    print(f"   Tipo de 'dias': {type(tool_args.get('dias'))}")
                    print(f"   Valor de 'dias': {repr(tool_args.get('dias'))}")
                    print()
                    
                    # Convertir 'dias' a entero si existe (Ollama a veces lo envía como string)
                    if 'dias' in tool_args and isinstance(tool_args['dias'], str):
                        try:
                            tool_args['dias'] = int(tool_args['dias'])
                            print(f"✅ Conversión exitosa de 'dias' a integer")
                        except ValueError:
                            print(f"⚠️  No se pudo convertir 'dias' a integer")
                    
                    print(f"\n📊 DESPUÉS de la conversión:")
                    print(f"   Tipo de 'dias': {type(tool_args.get('dias'))}")
                    print(f"   Valor de 'dias': {repr(tool_args.get('dias'))}")
                    print()
                    
                    print(f"🔧 Llamando al servidor MCP:")
                    print(f"   Herramienta: {tool_name}")
                    print(f"   Argumentos: {tool_args}")
                    print()
                    
                    # Llamar a la herramienta en el servidor MCP
                    try:
                        resultado = await session.call_tool(tool_name, tool_args)
                        resultado_texto = resultado.content[0].text
                        
                        # Verificar si hay error
                        if "Error" in resultado_texto or "error" in resultado_texto or "validation" in resultado_texto:
                            print(f"❌ ERROR en la respuesta del servidor:")
                            print("   " + "\n   ".join(resultado_texto.split('\n')[:10]))
                            print()
                            return False
                        else:
                            print(f"✅ Respuesta exitosa del servidor MCP:")
                            print("   " + "\n   ".join(resultado_texto.split('\n')[:5]))
                            print()
                            
                            # Segunda llamada: LLM procesa el resultado
                            mensajes.append(respuesta['message'])
                            mensajes.append({
                                'role': 'tool',
                                'content': resultado_texto
                            })
                            
                            print("🧠 Procesando respuesta con Ollama...")
                            respuesta_final = ollama.chat(
                                model='llama3.1:8b',
                                messages=mensajes
                            )
                            
                            print(f"\n🤖 Respuesta final:")
                            print(f"   {respuesta_final['message']['content']}")
                            print()
                            return True
                            
                    except Exception as e:
                        print(f"❌ Error al llamar al servidor MCP: {str(e)}")
                        return False
                else:
                    print("⚠️  Ollama no decidió usar herramientas")
                    print(f"   Respuesta: {respuesta['message']['content']}")
                    return False
                        
    except Exception as e:
        print(f"\n❌ Error en la prueba: {str(e)}")
        import traceback
        traceback.print_exc()
        return False
    
    return True

async def main():
    print("\n🚀 Iniciando prueba automatizada...\n")
    
    exito = await test_mcp()
    
    print("\n" + "="*60)
    if exito:
        print("✅ PRUEBA EXITOSA - El cliente MCP funciona correctamente")
    else:
        print("❌ PRUEBA FALLIDA - Hay errores en el cliente MCP")
    print("="*60 + "\n")
    
    return 0 if exito else 1

if __name__ == "__main__":
    exit_code = asyncio.run(main())
    exit(exit_code)
