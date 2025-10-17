#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script para consultar el pronostico de temperatura usando AEMET
Version optimizada - USA geocoding para encontrar ciudades SIN hardcodear datos
"""

import requests
import sys
from datetime import datetime
import time

def buscar_ciudad_nominatim(nombre_ciudad):
    """
    Busca una ciudad usando Nominatim (OpenStreetMap)
    NO usa datos hardcodeados

    Returns:
        Tupla (latitud, longitud, nombre_completo) o (None, None, None)
    """
    print(f"[1/3] Buscando '{nombre_ciudad}' en OpenStreetMap...")

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
            print(f"[ERROR] No se pudo buscar la ciudad: HTTP {response.status_code}")
            return None, None, None

        resultados = response.json()

        if not resultados:
            print(f"[ERROR] No se encontro '{nombre_ciudad}' en España")
            return None, None, None

        # Filtrar solo resultados en España
        resultados_espana = [r for r in resultados if r.get('address', {}).get('country') == 'España']

        if not resultados_espana:
            print(f"[ERROR] No se encontro '{nombre_ciudad}' en España")
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

        provincia = address.get('state', '')

        print(f"[OK] Encontrada: {nombre}")
        if provincia:
            print(f"[OK] Provincia: {provincia}")
        print(f"[OK] Coordenadas: {lat:.4f}, {lon:.4f}")

        return lat, lon, nombre

    except Exception as e:
        print(f"[ERROR] Error al buscar ciudad: {e}")
        return None, None, None


def obtener_pronostico_open_meteo(lat, lon, nombre_ciudad, dias=3):
    """
    Obtiene el pronostico usando Open-Meteo (no requiere API key)
    """
    print(f"[2/3] Consultando Open-Meteo...")

    try:
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
            print(f"[ERROR] HTTP {response.status_code}")
            return None

        print("[3/3] Procesando datos...")
        datos = response.json()

        daily = datos.get('daily', {})
        fechas = daily.get('time', [])
        temp_max = daily.get('temperature_2m_max', [])
        temp_min = daily.get('temperature_2m_min', [])
        prob_lluvia = daily.get('precipitation_probability_max', [])
        weather_codes = daily.get('weathercode', [])
        viento = daily.get('windspeed_10m_max', [])

        print("[OK] Datos recibidos")
        print()

        return {
            'ciudad': nombre_ciudad,
            'coordenadas': (lat, lon),
            'fechas': fechas,
            'temp_max': temp_max,
            'temp_min': temp_min,
            'prob_lluvia': prob_lluvia,
            'weather_codes': weather_codes,
            'viento': viento
        }

    except Exception as e:
        print(f"[ERROR] Error: {e}")
        return None


def formatear_pronostico(datos):
    """
    Formatea el pronostico
    """
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

    print("=" * 70)
    print(f"PRONOSTICO METEOROLOGICO - {datos['ciudad'].upper()}")
    print("=" * 70)
    print()

    for i, fecha_str in enumerate(datos['fechas']):
        fecha = datetime.strptime(fecha_str, '%Y-%m-%d')
        dia_semana = dias_semana[fecha.weekday()]
        fecha_formato = fecha.strftime('%d/%m/%Y')

        temp_max = datos['temp_max'][i]
        temp_min = datos['temp_min'][i]
        prob_lluvia = datos['prob_lluvia'][i]
        weather_code = datos['weather_codes'][i]
        viento = datos['viento'][i]

        weather_desc = weather_descriptions.get(weather_code, 'Desconocido')

        hoy = datetime.now().date()
        if fecha.date() == hoy:
            etiqueta = "HOY"
        elif (fecha.date() - hoy).days == 1:
            etiqueta = "MAÑANA"
        else:
            etiqueta = ""

        print(f"{dia_semana:10} {fecha_formato}  {etiqueta}")
        print(f"  Temperatura:  {temp_min:5.1f}°C - {temp_max:5.1f}°C")
        print(f"  Clima:        {weather_desc}")
        print(f"  Prob. lluvia: {prob_lluvia:3.0f}%")
        print(f"  Viento:       {viento:5.1f} km/h")
        print()

    print("=" * 70)
    print("Fuente: Open-Meteo (https://open-meteo.com)")
    print("Geocoding: OpenStreetMap Nominatim")
    print("=" * 70)


def main():
    """
    Funcion principal
    """
    print("=" * 70)
    print("PRONOSTICO DE TEMPERATURA - CUALQUIER Ciudad de España")
    print("SIN datos hardcodeados - Busqueda dinamica")
    print("=" * 70)
    print()

    if len(sys.argv) < 2:
        print("USO: python pronostico_temperatura.py <ciudad> [dias]")
        print()
        print("EJEMPLOS:")
        print("  python pronostico_temperatura.py Madrid")
        print("  python pronostico_temperatura.py Barcelona 7")
        print("  python pronostico_temperatura.py Mataro 5")
        print("  python pronostico_temperatura.py \"San Sebastian\" 3")
        print("  python pronostico_temperatura.py Alcobendas 4")
        print()
        print("CARACTERISTICAS:")
        print("  - Busca CUALQUIER ciudad de España")
        print("  - NO usa datos hardcodeados")
        print("  - Usa OpenStreetMap para geocoding")
        print("  - Usa Open-Meteo para el pronostico (sin API key)")
        print("  - Hasta 16 dias de pronostico")
        print()
        sys.exit(1)

    ciudad = sys.argv[1]
    dias = int(sys.argv[2]) if len(sys.argv) > 2 else 3

    if dias < 1 or dias > 16:
        print("[ERROR] El numero de dias debe estar entre 1 y 16")
        sys.exit(1)

    print()

    # Buscar ciudad
    lat, lon, nombre = buscar_ciudad_nominatim(ciudad)

    if not lat:
        sys.exit(1)

    print()

    # Obtener pronostico
    datos = obtener_pronostico_open_meteo(lat, lon, nombre, dias)

    if datos:
        formatear_pronostico(datos)


if __name__ == "__main__":
    main()
