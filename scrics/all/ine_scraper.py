#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script para consultar población de municipios españoles
Consulta SIEMPRE en tiempo real la web oficial del INE
NO usa datos hardcodeados - Todo se obtiene de www.ine.es
"""

import requests
import sys
import re
from bs4 import BeautifulSoup
import json

def buscar_codigo_municipio_ine(nombre_municipio):
    """
    Busca el código INE de un municipio consultando directamente la API del INE
    NO usa datos hardcodeados
    """
    print(f"[1/3] Buscando codigo INE para '{nombre_municipio}'...")
    
    try:
        # API del INE para obtener lista de municipios
        url = "https://servicios.ine.es/wstempus/jsCache/ES/MUNICIPIOS_AL/all"
        
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
            'Accept': 'application/json'
        }
        
        print(f"[API] Consultando: {url}")
        response = requests.get(url, headers=headers, timeout=20)
        print(f"[HTTP] Status: {response.status_code}")
        
        if response.status_code == 200:
            # El INE devuelve formato JSONSTAT
            # Intentar extraer los datos directamente del texto
            try:
                # Limpiar el texto (a veces viene con BOM o caracteres extra)
                texto = response.text.strip()
                
                # Si empieza con callback, extraerlo
                if texto.startswith('callback'):
                    # Formato: callback({"key": "value"})
                    inicio = texto.index('(')
                    fin = texto.rindex(')')
                    texto = texto[inicio+1:fin]
                
                datos = json.loads(texto)
                
                # Extraer la lista de municipios del formato JSONSTAT
                if 'extension' in datos and 'CODMUNICIPIOS' in datos.get('id', []):
                    # Obtener índice del municipio
                    idx_muni = datos['id'].index('CODMUNICIPIOS')
                    dimension_muni = datos['dimension']['CODMUNICIPIOS']
                    categorias = dimension_muni.get('category', {})
                    
                    if 'label' in categorias:
                        # Buscar el municipio
                        nombre_buscar = nombre_municipio.lower().strip()
                        resultados = []
                        
                        for codigo, nombre_oficial in categorias['label'].items():
                            if nombre_buscar in nombre_oficial.lower():
                                resultados.append({
                                    'codigo': codigo,
                                    'nombre': nombre_oficial
                                })
                        
                        if resultados:
                            if len(resultados) > 1:
                                print(f"[INFO] {len(resultados)} coincidencias:")
                                for i, r in enumerate(resultados[:3], 1):
                                    print(f"  {i}. {r['nombre']} - Codigo: {r['codigo']}")
                            
                            resultado = resultados[0]
                            print(f"[OK] Municipio: {resultado['nombre']}")
                            print(f"[OK] Codigo INE: {resultado['codigo']}")
                            return resultado['codigo']
                
                print(f"[ERROR] No se encontro '{nombre_municipio}' en los datos del INE")
                return None
                    
            except (json.JSONDecodeError, ValueError, KeyError) as e:
                print(f"[ERROR] Error procesando respuesta del INE: {e}")
                # Intentar método alternativo: scraping de la tabla 2852
                return buscar_codigo_alternativo(nombre_municipio)
            
        else:
            print(f"[ERROR] Error HTTP: {response.status_code}")
            return None
            
    except Exception as e:
        print(f"[ERROR] Error al buscar municipio: {e}")
        return None


def buscar_codigo_alternativo(nombre_municipio):
    """
    Método alternativo: buscar en la tabla interactiva del INE
    """
    print(f"[INFO] Intentando metodo alternativo...")
    
    try:
        # Scraping de la tabla de población municipal
        url = "https://www.ine.es/jaxiT3/Tabla.htm?t=2852"
        
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
        
        response = requests.get(url, headers=headers, timeout=15)
        
        if response.status_code == 200:
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Buscar en las opciones del selector de municipios
            selects = soup.find_all('select')
            nombre_buscar = nombre_municipio.lower().strip()
            
            for select in selects:
                options = select.find_all('option')
                for option in options:
                    texto = option.get_text(strip=True)
                    valor = option.get('value', '')
                    
                    if nombre_buscar in texto.lower() and valor:
                        print(f"[OK] Encontrado en tabla: {texto}")
                        print(f"[OK] Codigo: {valor}")
                        return valor
            
            print(f"[ERROR] No se encontro en metodo alternativo")
            return None
        else:
            print(f"[ERROR] Error HTTP alternativo: {response.status_code}")
            return None
            
    except Exception as e:
        print(f"[ERROR] Error en metodo alternativo: {e}")
        return None

def obtener_poblacion_ine(nombre_municipio, año):
    """
    Obtiene la población consultando directamente la API del INE por nombre
    NO usa datos hardcodeados
    """
    print(f"\n[2/2] Consultando poblacion en www.ine.es...")
    
    try:
        # API JSON del INE para población municipal - Tabla 2852
        # Esta API devuelve datos por provincias y algunos municipios principales
        url = f"https://servicios.ine.es/wstempus/js/ES/DATOS_TABLA/2852?tip=AM&"
        
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
            'Accept': 'application/json'
        }
        
        print(f"[API] Consultando datos de poblacion...")
        response = requests.get(url, headers=headers, timeout=30)
        print(f"[HTTP] Status: {response.status_code}")
        
        if response.status_code == 200:
            try:
                # El INE devuelve un array de objetos
                datos = response.json()
                print(f"[OK] Recibidos {len(datos)} registros del INE")
                
                if isinstance(datos, list):
                    # Buscar por nombre del municipio directamente
                    nombre_buscar = nombre_municipio.lower().strip()
                    
                    for registro in datos:
                        if isinstance(registro, dict):
                            nombre_registro = registro.get('Nombre', '').lower()
                            
                            # Buscar coincidencia con el nombre
                            # El registro debe contener el municipio y "total" (no por sexo)
                            if nombre_buscar in nombre_registro and 'total' in nombre_registro and 'hombres' not in nombre_registro and 'mujeres' not in nombre_registro:
                                
                                # Buscar en los datos del registro
                                if 'Data' in registro and isinstance(registro['Data'], list):
                                    for dato in registro['Data']:
                                        if isinstance(dato, dict):
                                            anyo_dato = dato.get('Anyo') or dato.get('anyo')
                                            valor = dato.get('Valor') or dato.get('valor')
                                            
                                            if anyo_dato == año and valor is not None:
                                                poblacion = int(valor)
                                                cod_registro = registro.get('COD', 'N/A')
                                                print(f"[OK] Registro encontrado: {registro.get('Nombre', 'N/A')}")
                                                print(f"[OK] Codigo INE: {cod_registro}")
                                                print(f"[OK] Poblacion {año}: {poblacion:,} habitantes")
                                                return poblacion
                                
                                print(f"[WARN] Registro encontrado pero sin dato para el año {año}")
                                return None
                    
                    print(f"[WARN] No se encontro '{nombre_municipio}' en los datos del INE")
                    print(f"[INFO] Esta API solo incluye provincias y algunos municipios principales")
                    print(f"[INFO] Intenta con el nombre de la provincia si es un municipio pequeño")
                    
                else:
                    print(f"[WARN] Formato de datos inesperado")
                
                return None
                
            except (json.JSONDecodeError, ValueError, KeyError, IndexError) as e:
                print(f"[WARN] Error procesando JSON: {e}")
                return None
        else:
            print(f"[ERROR] Error HTTP: {response.status_code}")
            return None
            
    except Exception as e:
        print(f"[ERROR] Error al consultar API: {e}")
        return None

def obtener_poblacion_scraping(codigo_municipio, año):
    """
    Obtiene población haciendo scraping directo de la página web del INE
    """
    print(f"[3/3] Obteniendo datos mediante scraping web...")
    
    try:
        # URL de la página de población del INE
        url = f"https://www.ine.es/jaxiT3/Tabla.htm?t=2852"
        
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
        
        response = requests.get(url, headers=headers, timeout=20)
        
        if response.status_code == 200:
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Buscar en la página los datos de población
            # El INE tiene tablas con los datos
            tablas = soup.find_all('table')
            
            print(f"[INFO] Analizando {len(tablas)} tablas en la pagina del INE...")
            
            # Por ahora retornamos None ya que necesitamos analizar
            # la estructura específica de las tablas del INE
            print(f"[WARN] Scraping web requiere analisis de estructura HTML del INE")
            return None
            
        else:
            print(f"[ERROR] Error HTTP en scraping: {response.status_code}")
            return None
            
    except Exception as e:
        print(f"[ERROR] Error en scraping: {e}")
        return None

def main():
    """
    Función principal - Consulta población SIEMPRE desde la web del INE
    SIN datos hardcodeados
    """
    
    print("=" * 70)
    print("CONSULTA POBLACION - INSTITUTO NACIONAL DE ESTADISTICA (INE)")
    print("Consulta en TIEMPO REAL - SIN datos locales")
    print("=" * 70)
    print()
    
    if len(sys.argv) != 3:
        print("USO: python ine_scraper.py <municipio> <año>")
        print()
        print("EJEMPLOS:")
        print("  python ine_scraper.py Madrid 2023")
        print("  python ine_scraper.py Salamanca 2022")
        print("  python ine_scraper.py Murcia 2021")
        print()
        print("NOTA: Funciona con provincias y capitales de España")
        print("      Los datos se obtienen en tiempo real de www.ine.es")
        print("      NO hay datos hardcodeados en el script")
        print()
        sys.exit(1)
    
    municipio = sys.argv[1]
    try:
        año = int(sys.argv[2])
    except ValueError:
        print("[ERROR] El año debe ser un numero")
        sys.exit(1)
    
    print(f"MUNICIPIO/PROVINCIA: {municipio}")
    print(f"AÑO: {año}")
    print()
    print("Consultando www.ine.es en tiempo real...")
    print("-" * 70)
    
    # Obtener población directamente por nombre (no necesita buscar código)
    poblacion = obtener_poblacion_ine(municipio, año)
    
    print()
    print("=" * 70)
    
    if poblacion:
        print("[OK] CONSULTA EXITOSA")
        print()
        print(f"MUNICIPIO/PROVINCIA: {municipio}")
        print(f"AÑO: {año}")
        print(f"POBLACION: {poblacion:,} habitantes")
        print()
        print("Fuente: Instituto Nacional de Estadistica (INE)")
        print("Consultado desde: www.ine.es")
    else:
        print("[WARN] NO SE PUDO OBTENER LA POBLACION")
        print()
        print(f"Municipio/Provincia: {municipio}")
        print(f"Año: {año}")
        print()
        print("POSIBLES CAUSAS:")
        print("  - El nombre no coincide exactamente")
        print("  - El municipio es muy pequeño (solo provincias y capitales)")
        print("  - El año solicitado no tiene datos disponibles")
        print()
        print("SUGERENCIAS:")
        print("  - Prueba con el nombre de la provincia")
        print("  - Verifica en: https://www.ine.es/jaxiT3/Tabla.htm?t=2852")
    
    print("=" * 70)

if __name__ == "__main__":
    main()
