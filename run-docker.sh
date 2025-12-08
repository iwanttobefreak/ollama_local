#!/bin/bash
# Script para construir y ejecutar el contenedor Docker de Ollama

set -e

IMAGE_NAME="ollama-python-env"
CONTAINER_NAME="ollama-container"

echo "🐳 Construyendo imagen Docker: $IMAGE_NAME"
echo "=========================================="

# Construir imagen
docker build -t $IMAGE_NAME .

echo ""
echo "🚀 Ejecutando contenedor: $CONTAINER_NAME"
echo "=========================================="

# Detener contenedor anterior si existe
if docker ps -a --format 'table {{.Names}}' | grep -q "^${CONTAINER_NAME}$"; then
    echo "Deteniendo contenedor anterior..."
    docker stop $CONTAINER_NAME || true
    docker rm $CONTAINER_NAME || true
fi

# Ejecutar nuevo contenedor
docker run -d \
    --name $CONTAINER_NAME \
    -p 11434:11434 \
    $IMAGE_NAME

echo ""
echo "⏳ Esperando que el contenedor esté listo..."
sleep 10

echo ""
echo "📊 Estado del contenedor:"
echo "========================"
docker ps | grep $CONTAINER_NAME

echo ""
echo "📝 Logs del contenedor:"
echo "======================"
docker logs $CONTAINER_NAME | tail -20

echo ""
echo "✅ Contenedor listo!"
echo "==================="
echo "🌐 Ollama disponible en: http://localhost:11434"
echo "🐚 Entrar al contenedor: docker exec -it $CONTAINER_NAME bash"
echo "🛑 Detener contenedor: docker stop $CONTAINER_NAME"