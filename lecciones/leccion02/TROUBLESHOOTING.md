# 🔧 Guía de Troubleshooting - Error al obtener temperatura

## El Problema

Cuando ejecutas `python mcp_client_temperatura.py`, el servidor MCP no puede obtener la temperatura y responde con un error.

## Diagnóstico

**Paso 1: Ejecutar el script de diagnóstico**

Desde tu contenedor Docker, ejecuta:

```bash
cd /scrics/ollama_local/lecciones/leccion02
python diagnostico.py
```

Este script te dirá exactamente qué está fallando:
- ✅ Si Python funciona
- ✅ Si encuentra el script de temperatura
- ✅ Si puede ejecutar el script
- ✅ Si las dependencias están instaladas
- ✅ Si Ollama está conectado

## Soluciones Comunes

### Problema 1: Script no encontrado

**Síntoma:**
```
Error: No se encuentra el script en /path/to/script
```

**Solución:**
Verifica que el script de la lección 1 exista:
```bash
ls -la ../leccion01/script_pronostico_temperatura.py
```

Si no existe, necesitas tener la lección 1 completa.

---

### Problema 2: Falta el módulo requests

**Síntoma:**
```
ModuleNotFoundError: No module named 'requests'
```

**Solución:**
```bash
pip install requests
```

O instalar todas las dependencias:
```bash
cd ../leccion01
pip install requests
```

---

### Problema 3: Error de permisos

**Síntoma:**
```
Permission denied
```

**Solución:**
```bash
chmod +x ../leccion01/script_pronostico_temperatura.py
```

---

### Problema 4: Ciudad no encontrada (OpenStreetMap)

**Síntoma:**
El script se ejecuta pero dice que no encuentra la ciudad.

**Solución:**
Prueba el script directamente:
```bash
cd ../leccion01
python script_pronostico_temperatura.py Madrid 1
```

Si falla aquí, el problema está en la conexión a internet o en el script de la lección 1.

---

### Problema 5: Input validation error (tipo incorrecto)

**Síntoma:**
```
Input validation error: '7' is not of type 'integer'
```

**Causa:**
Los parámetros de Ollama llegan como strings pero el schema de MCP espera integers.

**Solución:**
Este problema ya está resuelto en los archivos actualizados. El servidor MCP ahora convierte automáticamente:
```python
# En mcp_server_temperatura.py
dias = int(dias)  # Convierte string a integer
```

Si ves este error, asegúrate de tener la última versión de los archivos.

---

## Pruebas Paso a Paso

### Test 1: Verificar que el script de temperatura funciona

```bash
cd /scrics/ollama_local/lecciones/leccion01
python script_pronostico_temperatura.py Madrid 1
```

**Esperado:** Debe mostrar el pronóstico para Madrid.

### Test 2: Verificar el servidor MCP básico

```bash
cd /scrics/ollama_local/lecciones/leccion02
python mcp_client_minimo.py
```

**Esperado:** Debe mostrar "¡Hola María! Bienvenido al servidor MCP."

### Test 3: Verificar el diagnóstico completo

```bash
cd /scrics/ollama_local/lecciones/leccion02
python diagnostico.py
```

**Esperado:** Todas las comprobaciones con ✅

### Test 4: Ejecutar el cliente completo con debug

```bash
cd /scrics/ollama_local/lecciones/leccion02
python mcp_client_temperatura.py
```

Ahora verás información de debug si hay errores.

---

## Cambios Realizados

He actualizado dos archivos para ayudarte a diagnosticar:

### 1. `mcp_server_temperatura.py`

**Mejoras:**
- ✅ Detecta automáticamente si usar `python` o `python3`
- ✅ Verifica que el script exista antes de ejecutarlo
- ✅ Muestra errores más detallados (STDOUT y STDERR)
- ✅ Ejecuta desde el directorio correcto

### 2. `mcp_client_temperatura.py`

**Mejoras:**
- ✅ Muestra información de debug cuando hay errores
- ✅ Imprime las primeras líneas del error del servidor

### 3. `diagnostico.py` (NUEVO)

**Funciones:**
- ✅ Verifica toda la configuración
- ✅ Prueba ejecutar el script de temperatura
- ✅ Lista dependencias instaladas
- ✅ Verifica conexión con Ollama

---

## Solución Rápida

Si tienes prisa y solo quieres que funcione:

```bash
# 1. Ve a leccion01 y verifica que funcione
cd /scrics/ollama_local/lecciones/leccion01
python script_pronostico_temperatura.py Madrid 1

# 2. Si funciona, instala las dependencias en leccion02
cd ../leccion02
pip install requests

# 3. Ejecuta el diagnóstico
python diagnostico.py

# 4. Ejecuta el cliente
python mcp_client_temperatura.py
```

---

## Información Útil para Debugging

Cuando vuelvas a ejecutar `mcp_client_temperatura.py`, ahora verás algo como esto si hay un error:

```
✅ Consultando servidor MCP...
   🔧 Herramienta: obtener_temperatura
   📝 Ciudad: Madrid
   📅 Días: 7

⚠️  DEBUG - Respuesta del servidor:
   Error al obtener temperatura:
   STDERR: ModuleNotFoundError: No module named 'requests'
   STDOUT: ...
```

Esto te dirá exactamente qué está fallando.

---

## Preguntas Frecuentes

### ¿Por qué funciona en local pero no en Docker?

Posibles razones:
1. Diferentes versiones de Python
2. Dependencias no instaladas en el contenedor
3. Rutas diferentes
4. Problemas de red en el contenedor

### ¿Puedo usar un script diferente?

Sí, puedes modificar `mcp_server_temperatura.py` para usar cualquier script o API que quieras.

### ¿Necesito la lección 1 completa?

Sí, el servidor MCP usa `script_pronostico_temperatura.py` de la lección 1.

---

## Próximos Pasos

1. ✅ Ejecuta `python diagnostico.py`
2. ✅ Lee el output y resuelve los problemas indicados
3. ✅ Vuelve a ejecutar `python mcp_client_temperatura.py`
4. ✅ Si aún falla, copia el output del diagnóstico para más ayuda

---

**Nota:** Los cambios ya están aplicados en los archivos, solo necesitas volver a ejecutar el cliente.
