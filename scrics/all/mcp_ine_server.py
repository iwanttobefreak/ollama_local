#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Servidor MCP para consultar poblacion del INE
Expone la funcionalidad de consulta de poblacion como herramienta para Ollama
"""

import asyncio
import json
import requests
from mcp.server import Server
from mcp.server.stdio import stdio_server
from mcp.types import Tool, TextContent


# Funcion para obtener poblacion (copiada de ine_poblacion.py)
def obtener_poblacion_ine(nombre_lugar, año):
    """
    Consulta la poblacion de una provincia o municipio principal en el INE
    """
    try:
        # API del INE - Tabla 2852: Poblacion por municipios
        url = "https://servicios.ine.es/wstempus/js/ES/DATOS_TABLA/2852?tip=AM&"
        
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)',
            'Accept': 'application/json'
        }
        
        response = requests.get(url, headers=headers, timeout=30)
        
        if response.status_code != 200:
            return None, f"Error HTTP: {response.status_code}"
        
        # Parsear JSON
        datos = response.json()
        
        # Buscar por nombre
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
                        nombre_completo = registro.get('Nombre', nombre_lugar)
                        
                        resultado = {
                            'lugar': nombre_completo,
                            'codigo_ine': cod_ine,
                            'año': año,
                            'poblacion': poblacion,
                            'poblacion_formato': f"{poblacion:,}",
                            'fuente': 'INE - www.ine.es'
                        }
                        
                        return resultado, None
                
                # Si se encontro el registro pero no el año
                años_disponibles = sorted(set([
                    d.get('Anyo') for d in datos_registro 
                    if isinstance(d, dict) and d.get('Anyo')
                ]))
                
                return None, f"Se encontro '{nombre_lugar}' pero no tiene datos para {año}. Años disponibles: {años_disponibles[0]} - {años_disponibles[-1]}"
        
        return None, f"No se encontro '{nombre_lugar}' en la API del INE. Esta API incluye provincias y capitales principales."
        
    except Exception as e:
        return None, f"Error: {str(e)}"


# Crear servidor MCP
app = Server("ine-poblacion-server")


@app.list_tools()
async def list_tools() -> list[Tool]:
    """
    Lista las herramientas disponibles
    """
    return [
        Tool(
            name="consultar_poblacion_ine",
            description="Consulta la poblacion de una provincia o municipio principal de España en el Instituto Nacional de Estadistica (INE). Obtiene datos oficiales en tiempo real desde www.ine.es. Funciona con provincias y capitales de provincia. Datos disponibles desde 1996 hasta 2021.",
            inputSchema={
                "type": "object",
                "properties": {
                    "lugar": {
                        "type": "string",
                        "description": "Nombre de la provincia o municipio a consultar (ej: Madrid, Barcelona, Murcia, Salamanca)"
                    },
                    "año": {
                        "type": "integer",
                        "description": "Año para el que se consulta la poblacion (entre 1996 y 2021)",
                        "minimum": 1996,
                        "maximum": 2021
                    }
                },
                "required": ["lugar", "año"]
            }
        )
    ]


@app.call_tool()
async def call_tool(name: str, arguments: dict) -> list[TextContent]:
    """
    Ejecuta la herramienta solicitada
    """
    if name != "consultar_poblacion_ine":
        raise ValueError(f"Herramienta desconocida: {name}")
    
    # Validar argumentos
    lugar = arguments.get("lugar")
    año = arguments.get("año")
    
    if not lugar:
        return [TextContent(
            type="text",
            text="Error: Falta el parametro 'lugar'"
        )]
    
    if not año:
        return [TextContent(
            type="text",
            text="Error: Falta el parametro 'año'"
        )]
    
    try:
        año = int(año)
    except (ValueError, TypeError):
        return [TextContent(
            type="text",
            text=f"Error: El año debe ser un numero entero (recibido: {año})"
        )]
    
    # Validar rango de año
    if año < 1996 or año > 2021:
        return [TextContent(
            type="text",
            text=f"Advertencia: El año {año} esta fuera del rango habitual (1996-2021). Intentando consulta..."
        )]
    
    # Realizar consulta
    resultado, error = obtener_poblacion_ine(lugar, año)
    
    if error:
        return [TextContent(
            type="text",
            text=f"No se pudo obtener la poblacion:\n{error}\n\nSugerencias:\n- Verifica que el nombre sea correcto\n- Prueba con el nombre de la provincia\n- Usa años entre 1996 y 2021"
        )]
    
    if resultado:
        respuesta = f"""Poblacion obtenida del INE:

Lugar: {resultado['lugar']}
Codigo INE: {resultado['codigo_ine']}
Año: {resultado['año']}
Poblacion: {resultado['poblacion_formato']} habitantes

Fuente: {resultado['fuente']}
Tabla: 2852 - Poblacion por municipios"""
        
        return [TextContent(
            type="text",
            text=respuesta
        )]
    
    return [TextContent(
        type="text",
        text="Error desconocido al consultar la poblacion"
    )]


async def main():
    """
    Inicia el servidor MCP
    """
    async with stdio_server() as (read_stream, write_stream):
        await app.run(
            read_stream,
            write_stream,
            app.create_initialization_options()
        )


if __name__ == "__main__":
    asyncio.run(main())
