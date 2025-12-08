#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script para consultar el pronostico de temperatura de ciudades españolas
Utiliza la API de AEMET (Agencia Estatal de Meteorologia)
"""

import requests
import sys
from datetime import datetime


# IMPORTANTE: Necesitas una API Key de AEMET
# Obtener gratis en: https://opendata.aemet.es/centrodedescargas/altaUsuario
AEMET_API_KEY = "TU_API_KEY_AQUI"  # Reemplazar con tu API key


# Codigos de las principales ciudades españolas
CIUDADES_AEMET = {
    # Capitales de provincia
    'madrid': '28079',
    'barcelona': '08019',
    'valencia': '46250',
    'sevilla': '41091',
    'zaragoza': '50297',
    'malaga': '29067',
    'murcia': '30030',
    'palma': '07040',
    'palma de mallorca': '07040',
    'las palmas': '35016',
    'las palmas de gran canaria': '35016',
    'bilbao': '48020',
    'alicante': '03014',
    'cordoba': '14021',
    'valladolid': '47186',
    'vigo': '36057',
    'gijon': '33024',
    'hospitalet': '08101',
    'vitoria': '01059',
    'vitoria-gasteiz': '01059',
    'granada': '18087',
    'elche': '03065',
    'oviedo': '33044',
    'badalona': '08015',
    'cartagena': '30016',
    'terrassa': '08279',
    'jerez': '11020',
    'sabadell': '08187',
    'santander': '39075',
    'pamplona': '31201',
    'almeria': '04013',
    'san sebastian': '20069',
    'donostia': '20069',
    'burgos': '09059',
    'albacete': '02003',
    'castellon': '12040',
    'avila': '05019',
    'caceres': '10037',
    'ciudad real': '13034',
    'cuenca': '16078',
    'guadalajara': '19130',
    'huesca': '22125',
    'jaen': '23050',
    'leon': '24089',
    'lleida': '25120',
    'lerida': '25120',
    'logroño': '26089',
    'lugo': '27028',
    'orense': '32054',
    'ourense': '32054',
    'palencia': '34120',
    'pontevedra': '36038',
    'salamanca': '37274',
    'segovia': '40194',
    'soria': '42173',
    'tarragona': '43148',
    'teruel': '44216',
    'toledo': '45168',
    'zamora': '49275',
}


def obtener_codigo_ciudad(ciudad: str) -> str:
    """
    Obtiene el codigo AEMET de una ciudad
    """
    ciudad_lower = ciudad.lower().strip()
    return CIUDADES_AEMET.get(ciudad_lower)


def obtener_pronostico_aemet(ciudad: str, dias: int = 7) -> dict:
    """
    Obtiene el pronostico de temperatura de una ciudad española
    
    Args:
        ciudad: Nombre de la ciudad
        dias: Numero de dias de pronostico (por defecto 7)
    
    Returns:
        dict con el pronostico o None si hay error
    """
    print(f"Consultando pronostico de {ciudad}...")
    print()
    
    # Obtener codigo de ciudad
    codigo = obtener_codigo_ciudad(ciudad)
    
    if not codigo:
        print(f"[ERROR] Ciudad '{ciudad}' no encontrada")
        print("[INFO] Ciudades disponibles: Madrid, Barcelona, Valencia, Sevilla, etc.")
        return None
    
    print(f"[OK] Codigo AEMET: {codigo}")
    
    try:
        # Endpoint de AEMET para pronostico municipal
        url = f"https://opendata.aemet.es/opendata/api/prediccion/especifica/municipio/diaria/{codigo}"
        
        headers = {
            'api_key': AEMET_API_KEY
        }
        
        print(f"[1/2] Solicitando datos a AEMET...")
        response = requests.get(url, params=headers, timeout=10)
        
        if response.status_code == 401:
            print("[ERROR] API Key invalida")
            print("[INFO] Obten tu API key gratis en: https://opendata.aemet.es/centrodedescargas/altaUsuario")
            return None
        
        if response.status_code != 200:
            print(f"[ERROR] Error HTTP: {response.status_code}")
            return None
        
        # AEMET devuelve primero un JSON con la URL de los datos
        metadata = response.json()
        
        if metadata.get('estado') != 200:
            print(f"[ERROR] AEMET error: {metadata.get('descripcion', 'Desconocido')}")
            return None
        
        # Obtener la URL de los datos reales
        datos_url = metadata.get('datos')
        
        if not datos_url:
            print("[ERROR] No se recibio URL de datos")
            return None
        
        print(f"[2/2] Descargando pronostico...")
        datos_response = requests.get(datos_url, timeout=10)
        
        if datos_response.status_code != 200:
            print(f"[ERROR] Error descargando datos: {datos_response.status_code}")
            return None
        
        pronostico = datos_response.json()
        
        print(f"[OK] Pronostico obtenido")
        print()
        
        return pronostico
        
    except requests.RequestException as e:
        print(f"[ERROR] Error de conexion: {e}")
        return None
    except Exception as e:
        print(f"[ERROR] Error inesperado: {e}")
        return None


def formatear_pronostico(pronostico: dict, ciudad: str, dias: int = 3) -> str:
    """
    Formatea el pronostico de manera legible
    """
    if not pronostico or len(pronostico) == 0:
        return "No se pudo obtener el pronostico"
    
    # Obtener datos del primer elemento (prediccion)
    prediccion = pronostico[0].get('prediccion', {})
    nombre = pronostico[0].get('nombre', ciudad)
    provincia = pronostico[0].get('provincia', '')
    
    resultado = [
        f"PRONOSTICO METEOROLOGICO - {nombre.upper()}",
        f"Provincia: {provincia}",
        f"Fuente: AEMET (Agencia Estatal de Meteorologia)",
        "=" * 70,
        ""
    ]
    
    # Obtener dias de pronostico
    dias_pronostico = prediccion.get('dia', [])
    
    for i, dia in enumerate(dias_pronostico[:dias]):
        fecha = dia.get('fecha', 'N/A')
        
        # Temperatura
        temp_data = dia.get('temperatura', {})
        temp_max = temp_data.get('maxima', 'N/A')
        temp_min = temp_data.get('minima', 'N/A')
        
        # Estado del cielo
        estado_cielo = dia.get('estadoCielo', [])
        cielo_descripcion = estado_cielo[0].get('descripcion', 'N/A') if estado_cielo else 'N/A'
        
        # Probabilidad de precipitacion
        prob_precip = dia.get('probPrecipitacion', [])
        prob_value = prob_precip[0].get('value', 'N/A') if prob_precip else 'N/A'
        
        # Formatear fecha
        try:
            fecha_obj = datetime.strptime(fecha, '%Y-%m-%dT%H:%M:%S')
            fecha_str = fecha_obj.strftime('%d/%m/%Y - %A')
        except:
            fecha_str = fecha
        
        resultado.append(f"DIA {i+1}: {fecha_str}")
        resultado.append(f"  Temperatura: {temp_min}°C - {temp_max}°C")
        resultado.append(f"  Cielo: {cielo_descripcion}")
        resultado.append(f"  Prob. lluvia: {prob_value}%")
        resultado.append("")
    
    return "\n".join(resultado)


def main():
    """
    Funcion principal
    """
    print("=" * 70)
    print("PRONOSTICO DE TEMPERATURA - AEMET")
    print("Agencia Estatal de Meteorologia de España")
    print("=" * 70)
    print()
    
    # Verificar API key
    if AEMET_API_KEY == "TU_API_KEY_AQUI":
        print("[AVISO] No has configurado tu API key de AEMET")
        print()
        print("Para usar este script:")
        print("1. Registrate gratis en: https://opendata.aemet.es/centrodedescargas/altaUsuario")
        print("2. Obten tu API key")
        print("3. Edita este archivo y reemplaza 'TU_API_KEY_AQUI' con tu key")
        print()
        print("=" * 70)
        sys.exit(1)
    
    if len(sys.argv) < 2:
        print("USO: python aemet_temperatura.py <ciudad> [dias]")
        print()
        print("EJEMPLOS:")
        print("  python aemet_temperatura.py Madrid")
        print("  python aemet_temperatura.py Barcelona 5")
        print("  python aemet_temperatura.py Sevilla 3")
        print()
        print("CIUDADES DISPONIBLES:")
        ciudades_lista = sorted(set(CIUDADES_AEMET.keys()))
        for i in range(0, len(ciudades_lista), 5):
            print("  " + ", ".join(ciudades_lista[i:i+5]))
        print()
        sys.exit(1)
    
    ciudad = sys.argv[1]
    dias = int(sys.argv[2]) if len(sys.argv) > 2 else 3
    
    # Obtener pronostico
    pronostico = obtener_pronostico_aemet(ciudad, dias)
    
    if pronostico:
        # Formatear y mostrar
        print("=" * 70)
        print(formatear_pronostico(pronostico, ciudad, dias))
        print("=" * 70)
    else:
        print()
        print("=" * 70)
        print("[ERROR] No se pudo obtener el pronostico")
        print("=" * 70)


if __name__ == "__main__":
    main()
