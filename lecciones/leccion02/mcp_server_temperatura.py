#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Servidor MCP simple para consultar temperatura
Usa el script de la Lección 1 para obtener datos reales
"""
import asyncio
import subprocess
import os
from mcp.server import Server, NotificationOptions
from mcp.server.models import InitializationOptions
import mcp.server.stdio
import mcp.types as types

# Crear el servidor MCP
server = Server("temperatura-server")

@server.list_tools()
async def handle_list_tools() -> list[types.Tool]:
    """
    Lista las herramientas disponibles en este servidor MCP
    """
    return [
        types.Tool(
            name="obtener_temperatura",
            description="Obtiene el pronóstico de temperatura para ciudades españolas. Usa datos reales de Open-Meteo.",
            inputSchema={
                "type": "object",
                "properties": {
                    "ciudad": {
                        "type": "string",
                        "description": "Nombre de la ciudad española (ej: Madrid, Barcelona, Sevilla)"
                    },
                    "dias": {
                        "type": "integer",
                        "description": "Número de días de pronóstico (1-16). Por defecto: 3",
                        "default": 3,
                        "minimum": 1,
                        "maximum": 16
                    }
                },
                "required": ["ciudad"]
            }
        )
    ]

@server.call_tool()
async def handle_call_tool(
    name: str, arguments: dict | None
) -> list[types.TextContent]:
    """
    Ejecuta la herramienta solicitada por el cliente
    """
    
    if name != "obtener_temperatura":
        raise ValueError(f"Herramienta desconocida: {name}")
    
    if not arguments:
        raise ValueError("Se requieren argumentos para esta herramienta")
    
    ciudad = arguments.get("ciudad")
    dias = arguments.get("dias", 3)
    
    # Asegurar que dias es un entero
    try:
        dias = int(dias)
    except (ValueError, TypeError):
        dias = 3
    
    # Validar rango de días
    if dias < 1:
        dias = 1
    elif dias > 16:
        dias = 16
    
    if not ciudad:
        raise ValueError("El parámetro 'ciudad' es obligatorio")
    
    # Ruta al script de la lección 1
    script_dir = os.path.join(os.path.dirname(__file__), "..", "leccion01")
    script_path = os.path.join(script_dir, "script_pronostico_temperatura.py")
    
    # Verificar que el script existe
    if not os.path.exists(script_path):
        return [types.TextContent(
            type="text",
            text=f"Error: No se encuentra el script en {script_path}"
        )]
    
    # Detectar el comando Python correcto (python3 o python)
    python_cmd = 'python3'
    try:
        subprocess.run(['python3', '--version'], capture_output=True, check=True)
    except (subprocess.CalledProcessError, FileNotFoundError):
        python_cmd = 'python'
    
    # Ejecutar el script de temperatura
    try:
        resultado = subprocess.run(
            [python_cmd, script_path, ciudad, str(dias)],
            capture_output=True,
            text=True,
            timeout=30,
            cwd=script_dir  # Ejecutar desde el directorio del script
        )
        
        if resultado.returncode == 0:
            return [types.TextContent(
                type="text",
                text=resultado.stdout
            )]
        else:
            error_msg = resultado.stderr if resultado.stderr else "Error desconocido"
            # Incluir también stdout por si hay información útil
            full_error = f"STDERR: {error_msg}"
            if resultado.stdout:
                full_error += f"\nSTDOUT: {resultado.stdout}"
            return [types.TextContent(
                type="text",
                text=f"Error al obtener temperatura:\n{full_error}"
            )]
    except subprocess.TimeoutExpired:
        return [types.TextContent(
            type="text",
            text="Error: La consulta tardó demasiado tiempo (timeout)"
        )]
    except Exception as e:
        return [types.TextContent(
            type="text",
            text=f"Error ejecutando script: {str(e)}\nRuta script: {script_path}"
        )]

async def main():
    """
    Punto de entrada del servidor MCP
    Inicia el servidor y espera conexiones
    """
    async with mcp.server.stdio.stdio_server() as (read_stream, write_stream):
        await server.run(
            read_stream,
            write_stream,
            InitializationOptions(
                server_name="temperatura-server",
                server_version="1.0.0",
                capabilities=server.get_capabilities(
                    notification_options=NotificationOptions(),
                    experimental_capabilities={},
                )
            )
        )

if __name__ == "__main__":
    asyncio.run(main())
