#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
TOOL MÍNIMA POC - Para entender cómo funcionan las tools
"""

import subprocess
import os
from ollama import chat

def obtener_temperatura(ciudad="madrid"):
    """
    Función mínima que ejecuta el script de temperatura
    """
    script_path = os.path.join(os.path.dirname(__file__), 'consulta_temperatura.py')
    
    try:
        result = subprocess.run(
            ['python', script_path, ciudad],
            capture_output=True,
            text=True,
            timeout=10
        )
        return result.stdout.strip() if result.returncode == 0 else f"Error: {result.stderr}"
    except Exception as e:
        return f"Error: {str(e)}"

# DEFINICIÓN MÍNIMA DE LA TOOL
tool_definition = {
    'type': 'function',
    'function': {
        'name': 'obtener_temperatura',
        'description': 'Consulta la temperatura de una ciudad española',
        'parameters': {
            'type': 'object',
            'properties': {
                'ciudad': {
                    'type': 'string',
                    'description': 'Ciudad española (madrid, barcelona, valencia...)'
                }
            },
            'required': ['ciudad']
        }
    }
}

def chat_simple(pregunta, modelo='llama3.1:8b'):
    """
    Chat mínimo con una sola tool
    """
    print(f"🤖 Pregunta: {pregunta}")
    
    # 1. Primera llamada - Ollama decide si usar la tool
    response = chat(
        model=modelo,
        messages=[{'role': 'user', 'content': pregunta}],
        tools=[tool_definition]
    )
    
    # 2. Si usa la tool, ejecutarla
    if response.message.tool_calls:
        tool_call = response.message.tool_calls[0]
        ciudad = tool_call.function.arguments['ciudad']
        
        print(f"🔧 Ejecutando tool para: {ciudad}")
        resultado = obtener_temperatura(ciudad)
        print(f"📋 Resultado: {resultado[:50]}...")
        
        # 3. Segunda llamada con el resultado
        final_response = chat(
            model=modelo,
            messages=[
                {'role': 'user', 'content': pregunta},
                {'role': 'assistant', 'content': '', 'tool_calls': response.message.tool_calls},
                {'role': 'tool', 'content': resultado}
            ]
        )
        return final_response.message.content
    else:
        # Sin tools
        return response.message.content

if __name__ == "__main__":
    # PRUEBAS SIMPLES
    print("=== TOOL MÍNIMA POC ===")
    
    # Prueba 1: Pregunta que debería activar la tool
    print("\n1. Pregunta sobre temperatura:")
    respuesta = chat_simple("¿Qué temperatura hace en Barcelona?")
    print(f"✅ Respuesta: {respuesta}")
    
    # Prueba 2: Pregunta que NO debería activar la tool  
    print("\n2. Pregunta general:")
    respuesta = chat_simple("¿Cómo estás?")
    print(f"✅ Respuesta: {respuesta}")