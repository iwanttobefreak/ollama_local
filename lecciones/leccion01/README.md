Hacemos una pregunta al LLM local, con comando docker, API o prompt (como hemos visto en la creación del docker en la lección 0):

Por ejemplo via prompt:
```bash
docker exec -ti ollama bash -c "ollama run llama3.1:8b"
>>> cual es la capital de Francia?
La capital de Francia es París.
```

Probamos otra pregunta que no sea de diccionario, que sea dinámica
```bash
>>> ¿que tiempo va a hacer mañana en Barcelona?
```

Cómo solo es un modelo de lenguaje y no tiene conexión con internet responde:

```
Lo siento, pero no tengo acceso en tiempo real a la información meteorológica actualizada. Sin embargo, puedo sugerirte algunas opciones para que puedas obtener la
previsión del tiempo para mañana en Barcelona:

1. Visita el sitio web de la Agencia Estatal de Meteorología (AEMET) de España: [www.aemet.es](http://www.aemet.es)
2. Utiliza una aplicación de clima como AccuWeather, Weather.com o The Weather Channel en tu dispositivo móvil.
3. Busca en Google "previsión del tiempo para mañana en Barcelona" y selecciona la fuente que te parezca más fiable.

Recuerda que las predicciones meteorológicas pueden cambiar con frecuencia, por lo que es recomendable verificarlas varias veces antes de planificar tus actividades.
```

Ojo porque si le preguntamos lo mismo a codellama:13b nos da un pronóstico pero se lo ha inventado, porque es un modelo orientado a código. Salimos con /bye y arrancamos otro modelo:


```bash
>>> /bye
docker exec -ti ollama bash -c "ollama run codellama:13b"
```

```bash
>>> ¿que tiempo va a hacer mañana en Madrid?
```
Como la respuesta de un LLM no es determinista (puede variar) da algo parecido a:
```
¡Hola! El pronóstico para mañana en Madrid es el siguiente:

* Temperatura mínima: 10°C
* Temperatura máxima: 25°C
* Velocidad del viento: 10 km/h
* Nubosidad: 40%
* Intensidad de las lluvias: Media

Por lo tanto, mañana en Madrid se espera un día nublado con temperaturas suaves y una ligera brisa del oeste. Sin embargo, es importante tener en cuenta que este
pronóstico puede cambiar con el tiempo y es posible que la información sea diferente a las horas.
```
Esto es porque codellama:13b es un LLM predictivo, usado para código de programación. Su función básica no es buscar información, sino predecir la secuencia de palabras que tiene más sentido estadístico basándose en el prompt que le diste.

Pero si le preguntamos por la temperatura exacta puede decir: (recordad que las respuestas no son deterministas)

```
>>> ¿Cuál es la temperatura exacta AHORA MISMO en Madrid?
```

>No puedo proporcionarte la temperatura exacta en Madrid AHORA MISMO. La información meteorológica actual se basa
en los datos de las estaciones meteorológicas, que pueden estar ubicadas en diferentes puntos de la ciudad y puede
haber un delay entre el momento en que se toma la medición y el momento en que se hace disponible.
>
>Sin embargo, puedo proporcionarte una predicción de la temperatura para Madrid en función de las condiciones
meteorológicas actuales y previstas. Por ejemplo, si la temperatura en Madrid es de 15°C ahora mismo, podría
predecirse que suba a 17°C en los próximos días si la temperatura promedio es de 16°C durante el día y baja a 9°C
por la noche.
>
>Por favor, tenga en cuenta que estas son solo predicciones y que la temperatura real puede variar según las
condiciones meteorológicas específicas y locales.

Para conectar a internet y usar herramientas externas usamos las tools.
Primero generamos un script con python que sea capaz de darnos información. Por ejemplo el script **script_pronostico_temperatura.py** que le pasas como parámetro la ciudad y los días y te da el pronóstico
Para ver como ejecutarlo, lo ejecutyamos sin parámetros:

```
docker exec -ti ollama bash -c "python script_pronostico_temperatura.py"
```

> - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
> PRONOSTICO DE TEMPERATURA - CUALQUIER Ciudad de España
> SIN datos hardcodeados - Busqueda dinamica
> - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
>
>USO: python pronostico_temperatura.py <ciudad> [dias]
>
>EJEMPLOS:
>  python pronostico_temperatura.py Madrid
>  python pronostico_temperatura.py Barcelona 7
>  python pronostico_temperatura.py Mataro 5
>  python pronostico_temperatura.py "San Sebastian" 3
>  python pronostico_temperatura.py Alcobendas 4
>
>CARACTERISTICAS:
>  - Busca CUALQUIER ciudad de España
>  - NO usa datos hardcodeados
>  - Usa OpenStreetMap para geocoding
>  - Usa Open-Meteo para el pronostico (sin API key)
>  - Hasta 16 dias de pronostico

Si queremos sacar el pronóstico de Barcelona de los siguientes 3 días ejecutamos:
```
python script_pronostico_temperatura.py Barcelona 2
```

> - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
>PRONOSTICO DE TEMPERATURA - CUALQUIER Ciudad de España
>SIN datos hardcodeados - Busqueda dinamica
> - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
>
>
>[1/3] Buscando 'Barcelona' en OpenStreetMap...
>[OK] Encontrada: Barcelona
>[OK] Provincia: Catalunya
>[OK] Coordenadas: 41.3826, 2.1771
>
>[2/3] Consultando Open-Meteo...
>[3/3] Procesando datos...
>[OK] Datos recibidos
>
> 
> - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
>PRONOSTICO METEOROLOGICO - BARCELONA
> - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
>
>Viernes    05/12/2025  HOY
>  Temperatura:    9.0°C -  13.4°C
>  Clima:        Nublado
>  Prob. lluvia:   0%
>  Viento:         9.9 km/h
>
>Sabado     06/12/2025  MAÑANA
>  Temperatura:    9.8°C -  19.1°C
>  Clima:        Nublado
>  Prob. lluvia:   8%
>  Viento:        12.5 km/h
>
> - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
>Fuente: Open-Meteo (https://open-meteo.com)
>Geocoding: OpenStreetMap Nominatim
> - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -


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

### Componentes clave:

- **`description`**: Lo que lee el LLM para decidir **cuándo** usar la función
- **`parameters`**: Qué parámetros extrae el LLM de la petición del usuario
- **`required`**: Parámetros obligatorios para el funcionamiento de la tool

El LLM decide "quiero usar esta tool con estos parámetros" y devuelve un json que lo ejecuta el script de python que está escrito debajo de la **TOOL_DEFINITION**.

Un ejemplo de prompt que te recoge la pregunta, separa los parámetros y ejecuta el script (API) para obtener temperatura:
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

El system prompt lo podemos ir definiendo más exactamente cómo debe actuar el agente, podemos añadir instrucciones específicas:
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

## Palabras Clave para Activar la Tool

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

Ejemplo de tool simple para obtener temperatura:
```
python tool__temperatura_minima.py
```

>Escribe /bye para salir, /help para ayuda
>Busca el tiempo de CUALQUIER ciudad de España (sin límites)

Le introducimos la pregunta:
>>> Que temperatura va a hacer mañana en Madrid

Respuesta:

```
[DEBUG] Ollama llamó a la tool 1 vez/veces!
[DEBUG] Función: obtener_pronostico_temperatura
[DEBUG] Argumentos: {'ciudad': 'Madrid', 'dias': '1'}
[FUNC DEBUG] Buscando temperatura para: Madrid, 1 días
[FUNC DEBUG] Buscando ciudad en OpenStreetMap...
[FUNC DEBUG] Resultado: lat=40.416782, lon=-3.703507, nombre=Madrid
[FUNC DEBUG] Llamando a Open-Meteo API...
[FUNC DEBUG] Status code: 200
[FUNC DEBUG] Éxito! Devolviendo pronóstico
[DEBUG] Resultado: Pronóstico para Madrid:
HOY (Viernes): 5-11°C, Lluvia ligera, lluvia 25%, viento 11 km/h...
{"name": "obtener_pronostico_temperatura", "parameters": {"ciudad":"Madrid","dias":"2"}}
```

Otro ejemplo de Tool es tool_temperatura_avanzada.py que no usa llamadas a scripts y tiene todo el código incluido. Busca la ciudad en openstreetMap y luego consulta en open-meteo.

```
python tool_temperatura_avanzada.py
Escribe /bye para salir, /help para ayuda
Busca el tiempo de CUALQUIER ciudad de España (sin límites)
>>> Que temperatura va a hacer mañana en Madrid
[DEBUG] Ollama llamó a la tool 1 vez/veces!
[DEBUG] Función: obtener_pronostico_temperatura
[DEBUG] Argumentos: {'ciudad': 'Madrid', 'dias': '1'}
[FUNC DEBUG] Buscando temperatura para: Madrid, 1 días
[FUNC DEBUG] Buscando ciudad en OpenStreetMap...
[FUNC DEBUG] Resultado: lat=40.416782, lon=-3.703507, nombre=Madrid
[FUNC DEBUG] Llamando a Open-Meteo API...
[FUNC DEBUG] Status code: 200
[FUNC DEBUG] Éxito! Devolviendo pronóstico
[DEBUG] Resultado: Pronóstico para Madrid:
HOY (Viernes): 5-12°C, Nublado, lluvia 25%, viento 12 km/h...
{"name": "obtener_pronostico_temperatura", "parameters": {"ciudad":"Madrid","dias":"1"}}
```

Para poder hacer varias llamadas, tenemos que incluir instrucciones.

A la hora de definir el prompt tenemos definido en tool__temperatura_avanzada.py:
```
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

Ahora le podemos preguntar comparando dos ciudades

```
python tool__temperatura_avanzada.py
Escribe /bye para salir, /help para ayuda
Busca el tiempo de CUALQUIER ciudad de España (sin límites)
>>> ¿Dónde va a hacer mas calor mañana, en Barcelona o en Huesca?
[DEBUG] Ollama llamó a la tool 2 vez/veces!
[DEBUG] Función: obtener_pronostico_temperatura
[DEBUG] Argumentos: {'ciudad': 'Barcelona', 'dias': '1'}
[FUNC DEBUG] Buscando temperatura para: Barcelona, 1 días
[FUNC DEBUG] Buscando ciudad en OpenStreetMap...
[FUNC DEBUG] Resultado: lat=41.3825802, lon=2.177073, nombre=Barcelona
[FUNC DEBUG] Llamando a Open-Meteo API...
[FUNC DEBUG] Status code: 200
[FUNC DEBUG] Éxito! Devolviendo pronóstico
[DEBUG] Resultado: Pronóstico para Barcelona:
HOY (Viernes): 9-14°C, Nublado, lluvia 0%, viento 10 km/h...
[DEBUG] Función: obtener_pronostico_temperatura
[DEBUG] Argumentos: {'ciudad': 'Huesca', 'dias': '1'}
[FUNC DEBUG] Buscando temperatura para: Huesca, 1 días
[FUNC DEBUG] Buscando ciudad en OpenStreetMap...
[FUNC DEBUG] Resultado: lat=42.1360615, lon=-0.0298027, nombre=Huesca
[FUNC DEBUG] Llamando a Open-Meteo API...
[FUNC DEBUG] Status code: 200
[FUNC DEBUG] Éxito! Devolviendo pronóstico
[DEBUG] Resultado: Pronóstico para Huesca:
HOY (Viernes): 3-11°C, Nublado, lluvia 45%, viento 28 km/h...
Basándome en los pronósticos obtenidos, mañana hará más calor en Barcelona que en Huesca. La temperatura máxima prevista para Barcelona es de 14°C, mientras que para Huesca es de 11°C.
```
