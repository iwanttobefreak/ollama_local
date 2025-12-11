Hacemos una pregunta al LLM local, con comando docker, API o prompt (como hemos visto en la creación del docker en la lección 0):
**NOTA: Pongo los comandos con "bash -c" para que se vea mas claro que se ejecuta, pero se puede ejecutar sin, da igual cualquiera de los dos, pero "ollama ollama" es un poco repetitivo XD:
```bash
docker exec -ti ollama bash -c "ollama run llama3.1:8b"
docker exec -ti ollama ollama run llama3.1:8b
```

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
docker exec -ti ollama bash -c "python /app/scrics/tools/pronostico_temperatura.py"
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
docker exec -ti ollama bash -c "python /app/scrics/tools/pronostico_temperatura.py Barcelona 2"
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

Hasta aquí solo es python, no hay IA.

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
        ['python3', 'pronostico_temperatura.py', ciudad],
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
docker exec -ti ollama bash -c "python /app/scrics/tools/tool_temperatura.py"
```

```
=== TOOL CLIMA POC ===

Introduce una pregunta sobre el clima (o escribe 'salir' para terminar):
>>>
```

Le introducimos la misma pregunta que antes que no supo responder:
```
>>>  ¿que tiempo va a hacer mañana en Barcelona?
```

Respuesta:

```
[DEBUG] Pregunta recibida: ¿que tiempo va a hacer mañana en Barcelona?
[DEBUG] Prompt enviado al LLM:
  - role: user, content: ¿que tiempo va a hacer mañana en Barcelona?
[DEBUG] Tool definition disponible: consultar_clima
[DEBUG] Llamando al LLM (Ollama) con tools...
[DEBUG] Respuesta completa del LLM:
  - role: assistant
  - content:
  - tool_calls: [ToolCall(function=Function(name='consultar_clima', arguments={'ciudad': 'Barcelona', 'dias': '1'}))]
[DEBUG] El LLM ha decidido llamar a la tool porque la pregunta coincide con la descripción y parámetros definidos.
[DEBUG] tool_call: function=Function(name='consultar_clima', arguments={'ciudad': 'Barcelona', 'dias': '1'})
[DEBUG] Argumentos extraídos: ciudad=Barcelona, dias=1
[DEBUG] Ejecutando script externo para: Barcelona (1 dias)
[DEBUG] Resultado del script: ======================================================================
PRONOSTICO DE TEMPERATURA - C...
[DEBUG] Enviando resultado de la tool al LLM para respuesta final...
[DEBUG] Respuesta final del LLM:
  - role: assistant
  - content: El pronóstico del tiempo para Barcelona mañana es de niebla con una temperatura de 6,7°C a 19,6°C y una probabilidad de lluvia del 0%. El viento será suave con una velocidad de 8 km/h.

Respuesta: El pronóstico del tiempo para Barcelona mañana es de niebla con una temperatura de 6,7°C a 19,6°C y una probabilidad de lluvia del 0%. El viento será suave con una velocidad de 8 km/h.
```

Vemos en la respuesta del LLM que ha decidido llamar a la tool con unos parámetros:
```
  - tool_calls: [ToolCall(function=Function(name='consultar_clima', arguments={'ciudad': 'Barcelona', 'dias': '1'}))]
```
Si hacemos una llamada que no necesita la tool:
```bash
Introduce una pregunta sobre el clima (o escribe 'salir' para terminar):
>>> ¿Cual es la capital de Francia?
```
Respuesta:
```
[DEBUG] Pregunta recibida: ¿Cual es la capital de Francia?
[DEBUG] Prompt enviado al LLM:
  - role: user, content: ¿Cual es la capital de Francia?
[DEBUG] Tool definition disponible: consultar_clima
[DEBUG] Llamando al LLM (Ollama) con tools...
[DEBUG] Respuesta completa del LLM:
  - role: assistant
  - content: No se puede responder a esta pregunta con las funciones proporcionadas, ya que no hay ninguna función relacionada con geografia o demografia. La función "consultar_clima" solo se utiliza para consultar el clima en una ciudad española. Si deseas obtener la información sobre la capital de Francia, necesitaría tener acceso a otras fuentes de información.

Sin embargo, si quieres una respuesta aproximada, podrías utilizar otra fuente de información o hacer una pregunta relacionada con geografia o demografia que esté dentro del alcance de las funciones proporcionadas.
  - tool_calls: None
[DEBUG] El LLM NO ha solicitado llamar a la tool. Esto ocurre porque la pregunta no coincide con la descripción de la tool o los parámetros requeridos.
[DEBUG] Respuesta directa del LLM: No se puede responder a esta pregunta con las funciones proporcionadas, ya que no hay ninguna función relacionada con geografia o demografia. La función "consultar_clima" solo se utiliza para consultar el clima en una ciudad española. Si deseas obtener la información sobre la capital de Francia, necesitaría tener acceso a otras fuentes de información.

Sin embargo, si quieres una respuesta aproximada, podrías utilizar otra fuente de información o hacer una pregunta relacionada con geografia o demografia que esté dentro del alcance de las funciones proporcionadas.

Respuesta: No se puede responder a esta pregunta con las funciones proporcionadas, ya que no hay ninguna función relacionada con geografia o demografia. La función "consultar_clima" solo se utiliza para consultar el clima en una ciudad española. Si deseas obtener la información sobre la capital de Francia, necesitaría tener acceso a otras fuentes de información.

Sin embargo, si quieres una respuesta aproximada, podrías utilizar otra fuente de información o hacer una pregunta relacionada con geografia o demografia que esté dentro del alcance de las funciones proporcionadas.
```

Dependiendo de la definición de la tool, elige llamar o no a la tool, Se puede afinar y entrenar por si se hacen las preguntas de diferente tipo. Por ejemplo con esta pregunta no lanza la tool:
```
¿va a llover en Barcelona el sábado?
```
Pero con esta otra si:
```
¿va a haber lluvia en Barcelona el sábado?
```
En la definición de las palabras claves en **tool_temperatura.py** si tenemos definido lluvía pero no llover:
```
    # Palabras que Si indican clima
    palabras_clima = ['temperatura', 'clima', 'tiempo', 'lluvia', 'calor', 'frio', 'humedad', 'viento', 'nublado', 'sol', 'meteorologico', 'pronostico', 'manana', 'semana']
```
Podríamos coger pregunts que creemos que si son de clima y pedir a una IA que nos modifique la tool para que las incluya, por ejemplo estas preguntas, que saque palabras clave, ejemplos.... o lo podemos hacer a mano:
```
¿Va a llover mañana en Barcelona?
¿Habrá tormenta en Madrid esta semana?
¿Cuál es la probabilidad de nieve en Huesca?
¿El cielo estará despejado en Valencia mañana?
¿Qué velocidad tendrá el viento en Bilbao?
¿Cómo estará el clima en Sevilla el domingo?
¿Va a hacer sol en Málaga el sábado?
¿Cuál será la humedad en Zaragoza mañana?
```

Si le pedimos comparativas también las hace:
```
>>> Dónde va a hacer mas calor mañana, ¿En Madrid o en Bsrcelona?
```

Vemos que en tool_calls vienen 2 llamadas:
```
  - tool_calls: [
    ToolCall(function=Function(name='consultar_clima', arguments={'ciudad': 'Madrid', 'dias': '1'})), 
    ToolCall(function=Function(name='consultar_clima', arguments={'ciudad': 'Barcelona', 'dias': '1'}))
    ]
```

Podemos hacer la tool sin scripts externos, que todo venga incluido en el mismo fichero:

```
>>> ¿Dónde va a hacer mas temperatura la semana que viene? ¿En Barcelona o Zamora?
[DEBUG] Pregunta recibida: ¿Dónde va a hacer mas temperatura la semana que viene? ¿En Barcelona o Zamora?
[DEBUG] Prompt enviado al LLM:
  - role: user, content: ¿Dónde va a hacer mas temperatura la semana que viene? ¿En Barcelona o Zamora?
[DEBUG] Tool definition disponible: consultar_clima
[DEBUG] Llamando al LLM (Ollama) con tools...
[DEBUG] Respuesta completa del LLM:
  - role: assistant
  - content:
  - tool_calls: [
      function=Function(name='consultar_clima', arguments={'ciudad': 'Barcelona', 'dias': '7'}),
      function=Function(name='consultar_clima', arguments={'ciudad': 'Zamora', 'dias': '7'}),
    ]
[DEBUG] El LLM ha decidido llamar a la tool porque la pregunta coincide con la descripción y parámetros definidos.
[DEBUG] tool_call: function=Function(name='consultar_clima', arguments={'ciudad': 'Barcelona', 'dias': '7'})
[DEBUG] Argumentos extraídos: ciudad=Barcelona, dias=7
[DEBUG] Ejecutando función interna para: Barcelona (7 dias)
[DEBUG] Llamando a Nominatim: https://nominatim.openstreetmap.org/search params={'q': 'Barcelona, España', 'format': 'json', 'limit': 5, 'addressdetails': 1}
[DEBUG] Respuesta Nominatim status=200
[DEBUG] Respuesta Nominatim JSON: [{'place_id': 76094835, 'licence': 'Data © OpenStreetMap contributors, ODbL 1.0. http://osm.org/copyright', 'osm_type': 'relation', 'osm_id': 347950, 'lat': '41.3825802', 'lon': '2.1770730', 'class': 'boundary', 'type': 'administrative', 'place_rank': 16, 'importance': 0.8035003209691789, 'addresstype': 'city', 'name': 'Barcelona', 'display_name': 'Barcelona, Barcelonès, Barcelona, Catalunya, España', 'address': {'city': 'Barcelona', 'county': 'Barcelonès', 'province': 'Barcelona', 'ISO3166-2-lvl6': 'ES-B', 'state': 'Catalunya', 'ISO3166-2-lvl4': 'ES-CT', 'country': 'España', 'country_code': 'es'}, 'boundingbox': ['41.3170353', '41.4679135', '2.0524977', '2.2283555']}, {'place_id': 74703056, 'licence': 'Data © OpenStreetMap contributors, ODbL 1.0. http://osm.org/copyright', 'osm_type': 'relation', 'osm_id': 349035, 'lat': '41.7578700', 'lon': '2.0311820', 'class': 'boundary', 'type': 'administrative', 'place_rank': 10, 'importance': 0.6327090619193868, 'addresstype': 'province', 'name': 'Barcelona', 'display_name': 'Barcelona, Catalunya, España', 'address': {'province': 'Barcelona', 'ISO3166-2-lvl6': 'ES-B', 'state': 'Catalunya', 'ISO3166-2-lvl4': 'ES-CT', 'country': 'España', 'country_code': 'es'}, 'boundingbox': ['41.1927078', '42.3233011', '1.3603839', '2.7780029']}]
[DEBUG] Ciudad encontrada: Barcelona lat=41.3825802 lon=2.177073
[DEBUG] Llamando a Open-Meteo: https://api.open-meteo.com/v1/forecast params={'latitude': 41.3825802, 'longitude': 2.177073, 'daily': 'temperature_2m_max,temperature_2m_min,precipitation_probability_max,weathercode,windspeed_10m_max', 'timezone': 'Europe/Madrid'}
[DEBUG] Respuesta Open-Meteo status=200
[DEBUG] Respuesta Open-Meteo JSON: {'latitude': 41.4375, 'longitude': 2.1875, 'generationtime_ms': 0.1983642578125, 'utc_offset_seconds': 3600, 'timezone': 'Europe/Madrid', 'timezone_abbreviation': 'GMT+1', 'elevation': 30.0, 'daily_units': {'time': 'iso8601', 'temperature_2m_max': '°C', 'temperature_2m_min': '°C', 'precipitation_probability_max': '%', 'weathercode': 'wmo code', 'windspeed_10m_max': 'km/h'}, 'daily': {'time': ['2025-12-10', '2025-12-11', '2025-12-12', '2025-12-13', '2025-12-14', '2025-12-15', '2025-12-16'], 'temperature_2m_max': [19.4, 16.9, 16.7, 16.0, 15.4, 16.3, 16.8], 'temperature_2m_min': [6.7, 7.1, 7.8, 7.4, 6.4, 7.1, 7.2], 'precipitation_probability_max': [0, 0, 5, 4, 5, 31, 34], 'weathercode': [45, 45, 45, 45, 45, 45, 45], 'windspeed_10m_max': [7.7, 9.0, 7.0, 8.0, 7.3, 7.4, 7.9]}}
[DEBUG] Resultado de la función: Pronostico de temperatura para Barcelona:

Miercoles 10/12/2025 (HOY):
  Temperatura: 6.7°C - 19.4°C...
[DEBUG] Enviando resultado de la tool al LLM para respuesta final...
[DEBUG] Respuesta final del LLM:
  - role: assistant
  - content: Según el pronóstico del clima para la semana que viene, Barcelona tendrá una temperatura media alrededor de 12°C con algunas lluvias y niebla en algunos días. Zamora tendrá un promedio de temperatura de 4°C con precipitaciones. Por lo tanto, la ciudad que hará más temperatura será Barcelona.

Respuesta: Según el pronóstico del clima para la semana que viene, Barcelona tendrá una temperatura media alrededor de 12°C con algunas lluvias y niebla en algunos días. Zamora tendrá un promedio de temperatura de 4°C con precipitaciones. Por lo tanto, la ciudad que hará más temperatura será Barcelona.
```