#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Ejemplo de uso de la tool de temperatura con Ollama
Muestra diferentes formas de integrar la herramienta
"""

from ollama_temperatura_tool import obtener_pronostico_temperatura, TOOL_DEFINITION
import ollama


def ejemplo_1_uso_directo():
    """
    Ejemplo 1: Usar la funcion directamente (sin Ollama)
    """
    print("=" * 70)
    print("EJEMPLO 1: Uso Directo de la Funcion")
    print("=" * 70)
    print()
    
    # Llamar directamente a la funcion
    resultado = obtener_pronostico_temperatura("Madrid", 3)
    print(resultado)
    print()


def ejemplo_2_ollama_simple():
    """
    Ejemplo 2: Usar con Ollama en una consulta simple
    """
    print("=" * 70)
    print("EJEMPLO 2: Consulta Simple con Ollama")
    print("=" * 70)
    print()
    
    # Funciones disponibles
    available_functions = {
        'obtener_pronostico_temperatura': obtener_pronostico_temperatura
    }
    
    # Pregunta del usuario
    user_question = "¿Qué tiempo hará mañana en Barcelona?"
    print(f"Pregunta: {user_question}")
    print()
    
    # Llamar a Ollama
    response = ollama.chat(
        model='llama3.1',
        messages=[
            {'role': 'user', 'content': user_question}
        ],
        tools=[TOOL_DEFINITION]
    )
    
    # Ver si Ollama quiere usar la herramienta
    if response['message'].get('tool_calls'):
        print("[Ollama quiere usar la herramienta]")
        print()
        
        for tool_call in response['message']['tool_calls']:
            function_name = tool_call['function']['name']
            function_args = tool_call['function']['arguments']
            
            print(f"Funcion: {function_name}")
            print(f"Argumentos: {function_args}")
            print()
            
            # Ejecutar la funcion
            if function_name in available_functions:
                function_response = available_functions[function_name](**function_args)
                print("Resultado de la herramienta:")
                print("-" * 70)
                print(function_response)
                print("-" * 70)
                print()
                
                # Enviar el resultado a Ollama para que lo procese
                messages = [
                    {'role': 'user', 'content': user_question},
                    response['message'],
                    {'role': 'tool', 'content': function_response}
                ]
                
                final_response = ollama.chat(
                    model='llama3.1',
                    messages=messages
                )
                
                print("Respuesta final de Ollama:")
                print(final_response['message']['content'])
    else:
        # Respuesta directa
        print("Respuesta de Ollama:")
        print(response['message']['content'])
    
    print()


def ejemplo_3_multiple_ciudades():
    """
    Ejemplo 3: Comparar el tiempo en varias ciudades
    """
    print("=" * 70)
    print("EJEMPLO 3: Comparar Varias Ciudades")
    print("=" * 70)
    print()
    
    ciudades = ["Madrid", "Barcelona", "Sevilla"]
    
    print(f"Comparando el tiempo en: {', '.join(ciudades)}")
    print()
    
    for ciudad in ciudades:
        print(f"\n{'=' * 70}")
        print(f"{ciudad.upper()}")
        print('=' * 70)
        resultado = obtener_pronostico_temperatura(ciudad, 2)
        print(resultado)


def ejemplo_4_pregunta_compleja():
    """
    Ejemplo 4: Pregunta compleja que requiere multiples llamadas
    """
    print("=" * 70)
    print("EJEMPLO 4: Pregunta Compleja con Ollama")
    print("=" * 70)
    print()
    
    available_functions = {
        'obtener_pronostico_temperatura': obtener_pronostico_temperatura
    }
    
    # Pregunta que requiere comparar ciudades
    user_question = "¿Dónde hará mejor tiempo este fin de semana: Madrid o Barcelona? Dame detalles."
    print(f"Pregunta: {user_question}")
    print()
    
    messages = [{'role': 'user', 'content': user_question}]
    
    # Bucle para manejar multiples llamadas a herramientas
    max_iterations = 5
    for iteration in range(max_iterations):
        response = ollama.chat(
            model='llama3.1',
            messages=messages,
            tools=[TOOL_DEFINITION]
        )
        
        messages.append(response['message'])
        
        if response['message'].get('tool_calls'):
            print(f"[Iteracion {iteration + 1}: Ollama usa herramientas]")
            
            for tool_call in response['message']['tool_calls']:
                function_name = tool_call['function']['name']
                function_args = tool_call['function']['arguments']
                
                print(f"  - Consultando: {function_args.get('ciudad', 'N/A')}")
                
                if function_name in available_functions:
                    function_response = available_functions[function_name](**function_args)
                    messages.append({
                        'role': 'tool',
                        'content': function_response
                    })
            
            print()
        else:
            # Respuesta final
            print("Respuesta final de Ollama:")
            print("-" * 70)
            print(response['message']['content'])
            print("-" * 70)
            break
    
    print()


def menu():
    """
    Menu interactivo
    """
    print("=" * 70)
    print("EJEMPLOS DE USO - Tool de Temperatura para Ollama")
    print("=" * 70)
    print()
    print("Selecciona un ejemplo:")
    print()
    print("1. Uso directo de la funcion (sin Ollama)")
    print("2. Consulta simple con Ollama")
    print("3. Comparar varias ciudades")
    print("4. Pregunta compleja con Ollama")
    print("5. Ejecutar todos los ejemplos")
    print("0. Salir")
    print()
    
    while True:
        try:
            opcion = input("Opcion: ").strip()
            
            if opcion == "1":
                ejemplo_1_uso_directo()
                input("\nPresiona Enter para continuar...")
            elif opcion == "2":
                ejemplo_2_ollama_simple()
                input("\nPresiona Enter para continuar...")
            elif opcion == "3":
                ejemplo_3_multiple_ciudades()
                input("\nPresiona Enter para continuar...")
            elif opcion == "4":
                ejemplo_4_pregunta_compleja()
                input("\nPresiona Enter para continuar...")
            elif opcion == "5":
                ejemplo_1_uso_directo()
                input("\nPresiona Enter para continuar...")
                ejemplo_2_ollama_simple()
                input("\nPresiona Enter para continuar...")
                ejemplo_3_multiple_ciudades()
                input("\nPresiona Enter para continuar...")
                ejemplo_4_pregunta_compleja()
                input("\nPresiona Enter para continuar...")
            elif opcion == "0":
                print("\nAdios!")
                break
            else:
                print("Opcion no valida. Intenta de nuevo.")
        except KeyboardInterrupt:
            print("\n\nAdios!")
            break


if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1:
        # Ejecutar ejemplo especifico desde linea de comandos
        if sys.argv[1] == "1":
            ejemplo_1_uso_directo()
        elif sys.argv[1] == "2":
            ejemplo_2_ollama_simple()
        elif sys.argv[1] == "3":
            ejemplo_3_multiple_ciudades()
        elif sys.argv[1] == "4":
            ejemplo_4_pregunta_compleja()
        else:
            print("Uso: python ejemplos_ollama_temperatura.py [1|2|3|4]")
    else:
        # Menu interactivo
        menu()
