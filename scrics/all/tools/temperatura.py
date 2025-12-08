#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Tool: Pronóstico de Temperatura
Busca CUALQUIER ciudad de España usando OpenStreetMap + Open-Meteo
"""

import requests
from datetime import datetime


def buscar_ciudad_nominatim(nombre_ciudad):
    """Busca ciudad en OpenStreetMap Nominatim"""
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
    except Exception as e:
        print(f"[TEMP TOOL] Error en Nominatim: {e}")
        return None, None, None


def obtener_pronostico_temperatura(ciudad: str, dias: int = 3) -> str:
    """
    Obtiene pronóstico de temperatura para CUALQUIER ciudad de España
    
    Args:
        ciudad: Nombre de la ciudad española (cualquiera)
        dias: Días de pronóstico (1-16)
    
    Returns:
        String con el pronóstico formateado
    """
    try:
        # Convertir dias a int si viene como string
        if isinstance(dias, str):
            dias = int(dias)
        
        print(f"[TEMP TOOL] Buscando temperatura para: {ciudad}, {dias} días")
        
        if dias < 1 or dias > 16:
            return "Error: El pronóstico está disponible para 1-16 días"
        
        # Buscar ciudad
        lat, lon, nombre = buscar_ciudad_nominatim(ciudad)
        
        if not lat:
            return f"No encontré la ciudad '{ciudad}' en España. Verifica el nombre e intenta de nuevo."
        
        # Obtener pronóstico
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
            return f"Error al obtener pronóstico: HTTP {response.status_code}"
        
        datos = response.json()
        daily = datos.get('daily', {})
        
        # Códigos de clima
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
            
            resultado.append(
                f"{etiqueta} ({dia}): {temp_min:.0f}-{temp_max:.0f}°C, {clima}, "
                f"lluvia {lluvia:.0f}%, viento {viento:.0f} km/h"
            )
        
        resultado_final = f"Pronóstico para {nombre}:\n" + "\n".join(resultado)
        print(f"[TEMP TOOL] Éxito!")
        return resultado_final
        
    except Exception as e:
        error_msg = f"Error: {str(e)}"
        print(f"[TEMP TOOL] ERROR: {error_msg}")
        return error_msg


# Definición de la tool para Ollama
TOOL_DEFINITION = {
    'type': 'function',
    'function': {
        'name': 'obtener_pronostico_temperatura',
        'description': 'Obtiene el pronóstico del tiempo para ciudades de España. Funciona con CUALQUIER ciudad. Incluye temperatura, clima, lluvia y viento.',
        'parameters': {
            'type': 'object',
            'properties': {
                'ciudad': {
                    'type': 'string',
                    'description': 'Nombre de CUALQUIER ciudad española'
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

# Palabras clave para activar esta tool
KEYWORDS = [
    'temperatura', 'tiempo', 'clima', 'lluvia', 'viento', 
    'pronostico', 'pronóstico', 'calor', 'frio', 'frío',
    'grados', 'soleado', 'nublado', 'despejado', 'meteorolog',
    'nevar', 'nieve', 'tormenta', 'cielo',
    'semana', 'hoy', 'mañana', 'hará', 'estará'
]
