#!/bin/bash
# Script para gestionar el contenedor Docker de Ollama

set -e

CONTAINER_NAME="ollama"
OLLAMA_COMMAND="docker run --rm -d --name ${CONTAINER_NAME} -p 11434:11434 -p 5000:5000 --memory=\"16g\" -v /Users/T054810/ollama_local/scrics:/scrics -v /Users/T054810/ia/ollama/usr_local_lib:/usr/local/lib -v /Users/T054810/ia/ollama/root_ollama:/root/.ollama -ti ollama"

echo "🐳 Gestionando contenedor Ollama"
echo "==============================="

# Función para verificar si el contenedor existe
container_exists() {
    docker ps -a --format 'table {{.Names}}' | grep -q "^${CONTAINER_NAME}$"
}

# Función para verificar si el contenedor está corriendo
container_running() {
    docker ps --format 'table {{.Names}}' | grep -q "^${CONTAINER_NAME}$"
}

# Detener contenedor si existe
if container_exists; then
    echo "🛑 Deteniendo contenedor existente..."
    docker stop ${CONTAINER_NAME} 2>/dev/null || true
    docker rm ${CONTAINER_NAME} 2>/dev/null || true
    echo "✅ Contenedor detenido y eliminado"
fi

echo "🚀 Iniciando nuevo contenedor..."
echo "Comando: ${OLLAMA_COMMAND}"
echo ""

# Ejecutar el contenedor
CONTAINER_ID=$(${OLLAMA_COMMAND})

if [ $? -eq 0 ]; then
    echo "✅ Contenedor iniciado correctamente"
    echo "   ID: ${CONTAINER_ID}"
    echo ""
    echo "📊 Estado del contenedor:"
    docker ps | grep ${CONTAINER_NAME}
    echo ""
    echo "📝 Comandos útiles:"
    echo "   Ver logs: docker logs ${CONTAINER_NAME}"
    echo "   Entrar: docker exec -it ${CONTAINER_NAME} bash"
    echo "   Detener: docker stop ${CONTAINER_NAME}"
    echo ""
    echo "🌐 Servicios disponibles:"
    echo "   Ollama API: http://localhost:11434"
    echo "   Flask API: http://localhost:5000"
    echo ""
    echo "⏳ Esperando que los servicios estén listos..."
    sleep 10

    # Verificar que los servicios respondan
    echo "🔍 Verificando servicios..."

    if curl -s http://localhost:11434/api/version > /dev/null 2>&1; then
        echo "✅ Ollama API responde correctamente"
    else
        echo "⚠️  Ollama API no responde aún"
    fi

    if curl -s http://localhost:5000 > /dev/null 2>&1; then
        echo "✅ Flask API responde correctamente"
    else
        echo "⚠️  Flask API no responde aún"
    fi

    echo ""
    echo "🎉 ¡Contenedor listo!"
else
    echo "❌ Error al iniciar el contenedor"
    exit 1
fi