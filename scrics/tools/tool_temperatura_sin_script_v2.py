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
        print(f"[DEBUG] Llamando a Nominatim: {url} params={params}")
        response = requests.get(url, params=params, headers=headers, timeout=10)
        print(f"[DEBUG] Respuesta Nominatim status={response.status_code}")
        if response.status_code != 200:
            print(f"[DEBUG] Error Nominatim: status={response.status_code}, body={response.text}")
            return None, None, None
        resultados = response.json()
        print(f"[DEBUG] Respuesta Nominatim JSON: {resultados}")
        if not resultados:
            print("[DEBUG] Nominatim no devolvio resultados")
            return None, None, None
        # Filtrar solo resultados en España
        resultados_espana = [r for r in resultados if r.get('address', {}).get('country') == 'España']
        if not resultados_espana:
            print("[DEBUG] Nominatim no encontro resultados en España")
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
        print(f"[DEBUG] Ciudad encontrada: {nombre} lat={lat} lon={lon}")
        return lat, lon, nombre
    except Exception as e:
        print(f"[DEBUG] Excepcion en buscar_ciudad_nominatim: {e}")
        return None, None, None


def obtener_pronostico_temperatura(ciudad: str, dias: int = 3) -> str:
    """
    Obtiene el pronostico de temperatura para CUALQUIER ciudad española
    
    Args:
        ciudad: Nombre de la ciudad (ej: Madrid, Barcelona, Mataro, Alcobendas, etc.)
        dias: Numero de dias de pronostico (entre 1 y 16). Por defecto 3.
    
    Returns:
        Pronostico formateado como texto
    """
    try:
        # Convertir dias a int si viene como string
        try:
            dias = int(dias)
        except Exception as e:
            print(f"[DEBUG] Error convirtiendo 'dias' a int: {e} valor recibido: {dias}")
            return "Error: El parámetro 'dias' debe ser un número entero."
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
            'timezone': 'Europe/Madrid'
        }
        print(f"[DEBUG] Llamando a Open-Meteo: {url} params={params}")
        response = requests.get(url, params=params, timeout=15)
        print(f"[DEBUG] Respuesta Open-Meteo status={response.status_code}")
        if response.status_code != 200:
            print(f"[DEBUG] Error Open-Meteo: status={response.status_code}, body={response.text}")
            return f"Error: No se pudo obtener el pronostico (HTTP {response.status_code})"
        datos = response.json()
        print(f"[DEBUG] Respuesta Open-Meteo JSON: {datos}")
        daily = datos.get('daily', {})
        fechas = daily.get('time', [])
        temp_max = daily.get('temperature_2m_max', [])
        temp_min = daily.get('temperature_2m_min', [])
        prob_lluvia = daily.get('precipitation_probability_max', [])
        weather_codes = daily.get('weathercode', [])
        viento = daily.get('windspeed_10m_max', [])
        # Comprobar si hay datos suficientes
        if not (fechas and temp_max and temp_min and prob_lluvia and weather_codes and viento):
            print(f"[DEBUG] Datos insuficientes en respuesta Open-Meteo: {daily}")
            return "Error: La respuesta de la API del servicio meteorológico no contiene datos suficientes."
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
        print(f"[DEBUG] Excepcion en obtener_pronostico_temperatura: {e}")
        return f"Error al obtener el pronostico: {str(e)}"


# Definicion de la herramienta para Ollama
TOOL_DEFINITION = {
    'type': 'function',
    'function': {
        'name': 'obtener_pronostico_temperatura',
        'description': 'SOLO para consultas meteorologicas: temperatura, lluvia, clima, tiempo. Usar UNICAMENTE cuando el usuario pregunta por TIEMPO/CLIMA/TEMPERATURA/LLUVIA/HUMEDAD. NUNCA usar para: habitantes, poblacion, demografia, geografia, historia, economia, cultura, superficie, densidad, gente, personas. Ejemplo SI: "temperatura Madrid", "lluvias Valencia". Ejemplo NO: "habitantes Barcelona", "poblacion Sevilla". Obtiene el pronostico de temperatura y clima para CUALQUIER ciudad de España. Usa geocoding dinamico (SIN datos hardcodeados) para buscar cualquier ciudad, pueblo o municipio. Incluye temperatura maxima y minima, condiciones climaticas, probabilidad de lluvia y velocidad del viento para los proximos dias.',
        'parameters': {
            'type': 'object',
            'properties': {
                'ciudad': {
                    'type': 'string',
                    'description': 'Nombre de CUALQUIER ciudad española. Ejemplos: Madrid, Barcelona, Mataro, Alcobendas, San Sebastian, Pozuelo, Chinchon, etc. Funciona con ciudades grandes, pequeñas y pueblos.'
                },
                'dias': {
                    'type': 'integer',
                    'description': 'Numero de dias de pronostico (entre 1 y 16). Por defecto 3.',
                    'default': 3,
                    'minimum': 1,
                    'maximum': 16
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
            # Obtener pregunta del usuario
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
            
            # Agregar mensaje del usuario
            messages.append({
                'role': 'user',
                'content': user_input
            })
            
            # Llamar a Ollama con herramientas
            print(f"[DEBUG] Pregunta enviada al LLM: {messages[-1]['content']}")
            response = ollama.chat(
                model='llama3.1:8b',
                messages=messages,
                tools=[TOOL_DEFINITION]
            )
            print(f"[DEBUG] Respuesta del LLM: {response}")
            # Agregar respuesta al historial
            messages.append(response['message'])
            # Verificar si Ollama quiere usar una herramienta
            if response['message'].get('tool_calls'):
                print(f"[DEBUG] tool_calls detectados:")
                for tool_call in response['message']['tool_calls']:
                    function_name = tool_call['function']['name']
                    function_args = tool_call['function']['arguments']
                    print(f"[DEBUG] Ejecutando función: {function_name} con argumentos: {function_args}")
                    # Ejecutar la funcion
                    if function_name in available_functions:
                        print(f"\n[Consultando {function_args.get('ciudad')}...]\n")
                        function_response = available_functions[function_name](**function_args)
                        print(f"[DEBUG] Respuesta de la función {function_name}: {function_response}")
                        # Agregar resultado al historial
                        messages.append({
                            'role': 'tool',
                            'content': function_response
                        })
                # Llamar nuevamente a Ollama para que procese el resultado
                final_response = ollama.chat(
                    model='llama3.1:8b',
                    messages=messages
                )
                print(f"[DEBUG] Respuesta final del LLM: {final_response}")
                print(f"Ollama: {final_response['message']['content']}\n")
                messages.append(final_response['message'])
            else:
                print(f"[DEBUG] No se requiere tool-call. Respuesta directa del LLM.")
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
