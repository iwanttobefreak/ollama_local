import pprint
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Tool de Ollama para consultar pronostico de temperatura
Funciona con CUALQUIER ciudad - SIN datos hardcodeados
"""

import requests
from datetime import datetime


def buscar_ciudad_nominatim(nombre_ciudad):
    """
    Busca una ciudad usando Nominatim (OpenStreetMap)
    NO usa datos hardcodeados
    
    Returns:
        Tupla (latitud, longitud, nombre_completo) o (None, None, None)
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
        
        # Tomar el primer resultado
        lugar = resultados_espana[0]
        lat = float(lugar['lat'])
        lon = float(lugar['lon'])
        
        # Extraer nombre de la ciudad
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
    print(f"[DEBUG] obtener_pronostico_temperatura: ciudad={ciudad}, dias={dias}")
    """
    Obtiene el pronostico de temperatura para CUALQUIER ciudad española
    
    Args:
        ciudad: Nombre de la ciudad (ej: Madrid, Barcelona, Mataro, Alcobendas, etc.)
        dias: Numero de dias de pronostico (entre 1 y 16). Por defecto 3.
    
    Returns:
        Pronostico formateado como texto
    """
    try:
        # Validar dias
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
        'name': 'consultar_clima',
        'description': 'SOLO para consultas meteorológicas: temperatura, lluvia, clima, tiempo, humedad, viento, nublado, sol, pronóstico, semana, mañana, nieve, tormenta. Usar UNICAMENTE cuando el usuario pregunta por TIEMPO/CLIMA/TEMPERATURA/LLUVIA/HUMEDAD/VIENTO/NIEVE/TORMENTA. NUNCA usar para: habitantes, poblacion, demografia, geografia, historia, economia, cultura, superficie, densidad, gente, personas. Ejemplo SI: "temperatura Madrid", "lluvias Valencia", "¿va a nevar en Huesca?", "¿qué viento hará en Bilbao?". Ejemplo NO: "habitantes Barcelona", "poblacion Sevilla".',
        'parameters': {
            'type': 'object',
            'properties': {
                'ciudad': {
                    'type': 'string',
                    'description': 'Nombre de la ciudad española para consultar el clima'
                },
                'dias': {
                    'type': 'integer',
                    'description': 'Número de días para el pronóstico (1-7). Por defecto 3 días.',
                    'minimum': 1,
                    'maximum': 7,
                    'default': 3
                }
            },
            'required': ['ciudad']
        }
    }
}


# Para usar con Ollama
if __name__ == "__main__":
    import sys
    import ollama
    
    # Funciones disponibles
    available_functions = {
        'obtener_pronostico_temperatura': obtener_pronostico_temperatura
    }
    
    palabras_clima = ['temperatura', 'clima', 'tiempo', 'lluvia', 'calor', 'frio', 'humedad', 'viento', 'nublado', 'sol', 'meteorologico', 'pronostico', 'manana', 'semana', 'nieve', 'tormenta']
    palabras_no_clima = ['habitantes', 'poblacion', 'gente', 'personas', 'demografia', 'superficie', 'extension', 'economia', 'historia', 'cultura', 'cuantos', 'cuantas']

    def es_pregunta_climatica(pregunta):
        pregunta_lower = pregunta.lower()
        for palabra in palabras_no_clima:
            if palabra in pregunta_lower:
                return False
        for palabra in palabras_clima:
            if palabra in pregunta_lower:
                return True
        return False

    def chat_con_herramientas():
        """
        Chat interactivo con Ollama usando la herramienta de temperatura
        """
        print("=" * 70)
        print("CHAT DE TEMPERATURA CON OLLAMA")
        print("Pregunta sobre el tiempo en CUALQUIER ciudad de España")
        print("=" * 70)
        print()
        print("Ejemplos de preguntas:")
        print("  - ¿Que tiempo hara mañana en Madrid?")
        print("  - Pronostico de 5 dias para Mataro")
        print("  - ¿Llovera en Alcobendas esta semana?")
        print("  - Temperatura en Barcelona los proximos 3 dias")
        print()
        print("Escribe 'salir' para terminar")
        print()
        
        # Historial de conversacion
        messages = []
        
        while True:
            try:
                user_input = input("Tu: ").strip()
            except (EOFError, KeyboardInterrupt):
                print("\n\nAdios!")
                break
            if not user_input:
                continue
            if user_input.lower() in ['salir', 'exit', 'quit']:
                print("Adios!")
                break
            print(f"[DEBUG] Pregunta recibida: {user_input}")
            print(f"[DEBUG] ¿Es pregunta climática?: {es_pregunta_climatica(user_input)}")
            messages.append({
                'role': 'user',
                'content': user_input
            })
            print(f"[DEBUG] Mensajes enviados al LLM:")
            pprint.pprint(messages)
            print(f"[DEBUG] Tool definition disponible: {TOOL_DEFINITION['function']['name']}")
            response = ollama.chat(
                model='llama3.1:8b',
                messages=messages,
                tools=[TOOL_DEFINITION]
            )
            print(f"[DEBUG] Respuesta del LLM:")
            pprint.pprint(response)
            messages.append(response['message'])
            if response['message'].get('tool_calls'):
                print(f"[DEBUG] tool_calls detectados:")
                for tool_call in response['message']['tool_calls']:
                    pprint.pprint(tool_call)
                    function_name = tool_call['function']['name']
                    function_args = tool_call['function']['arguments']
                    print(f"[DEBUG] Ejecutando función: {function_name} con argumentos: {function_args}")
                    if function_name in available_functions:
                        print(f"\n[Consultando {function_args.get('ciudad')}...]\n")
                        function_response = available_functions[function_name](**function_args)
                        print(f"[DEBUG] Resultado de la función: {function_response[:100]}...")
                        messages.append({
                            'role': 'tool',
                            'content': function_response
                        })
                final_response = ollama.chat(
                    model='llama3.1:8b',
                    messages=messages
                )
                print(f"[DEBUG] Respuesta final del LLM:")
                pprint.pprint(final_response)
                print(f"Ollama: {final_response['message']['content']}\n")
                messages.append(final_response['message'])
            else:
                print(f"[DEBUG] El LLM NO ha solicitado llamar a la tool.")
                print(f"Ollama: {response['message']['content']}\n")
    
    # Ejecutar chat
    if len(sys.argv) > 1 and sys.argv[1] == "--test":
        # Modo test: probar la funcion directamente
        print("MODO TEST")
        print()
        resultado = obtener_pronostico_temperatura("Madrid", 3)
        print(resultado)
        print()
        resultado = obtener_pronostico_temperatura("Mataro", 2)
        print(resultado)
    else:
        # Modo chat interactivo
        chat_con_herramientas()
