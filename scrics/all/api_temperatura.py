#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
API REST para consultar temperatura de ciudades españolas
Servidor Flask que expone las funciones como endpoints HTTP
Para usar con Ollama remoto u otros clientes
"""

from flask import Flask, request, jsonify
from flask_cors import CORS
import requests
from datetime import datetime


app = Flask(__name__)
CORS(app)  # Permitir peticiones desde otros servidores


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


def obtener_pronostico_temperatura(ciudad: str, dias: int = 3):
    """
    Obtiene el pronostico de temperatura de una ciudad
    """
    # Buscar coordenadas
    ciudad_lower = ciudad.lower().strip()
    coordenadas = COORDENADAS_CIUDADES.get(ciudad_lower)
    
    if not coordenadas:
        return None, f"Ciudad '{ciudad}' no encontrada"
    
    lat, lon = coordenadas
    
    try:
        # API Open-Meteo
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
            return None, f"Error API Open-Meteo: HTTP {response.status_code}"
        
        datos = response.json()
        
        # Extraer datos diarios
        daily = datos.get('daily', {})
        
        # Codigos de clima WMO
        weather_descriptions = {
            0: 'Despejado', 1: 'Principalmente despejado', 2: 'Parcialmente nublado',
            3: 'Nublado', 45: 'Niebla', 48: 'Niebla con escarcha',
            51: 'Llovizna ligera', 53: 'Llovizna moderada', 55: 'Llovizna intensa',
            61: 'Lluvia ligera', 63: 'Lluvia moderada', 65: 'Lluvia intensa',
            71: 'Nevada ligera', 73: 'Nevada moderada', 75: 'Nevada intensa',
            80: 'Chubascos ligeros', 81: 'Chubascos moderados', 82: 'Chubascos intensos',
            95: 'Tormenta', 96: 'Tormenta con granizo ligero', 99: 'Tormenta con granizo intenso',
        }
        
        # Formatear resultado
        pronostico = []
        dias_semana = ['Lunes', 'Martes', 'Miercoles', 'Jueves', 'Viernes', 'Sabado', 'Domingo']
        
        fechas = daily.get('time', [])
        temp_max = daily.get('temperature_2m_max', [])
        temp_min = daily.get('temperature_2m_min', [])
        prob_lluvia = daily.get('precipitation_probability_max', [])
        weather_codes = daily.get('weathercode', [])
        viento = daily.get('windspeed_10m_max', [])
        
        for i in range(len(fechas)):
            fecha = datetime.strptime(fechas[i], '%Y-%m-%d')
            
            pronostico.append({
                'fecha': fechas[i],
                'dia_semana': dias_semana[fecha.weekday()],
                'temp_max': temp_max[i],
                'temp_min': temp_min[i],
                'prob_lluvia': prob_lluvia[i],
                'clima': weather_descriptions.get(weather_codes[i], 'Desconocido'),
                'viento': viento[i]
            })
        
        resultado = {
            'ciudad': ciudad.title(),
            'coordenadas': {'lat': lat, 'lon': lon},
            'pronostico': pronostico,
            'fuente': 'Open-Meteo'
        }
        
        return resultado, None
        
    except Exception as e:
        return None, f"Error: {str(e)}"


# ========== ENDPOINTS REST ==========

@app.route('/', methods=['GET'])
def index():
    """
    Endpoint de bienvenida
    """
    return jsonify({
        'servicio': 'API de Temperatura - España',
        'version': '1.0',
        'endpoints': {
            'GET /': 'Informacion del servicio',
            'GET /ciudades': 'Lista de ciudades disponibles',
            'GET /temperatura': 'Obtener pronostico (params: ciudad, dias)',
            'POST /temperatura': 'Obtener pronostico (body: {ciudad, dias})',
            'GET /health': 'Estado del servicio'
        }
    })


@app.route('/health', methods=['GET'])
def health():
    """
    Health check
    """
    return jsonify({'status': 'ok', 'servicio': 'temperatura-api'})


@app.route('/ciudades', methods=['GET'])
def listar_ciudades():
    """
    Lista todas las ciudades disponibles
    """
    ciudades = sorted(COORDENADAS_CIUDADES.keys())
    return jsonify({
        'total': len(ciudades),
        'ciudades': ciudades
    })


@app.route('/temperatura', methods=['GET', 'POST'])
def obtener_temperatura():
    """
    Obtiene el pronostico de temperatura
    
    GET: /temperatura?ciudad=Madrid&dias=3
    POST: /temperatura con body: {"ciudad": "Madrid", "dias": 3}
    """
    if request.method == 'POST':
        data = request.get_json()
        ciudad = data.get('ciudad')
        dias = data.get('dias', 3)
    else:
        ciudad = request.args.get('ciudad')
        dias = int(request.args.get('dias', 3))
    
    if not ciudad:
        return jsonify({
            'error': 'Parametro "ciudad" es requerido',
            'ejemplo': '/temperatura?ciudad=Madrid&dias=3'
        }), 400
    
    # Validar dias
    try:
        dias = int(dias)
        if dias < 1 or dias > 16:
            dias = 3
    except:
        dias = 3
    
    # Obtener pronostico
    resultado, error = obtener_pronostico_temperatura(ciudad, dias)
    
    if error:
        return jsonify({'error': error}), 404
    
    return jsonify(resultado)


if __name__ == '__main__':
    print("=" * 70)
    print("API REST - PRONOSTICO DE TEMPERATURA")
    print("=" * 70)
    print()
    print("Servidor iniciado en: http://0.0.0.0:5000")
    print()
    print("Endpoints disponibles:")
    print("  GET  /                    - Informacion del servicio")
    print("  GET  /ciudades            - Lista de ciudades")
    print("  GET  /temperatura         - Obtener pronostico")
    print("  POST /temperatura         - Obtener pronostico")
    print("  GET  /health              - Health check")
    print()
    print("Ejemplos:")
    print("  http://localhost:5000/temperatura?ciudad=Madrid&dias=3")
    print("  http://localhost:5000/ciudades")
    print()
    print("Para usar desde otro servidor, reemplaza 'localhost' con la IP")
    print("=" * 70)
    print()
    
    # Iniciar servidor
    app.run(host='0.0.0.0', port=5000, debug=True)
