#!/usr/bin/env python3
import asyncio
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

async def main():
    print("🧪 PRUEBA MÍNIMA DE MCP\n")
    
    server_params = StdioServerParameters(command="python3", args=["mcp_server_minimo.py"])
    
    async with stdio_client(server_params) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()
            
            tools = await session.list_tools()
            print(f"✅ Herramientas: {tools.tools[0].name}")
            
            resultado = await session.call_tool("saludar", {"nombre": "María"})
            print(f"📨 Respuesta: {resultado.content[0].text}")

if __name__ == "__main__":
    asyncio.run(main())
