#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Tool: MCP Adapter
Permite usar MCPs de Node.js desde Ollama
"""

import subprocess
import json


def ejecutar_mcp_nodejs(mcp_package: str, tool_name: str, arguments: dict) -> str:
    """
    Ejecuta un MCP de Node.js y devuelve el resultado
    
    Args:
        mcp_package: Nombre del paquete NPM (ej: '@modelcontextprotocol/server-git')
        tool_name: Nombre de la herramienta a ejecutar (ej: 'git_status')
        arguments: Argumentos para la herramienta
    
    Returns:
        String con el resultado
    """
    try:
        print(f"[MCP ADAPTER] Ejecutando MCP: {mcp_package}")
        print(f"[MCP ADAPTER] Tool: {tool_name}")
        print(f"[MCP ADAPTER] Args: {arguments}")
        
        # Construir comando para ejecutar MCP
        # Los MCPs usan stdio para comunicación
        request = {
            "jsonrpc": "2.0",
            "id": 1,
            "method": "tools/call",
            "params": {
                "name": tool_name,
                "arguments": arguments
            }
        }
        
        # Ejecutar MCP
        cmd = ['npx', '-y', mcp_package]
        
        result = subprocess.run(
            cmd,
            input=json.dumps(request),
            capture_output=True,
            text=True,
            timeout=30
        )
        
        if result.returncode != 0:
            return f"❌ Error ejecutando MCP:\n{result.stderr}"
        
        # Parsear respuesta JSON-RPC
        try:
            response = json.loads(result.stdout)
            if 'result' in response:
                return response['result']['content'][0]['text']
            elif 'error' in response:
                return f"❌ Error del MCP: {response['error']['message']}"
        except json.JSONDecodeError:
            return f"⚠️ Respuesta no JSON:\n{result.stdout}"
        
    except FileNotFoundError:
        return """❌ ERROR: Node.js/NPM no está instalado

Instalación:
- Ubuntu/Debian: curl -fsSL https://deb.nodesource.com/setup_20.x | sudo -E bash - && sudo apt-get install -y nodejs
- macOS: brew install node
- Windows: https://nodejs.org

Verifica: node --version && npm --version"""
    
    except subprocess.TimeoutExpired:
        return "❌ Timeout ejecutando MCP (30 segundos)"
    
    except Exception as e:
        return f"❌ Error: {str(e)}"


# Ejemplo: Git Status usando MCP oficial
def git_status_mcp(repo_path: str = ".") -> str:
    """
    Obtiene el estado de un repositorio Git usando MCP oficial de Anthropic
    
    Args:
        repo_path: Ruta al repositorio (default: directorio actual)
    
    Returns:
        Estado del repositorio
    """
    return ejecutar_mcp_nodejs(
        mcp_package='@modelcontextprotocol/server-git',
        tool_name='git_status',
        arguments={'repository': repo_path}
    )


# Ejemplo: GitHub Info usando MCP oficial
def github_repo_info_mcp(owner: str, repo: str, github_token: str = None) -> str:
    """
    Obtiene información de un repositorio de GitHub usando MCP oficial
    
    Args:
        owner: Propietario del repo (ej: 'microsoft')
        repo: Nombre del repo (ej: 'vscode')
        github_token: Token de GitHub (opcional, para rate limits más altos)
    
    Returns:
        Información del repositorio
    """
    args = {
        'owner': owner,
        'repo': repo
    }
    if github_token:
        args['token'] = github_token
    
    return ejecutar_mcp_nodejs(
        mcp_package='@modelcontextprotocol/server-github',
        tool_name='get_repository',
        arguments=args
    )


# Definiciones de tools para Ollama
GIT_STATUS_TOOL = {
    'type': 'function',
    'function': {
        'name': 'git_status_mcp',
        'description': 'Obtiene el estado de un repositorio Git local usando el MCP oficial de Anthropic. Muestra archivos modificados, staged, untracked, etc.',
        'parameters': {
            'type': 'object',
            'properties': {
                'repo_path': {
                    'type': 'string',
                    'description': 'Ruta al repositorio Git (default: directorio actual)',
                    'default': '.'
                }
            }
        }
    }
}

GITHUB_REPO_INFO_TOOL = {
    'type': 'function',
    'function': {
        'name': 'github_repo_info_mcp',
        'description': 'Obtiene información de un repositorio de GitHub: descripción, estrellas, forks, lenguajes, etc. Usa el MCP oficial de Anthropic.',
        'parameters': {
            'type': 'object',
            'properties': {
                'owner': {
                    'type': 'string',
                    'description': 'Propietario del repositorio (ej: microsoft, python, torvalds)'
                },
                'repo': {
                    'type': 'string',
                    'description': 'Nombre del repositorio (ej: vscode, cpython, linux)'
                },
                'github_token': {
                    'type': 'string',
                    'description': 'Token de GitHub (opcional, para evitar rate limits)'
                }
            },
            'required': ['owner', 'repo']
        }
    }
}

# Keywords para activar estas tools
KEYWORDS = [
    'git', 'status', 'estado', 'repo', 'repositorio',
    'github', 'información', 'estrellas', 'forks',
    'commits', 'branches', 'ramas'
]
