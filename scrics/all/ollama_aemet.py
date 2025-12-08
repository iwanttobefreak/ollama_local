#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Tool de Temperatura AEMET para Ollama
Usa la API oficial de AEMET (Agencia Estatal de Meteorología)
"""

import requests
import ollama
from datetime import datetime, timedelta


# Configuración AEMET
AEMET_API_KEY = "eyJhbGciOiJIUzI1NiJ9.eyJzdWIiOiJqb3NlQGxlZ2lkby5jb20iLCJqdGkiOiI3MzdhNWZlYy02ZTMyLTRlNmUtOTkwMy1mMGI5ZjQ0ZTliYWUiLCJpc3MiOiJBRU1FVCIsImlhdCI6MTY5MzI1MDM4NSwidXNlcklkIjoiNzM3YTVmZWMtNmUzMi00ZTZlLTk5MDMtZjBiOWY0NGU5YmFlIiwicm9sZSI6IiJ9.2PoU7S76ioZokGu51DYy8rsiaCe8U-dtORnpG60ahIA"  # Reemplazar con tu API key de https://opendata.aemet.es

# Códigos de municipios principales
MUNICIPIOS_AEMET = {
    'madrid': '28079',
    'barcelona': '08019',
    'valencia': '46250',
    'sevilla': '41091',
    'zaragoza': '50297',
    'málaga': '29067',
    'murcia': '30030',
    'palma': '07040',
    'las palmas': '35016',
    'bilbao': '48020',
    'alicante': '03014',
    'córdoba': '14021',
    'valladolid': '47186',
    'vigo': '36057',
    'gijón': '33024',
    'hospitalet': '08101',
    'vitoria': '01059',
    'granada': '18087',
    'elche': '03065',
    'oviedo': '33044',
    'badalona': '08015',
    'cartagena': '30016',
    'terrassa': '08279',
    'jerez': '11020',
    'sabadell': '08187',
    'móstoles': '28092',
    'santa cruz': '38038',
    'pamplona': '31201',
    'almería': '04013',
    'alcalá': '28006',
    'fuenlabrada': '28058',
    'leganés': '28074',
    'san sebastián': '20069',
    'santander': '39075',
    'burgos': '09059',
    'castellón': '12040',
    'albacete': '02003',
    'alcorcón': '28007',
    'getafe': '28065',
    'salamanca': '37274',
    'logroño': '26089',
    'badajoz': '06015',
    'huelva': '21041',
    'tarragona': '43148',
    'león': '24089',
    'lleida': '25120',
    'cádiz': '11012',
    'jaén': '23050',
    'ourense': '32054',
    'toledo': '45168',
    'mataró': '08121',
    'alcobendas': '28006'
}


def normalizar_ciudad(ciudad):
    """Normaliza nombre de ciudad para búsqueda"""
    ciudad_norm = ciudad.lower().strip()
    # Quitar acentos comunes
    reemplazos = {
        'á': 'a', 'é': 'e', 'í': 'i', 'ó': 'o', 'ú': 'u',
        'ñ': 'n'
    }
    for old, new in reemplazos.items():
        ciudad_norm = ciudad_norm.replace(old, new)
    return ciudad_norm


def obtener_codigo_municipio(ciudad):
    """Busca código de municipio AEMET"""
    ciudad_norm = normalizar_ciudad(ciudad)
    
    # Búsqueda exacta
    if ciudad_norm in MUNICIPIOS_AEMET:
        return MUNICIPIOS_AEMET[ciudad_norm]
    
    # Búsqueda parcial
    for nombre, codigo in MUNICIPIOS_AEMET.items():
        if ciudad_norm in nombre or nombre in ciudad_norm:
            return codigo
    
    return None


def obtener_pronostico_temperatura(ciudad: str, dias: int = 3) -> str:
    """
    Obtiene pronóstico de temperatura usando AEMET
    
    Args:
        ciudad: Nombre de la ciudad española
        dias: Días de pronóstico (1-7, AEMET da máximo 7 días)
    
    Returns:
        String con el pronóstico formateado
    """
    try:
        # IMPORTANTE: Convertir dias a int si viene como string
        if isinstance(dias, str):
            dias = int(dias)
        
        print(f"[FUNC DEBUG] Buscando temperatura para: {ciudad}, {dias} días")
        
        if dias < 1 or dias > 7:
            return "Error: AEMET solo proporciona pronóstico para 1-7 días"
        
        # Buscar código de municipio
        codigo = obtener_codigo_municipio(ciudad)
        if not codigo:
            ciudades_disponibles = ', '.join(sorted(set(MUNICIPIOS_AEMET.keys())))
            return f"Ciudad '{ciudad}' no encontrada. Ciudades disponibles: {ciudades_disponibles}"
        
        print(f"[FUNC DEBUG] Código municipio: {codigo}")
        
        # Llamar a AEMET API
        url = f"https://opendata.aemet.es/opendata/api/prediccion/especifica/municipio/diaria/{codigo}"
        headers = {'api_key': AEMET_API_KEY}
        
        print(f"[FUNC DEBUG] Llamando a AEMET API...")
        response = requests.get(url, headers=headers, timeout=10)
        print(f"[FUNC DEBUG] Status code: {response.status_code}")
        
        if response.status_code == 401:
            return "Error: API_KEY de AEMET inválida. Obtén una en https://opendata.aemet.es"
        
        if response.status_code == 429:
            return "Error: Límite de peticiones AEMET excedido. Espera unos minutos."
        
        if response.status_code != 200:
            return f"Error al conectar con AEMET: HTTP {response.status_code}"
        
        data = response.json()
        if data.get('estado') != 200:
            return f"Error AEMET: {data.get('descripcion', 'Desconocido')}"
        
        # Obtener datos reales
        datos_url = data.get('datos')
        print(f"[FUNC DEBUG] Obteniendo datos del pronóstico...")
        datos_response = requests.get(datos_url, timeout=10)
        
        if datos_response.status_code != 200:
            return f"Error al obtener datos: HTTP {datos_response.status_code}"
        
        pronostico = datos_response.json()
        
        # Extraer información
        prediccion = pronostico[0].get('prediccion', {})
        dia_datos = prediccion.get('dia', [])
        nombre_municipio = pronostico[0].get('nombre', ciudad.title())
        
        print(f"[FUNC DEBUG] Procesando {len(dia_datos)} días de pronóstico")
        
        # Formatear resultado
        dias_sem = ['Lunes', 'Martes', 'Miércoles', 'Jueves', 'Viernes', 'Sábado', 'Domingo']
        resultado = []
        
        for i, dia in enumerate(dia_datos[:dias]):
            fecha_str = dia.get('fecha', '')
            fecha = datetime.strptime(fecha_str, '%Y-%m-%dT%H:%M:%S')
            dia_semana = dias_sem[fecha.weekday()]
            
            # Temperaturas
            temp_max_data = dia.get('temperatura', {}).get('maxima', [])
            temp_min_data = dia.get('temperatura', {}).get('minima', [])
            
            temp_max = temp_max_data[0] if isinstance(temp_max_data, list) and temp_max_data else temp_max_data if isinstance(temp_max_data, (int, float)) else 'N/D'
            temp_min = temp_min_data[0] if isinstance(temp_min_data, list) and temp_min_data else temp_min_data if isinstance(temp_min_data, (int, float)) else 'N/D'
            
            # Probabilidad de lluvia
            prob_precipitacion = dia.get('probPrecipitacion', [])
            if isinstance(prob_precipitacion, list) and prob_precipitacion:
                lluvia = prob_precipitacion[0].get('value', 0)
            else:
                lluvia = 0
            
            # Estado del cielo
            estado_cielo = dia.get('estadoCielo', [])
            if isinstance(estado_cielo, list) and estado_cielo:
                descripcion = estado_cielo[0].get('descripcion', 'Variable')
            else:
                descripcion = 'Variable'
            
            # Viento
            viento_data = dia.get('viento', [])
            if isinstance(viento_data, list) and viento_data:
                velocidad_viento = viento_data[0].get('velocidad', [0])[0] if viento_data[0].get('velocidad') else 0
            else:
                velocidad_viento = 0
            
            # Etiqueta del día
            hoy = datetime.now().date()
            if fecha.date() == hoy:
                etiqueta = "HOY"
            elif (fecha.date() - hoy).days == 1:
                etiqueta = "MAÑANA"
            else:
                etiqueta = fecha.strftime('%d/%m')
            
            resultado.append(
                f"{etiqueta} ({dia_semana}): {temp_min}-{temp_max}°C, {descripcion}, "
                f"lluvia {lluvia}%, viento {velocidad_viento} km/h"
            )
        
        resultado_final = f"Pronóstico AEMET para {nombre_municipio}:\n" + "\n".join(resultado)
        print(f"[FUNC DEBUG] Éxito! Devolviendo pronóstico")
        return resultado_final
        
    except Exception as e:
        error_msg = f"Error: {str(e)}"
        print(f"[FUNC DEBUG ERROR] {error_msg}")
        import traceback
        traceback.print_exc()
        return error_msg


# Tool definition para Ollama
TOOL_DEFINITION = {
    'type': 'function',
    'function': {
        'name': 'obtener_pronostico_temperatura',
        'description': 'SOLO usar cuando el usuario pregunta específicamente por el TIEMPO, CLIMA, TEMPERATURA, LLUVIA o PRONÓSTICO meteorológico de una ciudad ESPAÑOLA. NO usar para otras preguntas generales.',
        'parameters': {
            'type': 'object',
            'properties': {
                'ciudad': {
                    'type': 'string',
                    'description': 'Nombre de la ciudad española (Madrid, Barcelona, Valencia, Sevilla, etc.)'
                },
                'dias': {
                    'type': 'integer',
                    'description': 'Días de pronóstico (1-7). AEMET proporciona máximo 7 días. Default: 3',
                    'default': 3,
                    'minimum': 1,
                    'maximum': 7
                }
            },
            'required': ['ciudad']
        }
    }
}


def main():
    """Chat con Ollama estilo 'ollama run'"""
    available_functions = {
        'obtener_pronostico_temperatura': obtener_pronostico_temperatura
    }
    
    # Palabras clave que indican pregunta sobre clima
    CLIMA_KEYWORDS = [
        'temperatura', 'tiempo', 'clima', 'lluvia', 'viento', 
        'pronostico', 'pronóstico', 'calor', 'frio', 'frío',
        'grados', 'soleado', 'nublado', 'despejado', 'meteorolog',
        'semana', 'hoy', 'mañana', 'hará', 'estará'
    ]
    
    # System prompt para que Ollama use los resultados de las tools
    messages = [
        {
            'role': 'system',
            'content': '''Eres un asistente útil con acceso a herramientas meteorológicas para España.

IMPORTANTE:
- Cuando uses herramientas, SIEMPRE presenta los resultados obtenidos de forma clara
- NO digas "no tengo acceso a información" si ya obtuviste datos de herramientas
- Si te preguntan por VARIAS ciudades, usa la herramienta VARIAS VECES (una por ciudad)
- Para comparaciones (ej: "¿dónde hará más calor, en X o Y?"), llama a la herramienta para CADA ciudad y luego compara los resultados'''
        }
    ]
    
    while True:
        try:
            user_input = input(">>> ").strip()
        except (EOFError, KeyboardInterrupt):
            print()
            break
        
        if not user_input:
            continue
        
        # Comandos
        if user_input in ['/bye', '/exit', '/quit']:
            break
        if user_input == '/clear':
            messages = [
                {
                    'role': 'system',
                    'content': '''Eres un asistente útil con acceso a herramientas meteorológicas para España.

IMPORTANTE:
- Cuando uses herramientas, SIEMPRE presenta los resultados obtenidos de forma clara
- NO digas "no tengo acceso a información" si ya obtuviste datos de herramientas
- Si te preguntan por VARIAS ciudades, usa la herramienta VARIAS VECES (una por ciudad)
- Para comparaciones (ej: "¿dónde hará más calor, en X o Y?"), llama a la herramienta para CADA ciudad y luego compara los resultados'''
                }
            ]
            continue
        if user_input == '/help':
            print("Comandos: /bye (salir), /clear (limpiar), /help (ayuda)")
            continue
        
        # Agregar mensaje del usuario
        messages.append({'role': 'user', 'content': user_input})
        
        # Detectar si es pregunta sobre clima
        es_pregunta_clima = any(keyword in user_input.lower() for keyword in CLIMA_KEYWORDS)
        
        # Llamar a Ollama con tools SOLO si es pregunta de clima
        try:
            if es_pregunta_clima:
                response = ollama.chat(
                    model='llama3.1:8b',
                    messages=messages,
                    tools=[TOOL_DEFINITION]
                )
            else:
                # Sin tools para preguntas generales
                response = ollama.chat(
                    model='llama3.1:8b',
                    messages=messages
                )
            
        except Exception as e:
            print(f"Error al conectar con Ollama: {e}")
            print("¿Está Ollama corriendo? (ollama serve)")
            messages.pop()
            continue
        
        messages.append(response['message'])
        
        # Si usa tools - PUEDE SER MÚLTIPLES VECES
        if response['message'].get('tool_calls'):
            print(f"[DEBUG] Ollama llamó a la tool {len(response['message']['tool_calls'])} vez/veces!")
            
            for tool_call in response['message']['tool_calls']:
                func_name = tool_call['function']['name']
                func_args = tool_call['function']['arguments']
                
                print(f"[DEBUG] Función: {func_name}")
                print(f"[DEBUG] Argumentos: {func_args}")
                
                if func_name in available_functions:
                    # Ejecutar función
                    func_result = available_functions[func_name](**func_args)
                    
                    print(f"[DEBUG] Resultado: {func_result[:150]}...")
                    
                    # Agregar resultado
                    messages.append({
                        'role': 'tool',
                        'content': func_result
                    })
            
            # Segunda llamada a Ollama para procesar TODOS los resultados
            try:
                final_response = ollama.chat(
                    model='llama3.1:8b',
                    messages=messages,
                    options={
                        'temperature': 0.3
                    }
                )
                print(final_response['message']['content'])
                print()
                messages.append(final_response['message'])
            except Exception as e:
                print(f"Error en respuesta final: {e}")
        else:
            # Respuesta directa
            print(response['message']['content'])
            print()


if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1 and sys.argv[1] == "--test":
        print("TEST - Función de temperatura AEMET\n")
        print(obtener_pronostico_temperatura("Madrid", 3))
    else:
        print("Escribe /bye para salir, /help para ayuda")
        print("Usando API AEMET oficial de España")
        main()
