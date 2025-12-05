#!/usr/bin/env python3
import ollama
import subprocess

# Definir la tool
TOOL = {
    'type': 'function',
    'function': {
        'name': 'obtener_temperatura',
        'description': 'Obtiene temperatura de ciudades españolas',
        'parameters': {
            'type': 'object',
            'properties': {
                'ciudad': {'type': 'string', 'description': 'Nombre de la ciudad'}
            },
            'required': ['ciudad']
        }
    }
}

# Función que ejecuta el script
def obtener_temp(ciudad):
    resultado = subprocess.run(
        ['python3', 'script_pronostico_temperatura.py', ciudad],
        capture_output=True,
        text=True
    )
    return resultado.stdout

# Chat
mensajes = [{'role': 'system', 'content': 'Asistente con acceso a herramientas meteorológicas.'}]

while True:
    pregunta = input("\nChat: ").strip()
    if pregunta.lower() == 'salir':
        break

    mensajes.append({'role': 'user', 'content': pregunta})

    # Primera llamada: LLM decide
    respuesta = ollama.chat(model='llama3.1:8b', messages=mensajes, tools=[TOOL])

    # ¿Usó la tool?
    if respuesta['message'].get('tool_calls'):
        ciudad = respuesta['message']['tool_calls'][0]['function']['arguments']['ciudad']
        resultado = obtener_temp(ciudad)

        mensajes.append(respuesta['message'])
        mensajes.append({'role': 'tool', 'content': resultado})

        # Segunda llamada: LLM procesa resultado
        respuesta = ollama.chat(model='llama3.1:8b', messages=mensajes)

    print(f"Asistente: {respuesta['message']['content']}")
    mensajes.append({'role': 'assistant', 'content': respuesta['message']['content']})
