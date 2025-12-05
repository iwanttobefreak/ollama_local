# Lección 2 - Guía de Instalación y Ejecución

## Requisitos Previos

### 1. Python 3.8 o superior
```bash
python3 --version
```

### 2. Ollama (opcional para ejemplos completos)

**Opción A: Docker (recomendado)**
```bash
# Verificar si Ollama está corriendo
docker ps | grep ollama

# Iniciar Ollama
docker start ollama

# Verificar modelos disponibles
docker exec ollama ollama list

# Descargar modelo si no está
docker exec ollama ollama pull llama3.2:3b
```

**Opción B: Instalación local**
```bash
# macOS/Linux
curl -fsSL https://ollama.ai/install.sh | sh

# Windows: Descargar de https://ollama.ai/download
```

---

## Instalación Rápida

### Método 1: Script Automático (Recomendado)

```bash
cd lecciones/leccion02
./test_leccion02.sh
```

El script te guiará por todas las opciones.

### Método 2: Instalación Manual

```bash
cd lecciones/leccion02

# Instalar dependencias
pip install -r requirements.txt

# O instalar individualmente
pip install mcp>=0.9.0
pip install ollama>=0.1.0
```

---

## Ejemplos Disponibles

### 1️⃣ Ejemplo Mínimo (Sin Ollama)

**Propósito:** Entender lo básico de MCP sin complicaciones

```bash
python3 mcp_client_minimo.py
```

**Salida esperada:**
```
🧪 PRUEBA MÍNIMA DE MCP

✅ Herramientas: saludar
📨 Respuesta: ¡Hola María! Bienvenido al servidor MCP.
```

**Lo que hace:**
- Inicia un servidor MCP simple
- Se conecta como cliente
- Lista las herramientas disponibles
- Ejecuta una herramienta de prueba

---

### 2️⃣ Ejemplo Completo (Con Ollama y Temperatura)

**Propósito:** Ver MCP en acción con un LLM real

**Requisitos:**
- Ollama corriendo (docker o local)
- Modelo llama3.2:3b descargado

```bash
python3 mcp_client_temperatura.py
```

**Ejemplo de uso:**
```
👤 Tú: ¿Qué temperatura hará mañana en Madrid?

🤔 Pensando...
✅ Consultando servidor MCP...
   🔧 Herramienta: obtener_temperatura
   📝 Ciudad: Madrid

🤖 Asistente: Según el pronóstico para Madrid mañana:
- Temperatura: Entre 9°C y 19°C
- Clima: Nublado
- Probabilidad de lluvia: 8%
```

---

## Estructura de Archivos

```
leccion02/
├── README.md                      # Documentación principal
├── COMPARACION.md                 # Lección 1 vs Lección 2
├── INSTALACION.md                 # Esta guía
├── requirements.txt               # Dependencias Python
├── test_leccion02.sh             # Script de prueba interactivo
│
├── mcp_server_minimo.py          # 🟢 Servidor MCP simple
├── mcp_client_minimo.py          # 🟢 Cliente para probar lo básico
│
├── mcp_server_temperatura.py     # 🔵 Servidor con temperatura real
└── mcp_client_temperatura.py     # 🔵 Cliente con Ollama integrado
```

**Leyenda:**
- 🟢 Básico: Sin dependencias de Ollama
- 🔵 Completo: Requiere Ollama corriendo

---

## Troubleshooting

### Error: "No se ha podido resolver la importación 'mcp'"

**Solución:**
```bash
pip install mcp
```

### Error: "connection refused" al ejecutar cliente

**Causa:** El servidor MCP no se inició correctamente

**Solución:** 
- El cliente inicia el servidor automáticamente
- Verifica que los permisos sean correctos
- Ejecuta desde el directorio `leccion02`

### Error: "Model not found" con Ollama

**Solución:**
```bash
# Docker
docker exec ollama ollama pull llama3.2:3b

# Local
ollama pull llama3.2:3b
```

### Docker: "Container ollama not found"

**Solución:**
```bash
# Listar contenedores
docker ps -a | grep ollama

# Si existe pero está parado
docker start ollama

# Si no existe, crearlo
docker run -d --name ollama \
  -p 11434:11434 \
  -v ollama:/root/.ollama \
  ollama/ollama
```

### El script de temperatura no funciona

**Verifica:**
```bash
# ¿Existe el script de la lección 1?
ls ../leccion01/script_pronostico_temperatura.py

# Prueba ejecutarlo directamente
python3 ../leccion01/script_pronostico_temperatura.py Madrid 3
```

---

## Verificación de la Instalación

### Test Completo

```bash
cd lecciones/leccion02

# 1. Verificar Python
python3 --version

# 2. Verificar dependencias
python3 -c "import mcp; print('MCP OK')"
python3 -c "import ollama; print('Ollama OK')"

# 3. Ejecutar prueba mínima
python3 mcp_client_minimo.py

# 4. Verificar Ollama (si está instalado)
docker exec ollama ollama list
# O en local: ollama list

# 5. Ejecutar prueba completa
python3 mcp_client_temperatura.py
```

---

## Preguntas Frecuentes

### ¿Necesito Ollama para todo?

**No.** El ejemplo mínimo (`mcp_client_minimo.py`) funciona sin Ollama.
Solo necesitas Ollama para el ejemplo completo con IA.

### ¿Puedo usar otros modelos de Ollama?

**Sí.** Edita el archivo `mcp_client_temperatura.py` y cambia:
```python
model='llama3.2:3b'  # Cambia esto
```

Modelos recomendados:
- `llama3.2:3b` - Rápido y ligero (recomendado)
- `llama3.1:8b` - Más preciso, más lento
- `mistral:7b` - Alternativa buena

### ¿Puedo ejecutar el servidor MCP en otra máquina?

**Sí**, pero esta lección usa `stdio` (local).
Para servidores remotos necesitarías configurar MCP sobre HTTP/WebSocket
(tema de lecciones avanzadas).

### ¿Funciona en Windows?

**Sí**, pero necesitas ajustar:
1. Usar `python` en vez de `python3`
2. No ejecutar `.sh` directamente (usar Git Bash o WSL)
3. Ollama: Descargar instalador de Windows

---

## Siguientes Pasos

1. ✅ Completa el ejemplo mínimo
2. ✅ Completa el ejemplo de temperatura
3. 📖 Lee [COMPARACION.md](COMPARACION.md) para entender diferencias
4. 🔧 Modifica los ejemplos para tus necesidades
5. 🚀 Crea tu propio servidor MCP

---

## Recursos Adicionales

- **Documentación MCP:** https://modelcontextprotocol.io/
- **Ollama Docs:** https://ollama.ai/docs
- **Python MCP SDK:** https://github.com/modelcontextprotocol/python-sdk
- **Ejemplos oficiales:** https://github.com/modelcontextprotocol/servers

---

**¿Problemas? Revisa:**
1. Los errores en la terminal
2. Que estés en el directorio correcto
3. Que las dependencias estén instaladas
4. Que Ollama esté corriendo (para ejemplos completos)
