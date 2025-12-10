#!/bin/bash
# Script para probar la API de Ollama

echo "🧪 Probando API de Ollama Server"
echo "==============================="

# Verificar que el contenedor esté corriendo
if ! docker ps | grep -q ollama; then
    echo "❌ El contenedor 'ollama' no está corriendo"
    echo "Ejecuta: docker run --rm -d --name ollama -p 11434:11434 -p 5000:5000 --memory=\"16g\" -v /Users/T054810/ollama_local/scrics:/scrics -v /Users/T054810/ia/ollama/usr_local_lib:/usr/local/lib -v /Users/T054810/ia/ollama/root_ollama:/root/.ollama -ti ollama"
    exit 1
fi

echo "✅ Contenedor corriendo"

# Esperar un poco para que la API esté lista
sleep 2

# Probar la API
echo ""
echo "📤 Probando endpoint /preguntar..."
echo "=================================="

curl -X POST http://localhost:5000/preguntar \
     -H "Content-Type: application/json" \
     -d '{"persona":"jandro", "pregunta":"¿Como se llama mi padre"}' \
     -w "\n📊 HTTP Status: %{http_code}\n"

echo ""
echo "🎉 Prueba completada"