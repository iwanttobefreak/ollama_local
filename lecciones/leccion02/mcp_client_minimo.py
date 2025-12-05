#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
CLIENTE MÍNIMO para probar el servidor MCP
"""
import asyncio
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

async def main():
    print("="*60)
    print("🧪 PRUEBA MÍNIMA DE MCP")
    print("="*60)
    
    # Iniciar servidor
    server_params = StdioServerParameters(
        command="python3",
        args=["mcp_server_minimo.py"],
        env=None
    )
    
    async with stdio_client(server_params) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()
            
            # Listar herramientas
            tools = await session.list_tools()
            print(f"\n✅ Herramientas disponibles: {len(tools.tools)}")
            for tool in tools.tools:
                print(f"   - {tool.name}: {tool.description}")
            
            # Probar la herramienta
            print("\n🔧 Probando herramienta 'saludar'...")
            resultado = await session.call_tool("saludar", {"nombre": "María"})
            print(f"📨 Respuesta: {resultado.content[0].text}")
            
            print("\n✅ Prueba completada con éxito!")

if __name__ == "__main__":
    asyncio.run(main())
