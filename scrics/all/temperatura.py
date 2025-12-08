#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script para consultar el pronostico de temperatura de ciudades españolas
Usa Open-Meteo (API gratuita, sin necesidad de registro)
"""

import requests
import sys
from datetime import datetime


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
    'palma de mallorca': (39.5696, 2.6502),
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
    'cadiz': (36.5271, -6.2886),
    'huelva': (37.2614, -6.9447),
    'leon': (42.5987, -5.5671),
    'caceres': (39.4753, -6.3724),
    'badajoz': (38.8794, -6.9706),
    'pontevedra': (42.4296, -8.6446),
    'ourense': (42.3405, -7.8644),
    'lugo': (43.0097, -7.5567),
    'a coruña': (43.3623, -8.4115),
}


def obtener_pronostico(ciudad: str, dias: int = 3):
    """
    Obtiene el pronostico de temperatura para una ciudad
    """
    print(f"Consultando pronostico para {ciudad.title()}...")
    print()
    
    # Buscar coordenadas
    ciudad_lower = ciudad.lower().strip()
    coordenadas = COORDENADAS_CIUDADES.get(ciudad_lower)
    
    if not coordenadas:
        print(f"[ERROR] Ciudad '{ciudad}' no encontrada")
        print()
        print("Ciudades disponibles:")
        ciudades = sorted(COORDENADAS_CIUDADES.keys())
        for i in range(0, len(ciudades), 5):
            print("  " + ", ".join(ciudades[i:i+5]))
        print()
        return None
    
    lat, lon = coordenadas
    print(f"[OK] Coordenadas: {lat}, {lon}")
    
    try:
        # API Open-Meteo (gratuita)
        url = "https://api.open-meteo.com/v1/forecast"
        
        params = {
            'latitude': lat,
            'longitude': lon,
            'daily': 'temperature_2m_max,temperature_2m_min,precipitation_probability_max,weathercode,windspeed_10m_max',
            'timezone': 'Europe/Madrid',
            'forecast_days': min(dias, 16)  # Max 16 dias
        }
        
        print("[1/2] Consultando Open-Meteo...")
        response = requests.get(url, params=params, timeout=15)
        
        if response.status_code != 200:
            print(f"[ERROR] HTTP {response.status_code}")
            return None
        
        print("[2/2] Procesando datos...")
        datos = response.json()
        
        # Extraer datos diarios
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
            'ciudad': ciudad.title(),
            'coordenadas': coordenadas,
            'fechas': fechas,
            'temp_max': temp_max,
            'temp_min': temp_min,
            'prob_lluvia': prob_lluvia,
            'weather_codes': weather_codes,
            'viento': viento
        }
        
    except requests.RequestException as e:
        print(f"[ERROR] Error de conexion: {e}")
        return None
    except Exception as e:
        print(f"[ERROR] Error: {e}")
        return None


def formatear_pronostico(datos):
    """
    Formatea el pronostico de manera legible
    """
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
        
        # Dia actual
        hoy = datetime.now().date()
        if fecha.date() == hoy:
            etiqueta = "HOY"
        elif fecha.date() == hoy.replace(day=hoy.day+1):
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
    print("=" * 70)


def main():
    """
    Funcion principal
    """
    print("=" * 70)
    print("PRONOSTICO DE TEMPERATURA - Ciudades de España")
    print("=" * 70)
    print()
    
    if len(sys.argv) < 2:
        print("USO: python temperatura.py <ciudad> [dias]")
        print()
        print("EJEMPLOS:")
        print("  python temperatura.py Madrid")
        print("  python temperatura.py Barcelona 7")
        print("  python temperatura.py Sevilla 5")
        print()
        print("CIUDADES DISPONIBLES:")
        ciudades = sorted(COORDENADAS_CIUDADES.keys())
        for i in range(0, len(ciudades), 5):
            print("  " + ", ".join([c.title() for c in ciudades[i:i+5]]))
        print()
        print("DIAS: Entre 1 y 16 (por defecto 3)")
        print()
        sys.exit(1)
    
    ciudad = sys.argv[1]
    dias = int(sys.argv[2]) if len(sys.argv) > 2 else 3
    
    # Validar dias
    if dias < 1 or dias > 16:
        print("[ERROR] El numero de dias debe estar entre 1 y 16")
        sys.exit(1)
    
    # Obtener pronostico
    datos = obtener_pronostico(ciudad, dias)
    
    if datos:
        formatear_pronostico(datos)


if __name__ == "__main__":
    main()
