# 📝 Guía: Integrar ollama_temperatura_dinamico.py en el sistema multi-tools

## Opción 1: Renombrar y mover (Recomendado)

### Paso 1: Renombrar el archivo
```bash
# En PowerShell (Windows)
Rename-Item ollama_temperatura_dinamico.py ollama_temperatura.py

# En Linux/Mac
mv ollama_temperatura_dinamico.py ollama_temperatura.py
```

### Paso 2: Mover a la carpeta tools
```bash
# En PowerShell (Windows)
Move-Item ollama_temperatura.py tools\

# En Linux/Mac
mv ollama_temperatura.py tools/
```

### Paso 3: Añadir exports al final de tools/ollama_temperatura.py

Abre el archivo `tools/ollama_temperatura.py` y añade **AL FINAL** (antes del `if __name__ == "__main__"`):

```python
# ===== EXPORTAR PARA OLLAMA_MULTI_TOOLS =====

# Tool definition (ya existe en el archivo, solo la renombramos para export)
# TOOL_DEFINITION ya está definida arriba

# Palabras clave para activar esta tool
KEYWORDS = [
    'temperatura', 'tiempo', 'clima', 'lluvia', 'viento', 
    'pronostico', 'pronóstico', 'calor', 'frio', 'frío',
    'grados', 'soleado', 'nublado', 'despejado', 'meteorolog',
    'nevar', 'nieve', 'tormenta', 'cielo',
    'semana', 'hoy', 'mañana', 'hará', 'estará'
]
```

### Paso 4: Verificar
```bash
python ollama_multi_tools.py --test
```

Si funciona, verás:
```
TEST MODE

============================================================
Test 1: Temperatura
Pronóstico para Madrid:
...
```

---

## Opción 2: Usar el archivo original sin moverlo

Si prefieres **NO mover** el archivo y mantener `ollama_temperatura_dinamico.py` en `apis/`:

### Modifica ollama_multi_tools.py

```python
# Al inicio, después de import ollama
import sys
import os

# Importar desde el mismo directorio (apis/)
from ollama_temperatura_dinamico import (
    obtener_pronostico_temperatura,
    TOOL_DEFINITION as TEMP_TOOL
)

# Definir keywords aquí
TEMP_KEYWORDS = [
    'temperatura', 'tiempo', 'clima', 'lluvia', 'viento', 
    'pronostico', 'pronóstico', 'calor', 'frio', 'frío',
    'grados', 'soleado', 'nublado', 'despejado', 'meteorolog',
    'nevar', 'nieve', 'tormenta', 'cielo',
    'semana', 'hoy', 'mañana', 'hará', 'estará'
]
```

---

## 🔍 Troubleshooting

### Error: "ModuleNotFoundError: No module named 'ollama_temperatura'"

**Causa:** El archivo no está en `tools/` o no tiene el nombre correcto

**Solución:**
```bash
# Verificar que el archivo existe
ls tools/ollama_temperatura.py  # Linux/Mac
dir tools\ollama_temperatura.py # Windows
```

### Error: "cannot import name 'KEYWORDS'"

**Causa:** El archivo no tiene la variable KEYWORDS exportada

**Solución:** Añade al final de `tools/ollama_temperatura.py`:
```python
KEYWORDS = [
    'temperatura', 'tiempo', 'clima', 'lluvia', 'viento', 
    'pronostico', 'pronóstico', 'calor', 'frio', 'frío',
    'grados', 'soleado', 'nublado', 'despejado', 'meteorolog',
    'nevar', 'nieve', 'tormenta', 'cielo',
    'semana', 'hoy', 'mañana', 'hará', 'estará'
]
```

### Error: "cannot import name 'TOOL_DEFINITION'"

**Solución:** Verifica que en `ollama_temperatura.py` existe esta variable (debería estar alrededor de la línea 160-180)

---

## ✅ Checklist final

- [ ] Archivo renombrado a `ollama_temperatura.py`
- [ ] Movido a carpeta `tools/`
- [ ] Variable `KEYWORDS` añadida al archivo
- [ ] Variable `TOOL_DEFINITION` existe en el archivo
- [ ] `ollama_multi_tools.py` importa correctamente
- [ ] Test ejecutado: `python ollama_multi_tools.py --test`

---

## 📂 Estructura esperada

```
apis/
├── ollama_multi_tools.py       ← Script principal
├── tools/
│   ├── __init__.py
│   ├── ollama_temperatura.py   ← Tu archivo aquí
│   └── git_clone.py
└── README_MULTI_TOOLS.md
```
