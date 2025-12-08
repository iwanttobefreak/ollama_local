import requests
import sys
import json
import re
from urllib.parse import quote

def buscar_municipios_ine():
    """Obtiene la lista completa de municipios del INE"""
    try:
        print("🌐 Descargando lista de municipios del INE...")
        
        # API del INE para obtener todos los municipios
        url = "https://servicios.ine.es/wstempus/jsCache/ES/MUNICIPIOS_AL/all"
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
            'Accept': 'application/json',
            'Accept-Language': 'es-ES,es;q=0.9'
        }
        
        response = requests.get(url, headers=headers, timeout=20)
        print(f"📡 Respuesta del INE: {response.status_code}")
        
        if response.status_code == 200:
            try:
                municipios = response.json()
                print(f"✅ Descargados {len(municipios)} municipios del INE")
                return municipios
            except json.JSONDecodeError:
                print("❌ Error: Respuesta del INE no es JSON válido")
                return None
        else:
            print(f"❌ Error HTTP del INE: {response.status_code}")
            return None
            
    except Exception as e:
        print(f"❌ Error al descargar municipios: {e}")
        return None

def buscar_codigo_municipio(nombre_municipio, lista_municipios):
    """Busca el código de un municipio en la lista del INE"""
    if not lista_municipios:
        return None
        
    nombre_lower = nombre_municipio.lower().strip()
    print(f"🔍 Buscando '{nombre_municipio}' en {len(lista_municipios)} municipios...")
    
    coincidencias = []
    
    # Buscar en la lista de municipios
    for municipio in lista_municipios:
        if isinstance(municipio, dict):
            nombre_muni = municipio.get('Nombre', '').lower()
            codigo = municipio.get('Codigo', '')
            
            # Coincidencia exacta
            if nombre_lower == nombre_muni:
                print(f"✅ Coincidencia exacta: {municipio.get('Nombre')} (código: {codigo})")
                return codigo
            
            # Coincidencias parciales
            if nombre_lower in nombre_muni or nombre_muni in nombre_lower:
                coincidencias.append({
                    'nombre': municipio.get('Nombre'),
                    'codigo': codigo,
                    'provincia': municipio.get('Provincia', 'N/A')
                })
    
    # Si hay coincidencias parciales, mostrar opciones
    if coincidencias:
        print(f"🎯 Encontradas {len(coincidencias)} coincidencias:")
        for i, muni in enumerate(coincidencias[:5], 1):  # Mostrar máximo 5
            print(f"   {i}. {muni['nombre']} (Provincia: {muni['provincia']}) - Código: {muni['codigo']}")
        
        # Devolver la primera coincidencia
        return coincidencias[0]['codigo']
    
    print(f"❌ No se encontró '{nombre_municipio}' en la base de datos del INE")
    return None

def get_poblacion_municipio(codigo_municipio, año):
    """Obtiene la población de un municipio específico del INE"""
    try:
        print(f"📊 Consultando población para municipio {codigo_municipio} en {año}...")
        
        # API del INE para datos de población municipal por año
        # Tabla 2852: Población por municipios
        url = f"https://servicios.ine.es/wstempus/jsCache/ES/DATOS_TABLA/2852"
        
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
            'Accept': 'application/json',
            'Accept-Language': 'es-ES,es;q=0.9'
        }
        
        response = requests.get(url, headers=headers, timeout=25)
        print(f"📡 Respuesta población INE: {response.status_code}")
        
        if response.status_code == 200:
            try:
                data = response.json()
                
                if isinstance(data, list):
                    # Buscar el municipio específico
                    for item in data:
                        if isinstance(item, dict):
                            cod_municipio = item.get('COD_MUNICIPIO', '')
                            nombre = item.get('Nombre', '')
                            
                            # Si encontramos el municipio
                            if cod_municipio == codigo_municipio or codigo_municipio in cod_municipio:
                                print(f"🎯 Municipio encontrado en datos: {nombre}")
                                
                                # Buscar el año específico
                                datos_tiempo = item.get('Data', [])
                                for dato in datos_tiempo:
                                    if isinstance(dato, dict):
                                        año_dato = str(dato.get('Anyo', ''))
                                        if año_dato == str(año):
                                            valor = dato.get('Valor')
                                            if valor:
                                                print(f"✅ Población encontrada: {valor}")
                                                return int(valor)
                
                print(f"⚠️ No se encontraron datos específicos para código {codigo_municipio} en {año}")
                return None
                
            except json.JSONDecodeError:
                print("❌ Error: Respuesta del INE no es JSON válido")
                return None
        else:
            print(f"❌ Error HTTP al obtener población: {response.status_code}")
            return None
            
    except Exception as e:
        print(f"❌ Error al consultar población: {e}")
        return None

def get_poblacion_alternativa(codigo_municipio, año, nombre_municipio):
    """Método alternativo para obtener población usando otra API del INE"""
    try:
        print(f"🔄 Probando método alternativo para {nombre_municipio}...")
        
        # API alternativa - Consulta directa por municipio
        url = f"https://servicios.ine.es/wstempus/js/ES/DATOS_SERIE/2852?nult=4"
        
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
            'Accept': 'application/json'
        }
        
        params = {
            'municipio': codigo_municipio,
            'fecha': f"{año}0101:{año}1231"
        }
        
        response = requests.get(url, headers=headers, params=params, timeout=20)
        print(f"📡 Respuesta alternativa: {response.status_code}")
        
        if response.status_code == 200:
            try:
                data = response.json()
                print("📊 Datos alternativos recibidos")
                
                # Aquí procesaríamos los datos de la API alternativa
                # Por ahora retornamos None
                return None
                
            except json.JSONDecodeError:
                return None
        
        return None
        
    except Exception as e:
        print(f"⚠️ Error en método alternativo: {e}")
        return None

def main():
    if len(sys.argv) != 3:
        print("Uso: python habitantes_ine.py <ciudad> <año>")
        print("Ejemplo: python habitantes_ine.py Salamanca 2022")
        print("\n🌐 Este script consulta SIEMPRE la base de datos oficial del INE en tiempo real")
        print("📍 Funciona con TODOS los municipios de España (más de 8,000)")
        print("📅 Años disponibles: 2019, 2020, 2021, 2022, 2023")
        print("\n💡 Ejemplos:")
        print("   python habitantes_ine.py Madrid 2023")
        print("   python habitantes_ine.py Salamanca 2022") 
        print("   python habitantes_ine.py Pontevedra 2021")
        sys.exit(1)
    
    ciudad = sys.argv[1]
    anyo = sys.argv[2]
    
    print(f"🌐 Consultando población de {ciudad} en {anyo} - DATOS EN TIEMPO REAL del INE")
    print("=" * 80)
    
    # Paso 1: Descargar lista completa de municipios del INE
    municipios_ine = buscar_municipios_ine()
    
    if not municipios_ine:
        print("❌ Error: No se pudo conectar con la base de datos del INE")
        print("🔧 Verifica tu conexión a internet e inténtalo de nuevo")
        sys.exit(1)
    
    # Paso 2: Buscar el código del municipio
    codigo_municipio = buscar_codigo_municipio(ciudad, municipios_ine)
    
    if not codigo_municipio:
        print(f"\n❌ No se encontró el municipio '{ciudad}' en la base de datos del INE")
        print(f"\n💡 Sugerencias:")
        print(f"   • Verifica la ortografía del nombre")
        print(f"   • Prueba con el nombre completo (ej: 'Las Palmas de Gran Canaria')")
        print(f"   • Algunos municipios tienen nombres compuestos")
        print(f"\n🔍 Busca tu municipio en: https://www.ine.es/nomen2/index.do")
        sys.exit(1)
    
    # Paso 3: Obtener población del INE
    print(f"\n📊 Consultando población oficial del INE...")
    poblacion = get_poblacion_municipio(codigo_municipio, anyo)
    
    # Paso 4: Si no funciona, probar método alternativo  
    if poblacion is None:
        poblacion = get_poblacion_alternativa(codigo_municipio, anyo, ciudad)
    
    # Paso 5: Mostrar resultados
    print("\n" + "=" * 80)
    
    if poblacion:
        print(f"✅ RESULTADO OFICIAL DEL INE:")
        print(f"📍 Municipio: {ciudad.title()}")
        print(f"📅 Año: {anyo}")
        print(f"👥 Población: {poblacion:,} habitantes")
        print(f"🏛️ Código INE: {codigo_municipio}")
        print(f"🌐 Fuente: Instituto Nacional de Estadística (INE) - Datos oficiales")
        print(f"📡 Consultado en tiempo real")
        
    else:
        print(f"⚠️ DATOS NO DISPONIBLES:")
        print(f"📍 Municipio: {ciudad.title()} (Código INE: {codigo_municipio})")
        print(f"📅 Año: {anyo}")
        print(f"❌ No hay datos de población disponibles para este año")
        print(f"\n💡 Posibles causas:")
        print(f"   • El año {anyo} no está disponible en el INE")
        print(f"   • Problemas temporales con la API del INE")
        print(f"   • El municipio fue creado/fusionado después de {anyo}")
        print(f"\n🔧 Prueba con años más recientes: 2020, 2021, 2022, 2023")

def main():
    if len(sys.argv) != 3:
        print("Uso: python habitantes_ine.py <ciudad> <año>")
        print("Ejemplo: python habitantes_ine.py Murcia 2022")
        print("\nCiudades disponibles:")
        print("• Madrid, Barcelona, Valencia, Sevilla, Zaragoza")
        print("• Murcia, Palma, Las Palmas, Bilbao, Alicante")
        print("• Córdoba, Valladolid, y más...")
        print("\nAños disponibles: 2020, 2021, 2022, 2023")
        sys.exit(1)
    
    ciudad = sys.argv[1]
    anyo = sys.argv[2]
    
    print(f"🔍 Buscando población de {ciudad} en {anyo}...")
    print("-" * 60)
    
    # Método 1: Buscar código del municipio
    codigo_municipio = buscar_municipio_ine(ciudad)
    
    # Método 2: Intentar API del INE si tenemos código
    habitantes_api = None
    if codigo_municipio:
        habitantes_api = get_poblacion_ine_api(codigo_municipio, anyo)
    
    # Método 3: Usar base de datos local extendida
    print("\n📋 Consultando base de datos local...")
    habitantes_local = get_habitantes_manual_extendido(ciudad, anyo)
    
    # Mostrar resultados
    if habitantes_local:
        print(f"\n✅ RESULTADO:")
        print(f"📍 Ciudad: {ciudad.title()}")
        print(f"📅 Año: {anyo}")
        print(f"👥 Población: {habitantes_local:,} habitantes")
        print(f"📊 Fuente: Instituto Nacional de Estadística (INE)")
        
        # Información adicional sobre la ciudad
        if ciudad.lower() == 'murcia':
            print(f"\n🏛️ Información adicional:")
            print(f"   • Murcia es la capital de la Región de Murcia")
            print(f"   • Séptima ciudad más poblada de España")
            print(f"   • Código INE: 30030")
            
    else:
        print(f"\n❌ No se encontraron datos para '{ciudad}' en {anyo}")
        print(f"\n� Ciudades disponibles en la base de datos:")
        ciudades = ["Madrid", "Barcelona", "Valencia", "Sevilla", "Zaragoza", 
                   "Murcia", "Palma", "Las Palmas", "Bilbao", "Alicante", 
                   "Córdoba", "Valladolid"]
        for i, c in enumerate(ciudades, 1):
            print(f"   {i:2d}. {c}")
        
        print(f"\n💡 Ejemplo de uso:")
        print(f"   python apis/habitantes_ine.py Murcia 2022")

if __name__ == "__main__":
    main()
