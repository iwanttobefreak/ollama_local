# 📑 ÍNDICE COMPLETO - Herramientas INE

## 📂 Estructura de archivos

```
C:\Users\joseantonio.legidoma\copilot\apis\
│
├── 🎯 ARCHIVOS PRINCIPALES (Para usar con Ollama)
│   ├── ollama_ine.py ⭐⭐⭐ RECOMENDADO
│   │   └── Cliente Ollama con consulta INE integrada
│   │       Modo conversacional interactivo
│   │       USO: python ollama_ine.py
│   │
│   ├── ine_poblacion.py ⭐⭐
│   │   └── Script standalone (sin Ollama)
│   │       USO: python ine_poblacion.py Madrid 2021
│   │
│   └── demo_ollama_ine.py ⭐
│       └── Demostración automática con ejemplos
│           USO: python demo_ollama_ine.py
│
├── 🔧 ARCHIVOS AVANZADOS (MCP)
│   ├── mcp_ine_server.py
│   │   └── Servidor MCP para integraciones avanzadas
│   │
│   ├── mcp_ine_config.json
│   │   └── Configuración para Claude Desktop
│   │
│   └── test_mcp_ine.py
│       └── Tests del servidor MCP
│
├── 📚 DOCUMENTACIÓN
│   ├── RESUMEN.md ⭐⭐⭐
│   │   └── Resumen ejecutivo y guía de inicio rápido
│   │
│   ├── README_OLLAMA.md ⭐⭐
│   │   └── Guía completa de uso con Ollama
│   │
│   ├── GUIA_OLLAMA.md ⭐
│   │   └── Guía detallada de integración
│   │
│   ├── README_MCP.md
│   │   └── Documentación del servidor MCP
│   │
│   └── INDICE.md
│       └── Este archivo
│
└── 🗂️ ARCHIVOS HISTÓRICOS (Versiones anteriores)
    ├── habitantes_ine.py
    │   └── Primera versión con datos hardcodeados
    │
    ├── habitantes_ine_web.py
    │   └── Versión híbrida (API + hardcoded)
    │
    ├── habitantes_ine_real.py
    │   └── Intento de versión solo API
    │
    └── ine_scraper.py
        └── Versión con scraping complejo
```

---

## 🚀 GUÍA RÁPIDA DE USO

### Para usuarios de Ollama (RECOMENDADO):

1. **Instalar:**
   ```powershell
   pip install ollama requests
   ollama pull llama3.2
   ```

2. **Ejecutar:**
   ```powershell
   cd C:\Users\joseantonio.legidoma\copilot\apis
   python ollama_ine.py
   ```

3. **Usar:**
   ```
   Tu: ¿Cuántos habitantes tenía Madrid en 2021?
   ```

### Para uso standalone (sin Ollama):

```powershell
python ine_poblacion.py Madrid 2021
```

### Para ver una demo:

```powershell
python demo_ollama_ine.py
```

---

## 📖 ¿Qué archivo leer primero?

### Si quieres empezar YA:
👉 **RESUMEN.md** - Todo lo esencial en 5 minutos

### Si quieres documentación completa:
👉 **README_OLLAMA.md** - Guía completa con ejemplos

### Si necesitas integración avanzada:
👉 **GUIA_OLLAMA.md** - Opciones de integración detalladas

### Si usas Claude Desktop o MCP:
👉 **README_MCP.md** - Servidor MCP

---

## 🎯 ¿Qué archivo ejecutar?

| Quiero... | Ejecutar |
|-----------|----------|
| Chat con Ollama | `python ollama_ine.py` |
| Consulta simple | `python ine_poblacion.py Madrid 2021` |
| Ver ejemplos | `python demo_ollama_ine.py` |
| Probar MCP | `python test_mcp_ine.py --direct` |
| Servidor MCP | `python mcp_ine_server.py` |

---

## 📊 Comparación de scripts

| Script | Ollama | Conversacional | Complejidad | Recomendado |
|--------|--------|----------------|-------------|-------------|
| **ollama_ine.py** | ✅ | ✅ | ⭐⭐ | ✅✅✅ |
| ine_poblacion.py | ❌ | ❌ | ⭐ | ✅✅ |
| demo_ollama_ine.py | ✅ | ❌ | ⭐ | ✅ |
| mcp_ine_server.py | ✅ | ✅ | ⭐⭐⭐ | ✅ (avanzado) |

---

## 🔍 Búsqueda rápida

### Quiero consultar población sin Ollama:
→ **ine_poblacion.py**

### Quiero chat interactivo con Ollama:
→ **ollama_ine.py**

### Quiero ver ejemplos funcionando:
→ **demo_ollama_ine.py**

### Quiero integrar con Claude Desktop:
→ **mcp_ine_server.py** + **README_MCP.md**

### Quiero entender todo:
→ **README_OLLAMA.md**

---

## 📝 Notas importantes

### ✅ Características comunes a TODOS los scripts:

- Sin datos hardcodeados
- Consulta en tiempo real al INE
- Datos oficiales y verificables
- Cobertura: provincias y capitales
- Rango: 1996 - 2021
- UTF-8 compatible

### ❌ Limitaciones:

- Solo provincias y capitales principales
- Datos hasta 2021
- Requiere internet
- Modelos Ollama: necesitan soportar function calling

---

## 🎓 Orden de lectura recomendado

Para alguien nuevo:

1. **RESUMEN.md** (5 min) - Visión general
2. **Ejecutar:** `python ollama_ine.py` (2 min)
3. **README_OLLAMA.md** (15 min) - Guía completa
4. **Experimentar** con preguntas propias

Para integración avanzada:

1. **GUIA_OLLAMA.md** - Opciones de integración
2. **README_MCP.md** - Servidor MCP
3. **mcp_ine_server.py** - Código del servidor

---

## 💡 Tips

### Tip 1: Modo debug
El script `ollama_ine.py` muestra automáticamente:
- Qué función se llama
- Con qué parámetros
- Qué resultado obtiene

### Tip 2: Pregunta única
```powershell
python ollama_ine.py "tu pregunta aquí"
```

### Tip 3: Cambiar modelo
Edita `ollama_ine.py` línea 211:
```python
def modo_conversacion(modelo: str = 'llama3.2'):  # Cambiar aquí
```

### Tip 4: Usar desde Python
```python
from ollama_ine import chat_con_herramientas
respuesta = chat_con_herramientas("¿Población de Madrid en 2021?")
```

---

## 🎯 Archivo ESTRELLA

### 🌟 **ollama_ine.py** 🌟

**Por qué es el mejor:**
- ✅ Fácil de usar
- ✅ Conversacional
- ✅ Integración perfecta con Ollama
- ✅ Sin configuración compleja
- ✅ Sin dependencias raras
- ✅ Documentado y claro

**Cómo empezar:**
```powershell
python ollama_ine.py
```

**Eso es todo.** 🚀

---

## 📞 Ayuda rápida

### ¿Qué archivo usar?
→ **ollama_ine.py**

### ¿Cómo ejecutarlo?
→ `python ollama_ine.py`

### ¿Qué dependencias?
→ `pip install ollama requests`

### ¿Qué modelo?
→ `ollama pull llama3.2`

### ¿Más ayuda?
→ Lee **RESUMEN.md**

---

## 🎉 ¡Empieza ya!

```powershell
cd C:\Users\joseantonio.legidoma\copilot\apis
python ollama_ine.py
```

**Haz tu primera pregunta:** "¿Cuántos habitantes tenía Barcelona en 2020?"

---

**Última actualización:** 15/10/2025
**Versión:** 1.0
**Estado:** ✅ Listo para usar
