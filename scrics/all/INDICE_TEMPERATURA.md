# Índice Completo - Scripts de Temperatura

## 🎯 ARCHIVO RECOMENDADO

### ⭐ ollama_temperatura_tool.py
**La mejor opción para usar con Ollama**

- ✅ Funciona con CUALQUIER ciudad (sin límites)
- ✅ SIN datos hardcodeados
- ✅ No requiere API_KEY
- ✅ Chat interactivo incluido
- ✅ Fácil integración con Ollama
- ✅ Probado y funcionando

**Uso:**
```bash
# Chat interactivo
python ollama_temperatura_tool.py

# Modo test
python ollama_temperatura_tool.py --test
```

---

## 📁 Todos los Archivos Creados

### Scripts Principales

#### 1. **ollama_temperatura_tool.py** ⭐ RECOMENDADO
- Tool completa para Ollama
- Chat interactivo
- Geocoding dinámico
- Sin datos hardcodeados
- **Estado:** ✅ Producción

#### 2. **pronostico_temperatura.py**
- Script standalone
- Mismo sistema que la tool
- Uso desde línea de comandos
- **Estado:** ✅ Producción

#### 3. **temperatura.py**
- 40 ciudades hardcodeadas
- Más rápido (sin geocoding)
- Limitado a ciudades predefinidas
- **Estado:** ✅ OK para ciudades comunes

#### 4. **temperatura_aemet.py**
- 70+ ciudades hardcodeadas
- Usa API oficial AEMET
- Requiere API_KEY
- Datos oficiales del gobierno
- **Estado:** ✅ OK si tienes API_KEY

#### 5. **temperatura_aemet_dinamico.py**
- Búsqueda dinámica en AEMET
- Requiere API_KEY
- **Problema:** Límites de peticiones (429)
- **Estado:** ⚠️ No recomendado

---

### APIs y Servicios

#### 6. **api_temperatura.py**
- API REST con Flask
- Endpoints HTTP para Ollama remoto
- Requiere Flask instalado
- **Estado:** ✅ Creado, pendiente instalación

#### 7. **tool_temperatura.py**
- Cliente para API REST
- Para usar desde servidor Ollama remoto
- **Estado:** ✅ Creado

---

### Ejemplos y Documentación

#### 8. **ejemplos_ollama_temperatura.py**
- 4 ejemplos de uso
- Uso directo de función
- Integración con Ollama
- Comparación de ciudades
- Preguntas complejas
- **Estado:** ✅ Completo

#### 9. **README_OLLAMA_TEMPERATURA.md**
- Documentación completa
- Guía de instalación
- Ejemplos de uso
- Solución de problemas
- **Estado:** ✅ Completo

#### 10. **README_SCRIPTS_TEMPERATURA.md**
- Comparativa de todos los scripts
- Pruebas realizadas
- Recomendaciones
- **Estado:** ✅ Completo

#### 11. **INDICE_TEMPERATURA.md** (este archivo)
- Índice de todos los archivos
- Guía rápida de selección

---

## 🚀 Guía Rápida de Selección

### ¿Qué archivo usar?

| Situación | Archivo | Motivo |
|-----------|---------|--------|
| **Usar con Ollama** | `ollama_temperatura_tool.py` | ⭐ Integración completa |
| **Línea de comandos** | `pronostico_temperatura.py` | Script standalone |
| **Solo ciudades grandes** | `temperatura.py` | Más rápido, 40 ciudades |
| **Datos oficiales AEMET** | `temperatura_aemet.py` | Si tienes API_KEY |
| **Ollama remoto** | `api_temperatura.py` + `tool_temperatura.py` | API REST |
| **Aprender a usar** | `ejemplos_ollama_temperatura.py` | Ejemplos prácticos |

---

## 📊 Comparativa Técnica

| Script | Ciudades | API Key | Hardcoded | Geocoding | Límites |
|--------|----------|---------|-----------|-----------|---------|
| **ollama_temperatura_tool.py** | ♾️ | ❌ | ❌ | ✅ | ❌ |
| **pronostico_temperatura.py** | ♾️ | ❌ | ❌ | ✅ | ❌ |
| **temperatura.py** | 40 | ❌ | ✅ | ❌ | ❌ |
| **temperatura_aemet.py** | 70+ | ✅ | ✅ | ❌ | ⚠️ |
| **temperatura_aemet_dinamico.py** | 8000+ | ✅ | ❌ | ❌ | ⚠️ 429 |

---

## 🔧 Tecnologías Usadas

### Geocoding
- **OpenStreetMap Nominatim**: Convierte nombres de ciudades a coordenadas
- Gratuito, sin registro
- Sin límites razonables

### Datos Meteorológicos
- **Open-Meteo**: Pronóstico hasta 16 días
- Gratuito, sin API Key
- Sin límites de peticiones

### Alternativas (requieren API Key)
- **AEMET**: API oficial del gobierno español
- Más precisa para España
- Límites de peticiones

---

## 📝 Pruebas Realizadas

### ✅ Ciudades Probadas Exitosamente

| Ciudad | Script | Resultado |
|--------|--------|-----------|
| Madrid | ollama_temperatura_tool.py | ✅ OK |
| Mataró | ollama_temperatura_tool.py | ✅ OK |
| Alcobendas | pronostico_temperatura.py | ✅ OK |
| Barcelona | ejemplos_ollama_temperatura.py | ✅ OK |

### 📊 Datos de Ejemplo (15/10/2025)

**Madrid:**
- Temperatura: 12.9°C - 24.9°C
- Clima: Nublado
- Prob. lluvia: 0%

**Mataró:**
- Temperatura: 16.8°C - 21.2°C
- Clima: Nublado
- Prob. lluvia: 23%

---

## 🎓 Ejemplos de Uso

### Chat con Ollama
```python
python ollama_temperatura_tool.py

Tu: ¿Qué tiempo hará en Madrid mañana?
[Consultando Madrid...]
Ollama: Mañana en Madrid tendremos temperaturas entre 13.9°C y 23.8°C...
```

### Línea de Comandos
```bash
python pronostico_temperatura.py Barcelona 5
```

### Como Módulo
```python
from ollama_temperatura_tool import obtener_pronostico_temperatura

resultado = obtener_pronostico_temperatura("Sevilla", 7)
print(resultado)
```

---

## 📦 Instalación

### Dependencias Básicas
```bash
pip install requests
```

### Para Ollama
```bash
pip install ollama requests
```

### Para API REST (Ollama remoto)
```bash
pip install flask flask-cors requests
```

---

## 🌟 Características Destacadas

### ollama_temperatura_tool.py

1. **Búsqueda Universal**
   - Cualquier ciudad, pueblo o municipio
   - No solo capitales

2. **Sin Mantenimiento**
   - No hay listas que actualizar
   - Todo dinámico

3. **Sin Límites**
   - APIs gratuitas
   - Sin cuotas

4. **Chat Natural**
   - "¿Lloverá mañana?"
   - "Tiempo en Barcelona"
   - "Pronóstico 5 días Madrid"

5. **Multiidioma** (en datos)
   - "San Sebastián" o "Donostia"
   - "La Coruña" o "A Coruña"

---

## 🔍 Casos de Uso

### 1. Asistente Personal
```python
python ollama_temperatura_tool.py
Tu: ¿Necesito paraguas mañana?
```

### 2. Planificación de Viajes
```python
python ejemplos_ollama_temperatura.py
# Ejecuta ejemplo 4: compara ciudades
```

### 3. Integración en App
```python
from ollama_temperatura_tool import obtener_pronostico_temperatura
# Usa en tu aplicación
```

### 4. API para Servicios Remotos
```bash
python api_temperatura.py
# Servidor HTTP en puerto 5000
```

---

## 📂 Estructura de Archivos

```
apis/
├── ollama_temperatura_tool.py          ⭐ PRINCIPAL
├── pronostico_temperatura.py           Standalone
├── temperatura.py                      40 ciudades
├── temperatura_aemet.py                AEMET + hardcoded
├── temperatura_aemet_dinamico.py       AEMET dinámico
├── api_temperatura.py                  API REST Flask
├── tool_temperatura.py                 Cliente API
├── ejemplos_ollama_temperatura.py      Ejemplos
├── README_OLLAMA_TEMPERATURA.md        Documentación
├── README_SCRIPTS_TEMPERATURA.md       Comparativa
└── INDICE_TEMPERATURA.md              Este archivo
```

---

## ✅ Estado del Proyecto

| Componente | Estado | Notas |
|------------|--------|-------|
| Tool Ollama | ✅ Producción | Probada y funcionando |
| Script Standalone | ✅ Producción | Probado |
| API REST | ✅ Creada | Pendiente instalación Flask |
| Documentación | ✅ Completa | 3 archivos README |
| Ejemplos | ✅ Completos | 4 ejemplos incluidos |
| Pruebas | ✅ Realizadas | Madrid, Mataró, Alcobendas, Barcelona |

---

## 🎯 Recomendación Final

### Para Ollama Local:
👉 **Usa `ollama_temperatura_tool.py`**

### Para Línea de Comandos:
👉 **Usa `pronostico_temperatura.py`**

### Para Ollama Remoto:
👉 **Usa `api_temperatura.py` + `tool_temperatura.py`**

### Para Aprender:
👉 **Empieza con `ejemplos_ollama_temperatura.py`**

---

**Creado:** 15/10/2025  
**Última actualización:** 15/10/2025  
**Estado:** ✅ Proyecto Completo y Funcional
