#!/bin/bash
source /ollama-agente/bin/activate

# Lanza Ollama en background
ollama serve &

# Lanza la API (ajusta el comando según tu caso)
python /app/scrics/chats/api_ollama_server.py &

# Espera a que cualquier comando extra (docker exec) se ejecute en este entorno
# Si el contenedor se lanza con un CMD, lo ejecuta; si no, mantiene el shell abierto
if [ "$#" -gt 0 ]; then
  exec "$@"
else
  # Mantén el contenedor vivo con un shell interactivo (opcional)
  exec bash
fi