import requests

MCP_CHAT_URL = "http://localhost:8000/api/chat"

def enviar_orden_mcp(orden):
    payload = {
        "model": "qwen2.5:latest",
        "messages": [
            {"role": "system", "content": "Eres un mcp server de git"},
            {"role": "user", "content": orden}
        ],
        "stream": False,
        "options": {
            "temperature": 0.7,
            "top_p": 0.9
        }
    }
    resp = requests.post(MCP_CHAT_URL, json=payload)
    if resp.ok:
        print("[RESPUESTA MCP]")
        print(resp.text)
        try:
            data = resp.json()
            content = data.get("message", {}).get("content", "")
            if content:
                print("\n[RESPUESTA FORMATEADA]")
                print(content)
        except Exception as e:
            print(f"[DEBUG] No se pudo formatear la respuesta: {e}")
    else:
        print("[ERROR]")
        print(resp.text)

def main():
    print("Prompt MCP server (filesystem). Escribe tu orden (exit para salir):")
    while True:
        orden = input(">>> ").strip()
        if orden.lower() in ("exit", "salir", "quit"):
            break
        enviar_orden_mcp(orden)

if __name__ == "__main__":
    main()

