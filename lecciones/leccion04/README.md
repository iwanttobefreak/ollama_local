**Persistencia en modelos LLM**

Cuando le haces una pregunta al LLM le pasas dos prompts:
- System Prompt
- User Prompt

El System prompt puedes meter como quieres que te conteste el LLM y algo de contexto. Los LLMs tienen un cierto número de tokens. 

| Modelo | Contexto (tokens) | Contexto (palabras) | Equivalente en páginas | Tamaño GB | Especialidad |
|-------|------------------|-------------------|----------------------|-----------|-------------|
| qwen2.5-coder:7b | 32K | ~24K | ~100 | 4.7 GB | Programación |
| qwen2.5:7b | 32K | ~24K | ~100 | 4.7 GB | Generalista |
| qwen3:32b | 32K-128K | 24K-96K | 100-400 | 20 GB | Generalista |
| llama3.1:8b | 128K | ~96K | ~400 | 4.9 GB | Versátil |
| llama3.2:1b | 128K | ~96K | ~400 | 1.3 GB | Rápido/Ligero |
| codellama:13b | 16K | ~12K | ~50 | 7.4 GB | Programación |

Notas:
- 1 token ≈ 0.75 palabras
- 1 página ≈ 250 palabras

Una vez que le haces una pregunta a un LLM, en la segunda pregunta no se acuerda de lo que le has preguntado en la primera, en las aplicaciones de chat, se suele enviar la respuesta en el contexto, pero como tiene una limitación de tamaño, lo que va haciendo es comprimir el contexto cada vez, por eso cuando la conversación es muy larga, pierde contexto y empieza a alucinar y dar respuestas incorrectas.

Si lo haces vía API, esa gestión del contexto la tienes que hacer tú a mano.

**Ejemplos con la API generate**

Por ejemplo, si le preguntamos cual es la capital de Francia:
```bash
curl --silent -X POST http://localhost:11434/api/generate -H "Content-Type: application/json" -d '{
  "model": "llama3.2:1b",
  "prompt": "¿Cuál es la capital de Francia?",
  "stream": false
}'|jq
```

```json
{
  "model": "llama3.2:1b",
  "created_at": "2025-12-16T09:39:38.035885038Z",
  "response": "La capital de Francia es París.",
  "done": true,
  "done_reason": "stop",
  "context": [
    128006,
    ...
    13
  ],
  "total_duration": 241696430,
  "load_duration": 73168596,
  "prompt_eval_count": 35,
  "prompt_eval_duration": 12144120,
  "eval_count": 10,
  "eval_duration": 152626650
}
```

Y si ahora le preguntamos por la población sin nombrar que es París, no se acuerda de la respuesta anterior:
```bash
curl --silent -X POST http://localhost:11434/api/generate -H "Content-Type: application/json" -d '{
  "model": "llama3.2:1b",
  "prompt": "¿Y cuál es su población?",
  "stream": false
}'|jq
```

```json
{
  "model": "llama3.2:1b",
  "created_at": "2025-12-16T09:40:04.208458353Z",
  "response": "No tengo información sobre un lugar o entidad específica que sea \"el centro de la pregunta\". ¿Podrías proporcionar más contexto o detalles sobre a qué te refieres con \"su población\"? Estoy aquí para ayudarte.",
  "done": true,
  "done_reason": "stop",
  "context": [
    128006,
    ...
    13
  ],
  "total_duration": 979567221,
  "load_duration": 72752593,
  "prompt_eval_count": 34,
  "prompt_eval_duration": 70885415,
  "eval_count": 49,
  "eval_duration": 821623158
}
```

En la respuesta da un array de números como contexto, que podemos usar para la siguiente pregunta, vamos a guardarlos en variables, primero toda la respuesta en la variable $peticion:
```bash
peticion=$(curl -s -X POST http://localhost:11434/api/generate \
  -H "Content-Type: application/json" \
  -d '{
    "model": "llama3.2:1b",
    "prompt": "¿Cuál es la capital de Francia?",
    "stream": false
  }')
```

Ahora sacamos la respuesta y el contexto:
```bash
respuesta=$(echo "$peticion" | jq -r '.response')
contexto=$(echo "$peticion" | jq -c '.context')
```
Podemos ver el valor con
```bash
echo $respuesta
echo $contexto
```

Usamos el contexto en la segunda petición:
```bash
curl -s -X POST http://localhost:11434/api/generate \
  -H "Content-Type: application/json" \
  -d "{
    \"model\": \"llama3.2:1b\",
    \"prompt\": \"¿Y cuál es su población?\",
    \"context\": $contexto,
    \"stream\": false
  }"|jq
```

**Ejemplos con la API chat**
En la api de chat tenemos 3 roles:
| Rol | Propósito | Cuándo usarlo | Ejemplo |
|-----|-----------|---------------|---------|
| system | Define la personalidad y comportamiento del asistente | Al inicio, solo una vez | "Eres un experto en programación que responde con ejemplos de código." |
| user | Preguntas y comandos del usuario | Para todas las preguntas/peticiones | "¿Cómo hago un loop for en Python?" |
| assistant | Respuestas anteriores del asistente | Para mantener historial de conversación | "Aquí tienes un ejemplo:\n\\`\`python\nfor i in range(10):\n    print(i)\n\`\`\`"` |

Le hacemos una pregunta sencilla:
```bash
curl --silent -X POST http://localhost:11434/api/chat -H "Content-Type: application/json" -d '{
  "model": "llama3.2:1b",
  "messages": [
    {"role": "user", "content": "¿Cuál es la capital de Francia?"}
  ],
  "stream": false
}'|jq
```

Respuesta:
```json
{
  "model": "llama3.2:1b",
  "created_at": "2025-12-16T10:31:35.362043615Z",
  "message": {
    "role": "assistant",
    "content": "La capital de Francia es París."
  },
  "done": true,
  "done_reason": "stop",
  "total_duration": 362241403,
  "load_duration": 73432820,
  "prompt_eval_count": 35,
  "prompt_eval_duration": 118322717,
  "eval_count": 10,
  "eval_duration": 166679383
}
````

Añadimos la respuesta (y su pregunta) en el contexto de la siguiente pregunta con el rol user y assistant (que es mas o menos lo que hace el chat modo interactivo, no vía API)
```bash
curl --silent -X POST http://localhost:11434/api/chat -H "Content-Type: application/json" -d '{
  "model": "llama3.2:1b",
  "messages": [
    {"role": "user", "content": "¿Cuál es la capital de Francia?"},
    {"role": "assistant", "content": "La capital de Francia es París."},
    {"role": "user", "content": "¿Y cuál es su población?"}
  ],
  "stream": false
}'|jq
```
Respuesta:
```json
{
  "model": "llama3.2:1b",
  "created_at": "2025-12-16T10:33:30.062625844Z",
  "message": {
    "role": "assistant",
    "content": "Según los últimos datos del Instituto Nacional de Estadística (Institut National de Statistique, ISTAT) de 2020, la población de París es aproximadamente 2,167 millones de habitantes. Sin embargo, es importante destacar que la población de Francia en general es mucho mayor, con un total de alrededor de 67 millones de habitantes según el Instituto Nacional de Estadística (Institut National de Statistique) de 2020."
  },
  "done": true,
  "done_reason": "stop",
  "total_duration": 1908418371,
  "load_duration": 73489577,
  "prompt_eval_count": 63,
  "prompt_eval_duration": 100789938,
  "eval_count": 104,
  "eval_duration": 1702920175
}
```

Y así ir añadiendo todas las preguntas en el contexto, que es grande, pero no infinito y tiene sus limitaciones.

Podríamos crear una función y una API que nos fuera comprimiendo o resumiendo el contexto, pero asumiendo que se pierde información.

Le pasamos la conversación en la variable $conversacion y definimos el role de system como:

**Resume esta conversación manteniendo solo información esencial: nombres, fechas, datos clave y decisiones importantes. Sé breve.**


```bash
curl -s -X POST http://localhost:11434/api/chat \
    -H "Content-Type: application/json" \
    -d '{
        "model": "llama3.2:1b",
        "messages": [
            {"role": "system", "content": "Resume esta conversación manteniendo solo información esencial: nombres, fechas, datos clave y decisiones importantes. Sé breve."},
            {"role": "user", "content": "'$conversacion'"}
        ],
        "stream": false
    }' | jq -r '.message.content'
```

Y podemos crear una estrategia de compresión:
1. Cada 10-15 mensajes → genera resumen
2. Mantener últimos 5-7 mensajes completos
3. Reemplazar el resto con resumen como system
4. Si >25 mensajes → compresión más agresiva

Esto está bien para una conversación dinámica, pero si queremos un contexto mas o menos fijo, estable o lo queremos alimentar con documentos usamos RAG (lección 5)
 