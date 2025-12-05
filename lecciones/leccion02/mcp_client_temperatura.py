#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Cliente MCP simple que se conecta al servidor de temperatura
Integra Ollama para procesamiento de lenguaje natural
"""
import asyncio
import ollama
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

async def main():
    print("="*60)
    print("🌐 CLIENTE MCP - Servidor de Temperatura")
    print("="*60)
    print("Este cliente se conecta a un servidor MCP que proporciona")
    print("información meteorológica de ciudades españolas.\n")
    
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
                
                print("="*60)
                print("💬 Chat con el asistente meteorológico")
                print("Escribe 'salir' para terminar\n")
                
                # Historial de mensajes
                mensajes = [
                    {
                        'role': 'system',
                        'content': 'Eres un asistente meteorológico. Usa las herramientas disponibles para responder preguntas sobre el tiempo en ciudades españolas. Sé amable y conciso.'
                    }
                ]
                
                # Loop de chat
                while True:
                    try:
                        pregunta = input("👤 Tú: ").strip()
                        
                        if pregunta.lower() in ['salir', 'exit', 'quit']:
                            print("\n👋 ¡Hasta luego!")
                            break
                        
                        if not pregunta:
                            continue
                        
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
                        print("🤔 Pensando...", end='', flush=True)
                        respuesta = ollama.chat(
                            model='llama3.1:8b',
                            messages=mensajes,
                            tools=tools_ollama
                        )
                        print("\r" + " "*50 + "\r", end='')  # Limpiar línea
                        
                        # ¿El LLM quiere usar una herramienta?
                        if respuesta['message'].get('tool_calls'):
                            print("✅ Consultando servidor MCP...")
                            
                            tool_call = respuesta['message']['tool_calls'][0]
                            tool_name = tool_call['function']['name']
                            tool_args = tool_call['function']['arguments']
                            
                            # Convertir 'dias' a entero si existe (Ollama a veces lo envía como string)
                            if 'dias' in tool_args and isinstance(tool_args['dias'], str):
                                try:
                                    tool_args['dias'] = int(tool_args['dias'])
                                except ValueError:
                                    pass  # Si no se puede convertir, dejar como está
                            
                            print(f"   🔧 Herramienta: {tool_name}")
                            print(f"   📝 Ciudad: {tool_args.get('ciudad')}")
                            if 'dias' in tool_args:
                                print(f"   📅 Días: {tool_args.get('dias')}")
                            
                            # Llamar a la herramienta en el servidor MCP
                            resultado = await session.call_tool(tool_name, tool_args)
                            
                            resultado_texto = resultado.content[0].text
                            
                            # Debug: mostrar si hay error
                            if "Error" in resultado_texto or "error" in resultado_texto:
                                print(f"\n⚠️  DEBUG - Respuesta del servidor:")
                                print("   " + "\n   ".join(resultado_texto.split('\n')[:10]))
                            
                            # Añadir resultado al historial
                            mensajes.append(respuesta['message'])
                            mensajes.append({
                                'role': 'tool',
                                'content': resultado_texto
                            })
                            
                            # Segunda llamada: LLM procesa el resultado
                            print("🧠 Procesando información...", end='', flush=True)
                            respuesta = ollama.chat(
                                model='llama3.1:8b',
                                messages=mensajes
                            )
                            print("\r" + " "*50 + "\r", end='')  # Limpiar línea
                        
                        # Mostrar respuesta
                        print(f"\n🤖 Asistente: {respuesta['message']['content']}\n")
                        mensajes.append(respuesta['message'])
                        
                    except KeyboardInterrupt:
                        print("\n\n👋 Interrumpido por el usuario. ¡Hasta luego!")
                        break
                    except Exception as e:
                        print(f"\n❌ Error: {str(e)}\n")
                        continue
                        
    except Exception as e:
        print(f"\n❌ Error al conectar con el servidor MCP: {str(e)}")
        print("\nAsegúrate de que:")
        print("1. Tienes instalado el SDK de MCP: pip install mcp")
        print("2. Tienes instalado ollama: pip install ollama")
        print("3. El servidor Ollama está corriendo (docker o local)")
        return 1
    
    return 0

if __name__ == "__main__":
    exit_code = asyncio.run(main())
    exit(exit_code)
