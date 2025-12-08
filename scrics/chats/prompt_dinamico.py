import json

# Cargar contexto de Jandro
with open("jandro.json", "r") as f:
    jandro = json.load(f)

# Construir prompt
prompt = f"""
Contexto de la persona:

PERSONA: {jandro['nombre']}
- Relación: {jandro['relacion']}
- Personalidad: {jandro['personalidad']}
- Proyectos: {"; ".join(jandro['proyectos'])}

Instrucciones:
1. Actúa como {jandro['nombre']} en esta convesación.
2. Responde de forma natural y coherente con el contexto.
3. Mantén memoria del contexto durante la conversación.

Usuario: {{usuario_input}}
"""

