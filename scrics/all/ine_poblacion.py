#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script para consultar poblacion de provincias y municipios principales de España
Consulta en tiempo real la API oficial del INE (Instituto Nacional de Estadistica)
SIN datos hardcodeados - Todo se obtiene directamente de www.ine.es
"""

import requests
import sys
import json


def obtener_poblacion_ine(nombre_lugar, año):
    """
    Consulta la poblacion de una provincia o municipio principal en el INE
    Busca directamente por nombre en la API
    
    Args:
        nombre_lugar (str): Nombre de la provincia o municipio
        año (int): Año de consulta
    
    Returns:
        int: Poblacion si se encuentra, None si no
    """
    print(f"Consultando poblacion de '{nombre_lugar}' para el año {año}...")
    print()
    
    try:
        # API del INE - Tabla 2852: Poblacion por municipios
        url = "https://servicios.ine.es/wstempus/js/ES/DATOS_TABLA/2852?tip=AM&"
        
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)',
            'Accept': 'application/json'
        }
        
        print("[1/2] Descargando datos del INE...")
        response = requests.get(url, headers=headers, timeout=30)
        
        if response.status_code != 200:
            print(f"[ERROR] Error HTTP: {response.status_code}")
            return None
        
        # Parsear JSON
        datos = response.json()
        print(f"[OK] Recibidos {len(datos)} registros de poblacion")
        print()
        
        # Buscar por nombre
        print(f"[2/2] Buscando '{nombre_lugar}' en los datos...")
        nombre_buscar = nombre_lugar.lower().strip()
        
        for registro in datos:
            if not isinstance(registro, dict):
                continue
            
            nombre_registro = registro.get('Nombre', '').lower()
            
            # Buscar coincidencia (debe ser Total, no por sexo)
            if (nombre_buscar in nombre_registro and 
                'total' in nombre_registro and 
                'hombres' not in nombre_registro and 
                'mujeres' not in nombre_registro):
                
                # Buscar el año en los datos
                datos_registro = registro.get('Data', [])
                
                for dato in datos_registro:
                    if not isinstance(dato, dict):
                        continue
                    
                    anyo_dato = dato.get('Anyo')
                    valor = dato.get('Valor')
                    
                    if anyo_dato == año and valor is not None:
                        poblacion = int(valor)
                        cod_ine = registro.get('COD', 'N/A')
                        
                        print(f"[OK] Encontrado: {registro.get('Nombre', 'N/A')}")
                        print(f"[OK] Codigo INE: {cod_ine}")
                        print(f"[OK] Poblacion {año}: {poblacion:,} habitantes")
                        print()
                        
                        return poblacion
                
                # Si se encontro el registro pero no el año
                años_disponibles = sorted(set([
                    d.get('Anyo') for d in datos_registro 
                    if isinstance(d, dict) and d.get('Anyo')
                ]))
                
                print(f"[WARN] Se encontro '{nombre_lugar}' pero no tiene datos para {año}")
                print(f"[INFO] Años disponibles: {años_disponibles[0]} - {años_disponibles[-1]}")
                print()
                return None
        
        print(f"[WARN] No se encontro '{nombre_lugar}' en la API del INE")
        print("[INFO] Esta API incluye provincias y capitales principales")
        print()
        return None
        
    except requests.RequestException as e:
        print(f"[ERROR] Error de conexion: {e}")
        return None
    except (json.JSONDecodeError, KeyError, ValueError) as e:
        print(f"[ERROR] Error procesando datos: {e}")
        return None
    except Exception as e:
        print(f"[ERROR] Error inesperado: {e}")
        return None


def main():
    """
    Funcion principal
    """
    print("=" * 70)
    print("CONSULTA DE POBLACION - INE (Instituto Nacional de Estadistica)")
    print("Datos en tiempo real desde www.ine.es")
    print("=" * 70)
    print()
    
    # Validar argumentos
    if len(sys.argv) != 3:
        print("USO: python ine_poblacion.py <lugar> <año>")
        print()
        print("EJEMPLOS:")
        print("  python ine_poblacion.py Madrid 2021")
        print("  python ine_poblacion.py Barcelona 2020")
        print("  python ine_poblacion.py Murcia 2019")
        print("  python ine_poblacion.py Salamanca 2018")
        print()
        print("NOTA:")
        print("  - Funciona con provincias y capitales de provincia")
        print("  - Datos disponibles: 1996 - 2021")
        print("  - SIN datos hardcodeados, todo desde www.ine.es")
        print()
        sys.exit(1)
    
    lugar = sys.argv[1]
    
    try:
        año = int(sys.argv[2])
    except ValueError:
        print("[ERROR] El año debe ser un numero entero")
        print()
        print("Ejemplo: python ine_poblacion.py Madrid 2021")
        print()
        sys.exit(1)
    
    # Validar año
    if año < 1900 or año > 2030:
        print(f"[WARN] El año {año} parece incorrecto")
        print("[INFO] Datos disponibles normalmente: 1996 - 2021")
        print()
    
    # Realizar consulta
    poblacion = obtener_poblacion_ine(lugar, año)
    
    # Mostrar resultado
    print("=" * 70)
    
    if poblacion:
        print("RESULTADO:")
        print()
        print(f"  Lugar:     {lugar.title()}")
        print(f"  Año:       {año}")
        print(f"  Poblacion: {poblacion:,} habitantes")
        print()
        print("Fuente: Instituto Nacional de Estadistica (www.ine.es)")
        print("Tabla: 2852 - Poblacion por municipios")
    else:
        print("NO SE PUDO OBTENER LA POBLACION")
        print()
        print(f"  Lugar: {lugar}")
        print(f"  Año:   {año}")
        print()
        print("SUGERENCIAS:")
        print("  - Verifica que el nombre sea correcto")
        print("  - Prueba con el nombre de la provincia")
        print("  - Usa años entre 1996 y 2021")
        print("  - Consulta manual: https://www.ine.es/jaxiT3/Tabla.htm?t=2852")
    
    print("=" * 70)


if __name__ == "__main__":
    main()
