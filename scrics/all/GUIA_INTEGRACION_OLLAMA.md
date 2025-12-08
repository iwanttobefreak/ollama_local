# Guía de Integración con Ollama

## 🚀 Integración Rápida (3 pasos)

### Paso 1: Verificar que Ollama está corriendo

Ya tienes `ollama serve` corriendo ✅

Verifica que tienes un modelo instalado:
```powershell
ollama list
```

Si no tienes llama3.1, instálalo:
```powershell
ollama pull llama3.1
```

### Paso 2: Instalar el paquete de Python de Ollama

```powershell
pip install ollama
```

### Paso 3: Ejecutar la tool

```powershell
cd C:\Users\joseantonio.legidoma\copilot\apis
python ollama_temperatura_tool.py
```

¡Y listo! Ya puedes chatear con Ollama sobre el tiempo.

---

## 💬 Ejemplo de Conversación

```
======================================================================
CHAT DE TEMPERATURA CON OLLAMA
Pregunta sobre el tiempo en CUALQUIER ciudad de España
======================================================================

Ejemplos de preguntas:
  - ¿Que tiempo hara mañana en Madrid?
  - Pronostico de 5 dias para Mataro
  - ¿Llovera en Alcobendas esta semana?
  - Temperatura en Barcelona los proximos 3 dias

Escribe 'salir' para terminar

Tu: ¿Qué tiempo hará mañana en Madrid?

[Consultando Madrid...]

Ollama: Según el pronóstico, mañana (jueves 16/10) en Madrid tendremos:
- Temperaturas entre 13.9°C y 23.8°C
- Cielo nublado
- 18% de probabilidad de lluvia
- Viento moderado de 7.2 km/h

Será un día agradable, con temperaturas cálidas. No parece necesario paraguas.

Tu: ¿Y en Barcelona?

[Consultando Barcelona...]

Ollama: En Barcelona para mañana el pronóstico es:
- Temperaturas entre 17.5°C y 21.3°C
- Parcialmente nublado
- 15% de probabilidad de lluvia
- Viento de 11 km/h

Algo más fresco que en Madrid, pero también buen tiempo.

Tu: salir
Adios!
```

---

## 🔧 Configuración Avanzada

### Opción 1: Chat Interactivo (Recomendado)

```powershell
python ollama_temperatura_tool.py
```

Ventajas:
- ✅ Conversación natural
- ✅ Múltiples preguntas seguidas
- ✅ Ollama procesa y resume los datos
- ✅ Contexto mantenido

### Opción 2: Usar en tu Propio Script

Crea un archivo `mi_chat_tiempo.py`:

```python
from ollama_temperatura_tool import obtener_pronostico_temperatura, TOOL_DEFINITION
import ollama

# Funciones disponibles
available_functions = {
    'obtener_pronostico_temperatura': obtener_pronostico_temperatura
}

def preguntar(pregunta):
    """Hace una pregunta sobre el tiempo"""
    
    # Llamar a Ollama
    response = ollama.chat(
        model='llama3.1',
        messages=[
            {'role': 'user', 'content': pregunta}
        ],
        tools=[TOOL_DEFINITION]
    )
    
    # Si Ollama quiere usar la herramienta
    if response['message'].get('tool_calls'):
        messages = [
            {'role': 'user', 'content': pregunta},
            response['message']
        ]
        
        for tool_call in response['message']['tool_calls']:
            function_name = tool_call['function']['name']
            function_args = tool_call['function']['arguments']
            
            # Ejecutar función
            if function_name in available_functions:
                print(f"[Consultando {function_args.get('ciudad')}...]")
                function_response = available_functions[function_name](**function_args)
                
                messages.append({
                    'role': 'tool',
                    'content': function_response
                })
        
        # Obtener respuesta final
        final_response = ollama.chat(
            model='llama3.1',
            messages=messages
        )
        
        return final_response['message']['content']
    else:
        return response['message']['content']

# Usar
respuesta = preguntar("¿Qué tiempo hará en Madrid los próximos 3 días?")
print(respuesta)
```

### Opción 3: Función Directa (Sin Chat)

Si solo quieres los datos sin que Ollama los procese:

```python
from ollama_temperatura_tool import obtener_pronostico_temperatura

# Obtener pronóstico directamente
resultado = obtener_pronostico_temperatura("Madrid", 3)
print(resultado)
```

---

## 🎯 Modelos de Ollama Compatibles

La tool funciona con cualquier modelo que soporte function calling:

- ✅ **llama3.1** (Recomendado)
- ✅ **llama3.2**
- ✅ **mistral**
- ✅ **mixtral**
- ✅ **qwen2.5**

Para cambiar de modelo, edita la línea en `ollama_temperatura_tool.py`:
```python
response = ollama.chat(
    model='llama3.1',  # Cambia aquí el modelo
    messages=messages,
    tools=[TOOL_DEFINITION]
)
```

---

## 🐛 Solución de Problemas

### Error: "Import ollama could not be resolved"

```powershell
pip install ollama
```

### Error: "Connection refused"

Verifica que Ollama está corriendo:
```powershell
# En otra terminal
ollama serve
```

O verifica el proceso:
```powershell
Get-Process ollama
```

### Error: "Model not found"

Descarga el modelo:
```powershell
ollama pull llama3.1
```

### Ollama no usa la herramienta

Algunas preguntas que funcionan mejor:
- ✅ "¿Qué tiempo hará en Madrid?"
- ✅ "Pronóstico para Barcelona"
- ✅ "¿Lloverá mañana en Sevilla?"

Evita:
- ❌ "Hola" (muy genérico)
- ❌ "¿Cómo estás?" (no relacionado con tiempo)

---

## 📊 Ejemplo Paso a Paso

### 1. Instalar Ollama (si no lo tienes)
```powershell
# Descargar de https://ollama.ai
# Ejecutar instalador
ollama serve
```

### 2. Instalar modelo
```powershell
ollama pull llama3.1
```

### 3. Instalar paquete Python
```powershell
pip install ollama
```

### 4. Ejecutar la tool
```powershell
cd C:\Users\joseantonio.legidoma\copilot\apis
python ollama_temperatura_tool.py
```

### 5. Hacer preguntas
```
Tu: ¿Qué tiempo hará mañana en Madrid?
Tu: ¿Y pasado mañana?
Tu: ¿Dónde hará mejor tiempo: Madrid o Barcelona?
Tu: salir
```

---

## 🎓 Ejemplos de Preguntas

### Preguntas Simples
- "¿Qué tiempo hará en Madrid?"
- "Pronóstico para Barcelona"
- "Temperatura en Sevilla"

### Con Detalles Temporales
- "¿Qué tiempo hará mañana en Valencia?"
- "Pronóstico de 5 días para Málaga"
- "¿Cómo estará el tiempo este fin de semana en Bilbao?"

### Preguntas Específicas
- "¿Lloverá mañana en Murcia?"
- "¿Necesito abrigo en Madrid esta semana?"
- "¿Hará calor en Sevilla los próximos días?"

### Comparaciones
- "¿Dónde hará mejor tiempo: Madrid o Barcelona?"
- "Compara el tiempo de Valencia y Alicante"

### Cualquier Ciudad
- "Tiempo en Mataró"
- "¿Qué tiempo hará en Alcobendas?"
- "Pronóstico para San Sebastián"

---

## 💡 Tips de Uso

### 1. Preguntas Naturales
Ollama entiende lenguaje natural. No necesitas comandos específicos.

### 2. Contexto Mantenido
Puedes hacer preguntas de seguimiento:
```
Tu: ¿Qué tiempo hará en Madrid?
Ollama: [responde]
Tu: ¿Y en Barcelona?  <- Entiende que sigues preguntando por el tiempo
```

### 3. Múltiples Ciudades
Ollama puede comparar automáticamente:
```
Tu: ¿Dónde lloverá más: Madrid o Barcelona?
```
Ollama consultará ambas ciudades y comparará.

### 4. Interpretación Inteligente
Ollama interpreta y resume los datos:
```
Tu: ¿Necesito paraguas mañana en Madrid?
Ollama: Consultará el pronóstico y responderá basándose en la probabilidad de lluvia
```

---

## 🔄 Integración con Otras Herramientas

Puedes combinar esta tool con otras tools de Ollama:

```python
from ollama_temperatura_tool import obtener_pronostico_temperatura, TOOL_DEFINITION as TEMP_TOOL
from ollama_ine import obtener_poblacion_ine, TOOL_DEFINITION as INE_TOOL
import ollama

# Combinar múltiples herramientas
response = ollama.chat(
    model='llama3.1',
    messages=[
        {'role': 'user', 'content': '¿Cuántos habitantes tiene Madrid y qué tiempo hará mañana?'}
    ],
    tools=[TEMP_TOOL, INE_TOOL]
)
```

---

## ✅ Checklist de Integración

- [ ] Ollama instalado
- [ ] `ollama serve` corriendo
- [ ] Modelo descargado (`ollama pull llama3.1`)
- [ ] Paquete Python instalado (`pip install ollama`)
- [ ] Tool descargada (`ollama_temperatura_tool.py`)
- [ ] Script ejecutándose (`python ollama_temperatura_tool.py`)
- [ ] Primera pregunta realizada

---

## 🎉 ¡Listo para Usar!

Una vez completados los pasos, simplemente ejecuta:

```powershell
python ollama_temperatura_tool.py
```

Y empieza a preguntar sobre el tiempo en cualquier ciudad de España.

**¡Disfruta de tu asistente meteorológico con IA!** ☁️🌤️⛈️
