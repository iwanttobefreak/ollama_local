#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Tool de Temperatura para Ollama (VERSION STANDALONE)
Copia este archivo al servidor donde corre Ollama y ejecutalo
NO necesita otros archivos - Todo incluido aqui
"""

import requests
import ollama
from datetime import datetime


def buscar_ciudad_nominatim(nombre_ciudad):
    """
    Busca una ciudad usando Nominatim (OpenStreetMap)
    """
    try:
        url = "https://nominatim.openstreetmap.org/search"
        params = {
            'q': f"{nombre_ciudad}, España",
            'format': 'json',
            'limit': 5,
            'addressdetails': 1
        }
        headers = {
            'User-Agent': 'PronosticoTemperatura/1.0'
        }
        
        response = requests.get(url, params=params, headers=headers, timeout=10)
        
        if response.status_code != 200:
            return None, None, None
        
        resultados = response.json()
        
        if not resultados:
            return None, None, None
        
        # Filtrar solo resultados en España
        resultados_espana = [r for r in resultados if r.get('address', {}).get('country') == 'España']
        
        if not resultados_espana:
            return None, None, None
        
        lugar = resultados_espana[0]
        lat = float(lugar['lat'])
        lon = float(lugar['lon'])
        
        address = lugar.get('address', {})
        nombre = (
            address.get('city') or 
            address.get('town') or 
            address.get('village') or 
            address.get('municipality') or
            nombre_ciudad.title()
        )
        
        return lat, lon, nombre
        
    except Exception as e:
        return None, None, None


def obtener_pronostico_temperatura(ciudad: str, dias: int = 3) -> str:
    """
    Obtiene el pronostico de temperatura para CUALQUIER ciudad española
    
    Args:
        ciudad: Nombre de la ciudad
        dias: Numero de dias de pronostico (1-16)
    
    Returns:
        Pronostico formateado como texto
    """
    try:
        if dias < 1 or dias > 16:
            return "Error: El numero de dias debe estar entre 1 y 16"
        
        # Buscar ciudad
        lat, lon, nombre = buscar_ciudad_nominatim(ciudad)
        
        if not lat:
            return f"Error: No se encontro la ciudad '{ciudad}' en España"
        
        # Obtener pronostico de Open-Meteo
        url = "https://api.open-meteo.com/v1/forecast"
        
        params = {
            'latitude': lat,
            'longitude': lon,
            'daily': 'temperature_2m_max,temperature_2m_min,precipitation_probability_max,weathercode,windspeed_10m_max',
            'timezone': 'Europe/Madrid',
            'forecast_days': min(dias, 16)
        }
        
        response = requests.get(url, params=params, timeout=15)
        
        if response.status_code != 200:
            return f"Error: No se pudo obtener el pronostico (HTTP {response.status_code})"
        
        datos = response.json()
        
        daily = datos.get('daily', {})
        fechas = daily.get('time', [])
        temp_max = daily.get('temperature_2m_max', [])
        temp_min = daily.get('temperature_2m_min', [])
        prob_lluvia = daily.get('precipitation_probability_max', [])
        weather_codes = daily.get('weathercode', [])
        viento = daily.get('windspeed_10m_max', [])
        
        # Formatear resultado
        weather_descriptions = {
            0: 'Despejado', 1: 'Principalmente despejado', 2: 'Parcialmente nublado',
            3: 'Nublado', 45: 'Niebla', 48: 'Niebla con escarcha',
            51: 'Llovizna ligera', 53: 'Llovizna moderada', 55: 'Llovizna intensa',
            61: 'Lluvia ligera', 63: 'Lluvia moderada', 65: 'Lluvia intensa',
            71: 'Nevada ligera', 73: 'Nevada moderada', 75: 'Nevada intensa',
            80: 'Chubascos ligeros', 81: 'Chubascos moderados', 82: 'Chubascos intensos',
            95: 'Tormenta', 96: 'Tormenta con granizo ligero', 99: 'Tormenta con granizo intenso',
        }
        
        dias_semana = ['Lunes', 'Martes', 'Miercoles', 'Jueves', 'Viernes', 'Sabado', 'Domingo']
        
        resultado = [f"Pronostico de temperatura para {nombre}:", ""]
        
        for i, fecha_str in enumerate(fechas):
            fecha = datetime.strptime(fecha_str, '%Y-%m-%d')
            dia_semana = dias_semana[fecha.weekday()]
            fecha_formato = fecha.strftime('%d/%m/%Y')
            
            temp_max_val = temp_max[i]
            temp_min_val = temp_min[i]
            prob_lluvia_val = prob_lluvia[i]
            weather_code = weather_codes[i]
            viento_val = viento[i]
            
            weather_desc = weather_descriptions.get(weather_code, 'Desconocido')
            
            hoy = datetime.now().date()
            if fecha.date() == hoy:
                etiqueta = " (HOY)"
            elif (fecha.date() - hoy).days == 1:
                etiqueta = " (MAÑANA)"
            else:
                etiqueta = ""
            
            resultado.append(f"{dia_semana} {fecha_formato}{etiqueta}:")
            resultado.append(f"  Temperatura: {temp_min_val:.1f}°C - {temp_max_val:.1f}°C")
            resultado.append(f"  Clima: {weather_desc}")
            resultado.append(f"  Probabilidad de lluvia: {prob_lluvia_val:.0f}%")
            resultado.append(f"  Viento: {viento_val:.1f} km/h")
            resultado.append("")
        
        resultado.append("Fuente: Open-Meteo")
        resultado.append(f"Coordenadas: {lat:.4f}, {lon:.4f}")
        
        return "\n".join(resultado)
        
    except Exception as e:
        return f"Error al obtener el pronostico: {str(e)}"


# Definicion de la herramienta para Ollama
TOOL_DEFINITION = {
    'type': 'function',
    'function': {
        'name': 'obtener_pronostico_temperatura',
        'description': 'Obtiene el pronostico de temperatura y clima para CUALQUIER ciudad de España. Incluye temperatura maxima y minima, condiciones climaticas, probabilidad de lluvia y velocidad del viento.',
        'parameters': {
            'type': 'object',
            'properties': {
                'ciudad': {
                    'type': 'string',
                    'description': 'Nombre de CUALQUIER ciudad española (Madrid, Barcelona, Mataro, Alcobendas, etc.)'
                },
                'dias': {
                    'type': 'integer',
                    'description': 'Numero de dias de pronostico (1-16). Por defecto 3.',
                    'default': 3,
                    'minimum': 1,
                    'maximum': 16
                }
            },
            'required': ['ciudad']
        }
    }
}


def chat_con_herramientas():
    """
    Chat interactivo con Ollama (estilo 'ollama run')
    Usa la tool de temperatura solo cuando sea necesario
    """
    # Funciones disponibles
    available_functions = {
        'obtener_pronostico_temperatura': obtener_pronostico_temperatura
    }
    
    messages = []
    
    while True:
        try:
            # Prompt igual que 'ollama run'
            user_input = input(">>> ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\n")
            break
        
        if not user_input:
            continue
        
        # Comandos especiales
        if user_input in ['/bye', '/exit']:
            break
        
        if user_input == '/clear':
            messages = []
            print("Conversacion limpiada")
            continue
        
        if user_input == '/help':
            print("\nComandos disponibles:")
            print("  /bye    - Salir del chat")
            print("  /clear  - Limpiar historial de conversacion")
            print("  /help   - Mostrar esta ayuda")
            print("\nPreguntame sobre cualquier tema.")
            print("Usare la herramienta de temperatura automaticamente si preguntas sobre el tiempo.\n")
            continue
        
        messages.append({
            'role': 'user',
            'content': user_input
        })
        
        # Llamar a Ollama con la tool disponible
        response = ollama.chat(
            model='llama3.1',
            messages=messages,
            tools=[TOOL_DEFINITION]
        )
        
        messages.append(response['message'])
        
        # Verificar si Ollama decide usar la herramienta
        if response['message'].get('tool_calls'):
            # Ollama decidió usar la tool (pregunta sobre el tiempo)
            for tool_call in response['message']['tool_calls']:
                function_name = tool_call['function']['name']
                function_args = tool_call['function']['arguments']
                
                if function_name in available_functions:
                    # Ejecutar la herramienta
                    function_response = available_functions[function_name](**function_args)
                    
                    # Debug: verificar respuesta
                    if not function_response or function_response.startswith("Error"):
                        print(f"[Error en la tool: {function_response}]")
                    
                    messages.append({
                        'role': 'tool',
                        'content': function_response
                    })
            
            # Obtener respuesta final de Ollama (sin tools para que no las llame de nuevo)
            final_response = ollama.chat(
                model='llama3.1',
                messages=messages
            )
            
            print(final_response['message']['content'])
            print()
            messages.append(final_response['message'])
        else:
            # Respuesta directa (no necesita la tool)
            print(response['message']['content'])
            print()


if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1 and sys.argv[1] == "--test":
        # Modo test
        print("MODO TEST - Probando la funcion\n")
        resultado = obtener_pronostico_temperatura("Madrid", 3)
        print(resultado)
    else:
        # Chat interactivo (estilo ollama run)
        print("Escribe /bye para salir o /help para ver comandos")
        chat_con_herramientas()
