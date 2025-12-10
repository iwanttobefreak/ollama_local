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
ollama serve --host 0.0.0.0 &

# Esperar a que Ollama esté listo
echo "⏳ Esperando que Ollama esté listo..."
sleep 5

# Verificar que Ollama responde
if curl -s http://localhost:11434/api/version > /dev/null; then
    echo "✅ Ollama serve iniciado correctamente en puerto 11434"
else
    echo "⚠️  Ollama serve iniciado, pero no responde aún. Puede tardar unos segundos..."
fi

# Verificar e instalar modelo si es necesario
echo "🤖 Verificando modelos disponibles..."
MODELS_RESPONSE=$(curl -s http://localhost:11434/api/tags)
if echo "$MODELS_RESPONSE" | grep -q "llama3.2:1b"; then
    echo "✅ Modelo llama3.2:1b ya está disponible"
else
    echo "📥 Modelo llama3.2:1b no encontrado. Instalando modelo básico..."
    echo "⏳ Esto puede tardar varios minutos..."
    
    # Instalar un modelo más pequeño y rápido para testing
    ollama pull llama3.2:1b &
    MODEL_PULL_PID=$!
    echo "✅ Descarga de modelo iniciada (PID: $MODEL_PULL_PID)"
    
    # Esperar a que el modelo se descargue (timeout de 5 minutos)
    timeout 300 bash -c "while ! curl -s http://localhost:11434/api/tags | grep -q 'llama3.2:1b'; do sleep 5; done" && echo "✅ Modelo descargado exitosamente" || echo "⚠️  Timeout en descarga de modelo, continuando de todos modos..."
fi

# Iniciar la API de Flask en background
echo "🌐 Iniciando API Ollama Server..."
if [ -f "/app/scrics/api/api_ollama_server.py" ]; then
    echo "📁 Cambiando a directorio: /app/scrics/api"
    cd /app/scrics/api
    echo "📄 Archivo encontrado: $(ls -la api_ollama_server.py)"
    echo "🐍 Ejecutando: python3 api_ollama_server.py"
    echo "🔧 Entorno virtual: $VIRTUAL_ENV"
    echo "🐍 Python path: $(which python3)"
    
    # Ejecutar en background
    python3 api_ollama_server.py &
    API_PID=$!
    echo "✅ API Ollama Server iniciado (PID: $API_PID) en puerto 5000"
else
    echo "⚠️  Archivo api_ollama_server.py no encontrado en /app/scrics/api/"
    ls -la /app/scrics/api/ 2>/dev/null || echo "Directorio no existe"
fi

echo "========================================================"
echo "🎉 Contenedor listo!"
echo "   - Entorno virtual: $VIRTUAL_ENV"
echo "   - Ollama corriendo en: http://localhost:11434"
echo "   - API Flask en: http://localhost:5000"
echo "========================================================"

# Mantener el contenedor corriendo
wait
