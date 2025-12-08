#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script para consultar el pronostico de temperatura de CUALQUIER ciudad española
Busca la ciudad dinamicamente en AEMET - SIN datos hardcodeados
Requiere API_KEY gratuita de https://opendata.aemet.es/centrodedescargas/inicio
"""

import requests
import sys
from datetime import datetime


# CONFIGURA TU API_KEY AQUI
# Registrate gratis en: https://opendata.aemet.es/centrodedescargas/inicio
API_KEY = "eyJhbGciOiJIUzI1NiJ9.eyJzdWIiOiJqb3NlQGxlZ2lkby5jb20iLCJqdGkiOiI3MzdhNWZlYy02ZTMyLTRlNmUtOTkwMy1mMGI5ZjQ0ZTliYWUiLCJpc3MiOiJBRU1FVCIsImlhdCI6MTY5MzI1MDM4NSwidXNlcklkIjoiNzM3YTVmZWMtNmUzMi00ZTZlLTk5MDMtZjBiOWY0NGU5YmFlIiwicm9sZSI6IiJ9.2PoU7S76ioZokGu51DYy8rsiaCe8U-dtORnpG60ahIA"  # API Key configurada


def buscar_municipio(nombre_ciudad):
    """
    Busca el codigo de municipio en AEMET para cualquier ciudad
    NO usa datos hardcodeados, consulta la API de AEMET
    
    Args:
        nombre_ciudad: Nombre de la ciudad a buscar
    
    Returns:
        Tupla (codigo, nombre_completo) o (None, None) si no se encuentra
    """
    print(f"[1/4] Buscando '{nombre_ciudad}' en base de datos AEMET...")
    
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
        return None, None
    
    try:
        # Endpoint para obtener TODOS los municipios de España
        url = "https://opendata.aemet.es/opendata/api/maestro/municipios"
        
        # AEMET usa api_key como parametro de query, no header
        params = {
            'api_key': API_KEY
        }
        
        response = requests.get(url, params=params, timeout=15)
        
        if response.status_code == 401:
            print("[ERROR] API_KEY invalida o no autorizada")
            print("[INFO] Verifica tu API Key en: https://opendata.aemet.es/centrodedescargas/inicio")
            return None, None
        
        if response.status_code == 429:
            print("[ERROR] Demasiadas peticiones a AEMET")
            print("[INFO] Espera unos minutos antes de volver a intentarlo")
            print("[INFO] AEMET tiene limite de peticiones por minuto")
            return None, None
        
        if response.status_code != 200:
            print(f"[ERROR] HTTP {response.status_code}")
            if response.text:
                print(f"[DEBUG] Respuesta: {response.text[:200]}")
            return None, None
        
        # AEMET devuelve URL a los datos
        datos_metadata = response.json()
        
        if datos_metadata.get('estado') != 200:
            print(f"[ERROR] AEMET respondio: {datos_metadata.get('descripcion', 'Error')}")
            return None, None
        
        url_datos = datos_metadata.get('datos')
        if not url_datos:
            print("[ERROR] No se obtuvo URL de datos")
            return None, None
        
        # Descargar lista de municipios
        response_datos = requests.get(url_datos, timeout=15)
        
        if response_datos.status_code != 200:
            print(f"[ERROR] No se pudieron descargar los municipios")
            return None, None
        
        municipios = response_datos.json()
        
        if not municipios:
            print("[ERROR] No se obtuvieron datos de municipios")
            return None, None
        
        print(f"[OK] Base de datos cargada ({len(municipios)} municipios)")
        
        # Buscar el municipio
        nombre_lower = nombre_ciudad.lower().strip()
        
        # Busqueda exacta primero
        for mun in municipios:
            nombre_mun = mun.get('nombre', '').lower()
            if nombre_mun == nombre_lower:
                codigo = mun.get('id')
                nombre_completo = mun.get('nombre')
                print(f"[OK] Encontrada: {nombre_completo} (codigo: {codigo})")
                return codigo, nombre_completo
        
        # Busqueda parcial (contiene)
        coincidencias = []
        for mun in municipios:
            nombre_mun = mun.get('nombre', '').lower()
            if nombre_lower in nombre_mun or nombre_mun in nombre_lower:
                coincidencias.append({
                    'codigo': mun.get('id'),
                    'nombre': mun.get('nombre'),
                    'provincia': mun.get('provincia', 'N/A')
                })
        
        if not coincidencias:
            print(f"[ERROR] No se encontro ninguna ciudad con '{nombre_ciudad}'")
            print("[INFO] Verifica el nombre de la ciudad")
            return None, None
        
        # Si hay una sola coincidencia, usarla
        if len(coincidencias) == 1:
            print(f"[OK] Encontrada: {coincidencias[0]['nombre']} ({coincidencias[0]['provincia']})")
            return coincidencias[0]['codigo'], coincidencias[0]['nombre']
        
        # Si hay multiples coincidencias, mostrar y elegir la primera
        print(f"[INFO] Se encontraron {len(coincidencias)} coincidencias:")
        for i, mun in enumerate(coincidencias[:10], 1):
            print(f"  {i}. {mun['nombre']} ({mun['provincia']}) - codigo: {mun['codigo']}")
        
        if len(coincidencias) > 10:
            print(f"  ... y {len(coincidencias) - 10} mas")
        
        print()
        print(f"[INFO] Usando la primera: {coincidencias[0]['nombre']} (codigo: {coincidencias[0]['codigo']})")
        return coincidencias[0]['codigo'], coincidencias[0]['nombre']
        
    except requests.RequestException as e:
        print(f"[ERROR] Error de conexion: {e}")
        return None, None
    except Exception as e:
        print(f"[ERROR] Error al buscar municipio: {e}")
        import traceback
        traceback.print_exc()
        return None, None


def obtener_pronostico(codigo_municipio, nombre_ciudad, dias=3):
    """
    Obtiene el pronostico de temperatura para un codigo de municipio
    
    Args:
        codigo_municipio: Codigo INE del municipio (5 digitos)
        nombre_ciudad: Nombre de la ciudad (para mostrar)
        dias: Numero de dias de pronostico
    
    Returns:
        Diccionario con los datos o None si hay error
    """
    try:
        # Determinar endpoint segun dias
        if dias == 1:
            endpoint = f"https://opendata.aemet.es/opendata/api/prediccion/especifica/municipio/horaria/{codigo_municipio}"
            tipo = "horaria"
        elif dias <= 7:
            endpoint = f"https://opendata.aemet.es/opendata/api/prediccion/especifica/municipio/diaria/{codigo_municipio}"
            tipo = "diaria"
        else:
            print("[INFO] AEMET solo ofrece hasta 7 dias de pronostico")
            print("[INFO] Usando pronostico de 7 dias")
            endpoint = f"https://opendata.aemet.es/opendata/api/prediccion/especifica/municipio/diaria/{codigo_municipio}"
            tipo = "diaria"
            dias = 7
        
        # AEMET usa api_key como parametro de query, no header
        params = {
            'api_key': API_KEY
        }
        
        print(f"[2/4] Consultando AEMET (pronostico {tipo})...")
        response = requests.get(endpoint, params=params, timeout=15)
        
        if response.status_code == 404:
            print(f"[ERROR] No hay datos disponibles para esta ciudad")
            return None
        
        if response.status_code != 200:
            print(f"[ERROR] HTTP {response.status_code}")
            return None
        
        # AEMET devuelve URL a los datos
        datos_metadata = response.json()
        
        if datos_metadata.get('estado') != 200:
            print(f"[ERROR] AEMET respondio: {datos_metadata.get('descripcion', 'Error')}")
            return None
        
        url_datos = datos_metadata.get('datos')
        if not url_datos:
            print("[ERROR] No se obtuvo URL de datos")
            return None
        
        print("[3/4] Descargando pronostico...")
        response_datos = requests.get(url_datos, timeout=15)
        
        if response_datos.status_code != 200:
            print(f"[ERROR] No se pudieron descargar los datos")
            return None
        
        print("[4/4] Procesando datos...")
        datos = response_datos.json()
        
        if not datos:
            print("[ERROR] No hay datos en la respuesta")
            return None
        
        print("[OK] Pronostico obtenido")
        print()
        
        return {
            'ciudad': nombre_ciudad,
            'codigo': codigo_municipio,
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
    Formatea el pronostico diario
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
        
        # Parsear fecha
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
        temp_max = temp_data.get('maxima')
        temp_min = temp_data.get('minima')
        
        if temp_max is not None and temp_min is not None:
            print(f"  Temperatura:  {temp_min:5.0f}°C - {temp_max:5.0f}°C")
        
        # Sensacion termica
        sens_term = dia_data.get('sensTermica', {})
        sens_max = sens_term.get('maxima')
        sens_min = sens_term.get('minima')
        if sens_max is not None and sens_min is not None:
            print(f"  Sens. termica:{sens_min:5.0f}°C - {sens_max:5.0f}°C")
        
        # Probabilidad de precipitacion
        prob_prec = dia_data.get('probPrecipitacion', [])
        if prob_prec:
            probs = [p.get('value', 0) for p in prob_prec if isinstance(p, dict) and p.get('value') is not None]
            if probs:
                prob_max = max(probs)
                print(f"  Prob. lluvia: {prob_max:3.0f}%")
        
        # Viento
        viento = dia_data.get('viento', [])
        if viento:
            velocidades = []
            for v in viento:
                if isinstance(v, dict):
                    vel = v.get('velocidad')
                    if vel is not None:
                        velocidades.append(vel if isinstance(vel, (int, float)) else (vel[0] if isinstance(vel, list) and vel else 0))
            
            if velocidades:
                vel_max = max(velocidades)
                print(f"  Viento:       {vel_max:5.0f} km/h")
        
        # Estado del cielo
        cielo = dia_data.get('estadoCielo', [])
        if cielo:
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
        try:
            fecha_elab = datetime.strptime(elaborado.split('T')[0], '%Y-%m-%d')
            print(f"Elaborado: {fecha_elab.strftime('%d/%m/%Y')}")
        except:
            pass
    print("Fuente: AEMET OpenData (https://opendata.aemet.es)")
    print("=" * 70)


def formatear_pronostico_horario(datos):
    """
    Formatea el pronostico horario (hoy)
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
    
    dia_hoy = dias_prediccion[0]
    
    print("PRONOSTICO DE HOY (cada 3 horas)")
    print("-" * 70)
    
    # Temperatura por hora
    temp_horaria = dia_hoy.get('temperatura', [])
    
    horas_mostrar = [0, 3, 6, 9, 12, 15, 18, 21]
    
    for temp_data in temp_horaria:
        if isinstance(temp_data, dict):
            periodo = temp_data.get('periodo', '')
            if periodo:
                try:
                    hora = int(periodo[:2])
                    if hora in horas_mostrar:
                        temp = temp_data.get('value', 'N/A')
                        print(f"{periodo[:5]}h  Temperatura: {temp}°C")
                except:
                    pass
    
    print()
    print("=" * 70)
    print("Fuente: AEMET OpenData (https://opendata.aemet.es)")
    print("=" * 70)


def main():
    """
    Funcion principal
    """
    print("=" * 70)
    print("PRONOSTICO AEMET - CUALQUIER Ciudad de España")
    print("SIN datos hardcodeados - Busqueda dinamica en AEMET")
    print("=" * 70)
    print()
    
    if len(sys.argv) < 2:
        print("USO: python temperatura_aemet_dinamico.py <ciudad> [dias]")
        print()
        print("EJEMPLOS:")
        print("  python temperatura_aemet_dinamico.py Madrid")
        print("  python temperatura_aemet_dinamico.py Barcelona 7")
        print("  python temperatura_aemet_dinamico.py \"San Sebastian\" 5")
        print("  python temperatura_aemet_dinamico.py Alcobendas 3")
        print("  python temperatura_aemet_dinamico.py \"Palma de Mallorca\" 4")
        print()
        print("CARACTERISTICAS:")
        print("  - Busca CUALQUIER ciudad de España (mas de 8.000 municipios)")
        print("  - NO usa datos hardcodeados")
        print("  - Consulta dinamica a la base de datos de AEMET")
        print("  - 1 dia: Pronostico horario")
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
    
    print()
    
    # Buscar municipio dinamicamente
    codigo, nombre_completo = buscar_municipio(ciudad)
    
    if not codigo:
        sys.exit(1)
    
    print()
    
    # Obtener pronostico
    datos = obtener_pronostico(codigo, nombre_completo, dias)
    
    if datos:
        if datos['tipo'] == 'horaria':
            formatear_pronostico_horario(datos)
        else:
            formatear_pronostico_diario(datos)


if __name__ == "__main__":
    main()
