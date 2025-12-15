def es_pregunta_climatica(pregunta):
    """
    Valida si una pregunta es realmente sobre clima/tiempo
    """
    pregunta_lower = pregunta.lower()
    palabras_clima = ['temperatura', 'clima', 'tiempo', 'lluvia', 'calor', 'frio', 'humedad', 'viento', 'nublado', 'sol', 'meteorologico', 'pronostico', 'manana', 'semana']
    palabras_no_clima = ['habitantes', 'poblacion', 'gente', 'personas', 'demografia', 'superficie', 'extension', 'economia', 'historia', 'cultura', 'cuantos', 'cuantas']
    for palabra in palabras_no_clima:
        if palabra in pregunta_lower:
            return False
    for palabra in palabras_clima:
        if palabra in pregunta_lower:
            return True
    return False
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


# Para usar con Ollama
if __name__ == "__main__":
    import sys
    import ollama

    def consultar_clima(ciudad, dias=3):
        return obtener_pronostico_temperatura(ciudad, dias)

    available_functions = {
        'consultar_clima': consultar_clima
    }

    def chat_simple(pregunta, modelo='llama3.1:8b'):
        print(f"[DEBUG] Pregunta recibida: {pregunta}")
        prompt_llm = [
            {'role': 'user', 'content': pregunta}
        ]
        print(f"[DEBUG] Prompt enviado al LLM:")
        for msg in prompt_llm:
            print(f"  - role: {msg['role']}, content: {msg['content']}")
        print(f"[DEBUG] Tool definition disponible: {TOOL_DEFINITION['function']['name']}")
        print("[DEBUG] Llamando al LLM (Ollama) con tools...")
        response = ollama.chat(
            model=modelo,
            messages=prompt_llm,
            tools=[TOOL_DEFINITION]
        )
        print(f"[DEBUG] Respuesta completa del LLM:")
        print(f"  - role: {response['message']['role']}")
        print(f"  - content: {response['message']['content']}")
        if response['message'].get('tool_calls'):
            print(f"  - tool_calls: [")
            for tc in response['message']['tool_calls']:
                print(f"      {tc},")
            print(f"    ]")
        else:
            print(f"  - tool_calls: None")
        if response['message'].get('tool_calls'):
            print("[DEBUG] El LLM ha decidido llamar a la tool porque la pregunta coincide con la descripción y parámetros definidos.")
            tool_call = response['message']['tool_calls'][0]
            print(f"[DEBUG] tool_call: {tool_call}")
            ciudad = tool_call['function']['arguments']['ciudad']
            dias = tool_call['function']['arguments'].get('dias', 3)
            print(f"[DEBUG] Argumentos extraídos: ciudad={ciudad}, dias={dias}")
            if not es_pregunta_climatica(pregunta):
                print(f"[ADVERTENCIA] Pregunta no parece climatica: {pregunta}")
                return "Lo siento, esa pregunta no es sobre clima o temperatura."
            print(f"[DEBUG] Ejecutando función interna para: {ciudad} ({dias} dias)")
            resultado = consultar_clima(ciudad, dias)
            print(f"[DEBUG] Resultado de la función: {resultado[:100]}...")
            print("[DEBUG] Enviando resultado de la tool al LLM para respuesta final...")
            final_response = ollama.chat(
                model=modelo,
                messages=[
                    {'role': 'user', 'content': pregunta},
                    {'role': 'assistant', 'content': '', 'tool_calls': response['message']['tool_calls']},
                    {'role': 'tool', 'content': resultado}
                ]
            )
            print(f"[DEBUG] Respuesta final del LLM:")
            print(f"  - role: {final_response['message']['role']}")
            print(f"  - content: {final_response['message']['content']}")
            return final_response['message']['content']
        else:
            print("[DEBUG] El LLM NO ha solicitado llamar a la tool. Esto ocurre porque la pregunta no coincide con la descripción de la tool o los parámetros requeridos.")
            print(f"[DEBUG] Respuesta directa del LLM: {response['message']['content']}")
            return response['message']['content']

    if len(sys.argv) > 1 and sys.argv[1] == "--test":
        print("MODO TEST")
        print()
        resultado = consultar_clima("Madrid", 3)
        print(resultado)
        print()
        resultado = consultar_clima("Mataro", 2)
        print(resultado)
    else:
        print("=== TOOL CLIMA POC ===")
        while True:
            print("\nIntroduce una pregunta sobre el clima (o escribe 'salir' para terminar):")
            pregunta = input('>>> ').strip()
            if pregunta.lower() in ("salir", "exit", "quit"):
                print("Saliendo del modo interactivo.")
                break
            if not pregunta:
                continue
            respuesta = chat_simple(pregunta)
            print(f"\nRespuesta: {respuesta}\n")
