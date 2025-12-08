# Pronóstico de Temperatura - Scripts Disponibles

## ✅ RECOMENDADO: pronostico_temperatura.py

**Script que funciona con CUALQUIER ciudad sin datos hardcodeados**

### Características:
- ✅ **Busca CUALQUIER ciudad de España** (y del mundo)
- ✅ **CERO datos hardcodeados** - Búsqueda dinámica
- ✅ **No requiere API_KEY** - Usa servicios gratuitos
- ✅ **Geocoding automático** via OpenStreetMap Nominatim
- ✅ **Pronóstico hasta 16 días** via Open-Meteo
- ✅ **Probado y funcionando**

### Uso:
```bash
python pronostico_temperatura.py <ciudad> [dias]

# Ejemplos
python pronostico_temperatura.py Madrid 3
python pronostico_temperatura.py Mataro 5
python pronostico_temperatura.py Alcobendas 7
python pronostico_temperatura.py "San Sebastian" 4
```

### Ventajas:
- ✅ Funciona con ciudades grandes y pequeñas
- ✅ Funciona con pueblos
- ✅ No necesita configuración
- ✅ Sin límites de peticiones
- ✅ Datos actualizados en tiempo real

---

## Scripts Alternativos

### 1. temperatura.py
- **40 ciudades principales hardcodeadas**
- Usa Open-Meteo
- No requiere API_KEY
- Rápido pero limitado a ciudades predefinidas

### 2. temperatura_aemet.py
- **70+ ciudades hardcodeadas**
- Usa API oficial AEMET
- Requiere API_KEY gratuita
- Datos oficiales del gobierno
- Limitado a ciudades predefinidas

### 3. temperatura_aemet_dinamico.py
- Búsqueda dinámica en base de datos AEMET
- Requiere API_KEY
- **PROBLEMA**: AEMET tiene límite de peticiones (429 Too Many Requests)
- No recomendado por límites de la API

---

## Comparativa

| Script | Ciudades | API_KEY | Hardcoded | Estado |
|--------|----------|---------|-----------|---------|
| **pronostico_temperatura.py** | ♾️ Cualquiera | ❌ No | ❌ No | ✅ **RECOMENDADO** |
| temperatura.py | 40 | ❌ No | ✅ Sí | ✅ OK |
| temperatura_aemet.py | 70+ | ✅ Sí | ✅ Sí | ✅ OK |
| temperatura_aemet_dinamico.py | 8000+ | ✅ Sí | ❌ No | ⚠️ Límites API |

---

## Pruebas Realizadas

### ✅ Madrid
```
Miercoles  15/10/2025  HOY
  Temperatura:   12.9°C -  24.9°C
  Clima:        Nublado
  Prob. lluvia:   0%
  Viento:         5.2 km/h
```

### ✅ Mataró
```
Miercoles  15/10/2025  HOY
  Temperatura:   16.8°C -  21.2°C
  Clima:        Nublado
  Prob. lluvia:  23%
  Viento:        12.7 km/h
```

### ✅ Alcobendas
```
Miercoles  15/10/2025  HOY
  Temperatura:   11.8°C -  24.7°C
  Clima:        Nublado
  Prob. lluvia:   0%
  Viento:         5.7 km/h
```

---

## Tecnologías Usadas

### pronostico_temperatura.py
1. **OpenStreetMap Nominatim** - Geocoding gratuito
   - Convierte nombre de ciudad → coordenadas
   - Sin límites razonables de uso
   - Búsqueda inteligente

2. **Open-Meteo API** - Datos meteorológicos
   - API gratuita sin registro
   - Datos precisos
   - Hasta 16 días de pronóstico

---

## Integración con Ollama

Para usar con Ollama remoto, puedes:

1. **Vía API REST**: Usar `api_temperatura.py` (Flask)
2. **Vía script directo**: Copiar `pronostico_temperatura.py` al servidor

El script `pronostico_temperatura.py` es el más adecuado porque:
- No requiere configuración
- Funciona con cualquier ciudad
- Sin límites de API
- No necesita datos hardcodeados

---

## Recomendación Final

**Usa `pronostico_temperatura.py`** para:
- ✅ Cualquier ciudad española
- ✅ Sin configuración
- ✅ Sin datos hardcodeados
- ✅ Máxima flexibilidad
- ✅ Funcionamiento garantizado

Creado: 15/10/2025
Última prueba: Madrid, Mataró, Alcobendas - ✅ OK
