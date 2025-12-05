#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
EJEMPLO MÍNIMO de servidor MCP
Solo devuelve un mensaje simple - sin dependencias externas
"""
import asyncio
from mcp.server import Server, NotificationOptions
from mcp.server.models import InitializationOptions
import mcp.server.stdio
import mcp.types as types

# Crear servidor
server = Server("ejemplo-minimo")

@server.list_tools()
async def handle_list_tools() -> list[types.Tool]:
    """Lista las herramientas disponibles"""
    return [
        types.Tool(
            name="saludar",
            description="Devuelve un saludo personalizado",
            inputSchema={
                "type": "object",
                "properties": {
                    "nombre": {
                        "type": "string",
                        "description": "Nombre de la persona a saludar"
                    }
                },
                "required": ["nombre"]
            }
        )
    ]

@server.call_tool()
async def handle_call_tool(
    name: str, arguments: dict | None
) -> list[types.TextContent]:
    """Ejecuta la herramienta"""
    
    if name != "saludar":
        raise ValueError(f"Herramienta desconocida: {name}")
    
    if not arguments:
        arguments = {}
    
    nombre = arguments.get("nombre", "desconocido")
    
    # Asegurar que nombre es string
    nombre = str(nombre)
    
    return [types.TextContent(
        type="text",
        text=f"¡Hola {nombre}! Bienvenido al servidor MCP."
    )]

async def main():
    """Punto de entrada"""
    async with mcp.server.stdio.stdio_server() as (read_stream, write_stream):
        await server.run(
            read_stream,
            write_stream,
            InitializationOptions(
                server_name="ejemplo-minimo",
                server_version="1.0.0",
                capabilities=server.get_capabilities(
                    notification_options=NotificationOptions(),
                    experimental_capabilities={},
                )
            )
        )

if __name__ == "__main__":
    asyncio.run(main())
