# 🛠️ Uso de Tools Sencillas

## 🤔 ¿Qué es una Tool?

Una **tool** (herramienta) es una funcionalidad que permite al LLM realizar **llamadas externas** a recursos que no conoce como modelo de lenguaje. Se utiliza para obtener información **dinámica** o ejecutar operaciones específicas.

### 📋 Ejemplos comunes de tools:
- 🧮 **Operaciones matemáticas** complejas
- 🌤️ **Consultas meteorológicas** en tiempo real
- 📺 **Programación de TV** actualizada
- 💻 **Comandos del sistema** (`ls`, `ps`, etc.)
- 🌐 **Llamadas a APIs** externas
- 📊 **Consultas a bases de datos**

---

## 📝 Definición Básica

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
