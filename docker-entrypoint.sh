#!/bin/bash
set -e

echo "🚀 Iniciando contenedor Ollama con entorno Python virtual..."
echo "========================================================"

# Verificar que el entorno virtual existe
if [ ! -d "/ollama-agente" ]; then
    echo "❌ Error: Entorno virtual no encontrado en /ollama-agente"
    exit 1
fi

# Activar entorno virtual
echo "🔧 Activando entorno virtual Python..."
source /ollama-agente/bin/activate

# Verificar activación
if [ -z "$VIRTUAL_ENV" ]; then
    echo "❌ Error: No se pudo activar el entorno virtual"
    exit 1
fi

echo "✅ Entorno virtual activado: $VIRTUAL_ENV"
echo "   Python: $(which python3)"
echo "   Pip: $(which pip)"

# Verificar que las dependencias están instaladas
echo "📦 Verificando dependencias Python..."
python3 -c "import ollama, mcp; print('✅ Dependencias OK')" || {
    echo "❌ Error: Dependencias Python no instaladas correctamente"
    exit 1
}

# Verificar que Ollama está instalado
if ! command -v ollama &> /dev/null; then
    echo "❌ Error: Ollama no está instalado"
    exit 1
fi

echo "🤖 Ollama instalado correctamente"
echo "========================================================"

# Iniciar Ollama serve en background
echo "🌐 Iniciando Ollama serve..."
ollama serve &

# Esperar a que Ollama esté listo
echo "⏳ Esperando que Ollama esté listo..."
sleep 5

# Verificar que Ollama está respondiendo
if curl -s http://localhost:11434/api/version > /dev/null; then
    echo "✅ Ollama serve iniciado correctamente en puerto 11434"
else
    echo "⚠️  Ollama serve iniciado, pero no responde aún. Puede tardar unos segundos..."
fi

# Iniciar la API de Flask en background
echo "🌐 Iniciando API Ollama Server..."
if [ -f "/scrics/chats/api_ollama_server.py" ]; then
    cd /scrics/chats
    python3 api_ollama_server.py &
    API_PID=$!
    echo "✅ API Ollama Server iniciado (PID: $API_PID) en puerto 5000"
else
    echo "⚠️  Archivo api_ollama_server.py no encontrado en /scrics/chats/"
fi

echo "========================================================"
echo "🎉 Contenedor listo!"
echo "   - Entorno virtual: $VIRTUAL_ENV"
echo "   - Ollama corriendo en: http://localhost:11434"
echo "   - API Server corriendo en: http://localhost:5000"
echo "========================================================"

# Función para manejar señales de terminación
cleanup() {
    echo "🛑 Recibida señal de terminación. Deteniendo servicios..."
    if [ ! -z "$API_PID" ]; then
        kill $API_PID 2>/dev/null || true
        echo "✅ API Server detenido"
    fi
    pkill -f "ollama serve" 2>/dev/null || true
    echo "✅ Ollama serve detenido"
    exit 0
}

# Configurar manejador de señales
trap cleanup SIGTERM SIGINT

# Mantener el contenedor corriendo y supervisar procesos
echo "👀 Supervisando servicios..."
while true; do
    # Verificar que Ollama sigue corriendo
    if ! pgrep -f "ollama serve" > /dev/null; then
        echo "❌ Ollama serve se detuvo. Reiniciando..."
        ollama serve &
    fi

    # Verificar que la API sigue corriendo (si se inició)
    if [ ! -z "$API_PID" ] && ! kill -0 $API_PID 2>/dev/null; then
        echo "❌ API Server se detuvo. Reiniciando..."
        cd /scrics/chats
        python3 api_ollama_server.py &
        API_PID=$!
        echo "✅ API Server reiniciado (PID: $API_PID)"
    fi

    sleep 10
done