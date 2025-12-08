#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script para consultar el pronostico de temperatura de ciudades españolas
Usa AEMET OpenData (API oficial del gobierno español)
Requiere API_KEY gratuita de https://opendata.aemet.es/centrodedescargas/inicio
"""

import requests
import sys
from datetime import datetime


# CONFIGURA TU API_KEY AQUI
# Registrate gratis en: https://opendata.aemet.es/centrodedescargas/inicio
API_KEY = "TU_API_KEY_AQUI"  # CAMBIA ESTO por tu API key


# Codigos de municipio AEMET (codigo INE de 5 digitos)
CODIGOS_MUNICIPIOS = {
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
    'vitoria': '01059',
    'vitoria-gasteiz': '01059',
    'l\'hospitalet': '08101',
    'hospitalet de llobregat': '08101',
    'a coruña': '15030',
    'la coruña': '15030',
    'granada': '18087',
    'oviedo': '33044',
    'badalona': '08015',
    'cartagena': '30016',
    'terrassa': '08279',
    'jerez': '11020',
    'jerez de la frontera': '11020',
    'sabadell': '08187',
    'santa cruz de tenerife': '38038',
    'mostoles': '28092',
    'alcala de henares': '28005',
    'fuenlabrada': '28058',
    'pamplona': '31201',
    'almeria': '04013',
    'leganes': '28074',
    'san sebastian': '20069',
    'donostia': '20069',
    'santander': '39075',
    'castellon': '12040',
    'castellon de la plana': '12040',
    'burgos': '09059',
    'albacete': '02003',
    'getafe': '28065',
    'alcorcon': '28007',
    'salamanca': '37274',
    'logroño': '26089',
    'huelva': '21041',
    'tarragona': '43148',
    'badajoz': '06015',
    'leon': '24089',
    'caceres': '10037',
    'ourense': '32054',
    'reus': '43123',
    'telde': '35025',
    'lugo': '27028',
    'santiago de compostela': '15078',
    'aviles': '33004',
    'cuenca': '16078',
    'guadalajara': '19130',
    'toledo': '45168',
    'cadiz': '11012',
    'jaen': '23050',
    'pontevedra': '36038',
    'ciudad real': '13034',
    'segovia': '40194',
    'palencia': '34120',
    'zamora': '49275',
    'soria': '42173',
    'teruel': '44216',
    'huesca': '22125',
}


def obtener_pronostico(ciudad: str, dias: int = 3):
    """
    Obtiene el pronostico de temperatura para una ciudad usando AEMET
    
    Args:
        ciudad: Nombre de la ciudad
        dias: Numero de dias (1=hoy, 2=hoy+mañana, 3=hoy+2dias, etc.)
    
    Returns:
        Diccionario con los datos del pronostico o None si hay error
    """
    print(f"Consultando pronostico AEMET para {ciudad.title()}...")
    print()
    
    # Verificar API_KEY
    if API_KEY == "TU_API_KEY_AQUI":
        print("[ERROR] Debes configurar tu API_KEY de AEMET")
        print()
        print("Pasos para obtener tu API_KEY gratuita:")
        print("1. Ve a: https://opendata.aemet.es/centrodedescargas/inicio")
        print("2. Haz clic en 'Solicitar API Key'")
        print("3. Rellena el formulario (es gratis)")
        print("4. Revisa tu email y activa la API Key")
        print("5. Edita este script y pon tu API Key en la linea 15:")
        print("   API_KEY = 'tu_clave_aqui'")
        print()
        return None
    
    # Buscar codigo de municipio
    ciudad_lower = ciudad.lower().strip()
    codigo = CODIGOS_MUNICIPIOS.get(ciudad_lower)
    
    if not codigo:
        print(f"[ERROR] Ciudad '{ciudad}' no encontrada")
        print()
        print("Ciudades disponibles:")
        ciudades = sorted(CODIGOS_MUNICIPIOS.keys())
        for i in range(0, len(ciudades), 4):
            print("  " + ", ".join([c.title() for c in ciudades[i:i+4]]))
        print()
        return None
    
    print(f"[OK] Codigo municipio: {codigo}")
    
    try:
        # Determinar endpoint segun dias
        if dias == 1:
            endpoint = f"https://opendata.aemet.es/opendata/api/prediccion/especifica/municipio/horaria/{codigo}"
            tipo = "horaria"
        elif dias <= 7:
            endpoint = f"https://opendata.aemet.es/opendata/api/prediccion/especifica/municipio/diaria/{codigo}"
            tipo = "diaria"
        else:
            print("[INFO] AEMET solo ofrece hasta 7 dias de pronostico")
            print("[INFO] Usando pronostico de 7 dias")
            endpoint = f"https://opendata.aemet.es/opendata/api/prediccion/especifica/municipio/diaria/{codigo}"
            tipo = "diaria"
            dias = 7
        
        # Headers con API_KEY
        headers = {
            'api_key': API_KEY
        }
        
        print(f"[1/3] Consultando AEMET (pronostico {tipo})...")
        response = requests.get(endpoint, headers=headers, timeout=15)
        
        if response.status_code == 401:
            print("[ERROR] API_KEY invalida o no autorizada")
            print("[INFO] Verifica tu API Key en: https://opendata.aemet.es/centrodedescargas/inicio")
            return None
        
        if response.status_code == 404:
            print(f"[ERROR] No hay datos disponibles para {ciudad}")
            return None
        
        if response.status_code != 200:
            print(f"[ERROR] HTTP {response.status_code}")
            print(f"[INFO] Respuesta: {response.text}")
            return None
        
        # AEMET devuelve una URL a los datos reales
        datos_metadata = response.json()
        
        if datos_metadata.get('estado') != 200:
            print(f"[ERROR] AEMET respondio: {datos_metadata.get('descripcion', 'Error desconocido')}")
            return None
        
        url_datos = datos_metadata.get('datos')
        
        if not url_datos:
            print("[ERROR] No se obtuvo URL de datos")
            return None
        
        print("[2/3] Descargando datos del pronostico...")
        response_datos = requests.get(url_datos, timeout=15)
        
        if response_datos.status_code != 200:
            print(f"[ERROR] No se pudieron descargar los datos: HTTP {response_datos.status_code}")
            return None
        
        print("[3/3] Procesando datos...")
        datos = response_datos.json()
        
        if not datos or len(datos) == 0:
            print("[ERROR] No hay datos en la respuesta")
            return None
        
        print("[OK] Datos recibidos")
        print()
        
        return {
            'ciudad': ciudad.title(),
            'codigo': codigo,
            'tipo': tipo,
            'dias_solicitados': dias,
            'datos': datos[0] if isinstance(datos, list) else datos
        }
        
    except requests.RequestException as e:
        print(f"[ERROR] Error de conexion: {e}")
        return None
    except Exception as e:
        print(f"[ERROR] Error: {e}")
        import traceback
        traceback.print_exc()
        return None


def formatear_pronostico_diario(datos):
    """
    Formatea el pronostico diario de AEMET
    """
    ciudad = datos['ciudad']
    info = datos['datos']
    
    nombre_completo = info.get('nombre', ciudad)
    provincia = info.get('provincia', '')
    
    dias_semana = ['Lunes', 'Martes', 'Miercoles', 'Jueves', 'Viernes', 'Sabado', 'Domingo']
    
    print("=" * 70)
    print(f"PRONOSTICO AEMET - {nombre_completo.upper()}")
    if provincia:
        print(f"Provincia: {provincia}")
    print("=" * 70)
    print()
    
    prediccion = info.get('prediccion', {})
    dias_prediccion = prediccion.get('dia', [])
    
    if not dias_prediccion:
        print("[ERROR] No hay datos de prediccion")
        return
    
    # Limitar a los dias solicitados
    dias_prediccion = dias_prediccion[:datos['dias_solicitados']]
    
    for dia_data in dias_prediccion:
        fecha_str = dia_data.get('fecha', '')
        
        if not fecha_str:
            continue
        
        # Parsear fecha (formato: YYYY-MM-DDTHH:MM:SS)
        fecha = datetime.strptime(fecha_str.split('T')[0], '%Y-%m-%d')
        dia_semana = dias_semana[fecha.weekday()]
        fecha_formato = fecha.strftime('%d/%m/%Y')
        
        # Etiqueta (HOY, MAÑANA)
        hoy = datetime.now().date()
        if fecha.date() == hoy:
            etiqueta = "HOY"
        elif (fecha.date() - hoy).days == 1:
            etiqueta = "MAÑANA"
        else:
            etiqueta = ""
        
        print(f"{dia_semana:10} {fecha_formato}  {etiqueta}")
        
        # Temperatura
        temp_data = dia_data.get('temperatura', {})
        temp_max_list = temp_data.get('maxima', [])
        temp_min_list = temp_data.get('minima', [])
        
        if temp_max_list and temp_min_list:
            # Puede haber multiples valores, tomar el primero o el valor numerico
            temp_max = temp_max_list if isinstance(temp_max_list, (int, float)) else (temp_max_list[0] if temp_max_list else None)
            temp_min = temp_min_list if isinstance(temp_min_list, (int, float)) else (temp_min_list[0] if temp_min_list else None)
            
            if temp_max and temp_min:
                print(f"  Temperatura:  {temp_min:5.0f}°C - {temp_max:5.0f}°C")
        
        # Sensacion termica
        sens_term = dia_data.get('sensTermica', {})
        sens_max = sens_term.get('maxima', None)
        sens_min = sens_term.get('minima', None)
        if sens_max and sens_min:
            print(f"  Sens. termica:{sens_min:5.0f}°C - {sens_max:5.0f}°C")
        
        # Probabilidad de precipitacion
        prob_prec = dia_data.get('probPrecipitacion', [])
        if prob_prec:
            # Obtener maxima probabilidad del dia
            probs = [p.get('value', 0) for p in prob_prec if isinstance(p, dict)]
            if probs:
                prob_max = max(probs)
                print(f"  Prob. lluvia: {prob_max:3.0f}%")
        
        # Viento
        viento = dia_data.get('viento', [])
        if viento:
            # Obtener velocidad maxima
            velocidades = []
            for v in viento:
                if isinstance(v, dict):
                    vel = v.get('velocidad', [])
                    if vel:
                        vel_val = vel if isinstance(vel, (int, float)) else (vel[0] if vel else 0)
                        velocidades.append(vel_val)
            
            if velocidades:
                vel_max = max(velocidades)
                print(f"  Viento:       {vel_max:5.0f} km/h")
        
        # Estado del cielo
        cielo = dia_data.get('estadoCielo', [])
        if cielo:
            # Tomar descripcion del primer periodo
            for c in cielo:
                if isinstance(c, dict):
                    descripcion = c.get('descripcion', '')
                    if descripcion:
                        print(f"  Cielo:        {descripcion}")
                        break
        
        print()
    
    print("=" * 70)
    elaborado = info.get('elaborado', '')
    if elaborado:
        fecha_elab = datetime.strptime(elaborado.split('T')[0], '%Y-%m-%d')
        print(f"Elaborado: {fecha_elab.strftime('%d/%m/%Y')}")
    print("Fuente: AEMET OpenData (https://opendata.aemet.es)")
    print("=" * 70)


def formatear_pronostico_horario(datos):
    """
    Formatea el pronostico horario de AEMET (para hoy)
    """
    ciudad = datos['ciudad']
    info = datos['datos']
    
    nombre_completo = info.get('nombre', ciudad)
    provincia = info.get('provincia', '')
    
    print("=" * 70)
    print(f"PRONOSTICO HORARIO AEMET - {nombre_completo.upper()}")
    if provincia:
        print(f"Provincia: {provincia}")
    print("=" * 70)
    print()
    
    prediccion = info.get('prediccion', {})
    dias_prediccion = prediccion.get('dia', [])
    
    if not dias_prediccion:
        print("[ERROR] No hay datos de prediccion")
        return
    
    # Solo el primer dia (hoy)
    dia_hoy = dias_prediccion[0]
    
    print("PRONOSTICO DE HOY (cada 3 horas)")
    print("-" * 70)
    
    # Temperatura por hora
    temp_horaria = dia_hoy.get('temperatura', [])
    
    # Seleccionar cada 3 horas para no saturar
    horas_mostrar = [0, 3, 6, 9, 12, 15, 18, 21]
    
    for temp_data in temp_horaria:
        if isinstance(temp_data, dict):
            periodo = temp_data.get('periodo', '')
            if periodo:
                hora = int(periodo[:2])
                if hora in horas_mostrar:
                    temp = temp_data.get('value', 'N/A')
                    print(f"{periodo[:5]}h  Temperatura: {temp}°C")
    
    print()
    print("=" * 70)
    print("Fuente: AEMET OpenData (https://opendata.aemet.es)")
    print("=" * 70)


def main():
    """
    Funcion principal
    """
    print("=" * 70)
    print("PRONOSTICO DE TEMPERATURA AEMET - Ciudades de España")
    print("=" * 70)
    print()
    
    if len(sys.argv) < 2:
        print("USO: python temperatura_aemet.py <ciudad> [dias]")
        print()
        print("EJEMPLOS:")
        print("  python temperatura_aemet.py Madrid")
        print("  python temperatura_aemet.py Barcelona 7")
        print("  python temperatura_aemet.py Sevilla 5")
        print()
        print("CIUDADES DISPONIBLES:")
        ciudades = sorted(CODIGOS_MUNICIPIOS.keys())
        for i in range(0, len(ciudades), 4):
            print("  " + ", ".join([c.title() for c in ciudades[i:i+4]]))
        print()
        print("DIAS: Entre 1 y 7 (por defecto 3)")
        print("  - 1 dia: Pronostico horario de hoy")
        print("  - 2-7 dias: Pronostico diario")
        print()
        print("NOTA: Necesitas configurar tu API_KEY de AEMET (gratuita)")
        print("      Registrate en: https://opendata.aemet.es/centrodedescargas/inicio")
        print()
        sys.exit(1)
    
    ciudad = sys.argv[1]
    dias = int(sys.argv[2]) if len(sys.argv) > 2 else 3
    
    # Validar dias
    if dias < 1:
        print("[ERROR] El numero de dias debe ser al menos 1")
        sys.exit(1)
    
    # Obtener pronostico
    datos = obtener_pronostico(ciudad, dias)
    
    if datos:
        if datos['tipo'] == 'horaria':
            formatear_pronostico_horario(datos)
        else:
            formatear_pronostico_diario(datos)


if __name__ == "__main__":
    main()
