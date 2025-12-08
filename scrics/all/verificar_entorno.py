#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script de verificación del entorno
Verifica que todas las dependencias estén instaladas
"""

import sys
import subprocess
import os


def check_python():
    """Verifica versión de Python"""
    version = sys.version_info
    print(f"✓ Python {version.major}.{version.minor}.{version.micro}")
    if version.major < 3 or (version.major == 3 and version.minor < 8):
        print("  ⚠️  Se recomienda Python 3.8+")
    return True


def check_package(package_name):
    """Verifica si un paquete está instalado"""
    try:
        __import__(package_name)
        print(f"✓ {package_name} instalado")
        return True
    except ImportError:
        print(f"✗ {package_name} NO instalado")
        print(f"  → Instalar: pip3 install {package_name}")
        return False


def check_git():
    """Verifica que Git esté instalado"""
    try:
        result = subprocess.run(
            ['git', '--version'],
            capture_output=True,
            text=True,
            timeout=5
        )
        if result.returncode == 0:
            version = result.stdout.strip()
            print(f"✓ {version}")
            return True
        else:
            print("✗ Git instalado pero no responde")
            return False
    except FileNotFoundError:
        print("✗ Git NO instalado")
        print("  → Ubuntu/Debian: sudo apt-get install -y git")
        print("  → CentOS/RHEL: sudo yum install -y git")
        print("  → Alpine: apk add git")
        return False
    except Exception as e:
        print(f"✗ Error al verificar Git: {e}")
        return False


def check_ollama():
    """Verifica que Ollama esté corriendo"""
    try:
        result = subprocess.run(
            ['ollama', 'list'],
            capture_output=True,
            text=True,
            timeout=10
        )
        if result.returncode == 0:
            print("✓ Ollama corriendo")
            # Mostrar modelos disponibles
            models = [line.split()[0] for line in result.stdout.strip().split('\n')[1:] if line.strip()]
            if models:
                print(f"  Modelos: {', '.join(models[:3])}")
            return True
        else:
            print("✗ Ollama instalado pero no responde")
            print("  → Iniciar: ollama serve")
            return False
    except FileNotFoundError:
        print("✗ Ollama NO instalado")
        print("  → Instalar: curl -fsSL https://ollama.com/install.sh | sh")
        return False
    except Exception as e:
        print(f"✗ Error al verificar Ollama: {e}")
        return False


def check_files():
    """Verifica que los archivos necesarios existan"""
    files_to_check = [
        'ollama_multi_tools.py',
        'tools/temperatura.py',
        'tools/git_clone.py',
        'tools/__init__.py'
    ]
    
    all_ok = True
    for file in files_to_check:
        if os.path.exists(file):
            size = os.path.getsize(file)
            print(f"✓ {file} ({size} bytes)")
        else:
            print(f"✗ {file} NO encontrado")
            all_ok = False
    
    return all_ok


def main():
    print("="*60)
    print("Verificación del entorno Ollama Multi-Tools")
    print("="*60)
    
    checks = {
        'Python': check_python(),
        'Paquete requests': check_package('requests'),
        'Paquete ollama': check_package('ollama'),
        'Git': check_git(),
        'Ollama': check_ollama(),
        'Archivos': check_files()
    }
    
    print("\n" + "="*60)
    print("RESUMEN")
    print("="*60)
    
    total = len(checks)
    passed = sum(checks.values())
    
    for name, status in checks.items():
        symbol = "✓" if status else "✗"
        print(f"{symbol} {name}")
    
    print(f"\nResultado: {passed}/{total} checks pasados")
    
    if passed == total:
        print("\n🎉 ¡Todo listo! Puedes ejecutar:")
        print("   python3 ollama_multi_tools.py")
    else:
        print("\n⚠️  Faltan dependencias. Revisa los errores arriba.")
        print("\nInstalación rápida de paquetes Python:")
        print("   pip3 install requests ollama")
    
    print("="*60)


if __name__ == "__main__":
    main()
