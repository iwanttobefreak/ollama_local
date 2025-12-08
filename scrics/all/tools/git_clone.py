#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Tool: Git Clone
Clona repositorios de GitHub/GitLab/etc.
"""

import subprocess
import os
import re


def clonar_repositorio_git(url: str, directorio: str = None) -> str:
    """
    Clona un repositorio de Git
    
    Args:
        url: URL del repositorio (https://github.com/user/repo.git o https://github.com/user/repo)
        directorio: Directorio destino (opcional, usa nombre del repo por defecto)
    
    Returns:
        String con el resultado de la operación
    """
    try:
        print(f"[GIT TOOL] Clonando repositorio: {url}")
        
        # Validar URL de Git - VERSIÓN MEJORADA
        # Acepta URLs con o sin .git, con o sin / final
        url = url.rstrip('/')  # Quitar / final si existe
        
        # Patrones válidos:
        # https://github.com/user/repo
        # https://github.com/user/repo.git
        # git@github.com:user/repo.git
        # https://gitlab.com/user/repo
        git_pattern = r'^(https?://|git@)[\w\-\.]+[:/][\w\-\./]+'
        
        if not re.match(git_pattern, url, re.IGNORECASE):
            return f"Error: URL inválida. Debe ser una URL de Git válida.\nEjemplo: https://github.com/usuario/repositorio"
        
        # Comando git clone
        cmd = ['git', 'clone', url]
        
        # Si se especifica directorio destino
        if directorio and directorio not in ['/path/donde/quieres/clonarlo', 'None', 'none']:
            cmd.append(directorio)
            destino = directorio
        else:
            # Extraer nombre del repo de la URL
            nombre_repo = url.rstrip('/').split('/')[-1].replace('.git', '')
            destino = nombre_repo
        
        print(f"[GIT TOOL] Destino: {destino}")
        print(f"[GIT TOOL] Ejecutando: {' '.join(cmd)}")
        
        # Verificar que git está instalado ANTES de ejecutar
        try:
            git_check = subprocess.run(
                ['git', '--version'],
                capture_output=True,
                text=True,
                timeout=5
            )
            if git_check.returncode != 0:
                return "❌ Error: Git no responde correctamente. Verifica la instalación."
            print(f"[GIT TOOL] Git version: {git_check.stdout.strip()}")
        except FileNotFoundError:
            return """❌ ERROR: Git NO está instalado en el sistema.

Instalación:
- Ubuntu/Debian: sudo apt-get update && sudo apt-get install -y git
- CentOS/RHEL: sudo yum install -y git
- macOS: brew install git
- Windows: Descarga de https://git-scm.com

Después de instalar, verifica con: git --version"""
        
        # Ejecutar git clone
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=120  # 2 minutos máximo
        )
        
        print(f"[GIT TOOL] Return code: {result.returncode}")
        print(f"[GIT TOOL] STDOUT: {result.stdout[:200]}")
        print(f"[GIT TOOL] STDERR: {result.stderr[:200]}")
        
        if result.returncode == 0:
            # Contar archivos clonados
            if os.path.exists(destino):
                num_archivos = sum([len(files) for r, d, files in os.walk(destino)])
                tamaño_dir = sum([os.path.getsize(os.path.join(r, f)) for r, d, files in os.walk(destino) for f in files])
                tamaño_mb = tamaño_dir / (1024 * 1024)
                
                ruta_completa = os.path.abspath(destino)
                
                return f"""✅ Repositorio clonado exitosamente!

📁 Directorio: {ruta_completa}
📄 Archivos: {num_archivos}
💾 Tamaño: {tamaño_mb:.2f} MB

Puedes navegar al repositorio con:
  cd {destino}"""
            else:
                return f"⚠️ Git clone ejecutado pero no se encontró el directorio {destino}"
        else:
            # Capturar y mostrar error completo
            error = result.stderr or result.stdout
            print(f"[GIT TOOL] Error completo: {error}")
            
            if 'already exists' in error.lower():
                return f"""⚠️ El directorio '{destino}' ya existe.

Opciones:
1. Eliminar: rm -rf {destino}
2. Usar otro nombre: especifica un directorio diferente"""
            elif 'not found' in error.lower() or '404' in error:
                return f"""❌ Repositorio no encontrado.

URL: {url}
Posibles causas:
- La URL es incorrecta
- El repositorio no existe
- El repositorio es privado (requiere autenticación)

Verifica la URL en el navegador primero."""
            elif 'authentication' in error.lower() or 'permission denied' in error.lower():
                return f"""❌ Error de autenticación.

El repositorio puede ser privado.
Para repositorios privados necesitas configurar SSH keys o usar:
  git config --global credential.helper store"""
            else:
                return f"""❌ Error al clonar repositorio

Comando: {' '.join(cmd)}
Código error: {result.returncode}

Error:
{error}

Intenta manualmente: git clone {url}"""
        
    except subprocess.TimeoutExpired:
        return """❌ Error: Timeout (2 minutos excedidos)

El repositorio es muy grande o la conexión es lenta.
Intenta clonarlo manualmente con:
  git clone --depth 1 {url}  (solo última versión)"""
    except FileNotFoundError:
        return """❌ ERROR CRÍTICO: Git NO está instalado

Instalación según tu sistema:
- Ubuntu/Debian: sudo apt-get update && sudo apt-get install -y git
- CentOS/RHEL: sudo yum install -y git  
- Alpine: apk add git
- macOS: brew install git
- Windows: https://git-scm.com

Verifica después con: git --version"""
    except Exception as e:
        error_msg = f"Error inesperado: {str(e)}"
        print(f"[GIT TOOL] ERROR CRÍTICO: {error_msg}")
        import traceback
        traceback.print_exc()
        return f"""❌ Error inesperado

Tipo: {type(e).__name__}
Mensaje: {str(e)}

Intenta el comando manualmente para ver más detalles:
  git clone {url}"""


# Definición de la tool para Ollama
TOOL_DEFINITION = {
    'type': 'function',
    'function': {
        'name': 'clonar_repositorio_git',
        'description': 'Clona un repositorio de Git (GitHub, GitLab, etc.) en el sistema local. Requiere que Git esté instalado. Usa el nombre del repositorio como directorio por defecto.',
        'parameters': {
            'type': 'object',
            'properties': {
                'url': {
                    'type': 'string',
                    'description': 'URL del repositorio a clonar. Puede ser con o sin .git (ej: https://github.com/usuario/repositorio o https://github.com/usuario/repositorio.git)'
                },
                'directorio': {
                    'type': 'string',
                    'description': 'Directorio destino OPCIONAL. Si no se especifica o es None, usa el nombre del repositorio automáticamente. Solo especificar si el usuario lo pide explícitamente.',
                }
            },
            'required': ['url']
        }
    }
}

# Palabras clave para activar esta tool
KEYWORDS = [
    'clonar', 'clone', 'git', 'repositorio', 'repo',
    'github', 'gitlab', 'bitbucket', 'descargar código',
    'bajar repo', 'obtener código'
]
