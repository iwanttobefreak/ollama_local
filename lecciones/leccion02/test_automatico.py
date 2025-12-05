#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script de prueba automática para mcp_client_temperatura.py
"""
import asyncio
import sys
sys.path.insert(0, '/scrics/ollama_local/lecciones/leccion02')

import ollama
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

async def test_temperatura():
    print("="*60)
    print("🧪 TEST AUTOMÁTICO - Cliente MCP Temperatura")
    print("="*60)
    
    # Parámetros del servidor MCP
    server_params = StdioServerParameters(
        command="python",
        args=["mcp_server_temperatura.py"],
        env=None
    )
    
    try:
        print("\n🔌 Conectando al servidor MCP...")
        async with stdio_client(server_params) as (read, write):
            async with ClientSession(read, write) as session:
                await session.initialize()
                
                # Listar herramientas
                tools = await session.list_tools()
                print(f"✅ Conectado al servidor MCP")
                print(f"📋 Herramientas disponibles: {len(tools.tools)}\n")
                
                for tool in tools.tools:
                    print(f"   🔧 {tool.name}")
                    print(f"      └─ {tool.description}\n")
                
                # Mensaje de prueba
                mensajes = [
                    {
                        'role': 'system',
                        'content': 'Eres un asistente meteorológico. Usa las herramientas disponibles para responder preguntas sobre el tiempo.'
                    },
                    {
                        'role': 'user',
                        'content': 'Madrid, ¿qué previsión hay para esta semana?'
                    }
                ]
                
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
                
                print("="*60)
                print("🤖 Probando consulta: 'Madrid, ¿qué previsión hay para esta semana?'")
                print("="*60)
                
                # Primera llamada: LLM decide
                print("\n🤔 Enviando pregunta a Ollama...")
                respuesta = ollama.chat(
                    model='llama3.1:8b',
                    messages=mensajes,
                    tools=tools_ollama
                )
                
                # ¿El LLM quiere usar una herramienta?
                if respuesta['message'].get('tool_calls'):
                    print("✅ Ollama decidió usar una herramienta MCP")
                    
                    tool_call = respuesta['message']['tool_calls'][0]
                    tool_name = tool_call['function']['name']
                    tool_args = tool_call['function']['arguments']
                    
                    print(f"\n📝 Detalles de la llamada:")
                    print(f"   🔧 Herramienta: {tool_name}")
                    print(f"   📍 Ciudad: {tool_args.get('ciudad')}")
                    print(f"   📅 Días: {tool_args.get('dias')}")
                    print(f"   🔢 Tipo de 'dias': {type(tool_args.get('dias'))}")
                    
                    # Llamar a la herramienta en el servidor MCP
                    print(f"\n🌐 Llamando al servidor MCP...")
                    resultado = await session.call_tool(tool_name, tool_args)
                    
                    resultado_texto = resultado.content[0].text
                    
                    # Mostrar resultado
                    if "Error" in resultado_texto or "error" in resultado_texto:
                        print("\n❌ ERROR - Respuesta del servidor:")
                        print("   " + "\n   ".join(resultado_texto.split('\n')[:15]))
                        return 1
                    else:
                        print("\n✅ Respuesta del servidor recibida correctamente")
                        print("\n📊 Primeras líneas del pronóstico:")
                        lines = resultado_texto.split('\n')[:20]
                        for line in lines:
                            print(f"   {line}")
                        
                        # Añadir resultado al historial
                        mensajes.append(respuesta['message'])
                        mensajes.append({
                            'role': 'tool',
                            'content': resultado_texto
                        })
                        
                        # Segunda llamada: LLM procesa el resultado
                        print("\n🧠 Procesando respuesta con Ollama...")
                        respuesta = ollama.chat(
                            model='llama3.1:8b',
                            messages=mensajes
                        )
                        
                        print("\n💬 Respuesta final del asistente:")
                        print("="*60)
                        print(respuesta['message']['content'])
                        print("="*60)
                        
                        return 0
                else:
                    print("❌ Ollama no decidió usar la herramienta")
                    print(f"Respuesta directa: {respuesta['message']['content']}")
                    return 1
                    
    except Exception as e:
        print(f"\n❌ Error: {str(e)}")
        import traceback
        traceback.print_exc()
        return 1

if __name__ == "__main__":
    exit_code = asyncio.run(test_temperatura())
    sys.exit(exit_code)
