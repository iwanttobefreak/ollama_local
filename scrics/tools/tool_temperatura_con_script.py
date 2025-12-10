#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import subprocess
import os
from ollama import chat

def es_pregunta_climatica(pregunta):
    """
    Valida si una pregunta es realmente sobre clima/tiempo
    """
    pregunta_lower = pregunta.lower()
    
    # Palabras que Si indican clima
    palabras_clima = ['temperatura', 'clima', 'tiempo', 'lluvia', 'calor', 'frio', 'humedad', 'viento', 'nublado', 'sol', 'meteorologico', 'pronostico', 'manana', 'semana']
    
    # Palabras que NO son clima (excluyen)
    palabras_no_clima = ['habitantes', 'poblacion', 'gente', 'personas', 'demografia', 'superficie', 'extension', 'economia', 'historia', 'cultura', 'cuantos', 'cuantas']
    
    # Si contiene palabras de no-clima, rechazar
    for palabra in palabras_no_clima:
        if palabra in pregunta_lower:
            return False
    
    # Si contiene palabras de clima, aceptar
    for palabra in palabras_clima:
        if palabra in pregunta_lower:
            return True
    
    # Si no encuentra nada claro, rechazar por seguridad
    return False

def consultar_clima(ciudad, dias=3):
    script_path = '/app/scrics/tools/script_temperatura.py'
    
    try:
        result = subprocess.run(
            ['python', script_path, ciudad, str(dias)],
            capture_output=True,
            text=True,
            timeout=15
        )
        return result.stdout.strip() if result.returncode == 0 else f"Error: {result.stderr}"
    except Exception as e:
        return f"Error: {str(e)}"

# DEFINICION MINIMA DE LA TOOL
tool_definition = {
    'type': 'function',
    'function': {
        'name': 'consultar_clima',
        'description': 'SOLO para consultas meteorologicas: temperatura, lluvia, clima, tiempo. Usar UNICAMENTE cuando el usuario pregunta por TIEMPO/CLIMA/TEMPERATURA/LLUVIA/HUMEDAD. NUNCA usar para: habitantes, poblacion, demografia, geografia, historia, economia, cultura, superficie, densidad, gente, personas. Ejemplo SI: "temperatura Madrid", "lluvias Valencia". Ejemplo NO: "habitantes Barcelona", "poblacion Sevilla".',
        'parameters': {
            'type': 'object',
            'properties': {
                'ciudad': {
                    'type': 'string',
                    'description': 'Nombre de la ciudad espanola para consultar el clima'
                },
                'dias': {
                    'type': 'integer',
                    'description': 'Numero de dias para el pronostico (1-7). Por defecto 3 dias.',
                    'minimum': 1,
                    'maximum': 7,
                    'default': 3
                }
            },
            'required': ['ciudad']
        }
    }
}

def chat_simple(pregunta, modelo='llama3.1:8b'):
    """
    Chat minimo con una sola tool
    """
    print(f"[DEBUG] Pregunta recibida: {pregunta}")
    prompt_llm = [
        {'role': 'user', 'content': pregunta}
    ]
    print(f"[DEBUG] Prompt enviado al LLM:")
    for msg in prompt_llm:
        print(f"  - role: {msg['role']}, content: {msg['content']}")
    print(f"[DEBUG] Tool definition disponible: {tool_definition['function']['name']}")
    print("[DEBUG] Llamando al LLM (Ollama) con tools...")
    response = chat(
        model=modelo,
        messages=prompt_llm,
        tools=[tool_definition]
    )
    print(f"[DEBUG] Respuesta completa del LLM:")
    print(f"  - role: {response.message.role}")
    print(f"  - content: {response.message.content}")
    if response.message.tool_calls:
        print(f"  - tool_calls: [")
        for tc in response.message.tool_calls:
            print(f"      {tc},")
        print(f"    ]")
    else:
        print(f"  - tool_calls: None")
    if response.message.tool_calls:
        print("[DEBUG] El LLM ha decidido llamar a la tool porque la pregunta coincide con la descripción y parámetros definidos.")
        tool_call = response.message.tool_calls[0]
        print(f"[DEBUG] tool_call: {tool_call}")
        ciudad = tool_call.function.arguments['ciudad']
        dias = tool_call.function.arguments.get('dias', 3)
        print(f"[DEBUG] Argumentos extraídos: ciudad={ciudad}, dias={dias}")
        if not es_pregunta_climatica(pregunta):
            print(f"[ADVERTENCIA] Pregunta no parece climatica: {pregunta}")
            return "Lo siento, esa pregunta no es sobre clima o temperatura."
        print(f"[DEBUG] Ejecutando script externo para: {ciudad} ({dias} dias)")
        resultado = consultar_clima(ciudad, dias)
        print(f"[DEBUG] Resultado del script: {resultado[:100]}...")
        print("[DEBUG] Enviando resultado de la tool al LLM para respuesta final...")
        final_response = chat(
            model=modelo,
            messages=[
                {'role': 'user', 'content': pregunta},
                {'role': 'assistant', 'content': '', 'tool_calls': response.message.tool_calls},
                {'role': 'tool', 'content': resultado}
            ]
        )
        print(f"[DEBUG] Respuesta final del LLM:")
        print(f"  - role: {final_response.message.role}")
        print(f"  - content: {final_response.message.content}")
        return final_response.message.content
    else:
        print("[DEBUG] El LLM NO ha solicitado llamar a la tool. Esto ocurre porque la pregunta no coincide con la descripción de la tool o los parámetros requeridos.")
        print(f"[DEBUG] Respuesta directa del LLM: {response.message.content}")
        return response.message.content

if __name__ == "__main__":
    # PRUEBAS ESPECIFICAS
    print("=== TOOL CLIMA POC ===")
    # Modo demo interactivo
    while True:
        print("\nIntroduce una pregunta sobre el clima (o escribe 'salir' para terminar):")
        pregunta = input('>>> ').strip()
        if pregunta.lower() in ("salir", "exit", "quit"):  # Salida
            print("Saliendo del modo interactivo.")
            break
        if not pregunta:
            continue
        respuesta = chat_simple(pregunta)
        print(f"\nRespuesta: {respuesta}\n")
