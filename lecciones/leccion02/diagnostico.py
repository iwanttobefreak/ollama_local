#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script de diagnóstico para verificar que todo funciona
"""
import os
import sys
import subprocess

print("="*60)
print("🔍 DIAGNÓSTICO - Lección 2 MCP")
print("="*60)
print()

# 1. Verificar Python
print("1️⃣ Verificando Python...")
print(f"   Python ejecutable: {sys.executable}")
print(f"   Python versión: {sys.version}")
print()

# 2. Verificar ubicación actual
print("2️⃣ Verificando ubicación...")
print(f"   Directorio actual: {os.getcwd()}")
print(f"   Este script está en: {os.path.dirname(__file__)}")
print()

# 3. Verificar estructura de directorios
print("3️⃣ Verificando estructura de directorios...")
leccion01_dir = os.path.join(os.path.dirname(__file__), "..", "leccion01")
script_temp = os.path.join(leccion01_dir, "script_pronostico_temperatura.py")

print(f"   Ruta leccion01: {os.path.abspath(leccion01_dir)}")
print(f"   ¿Existe leccion01? {os.path.exists(leccion01_dir)}")
print(f"   Ruta script temperatura: {os.path.abspath(script_temp)}")
print(f"   ¿Existe script? {os.path.exists(script_temp)}")

if os.path.exists(leccion01_dir):
    print(f"   Contenido de leccion01:")
    for item in os.listdir(leccion01_dir):
        print(f"      - {item}")
print()

# 4. Verificar dependencias
print("4️⃣ Verificando dependencias Python...")
dependencias = ['mcp', 'ollama', 'requests', 'aiohttp']
for dep in dependencias:
    try:
        __import__(dep)
        print(f"   ✅ {dep}")
    except ImportError:
        print(f"   ❌ {dep} (no instalado)")
print()

# 5. Probar ejecución del script de temperatura
print("5️⃣ Probando script de temperatura...")
if os.path.exists(script_temp):
    print(f"   Ejecutando: python {script_temp} Madrid 1")
    
    # Detectar comando Python
    python_cmd = 'python3'
    try:
        subprocess.run(['python3', '--version'], capture_output=True, check=True)
    except (subprocess.CalledProcessError, FileNotFoundError):
        python_cmd = 'python'
    
    try:
        resultado = subprocess.run(
            [python_cmd, script_temp, 'Madrid', '1'],
            capture_output=True,
            text=True,
            timeout=30,
            cwd=leccion01_dir
        )
        
        print(f"   Código de salida: {resultado.returncode}")
        
        if resultado.returncode == 0:
            print("   ✅ Script ejecutado correctamente")
            print("\n   📊 Primeras líneas de la salida:")
            lines = resultado.stdout.split('\n')[:10]
            for line in lines:
                print(f"   {line}")
        else:
            print("   ❌ Error al ejecutar script")
            print(f"\n   STDERR:")
            print(resultado.stderr)
            if resultado.stdout:
                print(f"\n   STDOUT:")
                print(resultado.stdout)
    except Exception as e:
        print(f"   ❌ Excepción: {str(e)}")
else:
    print(f"   ❌ Script no encontrado en {script_temp}")
print()

# 6. Verificar Ollama
print("6️⃣ Verificando Ollama...")
try:
    import ollama
    print("   ✅ Librería ollama instalada")
    try:
        # Intentar listar modelos
        models = ollama.list()
        print(f"   ✅ Conectado a Ollama")
        print(f"   Modelos disponibles: {len(models.get('models', []))}")
        for model in models.get('models', [])[:3]:
            print(f"      - {model.get('name', 'unknown')}")
    except Exception as e:
        print(f"   ⚠️  No se pudo conectar a Ollama: {str(e)}")
        print("   Asegúrate de que Ollama esté corriendo")
except ImportError:
    print("   ❌ Librería ollama no instalada")
print()

print("="*60)
print("✅ Diagnóstico completado")
print("="*60)
print()
print("💡 Siguientes pasos:")
print("   1. Si faltan dependencias: pip install -r requirements.txt")
print("   2. Si no encuentra el script: verifica que estés en leccion02/")
print("   3. Si Ollama no conecta: verifica que esté corriendo")
print()
