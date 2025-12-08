#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Cliente Ollama con herramienta de consulta de temperatura AEMET
Version SIMPLE usando Open-Meteo (API gratuita sin necesidad de registro)
"""

import requests
from ollama import chat
from datetime import datetime, timedelta


# Coordenadas de principales ciudades españolas
COORDENADAS_CIUDADES = {
    'madrid': (40.4168, -3.7038),
    'barcelona': (41.3851, 2.1734),
    'valencia': (39.4699, -0.3763),
    'sevilla': (37.3886, -5.9823),
    'zaragoza': (41.6488, -0.8891),
    'malaga': (36.7213, -4.4214),
    'murcia': (37.9922, -1.1307),
    'palma': (39.5696, 2.6502),
    'las palmas': (28.1248, -15.4300),
    'bilbao': (43.2630, -2.9350),
    'alicante': (38.3460, -0.4907),
    'cordoba': (37.8882, -4.7794),
    'valladolid': (41.6521, -4.7286),
    'vigo': (42.2328, -8.7226),
    'gijon': (43.5322, -5.6611),
    'vitoria': (42.8467, -2.6716),
    'granada': (37.1773, -3.5986),
    'oviedo': (43.3614, -5.8493),
    'santander': (43.4623, -3.8100),
    'pamplona': (42.8125, -1.6458),
    'almeria': (36.8381, -2.4597),
    'san sebastian': (43.3183, -1.9812),
    'donostia': (43.3183, -1.9812),
    'burgos': (42.3439, -3.6969),
    'albacete': (38.9942, -1.8585),
    'castellon': (39.9864, -0.0513),
    'salamanca': (40.9701, -5.6635),
    'logroño': (42.4627, -2.4450),
    'tarragona': (41.1189, 1.2445),
    'toledo': (39.8628, -4.0273),
}


def obtener_pronostico_temperatura(ciudad: str, dias: int = 3) -> str:
    """
    Obtiene el pronostico de temperatura de una ciudad española
    Usa Open-Meteo (API gratuita sin necesidad de registro)
    
    Args:
        ciudad: Nombre de la ciudad
        dias: Numero de dias de pronostico (1-7)
    
    Returns:
        Pronostico en formato texto
    """
    try:
        # Buscar coordenadas
        ciudad_lower = ciudad.lower().strip()
        coordenadas = COORDENADAS_CIUDADES.get(ciudad_lower)
        
        if not coordenadas:
            ciudades_disponibles = ", ".join(sorted(COORDENADAS_CIUDADES.keys())[:10])
            return f"Ciudad '{ciudad}' no encontrada. Ciudades disponibles: {ciudades_disponibles}..."
        
        lat, lon = coordenadas
        
        # API Open-Meteo (gratuita, sin registro)
        url = "https://api.open-meteo.com/v1/forecast"
        
        params = {
            'latitude': lat,
            'longitude': lon,
            'daily': 'temperature_2m_max,temperature_2m_min,precipitation_probability_max,weathercode',
            'timezone': 'Europe/Madrid',
            'forecast_days': min(dias, 7)
        }
        
        response = requests.get(url, params=params, timeout=10)
        
        if response.status_code != 200:
            return f"Error al consultar la API: HTTP {response.status_code}"
        
        datos = response.json()
        
        # Extraer datos diarios
        daily = datos.get('daily', {})
        fechas = daily.get('time', [])
        temp_max = daily.get('temperature_2m_max', [])
        temp_min = daily.get('temperature_2m_min', [])
        prob_lluvia = daily.get('precipitation_probability_max', [])
        weather_codes = daily.get('weathercode', [])
        
        # Codigos de clima WMO
        weather_descriptions = {
            0: 'Despejado',
            1: 'Principalmente despejado',
            2: 'Parcialmente nublado',
            3: 'Nublado',
            45: 'Niebla',
            48: 'Niebla con escarcha',
            51: 'Llovizna ligera',
            53: 'Llovizna moderada',
            55: 'Llovizna intensa',
            61: 'Lluvia ligera',
            63: 'Lluvia moderada',
            65: 'Lluvia intensa',
            71: 'Nevada ligera',
            73: 'Nevada moderada',
            75: 'Nevada intensa',
            80: 'Chubascos ligeros',
            81: 'Chubascos moderados',
            82: 'Chubascos intensos',
            95: 'Tormenta',
            96: 'Tormenta con granizo ligero',
            99: 'Tormenta con granizo intenso',
        }
        
        # Formatear resultado
        resultado = [
            f"Pronostico de temperatura para {ciudad.title()}:",
            f"Coordenadas: {lat}, {lon}",
            ""
        ]
        
        dias_semana = ['Lunes', 'Martes', 'Miercoles', 'Jueves', 'Viernes', 'Sabado', 'Domingo']
        
        for i in range(len(fechas)):
            fecha = datetime.strptime(fechas[i], '%Y-%m-%d')
            dia_semana = dias_semana[fecha.weekday()]
            fecha_str = fecha.strftime('%d/%m/%Y')
            
            temp_max_val = temp_max[i] if i < len(temp_max) else 'N/A'
            temp_min_val = temp_min[i] if i < len(temp_min) else 'N/A'
            prob_lluvia_val = prob_lluvia[i] if i < len(prob_lluvia) else 0
            weather_code = weather_codes[i] if i < len(weather_codes) else 0
            weather_desc = weather_descriptions.get(weather_code, 'Desconocido')
            
            resultado.append(f"{dia_semana} {fecha_str}:")
            resultado.append(f"  Temperatura: {temp_min_val}°C - {temp_max_val}°C")
            resultado.append(f"  Clima: {weather_desc}")
            resultado.append(f"  Prob. lluvia: {prob_lluvia_val}%")
            resultado.append("")
        
        resultado.append("Fuente: Open-Meteo (https://open-meteo.com)")
        
        return "\n".join(resultado)
        
    except requests.RequestException as e:
        return f"Error de conexion: {str(e)}"
    except Exception as e:
        return f"Error inesperado: {str(e)}"


# Mapeo de funciones disponibles
available_functions = {
    'obtener_pronostico_temperatura': obtener_pronostico_temperatura
}


# Definir herramientas para Ollama
tools = [{
    'type': 'function',
    'function': {
        'name': 'obtener_pronostico_temperatura',
        'description': 'Obtiene el pronostico de temperatura y clima para ciudades de España. Incluye temperatura maxima y minima, condiciones climaticas y probabilidad de lluvia para los proximos dias. Datos de Open-Meteo.',
        'parameters': {
            'type': 'object',
            'properties': {
                'ciudad': {
                    'type': 'string',
                    'description': 'Nombre de la ciudad española (ej: Madrid, Barcelona, Valencia, Sevilla, Murcia, Malaga, etc.)'
                },
                'dias': {
                    'type': 'integer',
                    'description': 'Numero de dias de pronostico (entre 1 y 7). Por defecto 3.',
                    'default': 3,
                    'minimum': 1,
                    'maximum': 7
                }
            },
            'required': ['ciudad']
        }
    }
}]


def chat_con_herramientas(pregunta: str, modelo: str = 'llama3.1:8b', verbose: bool = True):
    """
    Realiza una consulta a Ollama que puede usar la herramienta de temperatura
    
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
                
                # Valores por defecto
                if 'dias' not in function_args:
                    function_args['dias'] = 3
                
                function_result = function_to_call(**function_args)
                
                if verbose:
                    print("[Resultado del pronostico:]")
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


def modo_conversacion(modelo: str = 'llama3.1:8b'):
    """
    Modo de conversacion interactivo
    """
    print("=" * 70)
    print("CHAT CON OLLAMA - Pronostico de Temperatura")
    print("=" * 70)
    print()
    print(f"Modelo: {modelo}")
    print("Herramienta: obtener_pronostico_temperatura (Open-Meteo)")
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
