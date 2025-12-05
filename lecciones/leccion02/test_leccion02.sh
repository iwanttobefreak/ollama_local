#!/bin/bash
# Script para probar la Lección 2 - MCP Servers

echo "============================================================"
echo "  LECCIÓN 2: MCP Servers - Script de Prueba"
echo "============================================================"
echo ""

# Verificar si estamos en el directorio correcto
if [ ! -f "mcp_client_minimo.py" ]; then
    echo "❌ Error: Debes ejecutar este script desde el directorio leccion02"
    exit 1
fi

# Verificar Python
if ! command -v python3 &> /dev/null; then
    echo "❌ Error: Python 3 no está instalado"
    exit 1
fi

echo "✅ Python encontrado: $(python3 --version)"
echo ""

# Verificar Docker y Ollama (opcional)
echo "🐳 Verificando Docker y Ollama..."
if command -v docker &> /dev/null; then
    echo "✅ Docker instalado"
    if docker ps | grep -q ollama; then
        echo "✅ Contenedor Ollama corriendo"
    else
        echo "⚠️  Contenedor Ollama no está corriendo"
        echo "   Para iniciarlo: docker start ollama"
    fi
else
    echo "⚠️  Docker no encontrado (necesario para Ollama)"
fi
echo ""

# Instalar dependencias
echo "📦 Instalando dependencias..."
pip3 install -q mcp ollama 2>/dev/null
if [ $? -eq 0 ]; then
    echo "✅ Dependencias instaladas"
else
    echo "⚠️  Algunas dependencias pueden no haberse instalado correctamente"
fi
echo ""

# Menú de opciones
echo "============================================================"
echo "¿Qué ejemplo quieres ejecutar?"
echo "============================================================"
echo ""
echo "1) Ejemplo MÍNIMO (sin Ollama, solo MCP)"
echo "2) Ejemplo COMPLETO (con Ollama y temperatura)"
echo "3) Instalar dependencias solamente"
echo "4) Salir"
echo ""
read -p "Selecciona una opción (1-4): " opcion

case $opcion in
    1)
        echo ""
        echo "🧪 Ejecutando ejemplo mínimo..."
        echo "============================================================"
        python3 mcp_client_minimo.py
        ;;
    2)
        echo ""
        echo "🌡️  Ejecutando ejemplo completo de temperatura..."
        echo "============================================================"
        echo "Asegúrate de que Ollama esté corriendo:"
        echo "  - Docker: docker start ollama"
        echo "  - Local: ollama serve"
        echo ""
        read -p "¿Continuar? (s/n): " continuar
        if [ "$continuar" = "s" ] || [ "$continuar" = "S" ]; then
            python3 mcp_client_temperatura.py
        fi
        ;;
    3)
        echo ""
        echo "📦 Instalando todas las dependencias..."
        pip3 install -r requirements.txt
        echo "✅ Instalación completa"
        ;;
    4)
        echo "👋 ¡Hasta luego!"
        exit 0
        ;;
    *)
        echo "❌ Opción no válida"
        exit 1
        ;;
esac

echo ""
echo "============================================================"
echo "✅ Ejecución completada"
echo "============================================================"
