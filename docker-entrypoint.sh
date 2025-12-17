#!/bin/bash
source /ollama-agente/bin/activate

# Lanza Ollama en background
export OLLAMA_HOST=0.0.0.0:11434
ollama serve &

# Lanza la API (ajusta el comando según tu caso)
#python /app/scrics/api/api_ollama_server.py &

# Espera a que cualquier comando extra (docker exec) se ejecute en este entorno
# Si el contenedor se lanza con un CMD, lo ejecuta; si no, mantiene el shell abierto
if [ "$#" -gt 0 ]; then
  exec "$@"
else
  # Mantén el contenedor vivo con un shell interactivo (opcional)
  exec tail -f /dev/null
fi
