#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script simple para consultar temperatura - POC
"""

import requests
import sys
from datetime import datetime

# Coordenadas de principales ciudades españolas
COORDENADAS = {
    'madrid': (40.4168, -3.7038),
    'barcelona': (41.3851, 2.1734),
    'valencia': (39.4699, -0.3763),
    'sevilla': (37.3886, -5.9823),
    'bilbao': (43.2630, -2.9350),
    'malaga': (36.7213, -4.4214),
}

def consultar_temperatura(ciudad="madrid"):
    """
    Consulta la temperatura actual de una ciudad
    """
    try:
        ciudad = ciudad.lower().strip()
        
        if ciudad not in COORDENADAS:
            return f"❌ Ciudad '{ciudad}' no disponible. Ciudades: {', '.join(COORDENADAS.keys())}"
        
        lat, lon = COORDENADAS[ciudad]
        
        # API gratuita Open-Meteo
        url = f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&current=temperature_2m,weather_code&timezone=Europe/Madrid"
        
        response = requests.get(url, timeout=10)
        
        if response.status_code != 200:
            return f"❌ Error HTTP {response.status_code}"
        
        datos = response.json()
        temp_actual = datos['current']['temperature_2m']
        
        # Estados del tiempo básicos
        weather_code = datos['current']['weather_code']
        estados = {
            0: "☀️ Despejado", 1: "🌤️ Poco nublado", 2: "⛅ Nublado", 3: "☁️ Muy nublado",
            45: "🌫️ Niebla", 48: "🌫️ Niebla", 51: "🌦️ Llovizna ligera", 
            61: "🌧️ Lluvia ligera", 80: "🌦️ Chubascos"
        }
        clima = estados.get(weather_code, "🌡️ Variado")
        
        ahora = datetime.now().strftime("%H:%M")
        
        resultado = f"""
🌡️ TEMPERATURA EN {ciudad.upper()}
📅 Hora: {ahora}
🌡️ Temperatura: {temp_actual}°C
{clima}
"""
        return resultado.strip()
        
    except Exception as e:
        return f"❌ Error: {str(e)}"

if __name__ == "__main__":
    ciudad = sys.argv[1] if len(sys.argv) > 1 else "madrid"
    print(consultar_temperatura(ciudad))