#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Tool sencilla POC - Ejecuta consulta_temperatura.py cuando preguntan por temperatura
"""

import subprocess
import os
from ollama import chat

# Ruta del script de temperatura
SCRIPT_PATH = os.path.join(os.path.dirname(__file__), 'consulta_temperatura.py')

def ejecutar_consulta_temperatura(ciudad: str = "madrid") -> str:
    """
    Ejecuta el script consulta_temperatura.py
    
    Args:
        ciudad: Ciudad para consultar (default: madrid)
    
    Returns:
        Resultado de la consulta de temperatura
    """
    try:
        # Ejecutar el script Python
        result = subprocess.run(
            ['python', SCRIPT_PATH, ciudad.lower()],
            capture_output=True,
            text=True,
            timeout=15
        )
        
        if result.returncode == 0:
            return result.stdout.strip()
        else:
            return f"❌ Error ejecutando script: {result.stderr}"
            
    except subprocess.TimeoutExpired:
        return "❌ Timeout: El script tardó demasiado"
    except Exception as e:
        return f"❌ Error inesperado: {str(e)}"

# Definición de la herramienta para Ollama
tools = [{
    'type': 'function',
    'function': {
        'name': 'ejecutar_consulta_temperatura',
        'description': 'Ejecuta un script para consultar la temperatura actual en ciudades españolas. Usar cuando pregunten por temperatura, clima o tiempo meteorológico.',
        'parameters': {
            'type': 'object',
            'properties': {
                'ciudad': {
                    'type': 'string',
                    'description': 'Nombre de la ciudad española (madrid, barcelona, valencia, sevilla, bilbao, malaga)',
                    'default': 'madrid'
                }
            },
            'required': ['ciudad']
        }
    }
}]

# Mapeo de funciones disponibles
available_functions = {
    'ejecutar_consulta_temperatura': ejecutar_consulta_temperatura
}

def chat_con_temperatura(pregunta: str, modelo: str = 'llama3.1:8b'):
    """
    Chat con Ollama que puede ejecutar consultas de temperatura
    
    Args:
        pregunta: Pregunta del usuario
        modelo: Modelo de Ollama a usar
    """
    try:
        print(f"🤖 Usando modelo: {modelo}")
        print(f"❓ Pregunta: {pregunta}")
        print("─" * 50)
        
        # Primera llamada a Ollama con las herramientas
        response = chat(
            model=modelo,
            messages=[{'role': 'user', 'content': pregunta}],
            tools=tools,
        )
        
        # Si hay llamadas a herramientas, ejecutarlas
        if response.message.tool_calls:
            print("🔧 Ejecutando herramienta de temperatura...")
            
            # Ejecutar cada herramienta llamada
            for tool_call in response.message.tool_calls:
                function_name = tool_call.function.name
                function_args = tool_call.function.arguments
                
                if function_name in available_functions:
                    print(f"   → Consultando temperatura para: {function_args.get('ciudad', 'madrid')}")
                    
                    # Ejecutar la función
                    function_result = available_functions[function_name](**function_args)
                    print(f"   ✅ Resultado obtenido")
                    
                    # Segunda llamada con el resultado
                    final_response = chat(
                        model=modelo,
                        messages=[
                            {'role': 'user', 'content': pregunta},
                            {'role': 'assistant', 'content': '', 'tool_calls': response.message.tool_calls},
                            {'role': 'tool', 'content': function_result}
                        ],
                    )
                    
                    print("─" * 50)
                    print("🤖 Respuesta:")
                    print(final_response.message.content)
                    return final_response.message.content
        else:
            # No hay herramientas, respuesta directa
            print("💬 Respuesta directa:")
            print(response.message.content)
            return response.message.content
            
    except Exception as e:
        error_msg = f"❌ Error en chat: {str(e)}"
        print(error_msg)
        return error_msg

def main():
    """
    Función principal - modo interactivo
    """
    print("🌡️ TOOL TEMPERATURA POC")
    print("═" * 40)
    print("Pregunta por temperatura de ciudades españolas")
    print("Ciudades disponibles: madrid, barcelona, valencia, sevilla, bilbao, malaga")
    print("Escribe 'salir' para terminar")
    print("═" * 40)
    
    while True:
        try:
            pregunta = input("\n❓ Tu pregunta: ").strip()
            
            if not pregunta:
                continue
                
            if pregunta.lower() in ['salir', 'exit', 'quit']:
                print("👋 ¡Hasta luego!")
                break
            
            # Procesar la pregunta
            chat_con_temperatura(pregunta)
            
        except KeyboardInterrupt:
            print("\n👋 ¡Hasta luego!")
            break
        except Exception as e:
            print(f"❌ Error: {e}")

if __name__ == "__main__":
    main()