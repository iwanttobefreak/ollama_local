#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Tool de Temperatura para Ollama - VERSION MEJORADA
Chat igual que 'ollama run' pero con herramienta de temperatura integrada
"""

import requests
import ollama
from datetime import datetime


def buscar_ciudad_nominatim(nombre_ciudad):
    """Busca ciudad en OpenStreetMap"""
    try:
        url = "https://nominatim.openstreetmap.org/search"
        params = {
            'q': f"{nombre_ciudad}, España",
            'format': 'json',
            'limit': 5,
            'addressdetails': 1
        }
        headers = {'User-Agent': 'PronosticoTemperatura/1.0'}
        
        response = requests.get(url, params=params, headers=headers, timeout=10)
        if response.status_code != 200:
            return None, None, None
        
        resultados = response.json()
        if not resultados:
            return None, None, None
        
        # Filtrar resultados en España
        resultados_espana = [r for r in resultados if r.get('address', {}).get('country') == 'España']
        if not resultados_espana:
            return None, None, None
        
        lugar = resultados_espana[0]
        lat = float(lugar['lat'])
        lon = float(lugar['lon'])
        
        address = lugar.get('address', {})
        nombre = (
            address.get('city') or address.get('town') or 
            address.get('village') or address.get('municipality') or
            nombre_ciudad.title()
        )
        
        return lat, lon, nombre
    except:
        return None, None, None


def obtener_pronostico_temperatura(ciudad: str, dias: int = 3) -> str:
    """Obtiene pronóstico de temperatura"""
    try:
        print(f"[FUNC DEBUG] Buscando temperatura para: {ciudad}, {dias} días")
        
        if dias < 1 or dias > 16:
            return "Error: dias debe estar entre 1 y 16"
        
        # Buscar ciudad
        print(f"[FUNC DEBUG] Llamando a Nominatim...")
        lat, lon, nombre = buscar_ciudad_nominatim(ciudad)
        print(f"[FUNC DEBUG] Resultado: lat={lat}, lon={lon}, nombre={nombre}")
        
        if not lat:
            return f"No encontré la ciudad '{ciudad}' en España"
        
        # Obtener pronóstico
        url = "https://api.open-meteo.com/v1/forecast"
        params = {
            'latitude': lat,
            'longitude': lon,
            'daily': 'temperature_2m_max,temperature_2m_min,precipitation_probability_max,weathercode,windspeed_10m_max',
            'timezone': 'Europe/Madrid',
            'forecast_days': min(dias, 16)
        }
        
        print(f"[FUNC DEBUG] Llamando a Open-Meteo API...")
        response = requests.get(url, params=params, timeout=15)
        print(f"[FUNC DEBUG] Status code: {response.status_code}")
        
        if response.status_code != 200:
            return f"Error al obtener pronóstico: HTTP {response.status_code}"
        
        datos = response.json()
        daily = datos.get('daily', {})
        
        # Formatear resultado de forma más concisa para Ollama
        weather_desc = {
            0: 'Despejado', 1: 'Mayormente despejado', 2: 'Parcialmente nublado', 3: 'Nublado',
            45: 'Niebla', 48: 'Niebla con escarcha',
            51: 'Llovizna ligera', 53: 'Llovizna', 55: 'Llovizna intensa',
            61: 'Lluvia ligera', 63: 'Lluvia', 65: 'Lluvia intensa',
            71: 'Nevada ligera', 73: 'Nevada', 75: 'Nevada intensa',
            80: 'Chubascos', 81: 'Chubascos fuertes', 82: 'Chubascos muy fuertes',
            95: 'Tormenta', 96: 'Tormenta con granizo', 99: 'Tormenta fuerte'
        }
        
        dias_sem = ['Lunes', 'Martes', 'Miércoles', 'Jueves', 'Viernes', 'Sábado', 'Domingo']
        
        resultado = []
        for i, fecha_str in enumerate(daily.get('time', [])):
            fecha = datetime.strptime(fecha_str, '%Y-%m-%d')
            dia = dias_sem[fecha.weekday()]
            
            temp_min = daily['temperature_2m_min'][i]
            temp_max = daily['temperature_2m_max'][i]
            lluvia = daily['precipitation_probability_max'][i]
            clima = weather_desc.get(daily['weathercode'][i], 'Variable')
            viento = daily['windspeed_10m_max'][i]
            
            hoy = datetime.now().date()
            if fecha.date() == hoy:
                etiqueta = "HOY"
            elif (fecha.date() - hoy).days == 1:
                etiqueta = "MAÑANA"
            else:
                etiqueta = fecha.strftime('%d/%m')
            
            resultado.append(f"{etiqueta} ({dia}): {temp_min:.0f}-{temp_max:.0f}°C, {clima}, lluvia {lluvia:.0f}%, viento {viento:.0f} km/h")
        
        resultado_final = f"Pronóstico para {nombre}:\n" + "\n".join(resultado)
        print(f"[FUNC DEBUG] Éxito! Devolviendo pronóstico")
        return resultado_final
        
    except Exception as e:
        error_msg = f"Error: {str(e)}"
        print(f"[FUNC DEBUG ERROR] {error_msg}")
        import traceback
        traceback.print_exc()
        return error_msg


# Tool definition para Ollama
TOOL_DEFINITION = {
    'type': 'function',
    'function': {
        'name': 'obtener_pronostico_temperatura',
        'description': 'SOLO usar cuando el usuario pregunta específicamente por el TIEMPO, CLIMA, TEMPERATURA, LLUVIA o PRONÓSTICO meteorológico de una ciudad ESPAÑOLA. NO usar para otras preguntas generales.',
        'parameters': {
            'type': 'object',
            'properties': {
                'ciudad': {
                    'type': 'string',
                    'description': 'Nombre de la ciudad española (Madrid, Barcelona, Valencia, etc.)'
                },
                'dias': {
                    'type': 'integer',
                    'description': 'Días de pronóstico (1-16). Default: 3',
                    'default': 3,
                    'minimum': 1,
                    'maximum': 16
                }
            },
            'required': ['ciudad']
        }
    }
}


def main():
    """Chat con Ollama estilo 'ollama run'"""
    available_functions = {
        'obtener_pronostico_temperatura': obtener_pronostico_temperatura
    }
    
    # Palabras clave que indican pregunta sobre clima
    CLIMA_KEYWORDS = [
        'temperatura', 'tiempo', 'clima', 'lluvia', 'viento', 
        'pronostico', 'pronóstico', 'calor', 'frio', 'frío',
        'grados', 'soleado', 'nublado', 'despejado', 'meteorolog'
    ]
    
    messages = []
    
    while True:
        try:
            user_input = input(">>> ").strip()
        except (EOFError, KeyboardInterrupt):
            print()
            break
        
        if not user_input:
            continue
        
        # Comandos
        if user_input in ['/bye', '/exit', '/quit']:
            break
        if user_input == '/clear':
            messages = []
            continue
        if user_input == '/help':
            print("Comandos: /bye (salir), /clear (limpiar), /help (ayuda)")
            continue
        
        # Agregar mensaje del usuario
        messages.append({'role': 'user', 'content': user_input})
        
        # Detectar si es pregunta sobre clima
        es_pregunta_clima = any(keyword in user_input.lower() for keyword in CLIMA_KEYWORDS)
        
        # Llamar a Ollama con tools SOLO si es pregunta de clima
        try:
            if es_pregunta_clima:
                response = ollama.chat(
                    model='llama3.1:8b',
                    messages=messages,
                    tools=[TOOL_DEFINITION]
                )
            else:
                # Sin tools para preguntas generales
                response = ollama.chat(
                    model='llama3.1:8b',
                    messages=messages
                )
            
        except Exception as e:
            print(f"Error al conectar con Ollama: {e}")
            print("¿Está Ollama corriendo? (ollama serve)")
            messages.pop()  # Quitar último mensaje
            continue
        
        messages.append(response['message'])
        
        # Si usa tools
        if response['message'].get('tool_calls'):
            print(f"[DEBUG] Ollama llamó a la tool!")
            for tool_call in response['message']['tool_calls']:
                func_name = tool_call['function']['name']
                func_args = tool_call['function']['arguments']
                
                print(f"[DEBUG] Función: {func_name}")
                print(f"[DEBUG] Argumentos: {func_args}")
                
                if func_name in available_functions:
                    # Ejecutar función
                    func_result = available_functions[func_name](**func_args)
                    
                    print(f"[DEBUG] Resultado: {func_result[:200]}...")
                    
                    # Agregar resultado
                    messages.append({
                        'role': 'tool',
                        'content': func_result
                    })
            
            # Segunda llamada a Ollama para procesar el resultado
            try:
                final_response = ollama.chat(
                    model='llama3.1:8b',
                    messages=messages
                )
                print(final_response['message']['content'])
                print()
                messages.append(final_response['message'])
            except Exception as e:
                print(f"Error en respuesta final: {e}")
        else:
            # Respuesta directa
            print(response['message']['content'])
            print()


if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1 and sys.argv[1] == "--test":
        print("TEST - Función de temperatura\n")
        print(obtener_pronostico_temperatura("Madrid", 3))
    else:
        print("Escribe /bye para salir, /help para ayuda")
        main()
