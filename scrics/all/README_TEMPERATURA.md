# 🌡️ Herramientas de Pronóstico de Temperatura para España

Scripts para consultar el pronóstico de temperatura de ciudades españolas.

## 📁 Archivos creados

### 1. **temperatura.py** ⭐⭐⭐ (RECOMENDADO)
   - Script standalone (no requiere Ollama)
   - API gratuita Open-Meteo (sin necesidad de registro)
   - **Uso:** `python temperatura.py Madrid 5`

### 2. **ollama_temperatura.py** ⭐⭐
   - Cliente Ollama con herramienta de temperatura
   - Conversacional e interactivo
   - **Uso:** `python ollama_temperatura.py`

### 3. **aemet_temperatura.py** ⭐
   - Usa API oficial de AEMET
   - Requiere registro y API key gratuita
   - **Uso:** Necesita configuración previa

---

## 🚀 INICIO RÁPIDO

### Opción 1: Script simple (SIN Ollama)

```powershell
cd C:\Users\joseantonio.legidoma\copilot\apis
python temperatura.py Madrid
```

**Ejemplos:**
```powershell
python temperatura.py Barcelona 7    # 7 días de pronóstico
python temperatura.py Sevilla 3      # 3 días
python temperatura.py Murcia         # 3 días (por defecto)
```

### Opción 2: Con Ollama (conversacional)

```powershell
python ollama_temperatura.py
```

Luego pregunta:
```
Tu: ¿Qué temperatura hará en Madrid mañana?
Tu: Dame el pronóstico de Barcelona para esta semana
Tu: ¿Lloverá en Sevilla el fin de semana?
```

---

## 📊 Características

### ✅ temperatura.py (Simple)

- **API:** Open-Meteo (gratuita, sin registro)
- **Ciudades:** 40+ ciudades españolas
- **Datos:**
  - Temperatura mín/máx
  - Condiciones climáticas
  - Probabilidad de lluvia
  - Velocidad del viento
- **Pronóstico:** Hasta 16 días
- **Ventajas:**
  - ✅ No requiere registro
  - ✅ Sin límites de consultas
  - ✅ Fácil de usar
  - ✅ Sin dependencias de Ollama

### ✅ ollama_temperatura.py (Con Ollama)

- **API:** Open-Meteo (gratuita)
- **Ciudades:** 40+ ciudades españolas
- **Características:**
  - Chat conversacional
  - Preguntas en lenguaje natural
  - Integración perfecta con Ollama
- **Requiere:**
  - Ollama instalado
  - Modelo compatible (llama3.2, mistral, etc.)

### ⚙️ aemet_temperatura.py (Oficial)

- **API:** AEMET oficial
- **Datos:** Más detallados y oficiales
- **Requiere:**
  - Registro gratuito en AEMET
  - API Key (gratis)
- **Ventajas:**
  - Datos oficiales del gobierno
  - Más precisos para España

---

## 🏙️ Ciudades disponibles

**Principales:**
- Madrid, Barcelona, Valencia, Sevilla
- Zaragoza, Málaga, Murcia, Palma
- Las Palmas, Bilbao, Alicante, Córdoba
- Valladolid, Vigo, Gijón, Granada

**Y muchas más:** Vitoria, Santander, Pamplona, San Sebastián, Salamanca, Burgos, Albacete, Toledo, Cádiz, Huelva, León, Cáceres, Badajoz, Pontevedra, Ourense, Lugo, A Coruña, Tarragona, Castellón, Logroño...

Para ver la lista completa:
```powershell
python temperatura.py
```

---

## 💡 Ejemplos de uso

### Ejemplo 1: Pronóstico simple

```powershell
python temperatura.py Madrid
```

**Salida:**
```
PRONOSTICO METEOROLOGICO - MADRID
==================================================================

Miercoles  15/10/2025  HOY
  Temperatura:   12.9°C -  24.9°C
  Clima:        Nublado
  Prob. lluvia:   0%
  Viento:         5.2 km/h

Jueves     16/10/2025  MAÑANA
  Temperatura:   13.9°C -  23.8°C
  Clima:        Nublado
  Prob. lluvia:  18%
  Viento:         7.2 km/h
...
```

### Ejemplo 2: Pronóstico de 7 días

```powershell
python temperatura.py Barcelona 7
```

### Ejemplo 3: Con Ollama (conversacional)

```powershell
python ollama_temperatura.py

Tu: ¿Qué temperatura hará en Sevilla mañana?

[Ollama llama a: obtener_pronostico_temperatura]
[Argumentos: {'ciudad': 'Sevilla', 'dias': 3}]

[Resultado del pronostico:]
Pronostico de temperatura para Sevilla:
...

Ollama: Mañana en Sevilla la temperatura estará entre 
15°C y 27°C, con cielo parcialmente nublado...
```

---

## 🔧 Instalación

### Requisitos:

```powershell
pip install requests
```

### Para Ollama (opcional):

```powershell
pip install ollama
ollama pull llama3.2
```

---

## 📖 Comparación de scripts

| Script | API | Requiere registro | Ollama | Días máx | Recomendado |
|--------|-----|-------------------|--------|----------|-------------|
| **temperatura.py** | Open-Meteo | ❌ No | ❌ No | 16 | ✅✅✅ |
| ollama_temperatura.py | Open-Meteo | ❌ No | ✅ Sí | 7 | ✅✅ |
| aemet_temperatura.py | AEMET | ✅ Sí (gratis) | ❌ No | 7 | ✅ |

**Recomendación:** Usa `temperatura.py` para consultas rápidas, y `ollama_temperatura.py` si quieres conversar con IA.

---

## 🌐 APIs utilizadas

### Open-Meteo
- **URL:** https://open-meteo.com
- **Registro:** No necesario
- **Límites:** Sin límites
- **Cobertura:** Mundial
- **Ventajas:** Gratuita, sin registro, datos precisos

### AEMET (Agencia Estatal de Meteorología)
- **URL:** https://opendata.aemet.es
- **Registro:** Gratis en https://opendata.aemet.es/centrodedescargas/altaUsuario
- **Límites:** Razonables para uso personal
- **Cobertura:** España
- **Ventajas:** Datos oficiales del gobierno

---

## 🎯 Usar con Ollama

### Integrar ambas herramientas (población + temperatura):

Puedes combinar los dos scripts para crear un asistente completo:

```python
from ollama import chat
from ollama_ine import consultar_poblacion_ine
from ollama_temperatura import obtener_pronostico_temperatura

tools = [
    # Herramienta de población
    {
        'type': 'function',
        'function': {
            'name': 'consultar_poblacion_ine',
            'description': 'Consulta población de España',
            'parameters': {...}
        }
    },
    # Herramienta de temperatura
    {
        'type': 'function',
        'function': {
            'name': 'obtener_pronostico_temperatura',
            'description': 'Consulta pronóstico de temperatura',
            'parameters': {...}
        }
    }
]

# Ahora Ollama puede usar ambas herramientas
```

---

## ❓ Troubleshooting

### Error: "requests module not found"
```powershell
pip install requests
```

### Error: "Ciudad no encontrada"
- Verifica la ortografía
- Usa la lista de ciudades disponibles
- Para ciudades pequeñas, usa la provincia

### Error de conexión a Open-Meteo
- Verifica tu conexión a internet
- El servicio es gratuito pero puede tener mantenimiento ocasional

### AEMET: "API Key invalida"
1. Regístrate en: https://opendata.aemet.es/centrodedescargas/altaUsuario
2. Copia tu API key
3. Edita `aemet_temperatura.py` y pega tu key en `AEMET_API_KEY`

---

## 📝 Resumen

**Para uso simple:**
```powershell
python temperatura.py Madrid
```

**Para conversación con IA:**
```powershell
python ollama_temperatura.py
```

**Para datos oficiales:**
```powershell
python aemet_temperatura.py Madrid  # (necesita API key)
```

---

## 🎉 ¡Listo!

Ya tienes herramientas completas para:
- ✅ Consultar población de España (INE)
- ✅ Consultar temperatura de España (Open-Meteo/AEMET)
- ✅ Integrar con Ollama para conversaciones naturales

**Archivo principal:** `temperatura.py` (más simple y sin dependencias)
**Con Ollama:** `ollama_temperatura.py` (conversacional)
