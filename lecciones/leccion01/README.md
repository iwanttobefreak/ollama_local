Hacemos una pregunta al LLM local:
ollama run llama3.1:8b
```¿que tiempo va a hacer mañana en Madrid?```
Cómo solo es un modelo de leguaje y no tiene conexión con internet es:
```
Lo siento, pero no tengo acceso a información de tiempo real o actualizada sobre el clima. Sin embargo, puedo
sugerirte algunas formas de obtener la información que buscas
```
Ojo porque si le preguntamos lo mismo a codellama:13b nos responde pero se lo ha inventado:
```ollama run codellama:13b```
```
I can provide you with information about the weather in Madrid, but I cannot predict the future. However, I can
tell you the current weather conditions and forecast for Madrid.

According to data from AEMET (the Spanish National Meteorological Agency), the current weather conditions in
Madrid are:

* Temperature: 15°C (59°F)
* Humidity: 60%
* Wind: 2 km/h (1.2 mph)
* Clouds: Scattered clouds

As for the forecast, AEMET predicts that the weather will be mostly sunny with a high of 22°C (72°F) and a low of
9°C (48°F) on Monday. There is a chance of scattered thunderstorms in the afternoon.

Please note that this information may not reflect the actual weather conditions in Madrid, as weather can change
rapidly and it's always best to check with local authorities or a reliable weather source for the most up-to-date
information.
```
Esto es porque se lo inventa, porque codellama está entrenado para usar APIs y generar código y entonces se inventa que lo puede conseguir. Si le preguntamos:
```¿Cuál es la temperatura exacta AHORA MISMO en Madrid?```
```
No puedo proporcionarte la temperatura exacta en Madrid AHORA MISMO. La información meteorológica actual se basa
en los datos de las estaciones meteorológicas, que pueden estar ubicadas en diferentes puntos de la ciudad y puede
haber un delay entre el momento en que se toma la medición y el momento en que se hace disponible.

Sin embargo, puedo proporcionarte una predicción de la temperatura para Madrid en función de las condiciones
meteorológicas actuales y previstas. Por ejemplo, si la temperatura en Madrid es de 15°C ahora mismo, podría
predecirse que suba a 17°C en los próximos días si la temperatura promedio es de 16°C durante el día y baja a 9°C
por la noche.

Por favor, tenga en cuenta que estas son solo predicciones y que la temperatura real puede variar según las
condiciones meteorológicas específicas y locales.
```
Para conectar a internet y usar herramientas externas usamos las tools.
Primero generamos un script con python que sea capaz de darnos información. Por ejemplo el script **script_pronostico_temperatura.py** que le pasas como parámetro la ciudad y los días y te da el pronóstico
Para ver como ejecutarlo, lo ejecutyamos sin parámetros:
```python script_pronostico_temperatura.py```

Si queremos sacar el pronóstico de Barcelona de los siguientes 3 días ejecutamos:
```python pronostico_temperatura.py Barcelona 7 ```

Ahora vamos a integrar este script de python con una tool que sea capaz de ejecutar ollama.

La estructura básica de una tool definition sigue este formato:

```python
TOOL_DEFINITION = {
    'type': 'function',
    'function': {
        'name': 'obtener_pronostico_temperatura',
        'description': 'SOLO usar cuando el usuario pregunta específicamente por el TIEMPO, CLIMA, TEMPERATURA, LLUVIA o PRONOSTICO meteorológico de una ciudad ESPAÑOLA. Funciona con CUALQUIER ciudad de España. NO usar para otras preguntas generales.',
        'parameters': {
            'type': 'object',
            'properties': {
                'ciudad': {
                    'type': 'string',
                    'description': 'Nombre de CUALQUIER ciudad española (Madrid, Barcelona, Mataró, Alcobendas, pueblos pequeños, etc.)'
                },
                'dias': {
                    'type': 'integer',
                    'description': 'Días de pronóstico (1-16). Default: 3',
                    'default': 3,
                    'minimum': 1,
                    'maximum': 16
                }
            },
            'required': ['ciudad']
        }
    }
}
```

### 🔍 Componentes clave:

- **📖 `description`**: Lo que lee el LLM para decidir **cuándo** usar la función
- **⚙️ `parameters`**: Qué parámetros extrae el LLM de la petición del usuario
- **❗ `required`**: Parámetros obligatorios para el funcionamiento de la tool

El LLM decide "quiero usar esta tool con estos parámetros" y devuelve un json que lo ejecuta el script de python que está escrito debajo de la **TOOL_DEFINITION**.

```
# Función que ejecuta el script
def obtener_temp(ciudad):
    resultado = subprocess.run(
        ['python3', 'script_pronostico_temperatura.py', ciudad],
        capture_output=True,
        text=True
    )
    return resultado.stdout

# Chat
mensajes = [{'role': 'system', 'content': 'Asistente con acceso a herramientas meteorológicas.'}]

while True:
    pregunta = input("\nChat: ").strip()

    mensajes.append({'role': 'user', 'content': pregunta})

    # Primera llamada: LLM decide
    respuesta = ollama.chat(model='llama3.1:8b', messages=mensajes, tools=[TOOL])

    # ¿Usó la tool?
    if respuesta['message'].get('tool_calls'):
        ciudad = respuesta['message']['tool_calls'][0]['function']['arguments']['ciudad']
        resultado = obtener_temp(ciudad)

        mensajes.append(respuesta['message'])
        mensajes.append({'role': 'tool', 'content': resultado})

        # Segunda llamada: LLM procesa resultado
        respuesta = ollama.chat(model='llama3.1:8b', messages=mensajes)

    print(f"Asistente: {respuesta['message']['content']}")
    mensajes.append({'role': 'assistant', 'content': respuesta['message']['content']})
```




---

## 🤖 Configuración del System Prompt

Para definir más exactamente cómo debe actuar el agente, podemos añadir instrucciones específicas al system prompt:

```python
messages = [
    {
        'role': 'system',
        'content': '''Eres un asistente útil con acceso a herramientas meteorológicas para España.

IMPORTANTE:
- Cuando uses herramientas, SIEMPRE presenta los resultados obtenidos de forma clara
- NO digas "no tengo acceso a información" si ya obtuviste datos de herramientas
- Si te preguntan por VARIAS ciudades, usa la herramienta VARIAS VECES (una por ciudad)
- Para comparaciones (ej: "¿dónde hará más calor, en X o Y?"), llama a la herramienta para CADA ciudad y luego compara los resultados'''
    }
]
```

---

## 🔍 Palabras Clave para Activar la Tool

Lista de keywords que ayudan a detectar cuándo el usuario necesita información meteorológica:

```python
KEYWORDS = [
    'temperatura', 'tiempo', 'clima', 'lluvia', 'viento',
    'pronostico', 'pronóstico', 'calor', 'frio', 'frío',
    'grados', 'soleado', 'nublado', 'despejado', 'meteorolog',
    'nevar', 'nieve', 'tormenta', 'cielo',
    'semana', 'hoy', 'mañana', 'hará', 'estará'
]
```

### 💡 Propósito de las keywords:
- **🎯 Detección automática** de intenciones del usuario
- **⚡ Activación rápida** de la tool apropiada
- **🔄 Filtrado eficiente** de consultas relevantes
