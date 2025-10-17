Uso de tools sencillas
¿Que es una tool?
Es una herramienta para que el LLM realice llamadas externas que no conoce como LLM, cosas dinámicas, por ejemplo operaciones matemáticas, consultas del tiempo, programación de TV, 

```
# Tool definition para Ollama
TOOL_DEFINITION = {
    'type': 'function',
    'function': {
        'name': 'obtener_pronostico_temperatura',
        'description': 'SOLO usar cuando el usuario pregunta específicamente por el TIEMPO, CLIMA, TEMPERATURA, LLUVIA o PRON▒~SSTICO meteorológico de una ciudad ESPA▒~QOLA. Funcii
ona con CUALQUIER ciudad de España. NO usar para otras preguntas generales.',
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

Prueba 1
Con una tool que tiene integrado la consulta del tiempo
