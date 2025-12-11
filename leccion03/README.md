Arranco ollama bridge para conectar dar configuración para conectar al MCP server pasándole el fichero de configuración:
ollama-mcp-bridge --config /app/scrics/tools/mcp-bridge-config.json

y me dice:
2025-12-11 10:03:25.856 | INFO     | ollama_mcp_bridge.mcp_manager:_connect_server:66 - Connected to 'filesystem' with 14 tools

Levantamos el chat con mcp-server
python /app/scrics/tools/mcp-chat.py

```bash
>>> ¿Que ficheros hay en /tmp/?
```

