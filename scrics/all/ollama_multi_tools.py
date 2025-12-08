#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Ollama Chat con MÚLTIPLES TOOLS
Sistema modular que carga tools desde la carpeta tools/
"""

import sys
import os
import ollama

# Añadir carpeta tools al path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'tools'))

# Importar todas las tools
from ollama_temperatura import (
    obtener_pronostico_temperatura,
    TOOL_DEFINITION as TEMP_TOOL,
    KEYWORDS as TEMP_KEYWORDS
)

from git_clone import (
    clonar_repositorio_git,
    TOOL_DEFINITION as GIT_TOOL,
    KEYWORDS as GIT_KEYWORDS
)


def main():
    """Chat con Ollama usando múltiples tools"""
    
    # Registro de funciones disponibles
    available_functions = {
        'obtener_pronostico_temperatura': obtener_pronostico_temperatura,
        'clonar_repositorio_git': clonar_repositorio_git
    }
    
    # Registro de tools con sus keywords
    tools_registry = [
        {
            'definition': TEMP_TOOL,
            'keywords': TEMP_KEYWORDS,
            'name': 'temperatura'
        },
        {
            'definition': GIT_TOOL,
            'keywords': GIT_KEYWORDS,
            'name': 'git'
        }
    ]
    
    # System prompt
    messages = [
        {
            'role': 'system',
            'content': '''Eres un asistente útil con acceso a múltiples herramientas:

1. TEMPERATURA: Pronóstico del tiempo para ciudades de España
2. GIT CLONE: Clonar repositorios de Git

IMPORTANTE:
- Cuando uses herramientas, SIEMPRE presenta los resultados obtenidos de forma clara
- NO digas "no tengo acceso a información" si ya obtuviste datos de herramientas
- Si te preguntan por VARIAS ciudades o repos, usa la herramienta VARIAS VECES
- Para comparaciones, llama a la herramienta para CADA elemento y luego compara'''
        }
    ]
    
    print("="*60)
    print("Ollama Chat - Múltiples Tools")
    print("="*60)
    print("Tools disponibles:")
    for tool in tools_registry:
        print(f"  - {tool['name']}")
    print("\nComandos: /bye (salir), /clear (limpiar), /help (ayuda)")
    print("="*60)
    
    while True:
        try:
            user_input = input("\n>>> ").strip()
        except (EOFError, KeyboardInterrupt):
            print()
            break
        
        if not user_input:
            continue
        
        # Comandos
        if user_input in ['/bye', '/exit', '/quit']:
            break
            
        if user_input == '/clear':
            messages = [messages[0]]  # Mantener system prompt
            print("Conversación limpiada")
            continue
            
        if user_input == '/help':
            print("\nComandos disponibles:")
            print("  /bye    - Salir")
            print("  /clear  - Limpiar conversación")
            print("  /help   - Esta ayuda")
            print("\nTools disponibles:")
            for tool in tools_registry:
                print(f"  - {tool['name']}: {', '.join(tool['keywords'][:5])}...")
            continue
        
        # Agregar mensaje del usuario
        messages.append({'role': 'user', 'content': user_input})
        
        # Detectar qué tools activar basándose en keywords
        user_lower = user_input.lower()
        active_tools = []
        
        for tool in tools_registry:
            if any(keyword in user_lower for keyword in tool['keywords']):
                active_tools.append(tool['definition'])
        
        # Llamar a Ollama
        try:
            if active_tools:
                # Con tools activadas
                response = ollama.chat(
                    model='llama3.1:8b',
                    messages=messages,
                    tools=active_tools
                )
            else:
                # Sin tools (pregunta general)
                response = ollama.chat(
                    model='llama3.1:8b',
                    messages=messages
                )
            
        except Exception as e:
            print(f"❌ Error al conectar con Ollama: {e}")
            print("¿Está Ollama corriendo? (ollama serve)")
            messages.pop()
            continue
        
        messages.append(response['message'])
        
        # Si usó tools
        if response['message'].get('tool_calls'):
            num_calls = len(response['message']['tool_calls'])
            print(f"[DEBUG] Ollama usó {num_calls} tool(s)")
            
            for tool_call in response['message']['tool_calls']:
                func_name = tool_call['function']['name']
                func_args = tool_call['function']['arguments']
                
                print(f"[DEBUG] Función: {func_name}")
                print(f"[DEBUG] Argumentos: {func_args}")
                
                if func_name in available_functions:
                    # Ejecutar función
                    func_result = available_functions[func_name](**func_args)
                    
                    # Agregar resultado
                    messages.append({
                        'role': 'tool',
                        'content': func_result
                    })
            
            # Segunda llamada para procesar resultados
            try:
                final_response = ollama.chat(
                    model='llama3.1:8b',
                    messages=messages,
                    options={'temperature': 0.3}
                )
                
                print(f"\n{final_response['message']['content']}")
                messages.append(final_response['message'])
                
            except Exception as e:
                print(f"❌ Error en respuesta final: {e}")
        else:
            # Respuesta directa
            print(f"\n{response['message']['content']}")


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "--test":
        print("TEST MODE\n")
        print("="*60)
        print("Test 1: Temperatura")
        print(obtener_pronostico_temperatura("Madrid", 3))
        print("\n" + "="*60)
        print("Test 2: Git Clone (simulado)")
        print(clonar_repositorio_git("https://github.com/python/cpython.git", "test_repo"))
    else:
        main()
