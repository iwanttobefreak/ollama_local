# Tool de Temperatura para Ollama

## 📋 Descripción

Tool para Ollama que obtiene pronósticos de temperatura para **CUALQUIER ciudad de España** sin datos hardcodeados. Usa geocoding dinámico y APIs gratuitas.

## ✨ Características

- ✅ **Funciona con CUALQUIER ciudad** (Madrid, Barcelona, Mataró, Alcobendas, pueblos pequeños, etc.)
- ✅ **SIN datos hardcodeados** - Búsqueda dinámica con OpenStreetMap
- ✅ **No requiere API_KEY** - Usa servicios gratuitos (Open-Meteo)
- ✅ **Hasta 16 días de pronóstico**
- ✅ **Integración completa con Ollama**
- ✅ **Chat interactivo incluido**

## 📦 Instalación

```powershell
# Instalar dependencias
pip install ollama requests

# Verificar que Ollama está corriendo
ollama serve
```

## 🚀 Uso

### Modo 1: Chat Interactivo

```powershell
python ollama_temperatura_tool.py
```

**Ejemplos de preguntas:**
- "¿Qué tiempo hará mañana en Madrid?"
- "Pronóstico de 5 días para Mataró"
- "¿Lloverá en Alcobendas esta semana?"
- "Temperatura en Barcelona los próximos 3 días"
- "Tiempo en San Sebastián para el fin de semana"

### Modo 2: Test de la Función

```powershell
python ollama_temperatura_tool.py --test
```

Prueba la función con Madrid y Mataró para verificar que funciona.

### Modo 3: Usar como Módulo en Tu Script

```python
from ollama_temperatura_tool import obtener_pronostico_temperatura, TOOL_DEFINITION
import ollama

# Usar la herramienta
resultado = obtener_pronostico_temperatura("Madrid", 3)
print(resultado)

# O integrarla con Ollama
response = ollama.chat(
    model='llama3.1',
    messages=[
        {'role': 'user', 'content': '¿Qué tiempo hará en Barcelona?'}
    ],
    tools=[TOOL_DEFINITION]
)
```

## 📊 Datos Proporcionados

Para cada día del pronóstico:
- 🌡️ **Temperatura**: Mínima y máxima en °C
- ☁️ **Clima**: Condiciones (Despejado, Nublado, Lluvia, etc.)
- 💧 **Probabilidad de lluvia**: Porcentaje
- 💨 **Viento**: Velocidad en km/h
- 📅 **Fecha**: Día de la semana y fecha

## 🔧 Configuración de la Tool

La herramienta se define así para Ollama:

```python
TOOL_DEFINITION = {
    'type': 'function',
    'function': {
        'name': 'obtener_pronostico_temperatura',
        'description': 'Obtiene el pronóstico de temperatura para CUALQUIER ciudad de España',
        'parameters': {
            'type': 'object',
            'properties': {
                'ciudad': {
                    'type': 'string',
                    'description': 'Nombre de CUALQUIER ciudad española'
                },
                'dias': {
                    'type': 'integer',
                    'description': 'Número de días (1-16)',
                    'default': 3
                }
            },
            'required': ['ciudad']
        }
    }
}
```

## 💡 Ejemplos de Salida

### Madrid - 3 días
```
Pronostico de temperatura para Madrid:

Miercoles 15/10/2025 (HOY):
  Temperatura: 12.9°C - 24.9°C
  Clima: Nublado
  Probabilidad de lluvia: 0%
  Viento: 5.2 km/h

Jueves 16/10/2025 (MAÑANA):
  Temperatura: 13.9°C - 23.8°C
  Clima: Nublado
  Probabilidad de lluvia: 18%
  Viento: 7.2 km/h

Viernes 17/10/2025:
  Temperatura: 12.4°C - 23.9°C
  Clima: Nublado
  Probabilidad de lluvia: 26%
  Viento: 6.2 km/h

Fuente: Open-Meteo
Coordenadas: 40.4167, -3.7036
```

## 🌐 APIs Utilizadas

1. **OpenStreetMap Nominatim**
   - Geocoding gratuito
   - Convierte nombre de ciudad → coordenadas
   - Sin límites razonables de uso

2. **Open-Meteo**
   - Datos meteorológicos gratuitos
   - Sin necesidad de registro
   - Hasta 16 días de pronóstico

## 🔍 Cómo Funciona

1. **Usuario pregunta** a Ollama sobre el tiempo
2. **Ollama identifica** que necesita la herramienta
3. **La herramienta:**
   - Busca la ciudad en OpenStreetMap (geocoding)
   - Obtiene coordenadas (lat, lon)
   - Consulta Open-Meteo con las coordenadas
   - Formatea los datos
4. **Ollama recibe** los datos y responde al usuario

## 🎯 Ventajas vs Otras Soluciones

| Característica | Esta Tool | Otras |
|----------------|-----------|-------|
| Ciudades | ♾️ Cualquiera | 40-70 hardcodeadas |
| API Key | ❌ No necesita | ✅ Necesita |
| Límites | ❌ Sin límites | ⚠️ Límites AEMET |
| Hardcoded | ❌ Cero datos | ✅ Listas fijas |
| Funciona con | Ciudades + Pueblos | Solo capitales |

## 🐛 Solución de Problemas

### Error: "No se encontró la ciudad"
- Verifica la ortografía
- Prueba con el nombre completo
- Ejemplo: "San Sebastian" o "Donostia"

### Error: "HTTP 429"
- No debería ocurrir con esta tool (sin límites)
- Si ocurre, espera 1 minuto

### Ollama no llama a la herramienta
- Verifica que usas un modelo compatible (llama3.1, mistral, etc.)
- Haz preguntas claras sobre el tiempo

## 📝 Registro de Pruebas

✅ **Madrid** - Funciona
✅ **Mataró** - Funciona  
✅ **Alcobendas** - Funciona
✅ **Barcelona** - Funciona
✅ **Pueblos pequeños** - Funciona

## 🚀 Uso Remoto (Servidor Ollama)

Si tu Ollama está en otro servidor:

1. **Copia este archivo** al servidor de Ollama
2. **No necesitas cambiar nada** - funciona tal cual
3. **Ejecuta** en el servidor:
   ```bash
   python ollama_temperatura_tool.py
   ```

No necesitas configurar IPs ni puertos porque la tool se ejecuta en el mismo servidor que Ollama.

## 📚 Archivos Relacionados

- `ollama_temperatura_tool.py` - **Esta tool** (RECOMENDADA)
- `pronostico_temperatura.py` - Script standalone
- `temperatura.py` - Version con 40 ciudades hardcodeadas
- `api_temperatura.py` - API REST Flask

## 🎓 Ejemplo de Conversación

```
Tu: ¿Qué tiempo hará en Mataró los próximos 5 días?

[Consultando Mataro...]

Ollama: Aquí está el pronóstico para Mataró:

Para hoy (miércoles 15/10):
- Temperatura entre 16.8°C y 21.2°C
- Cielo nublado
- 23% de probabilidad de lluvia
- Viento de 12.7 km/h

...
```

## ✅ Ventajas Clave

1. **Sin mantenimiento** - No hay listas de ciudades que actualizar
2. **Siempre actualizado** - Geocoding en tiempo real
3. **Sin límites** - APIs gratuitas y sin cuotas
4. **Flexible** - Funciona con cualquier ciudad
5. **Simple** - No requiere configuración

---

**Creado:** 15/10/2025  
**Última prueba:** ✅ Funcionando con Madrid, Mataró, Alcobendas  
**Estado:** ✅ Producción Ready
