#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Cliente Ollama con herramienta de consulta de poblacion INE
Version SIMPLE - Sin necesidad de MCP server
"""

import requests
from ollama import chat


def consultar_poblacion_ine(lugar: str, año: int) -> str:
    """
    Consulta la poblacion de una provincia o ciudad española en el INE
    
    Args:
        lugar: Nombre de la provincia o ciudad
        año: Año de consulta (1996-2021)
    
    Returns:
        Resultado de la consulta en formato texto
    """
    try:
        # API del INE
        url = "https://servicios.ine.es/wstempus/js/ES/DATOS_TABLA/2852?tip=AM&"
        
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)',
            'Accept': 'application/json'
        }
        
        response = requests.get(url, headers=headers, timeout=30)
        
        if response.status_code != 200:
            return f"Error al consultar el INE: HTTP {response.status_code}"
        
        datos = response.json()
        nombre_buscar = lugar.lower().strip()
        
        # Buscar en los datos
        for registro in datos:
            if not isinstance(registro, dict):
                continue
            
            nombre_registro = registro.get('Nombre', '').lower()
            
            # Buscar coincidencia (Total, no por sexo)
            if (nombre_buscar in nombre_registro and 
                'total' in nombre_registro and 
                'hombres' not in nombre_registro and 
                'mujeres' not in nombre_registro):
                
                # Buscar el año
                for dato in registro.get('Data', []):
                    if not isinstance(dato, dict):
                        continue
                    
                    if dato.get('Anyo') == año:
                        poblacion = int(dato['Valor'])
                        nombre_completo = registro.get('Nombre', lugar)
                        cod_ine = registro.get('COD', 'N/A')
                        
                        return f"""Poblacion de {lugar} en {año}:
- Lugar: {nombre_completo}
- Codigo INE: {cod_ine}
- Poblacion: {poblacion:,} habitantes
- Fuente: INE (www.ine.es)"""
                
                # Encontrado pero sin dato para ese año
                return f"Se encontro {lugar} pero no hay datos para el año {año}. Prueba con años entre 1996 y 2021."
        
        return f"No se encontro '{lugar}' en la base de datos del INE. Esta API incluye provincias y capitales principales de España."
    
    except requests.RequestException as e:
        return f"Error de conexion: {str(e)}"
    except Exception as e:
        return f"Error inesperado: {str(e)}"


# Mapeo de funciones disponibles
available_functions = {
    'consultar_poblacion_ine': consultar_poblacion_ine
}


# Definir herramientas para Ollama
tools = [{
    'type': 'function',
    'function': {
        'name': 'consultar_poblacion_ine',
        'description': 'Consulta la poblacion oficial de provincias y ciudades principales de España en el Instituto Nacional de Estadistica (INE). Datos disponibles desde 1996 hasta 2021. Incluye todas las provincias y capitales de provincia.',
        'parameters': {
            'type': 'object',
            'properties': {
                'lugar': {
                    'type': 'string',
                    'description': 'Nombre de la provincia o ciudad española (ej: Madrid, Barcelona, Murcia, Salamanca, Sevilla, Valencia, Zaragoza, etc.)'
                },
                'año': {
                    'type': 'integer',
                    'description': 'Año para el que se consulta la poblacion. Debe estar entre 1996 y 2021.'
                }
            },
            'required': ['lugar', 'año']
        }
    }
}]


def chat_con_herramientas(pregunta: str, modelo: str = 'llama3.2', verbose: bool = True):
    """
    Realiza una consulta a Ollama que puede usar la herramienta de poblacion INE
    
    Args:
        pregunta: Pregunta del usuario
        modelo: Modelo de Ollama a usar
        verbose: Mostrar detalles de las llamadas
    
    Returns:
        Respuesta del modelo
    """
    messages = [{'role': 'user', 'content': pregunta}]
    
    if verbose:
        print(f"Usuario: {pregunta}")
        print()
    
    # Primera llamada a Ollama
    response = chat(
        model=modelo,
        messages=messages,
        tools=tools
    )
    
    # Verificar si el modelo quiere usar herramientas
    if response.message.tool_calls:
        # Procesar cada llamada a herramienta
        for tool_call in response.message.tool_calls:
            function_name = tool_call.function.name
            function_args = tool_call.function.arguments
            
            if verbose:
                print(f"[Ollama llama a: {function_name}]")
                print(f"[Argumentos: {function_args}]")
                print()
            
            # Ejecutar la funcion
            if function_name in available_functions:
                function_to_call = available_functions[function_name]
                function_result = function_to_call(**function_args)
                
                if verbose:
                    print("[Resultado de la consulta:]")
                    print(function_result)
                    print()
                
                # Agregar el resultado al historial
                messages.append(response.message)
                messages.append({
                    'role': 'tool',
                    'content': function_result
                })
            else:
                if verbose:
                    print(f"[ERROR] Funcion desconocida: {function_name}")
                return None
        
        # Segunda llamada con el resultado de la herramienta
        final_response = chat(
            model=modelo,
            messages=messages
        )
        
        if verbose:
            print(f"Ollama: {final_response.message.content}")
            print()
        
        return final_response.message.content
    
    else:
        # Respuesta directa sin usar herramientas
        if verbose:
            print(f"Ollama: {response.message.content}")
            print()
        
        return response.message.content


def modo_conversacion(modelo: str = 'llama3.2'):
    """
    Modo de conversacion interactivo
    """
    print("=" * 70)
    print("CHAT CON OLLAMA - Consulta de Poblacion INE")
    print("=" * 70)
    print()
    print(f"Modelo: {modelo}")
    print("Herramienta: consultar_poblacion_ine (INE - www.ine.es)")
    print()
    print("Escribe 'salir' para terminar")
    print("=" * 70)
    
    while True:
        try:
            pregunta = input("\nTu: ").strip()
            
            if not pregunta:
                continue
            
            if pregunta.lower() in ['salir', 'exit', 'quit', 'q']:
                print("\nAdios!")
                break
            
            print()
            chat_con_herramientas(pregunta, modelo=modelo, verbose=True)
            
        except KeyboardInterrupt:
            print("\n\nInterrumpido por el usuario. Adios!")
            break
        except Exception as e:
            print(f"\n[ERROR] {e}")


def main():
    """
    Funcion principal
    """
    import sys
    
    if len(sys.argv) > 1:
        # Modo de pregunta unica
        pregunta = ' '.join(sys.argv[1:])
        chat_con_herramientas(pregunta)
    else:
        # Modo conversacion
        modo_conversacion()


if __name__ == "__main__":
    main()
