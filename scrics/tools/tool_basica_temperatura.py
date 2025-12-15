#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Tool MUY BÁSICA que usa script_pronostico_temperatura.py
"""

import ollama
import subprocess
import json

# 1️⃣ DEFINIR LA TOOL (lo que lee el LLM)
TOOL_DEFINITION = {
    'type': 'function',
    'function': {
        'name': 'obtener_temperatura',
        'description': 'Obtiene el pronóstico de temperatura para una ciudad española',
        'parameters': {
            'type': 'object',
            'properties': {
                'ciudad': {
                    'type': 'string',
                    'description': 'Nombre de la ciudad española (ej: Madrid, Barcelona)'
                }
            },
            'required': ['ciudad']
        }
    }
}

# 2️⃣ FUNCIÓN que ejecuta el script Python
def ejecutar_script_temperatura(ciudad):
    """
    Ejecuta script_pronostico_temperatura.py y devuelve el resultado
    """
    print(f"\n🔧 [TOOL] Ejecutando script para: {ciudad}")
    
    try:
        # Ejecutar el script Python
        resultado = subprocess.run(
            ['python3', 'script_pronostico_temperatura.py', ciudad],
            capture_output=True,
            text=True,
            timeout=30
        )
        
        if resultado.returncode == 0:
            return resultado.stdout
        else:
            return f"Error al obtener temperatura: {resultado.stderr}"
            
    except Exception as e:
        return f"Error ejecutando script: {str(e)}"

# 3️⃣ CHAT con el LLM
def chat_con_tools():
    print("="*60)
    print("🤖 CHAT CON TOOL BÁSICA DE TEMPERATURA")
    print("="*60)
    print("Escribe 'salir' para terminar\n")
    
    mensajes = [
        {
            'role': 'system',
            'content': 'Eres un asistente que puede consultar el pronóstico de temperatura de ciudades españolas usando herramientas.'
        }
    ]
    
    while True:
        # Pedir pregunta al usuario
        pregunta = input("\n👤 Tú: ").strip()
        
        if pregunta.lower() in ['salir', 'exit', 'quit']:
            print("👋 ¡Hasta luego!")
            break
            
        if not pregunta:
            continue
        
        # Añadir mensaje del usuario
        mensajes.append({'role': 'user', 'content': pregunta})
        
        # 🔹 Primera llamada: LLM decide si usa la tool
        print("\n🤔 Pensando...")
        respuesta = ollama.chat(
            model='llama3.2:3b',
            messages=mensajes,
            tools=[TOOL_DEFINITION]
        )
        
        # 🔹 ¿El LLM quiere usar la tool?
        if respuesta['message'].get('tool_calls'):
            print("✅ El LLM decidió usar la tool")
            
            # Obtener parámetros que extrajo el LLM
            tool_call = respuesta['message']['tool_calls'][0]
            ciudad = tool_call['function']['arguments']['ciudad']
            
            # Ejecutar el script Python
            resultado_temperatura = ejecutar_script_temperatura(ciudad)
            
            # Añadir la llamada a la tool a los mensajes
            mensajes.append(respuesta['message'])
            
            # Añadir el resultado de la tool
            mensajes.append({
                'role': 'tool',
                'content': resultado_temperatura
            })
            
            # 🔹 Segunda llamada: LLM procesa el resultado de la tool
            print("📝 Generando respuesta final...")
            respuesta_final = ollama.chat(
                model='llama3.2:3b',
                messages=mensajes
            )
            
            respuesta_texto = respuesta_final['message']['content']
            
        else:
            # No usó la tool, respuesta directa
            print("ℹ️  El LLM respondió sin usar la tool")
            respuesta_texto = respuesta['message']['content']
        
        # Mostrar respuesta al usuario
        print(f"\n🤖 Asistente: {respuesta_texto}")
        
        # Añadir respuesta a los mensajes
        mensajes.append({'role': 'assistant', 'content': respuesta_texto})

# 4️⃣ EJECUTAR
if __name__ == '__main__':
    print("\n⚠️  IMPORTANTE: Asegúrate de tener script_pronostico_temperatura.py en el mismo directorio\n")
    
    try:
        chat_con_tools()
    except KeyboardInterrupt:
        print("\n\n👋 Chat interrumpido. ¡Hasta luego!")
    except Exception as e:
        print(f"\n❌ Error: {e}")
