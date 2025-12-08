# 🤖 Ollama Multi-Tools

Sistema modular para usar múltiples herramientas con Ollama.

## 📁 Estructura

```
apis/
├── ollama_multi_tools.py       # Chat principal con todas las tools
├── tools/                       # Carpeta de herramientas
│   ├── __init__.py             # Inicializador del módulo
│   ├── temperatura.py          # Tool: Pronóstico del tiempo
│   └── git_clone.py            # Tool: Clonar repositorios Git
```

## 🚀 Uso

### Ejecutar el chat multi-tool

```bash
python ollama_multi_tools.py
```

### Test de las tools

```bash
python ollama_multi_tools.py --test
```

## 🔧 Tools disponibles

### 1. **Temperatura** (`temperatura.py`)
- **Función:** `obtener_pronostico_temperatura(ciudad, dias)`
- **Descripción:** Pronóstico del tiempo para CUALQUIER ciudad de España
- **Keywords:** temperatura, tiempo, clima, lluvia, calor, frío, etc.
- **Ejemplo:** "¿Qué temperatura habrá mañana en Madrid?"

### 2. **Git Clone** (`git_clone.py`)
- **Función:** `clonar_repositorio_git(url, directorio)`
- **Descripción:** Clona repositorios de GitHub/GitLab
- **Keywords:** clonar, clone, git, repositorio, github, gitlab
- **Ejemplo:** "Clona el repositorio https://github.com/user/repo.git"

## ➕ Añadir una nueva tool

### Paso 1: Crear el archivo de la tool

Crea un nuevo archivo en `tools/`, por ejemplo `tools/mi_nueva_tool.py`:

```python
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Tool: Descripción de tu tool
"""

def mi_funcion_tool(parametro1: str, parametro2: int = 10) -> str:
    """
    Descripción de lo que hace
    
    Args:
        parametro1: Descripción del parámetro
        parametro2: Otro parámetro (opcional)
    
    Returns:
        String con el resultado
    """
    try:
        print(f"[MI TOOL] Ejecutando con {parametro1}")
        
        # Tu lógica aquí
        resultado = f"Procesado: {parametro1}"
        
        return resultado
        
    except Exception as e:
        return f"Error: {str(e)}"


# Definición de la tool para Ollama
TOOL_DEFINITION = {
    'type': 'function',
    'function': {
        'name': 'mi_funcion_tool',
        'description': 'Descripción clara de qué hace la tool',
        'parameters': {
            'type': 'object',
            'properties': {
                'parametro1': {
                    'type': 'string',
                    'description': 'Descripción del parámetro'
                },
                'parametro2': {
                    'type': 'integer',
                    'description': 'Descripción del parámetro opcional',
                    'default': 10
                }
            },
            'required': ['parametro1']
        }
    }
}

# Palabras clave que activan esta tool
KEYWORDS = [
    'palabra1', 'palabra2', 'palabra3'
]
```

### Paso 2: Registrar la tool en `ollama_multi_tools.py`

```python
# Importar tu nueva tool
from mi_nueva_tool import (
    mi_funcion_tool,
    TOOL_DEFINITION as MI_TOOL,
    KEYWORDS as MI_KEYWORDS
)

# Añadir a available_functions
available_functions = {
    'obtener_pronostico_temperatura': obtener_pronostico_temperatura,
    'clonar_repositorio_git': clonar_repositorio_git,
    'mi_funcion_tool': mi_funcion_tool,  # ← Nueva tool
}

# Añadir a tools_registry
tools_registry = [
    {
        'definition': TEMP_TOOL,
        'keywords': TEMP_KEYWORDS,
        'name': 'temperatura'
    },
    {
        'definition': GIT_TOOL,
        'keywords': GIT_KEYWORDS,
        'name': 'git'
    },
    {
        'definition': MI_TOOL,  # ← Nueva tool
        'keywords': MI_KEYWORDS,
        'name': 'mi_tool'
    }
]
```

### Paso 3: ¡Listo!

Ahora puedes usarla:

```bash
python ollama_multi_tools.py
>>> Ejecuta mi_funcion_tool con "hola mundo"
```

## 💡 Ventajas de esta estructura

✅ **Modular:** Cada tool en su propio archivo
✅ **Escalable:** Fácil añadir nuevas tools
✅ **Organizado:** Código limpio y mantenible
✅ **Flexible:** Cada tool con sus propias keywords
✅ **Debug:** Mensajes claros por tool
✅ **Reutilizable:** Puedes importar tools en otros scripts

## 🎯 Ejemplos de uso

```
>>> ¿Qué tiempo hará mañana en Madrid?
[Usa tool: temperatura]

>>> Clona https://github.com/python/cpython.git
[Usa tool: git_clone]

>>> ¿Dónde hará más calor, en Sevilla o en Barcelona?
[Usa tool: temperatura 2 veces y compara]

>>> ¿Cuál es la capital de Francia?
[Respuesta directa sin tools]
```

## 📦 Dependencias

```bash
pip install ollama requests
```

Para git_clone también necesitas:
```bash
# Linux/Mac
sudo apt install git

# Windows
# Descarga de https://git-scm.com
```

## 🔐 Desplegar en servidor remoto

1. Copia toda la carpeta `apis/` al servidor
2. Instala dependencias:
   ```bash
   pip3 install ollama requests
   ```
3. Ejecuta:
   ```bash
   python3 ollama_multi_tools.py
   ```

## 📝 Ideas de nuevas tools

- **Búsqueda web** (usando DuckDuckGo API)
- **Calculadora avanzada** (eval seguro con sympy)
- **Consulta base de datos** (PostgreSQL, MySQL)
- **API REST** (hacer peticiones HTTP)
- **Archivos** (leer, escribir, buscar)
- **Sistema** (info del sistema, procesos)
- **Traducción** (usando APIs gratuitas)
- **Noticias** (RSS feeds)

---

**Autor:** José Antonio Legido  
**Fecha:** 2025  
**Licencia:** MIT
