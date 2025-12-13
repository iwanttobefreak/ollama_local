#!/usr/bin/env python3
import asyncio
from mcp.server import Server, NotificationOptions
from mcp.server.models import InitializationOptions
import mcp.server.stdio
import mcp.types as types

server = Server("ejemplo-minimo")

@server.list_tools()
async def handle_list_tools() -> list[types.Tool]:
    return [
        types.Tool(
            name="saludar",
            description="Devuelve un saludo personalizado",
            inputSchema={
                "type": "object",
                "properties": {
                    "nombre": {"type": "string", "description": "Nombre de la persona"}
                },
                "required": ["nombre"]
            }
        )
    ]

@server.call_tool()
async def handle_call_tool(name: str, arguments: dict | None) -> list[types.TextContent]:
    if name != "saludar":
        raise ValueError(f"Herramienta desconocida: {name}")
    nombre = arguments.get("nombre", "desconocido")
    return [types.TextContent(type="text", text=f"¡Hola {nombre}! Bienvenido al servidor MCP.")]

async def main():
    async with mcp.server.stdio.stdio_server() as (read_stream, write_stream):
        await server.run(read_stream, write_stream, 
            InitializationOptions(server_name="ejemplo-minimo", server_version="1.0.0",
                capabilities=server.get_capabilities(notification_options=NotificationOptions(), 
                    experimental_capabilities={})))

if __name__ == "__main__":
    asyncio.run(main())
