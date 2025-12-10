import json
import requests

# 1️⃣ Cargar contexto de Jandro desde JSON
with open("jandro.json", "r") as f:
    jandro = json.load(f)

# 2️⃣ Construir prompt
prompt = f"""
Contexto de la persona:

PERSONA: {jandro['nombre']}
- Relación: {jandro['relacion']}
- Personalidad: {jandro['personalidad']}
- Proyectos: {"; ".join(jandro['proyectos'])}

Instrucciones:
1. Actúa como {jandro['nombre']} en esta conversación.
2. Responde de forma natural y coherente con el contexto.
3. Mantén memoria del contexto durante la conversación.

Usuario: {{usuario_input}}
"""

# 3️⃣ Pregunta que queremos hacer
usuario_input = "¿Dónde vamos a llevar las cajas?"
final_prompt = prompt.replace("{{usuario_input}}", usuario_input)

# 4️⃣ Llamada a Ollama API
response = requests.post(
    "http://localhost:11434/v1/chat",
    json={
        "model": "llama3.1:8b",
        "messages": [
            {"role": "system", "content": final_prompt}
        ]
    }
)

# 5️⃣ Mostrar respuesta
print(response.json()['choices'][0]['message']['content'])

