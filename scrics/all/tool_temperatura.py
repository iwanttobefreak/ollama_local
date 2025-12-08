#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Cliente para usar la API de temperatura con Ollama remoto
Conecta con el servidor de API REST de temperatura
"""

import requests
import json


# Configuracion del servidor de API
API_URL = "http://localhost:5000"  # Cambiar por la IP del servidor donde corre api_temperatura.py


def obtener_pronostico_temperatura(ciudad: str, dias: int = 3) -> str:
    """
    Llama a la API REST para obtener el pronostico
    
    Args:
        ciudad: Nombre de la ciudad
        dias: Numero de dias de pronostico
    
    Returns:
        Pronostico en formato texto
    """
    try:
        # Llamar a la API
        url = f"{API_URL}/temperatura"
        params = {
            'ciudad': ciudad,
            'dias': dias
        }
        
        response = requests.get(url, params=params, timeout=10)
        
        if response.status_code != 200:
            error_data = response.json()
            return f"Error: {error_data.get('error', 'Desconocido')}"
        
        datos = response.json()
        
        # Formatear resultado
        resultado = [
            f"Pronostico de temperatura para {datos['ciudad']}:",
            f"Coordenadas: {datos['coordenadas']['lat']}, {datos['coordenadas']['lon']}",
            ""
        ]
        
        for dia in datos['pronostico']:
            resultado.append(f"{dia['dia_semana']} {dia['fecha']}:")
            resultado.append(f"  Temperatura: {dia['temp_min']:.1f}°C - {dia['temp_max']:.1f}°C")
            resultado.append(f"  Clima: {dia['clima']}")
            resultado.append(f"  Prob. lluvia: {dia['prob_lluvia']:.0f}%")
            resultado.append(f"  Viento: {dia['viento']:.1f} km/h")
            resultado.append("")
        
        resultado.append(f"Fuente: {datos['fuente']}")
        
        return "\n".join(resultado)
        
    except requests.ConnectionError:
        return f"Error: No se pudo conectar a la API en {API_URL}. Verifica que el servidor este corriendo."
    except requests.Timeout:
        return "Error: Timeout al conectar con la API"
    except Exception as e:
        return f"Error inesperado: {str(e)}"


def obtener_ciudades_disponibles() -> str:
    """
    Obtiene la lista de ciudades disponibles desde la API
    """
    try:
        url = f"{API_URL}/ciudades"
        response = requests.get(url, timeout=5)
        
        if response.status_code == 200:
            datos = response.json()
            ciudades = datos.get('ciudades', [])
            return ", ".join(ciudades[:20]) + "..."
        
        return "No se pudo obtener la lista de ciudades"
    
    except:
        return "Madrid, Barcelona, Valencia, Sevilla, Murcia..."


# Definicion de la herramienta para Ollama
TOOL_DEFINITION = {
    'type': 'function',
    'function': {
        'name': 'obtener_pronostico_temperatura',
        'description': 'Obtiene el pronostico de temperatura y clima para ciudades de España. Incluye temperatura maxima y minima, condiciones climaticas, probabilidad de lluvia y velocidad del viento para los proximos dias. Usa una API REST conectada a Open-Meteo.',
        'parameters': {
            'type': 'object',
            'properties': {
                'ciudad': {
                    'type': 'string',
                    'description': 'Nombre de la ciudad española (ej: Madrid, Barcelona, Valencia, Sevilla, Murcia, Malaga, etc.)'
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


# Mapeo de funciones disponibles
AVAILABLE_FUNCTIONS = {
    'obtener_pronostico_temperatura': obtener_pronostico_temperatura
}


def test_api():
    """
    Prueba la conexion con la API
    """
    print("=" * 70)
    print("TEST DE CONEXION CON LA API")
    print("=" * 70)
    print()
    print(f"API URL: {API_URL}")
    print()
    
    # Test 1: Health check
    print("[1/3] Verificando que la API este corriendo...")
    try:
        response = requests.get(f"{API_URL}/health", timeout=5)
        if response.status_code == 200:
            print("[OK] API esta corriendo")
        else:
            print(f"[ERROR] API respondio con codigo {response.status_code}")
            return False
    except:
        print(f"[ERROR] No se pudo conectar a {API_URL}")
        print("[INFO] Asegurate de que el servidor este corriendo:")
        print(f"       python api_temperatura.py")
        return False
    
    # Test 2: Listar ciudades
    print()
    print("[2/3] Obteniendo lista de ciudades...")
    try:
        response = requests.get(f"{API_URL}/ciudades", timeout=5)
        if response.status_code == 200:
            datos = response.json()
            print(f"[OK] {datos['total']} ciudades disponibles")
        else:
            print("[ERROR] No se pudo obtener la lista")
    except Exception as e:
        print(f"[ERROR] {e}")
    
    # Test 3: Obtener pronostico
    print()
    print("[3/3] Probando consulta de temperatura...")
    resultado = obtener_pronostico_temperatura("Madrid", 2)
    print()
    print(resultado)
    print()
    
    print("=" * 70)
    print("[OK] PRUEBA COMPLETADA")
    print("=" * 70)
    
    return True


if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1 and sys.argv[1] == "--test":
        # Modo test
        test_api()
    elif len(sys.argv) > 1 and sys.argv[1] == "--config":
        # Configurar URL de la API
        if len(sys.argv) > 2:
            nueva_url = sys.argv[2]
            print(f"Para cambiar la URL de la API, edita este archivo:")
            print(f"  {__file__}")
            print(f"Y modifica la linea:")
            print(f'  API_URL = "{API_URL}"')
            print(f"Por:")
            print(f'  API_URL = "{nueva_url}"')
        else:
            print(f"URL actual de la API: {API_URL}")
            print()
            print("Para cambiar, ejecuta:")
            print("  python tool_temperatura.py --config http://TU_SERVIDOR:5000")
    else:
        # Consulta directa
        if len(sys.argv) < 2:
            print("USO:")
            print("  python tool_temperatura.py <ciudad> [dias]")
            print("  python tool_temperatura.py --test")
            print("  python tool_temperatura.py --config [nueva_url]")
            print()
            print("EJEMPLOS:")
            print("  python tool_temperatura.py Madrid 3")
            print("  python tool_temperatura.py --test")
            sys.exit(1)
        
        ciudad = sys.argv[1]
        dias = int(sys.argv[2]) if len(sys.argv) > 2 else 3
        
        resultado = obtener_pronostico_temperatura(ciudad, dias)
        print(resultado)
