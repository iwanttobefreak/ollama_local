Uso de tools sencillas
¿Que es una tool?
Es una herramienta para que el LLM realice llamadas externas que no conoce como LLM, cosas dinámicas, por ejemplo operaciones matemáticas, consultas del tiempo, programación de TV,.... En general, ejecutar un comando, que puede ser un comando de sistema (un ls), una llamada a una api, .....

Definición básica

```
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
La description es lo que lee el LLM para decidir cuando usar la función
En parameters ponemos que parámetros coge LLM de la petición.

Parámetros útiles
Podemos añadir una explicación al system_prompt para definir mas exactamente como tiene que actuar el agente:
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

Palabras clave para activar esta tool
```
KEYWORDS = [
    'temperatura', 'tiempo', 'clima', 'lluvia', 'viento',
    'pronostico', 'pronóstico', 'calor', 'frio', 'frío',
    'grados', 'soleado', 'nublado', 'despejado', 'meteorolog',
    'nevar', 'nieve', 'tormenta', 'cielo',
    'semana', 'hoy', 'mañana', 'hará', 'estará'
]
```
