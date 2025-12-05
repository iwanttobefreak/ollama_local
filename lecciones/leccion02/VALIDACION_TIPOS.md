# ⚠️ Nota Importante: Validación de Tipos en MCP

## El Problema

Cuando Ollama (u otros LLMs) llaman a herramientas MCP, **todos los parámetros llegan como strings**, incluso si el schema define que deberían ser integers, booleans, etc.

### Ejemplo del Problema

**Schema MCP definido:**
```python
{
    "type": "object",
    "properties": {
        "dias": {
            "type": "integer",  # ← Definimos INTEGER
            "description": "Número de días"
        }
    }
}
```

**Lo que llega en realidad:**
```python
arguments = {
    "dias": "7"  # ← Llega como STRING, no INTEGER
}
```

**Error resultante:**
```
Input validation error: '7' is not of type 'integer'
```

## La Solución

**Siempre convierte los tipos en el servidor MCP:**

```python
@server.call_tool()
async def handle_call_tool(name: str, arguments: dict | None):
    
    # ❌ INCORRECTO - No validar
    dias = arguments.get("dias", 3)
    
    # ✅ CORRECTO - Convertir explícitamente
    dias = int(arguments.get("dias", 3))
    
    # ✅ AÚN MEJOR - Con manejo de errores
    try:
        dias = int(arguments.get("dias", 3))
    except (ValueError, TypeError):
        dias = 3  # Valor por defecto si falla
```

## Conversiones Comunes

### Integer

```python
# Método básico
dias = int(arguments.get("dias", 3))

# Método robusto con validación
def get_int_param(arguments, key, default, min_val=None, max_val=None):
    try:
        value = int(arguments.get(key, default))
        if min_val is not None and value < min_val:
            value = min_val
        if max_val is not None and value > max_val:
            value = max_val
        return value
    except (ValueError, TypeError):
        return default

# Uso
dias = get_int_param(arguments, "dias", 3, min_val=1, max_val=16)
```

### Boolean

```python
# Los booleans pueden llegar como "true", "false", "True", "False", 1, 0
def get_bool_param(arguments, key, default):
    value = arguments.get(key, default)
    if isinstance(value, bool):
        return value
    if isinstance(value, str):
        return value.lower() in ['true', '1', 'yes', 'si', 'sí']
    if isinstance(value, int):
        return value != 0
    return default

# Uso
incluir_detalles = get_bool_param(arguments, "incluir_detalles", False)
```

### Float

```python
def get_float_param(arguments, key, default):
    try:
        return float(arguments.get(key, default))
    except (ValueError, TypeError):
        return default

# Uso
temperatura_min = get_float_param(arguments, "temperatura_min", 0.0)
```

### String

```python
# Los strings generalmente no necesitan conversión, pero puedes validar
def get_string_param(arguments, key, default, max_length=None):
    value = str(arguments.get(key, default))
    if max_length and len(value) > max_length:
        value = value[:max_length]
    return value.strip()

# Uso
ciudad = get_string_param(arguments, "ciudad", "", max_length=100)
```

## Ejemplo Completo

```python
@server.call_tool()
async def handle_call_tool(
    name: str, arguments: dict | None
) -> list[types.TextContent]:
    
    if not arguments:
        arguments = {}
    
    if name == "obtener_temperatura":
        # Validar y convertir ciudad (string)
        ciudad = str(arguments.get("ciudad", "")).strip()
        if not ciudad:
            raise ValueError("El parámetro 'ciudad' es obligatorio")
        
        # Validar y convertir días (integer)
        try:
            dias = int(arguments.get("dias", 3))
            # Validar rango
            if dias < 1:
                dias = 1
            elif dias > 16:
                dias = 16
        except (ValueError, TypeError):
            dias = 3
        
        # Validar incluir_detalles (boolean)
        incluir_detalles_raw = arguments.get("incluir_detalles", False)
        if isinstance(incluir_detalles_raw, str):
            incluir_detalles = incluir_detalles_raw.lower() in ['true', '1', 'yes']
        else:
            incluir_detalles = bool(incluir_detalles_raw)
        
        # Ahora usa los parámetros validados...
        resultado = consultar_api(ciudad, dias, incluir_detalles)
        
        return [types.TextContent(type="text", text=resultado)]
```

## Por Qué Sucede Esto

1. **HTTP/JSON**: Cuando los datos viajan por red, todo se serializa como strings
2. **Ollama API**: Ollama convierte los parámetros del LLM a JSON, pero no siempre respeta los tipos
3. **MCP Protocol**: El protocolo MCP recibe los datos tal como vienen del cliente

## Mejores Prácticas

### ✅ DO (Hacer)

```python
# 1. Siempre validar y convertir tipos
dias = int(arguments.get("dias", 3))

# 2. Manejar errores de conversión
try:
    dias = int(arguments.get("dias", 3))
except (ValueError, TypeError):
    dias = 3

# 3. Validar rangos y restricciones
if dias < 1 or dias > 16:
    raise ValueError("Los días deben estar entre 1 y 16")

# 4. Documentar los tipos esperados en la descripción
inputSchema={
    "properties": {
        "dias": {
            "type": "integer",
            "description": "Número de días (1-16). Se convertirá automáticamente si llega como string"
        }
    }
}
```

### ❌ DON'T (No hacer)

```python
# 1. No asumir que el tipo es correcto
dias = arguments.get("dias", 3)  # Podría ser "3" (string)

# 2. No ignorar errores de validación
dias = int(arguments["dias"])  # Crash si no existe o no es convertible

# 3. No confiar solo en el schema
# El schema es documentación, NO validación automática
```

## Testing

Prueba tu servidor con diferentes tipos de entrada:

```python
# Test manual
import asyncio

async def test():
    # Test 1: String que debería ser integer
    result = await handle_call_tool("obtener_temperatura", {
        "ciudad": "Madrid",
        "dias": "7"  # String
    })
    print(result)
    
    # Test 2: Integer correcto
    result = await handle_call_tool("obtener_temperatura", {
        "ciudad": "Madrid",
        "dias": 7  # Integer
    })
    print(result)
    
    # Test 3: Valor inválido
    result = await handle_call_tool("obtener_temperatura", {
        "ciudad": "Madrid",
        "dias": "abc"  # No convertible
    })
    print(result)

asyncio.run(test())
```

## Resumen

| Problema | Solución |
|----------|----------|
| Parámetro llega como string | Convertir: `int()`, `float()`, `bool()` |
| Valor puede ser inválido | Usar try/except con valor por defecto |
| Necesitas validar rango | Agregar if/elif después de conversión |
| Múltiples tipos posibles | Función helper con lógica de conversión |

---

**Nota:** Todos los archivos de ejemplo en esta lección ya incluyen la conversión de tipos correcta. Si encuentras errores de validación, verifica que estés usando las últimas versiones de los archivos.
