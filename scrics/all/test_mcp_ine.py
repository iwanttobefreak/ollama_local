#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script de prueba para el servidor MCP de consulta de poblacion INE
"""

import asyncio
import json
import sys
from pathlib import Path

# Agregar el directorio apis al path
sys.path.insert(0, str(Path(__file__).parent))

from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client


async def test_mcp_server():
    """
    Prueba el servidor MCP de consulta de poblacion
    """
    print("=" * 70)
    print("PRUEBA DEL SERVIDOR MCP - CONSULTA POBLACION INE")
    print("=" * 70)
    print()
    
    # Configurar parametros del servidor
    server_params = StdioServerParameters(
        command="python",
        args=[str(Path(__file__).parent / "mcp_ine_server.py")],
        env=None
    )
    
    print("[1/4] Iniciando servidor MCP...")
    
    try:
        async with stdio_client(server_params) as (read, write):
            async with ClientSession(read, write) as session:
                print("[OK] Servidor iniciado")
                print()
                
                # Inicializar sesion
                print("[2/4] Inicializando sesion...")
                await session.initialize()
                print("[OK] Sesion inicializada")
                print()
                
                # Listar herramientas disponibles
                print("[3/4] Listando herramientas...")
                tools_response = await session.list_tools()
                tools = tools_response.tools
                
                print(f"[OK] {len(tools)} herramienta(s) disponible(s):")
                for tool in tools:
                    print(f"  - {tool.name}")
                    print(f"    Descripcion: {tool.description[:80]}...")
                print()
                
                # Probar la herramienta con varios ejemplos
                print("[4/4] Probando herramienta...")
                print()
                
                tests = [
                    {"lugar": "Madrid", "año": 2021},
                    {"lugar": "Barcelona", "año": 2020},
                    {"lugar": "Murcia", "año": 2019},
                ]
                
                for i, test_args in enumerate(tests, 1):
                    print(f"--- Prueba {i}/3: {test_args['lugar']} ({test_args['año']}) ---")
                    
                    try:
                        result = await session.call_tool(
                            "consultar_poblacion_ine",
                            test_args
                        )
                        
                        if result.content:
                            print(result.content[0].text)
                        else:
                            print("[WARN] Sin contenido en la respuesta")
                        
                    except Exception as e:
                        print(f"[ERROR] {e}")
                    
                    print()
                
                print("=" * 70)
                print("[OK] PRUEBAS COMPLETADAS")
                print("=" * 70)
                
    except Exception as e:
        print(f"[ERROR] Error al ejecutar el servidor MCP: {e}")
        import traceback
        traceback.print_exc()


async def test_direct_function():
    """
    Prueba la funcion de consulta directamente (sin MCP)
    """
    print("=" * 70)
    print("PRUEBA DIRECTA DE LA FUNCION (SIN MCP)")
    print("=" * 70)
    print()
    
    # Importar la funcion
    from mcp_ine_server import obtener_poblacion_ine
    
    tests = [
        ("Madrid", 2021),
        ("Barcelona", 2020),
        ("Sevilla", 2019),
    ]
    
    for lugar, año in tests:
        print(f"Consultando: {lugar} - {año}")
        resultado, error = obtener_poblacion_ine(lugar, año)
        
        if error:
            print(f"[ERROR] {error}")
        elif resultado:
            print(f"[OK] {resultado['poblacion_formato']} habitantes")
        else:
            print("[WARN] Sin resultado")
        
        print()
    
    print("=" * 70)


def main():
    """
    Funcion principal
    """
    import sys
    
    if len(sys.argv) > 1 and sys.argv[1] == "--direct":
        # Prueba directa
        asyncio.run(test_direct_function())
    else:
        # Prueba del servidor MCP
        asyncio.run(test_mcp_server())


if __name__ == "__main__":
    main()
