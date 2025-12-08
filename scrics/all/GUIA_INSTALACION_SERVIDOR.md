# 🚀 Guía de Instalación en Servidor Ollama Remoto

## 📋 PASOS PARA INSTALAR LA TOOL EN TU SERVIDOR OLLAMA

### 📦 Paso 1: Copiar el archivo al servidor

#### Opción A: Usando SCP (desde Windows)

```powershell
# Desde tu PC Windows
scp C:\Users\joseantonio.legidoma\copilot\apis\ollama_tool_standalone.py usuario@servidor:/home/usuario/
```

#### Opción B: Usando WinSCP o FileZilla

1. Abre WinSCP o FileZilla
2. Conecta a tu servidor
3. Navega a: `C:\Users\joseantonio.legidoma\copilot\apis\`
4. Copia `ollama_tool_standalone.py` al servidor
5. Colócalo en `/home/usuario/` o donde prefieras

#### Opción C: Copiar y pegar manualmente

1. Abre el archivo `ollama_tool_standalone.py` en Windows
2. Copia todo el contenido (Ctrl+A, Ctrl+C)
3. Conéctate al servidor por SSH
4. Crea el archivo:
   ```bash
   nano ollama_tool_standalone.py
   ```
5. Pega el contenido (Ctrl+Shift+V en la mayoría de terminales)
6. Guarda (Ctrl+O, Enter, Ctrl+X)

---

### 🔧 Paso 2: Instalar dependencias en el servidor

Conéctate al servidor por SSH y ejecuta:

```bash
# Instalar paquetes de Python
pip install ollama requests

# O si usas pip3
pip3 install ollama requests
```

---

### ✅ Paso 3: Verificar que Ollama está corriendo

En el servidor, verifica:

```bash
# Ver si Ollama está corriendo
ps aux | grep ollama

# O intentar conectar
curl http://localhost:11434/api/version
```

Si no está corriendo:

```bash
# Iniciar Ollama
ollama serve

# O en segundo plano
nohup ollama serve > /dev/null 2>&1 &
```

---

### 📥 Paso 4: Descargar modelo (si no lo tienes)

```bash
# Verificar modelos instalados
ollama list

# Si no tienes llama3.1, descargarlo
ollama pull llama3.1
```

---

### 🚀 Paso 5: Ejecutar la tool

```bash
# Chat interactivo
python3 ollama_tool_standalone.py

# O modo test
python3 ollama_tool_standalone.py --test
```

---

## 💬 Ejemplo de Uso

```bash
$ python3 ollama_tool_standalone.py
======================================================================
CHAT DE TEMPERATURA CON OLLAMA
======================================================================

Ejemplos de preguntas:
  - ¿Que tiempo hara mañana en Madrid?
  - Pronostico de 5 dias para Barcelona
  - ¿Llovera en Sevilla esta semana?

Escribe 'salir' para terminar

Tu: ¿Qué tiempo hará mañana en Madrid?

[Consultando Madrid...]

Ollama: Según el pronóstico, mañana en Madrid tendremos temperaturas 
entre 13.9°C y 23.8°C, con cielo nublado y 18% de probabilidad de 
lluvia. No será necesario paraguas.

Tu: ¿Y en Barcelona?

[Consultando Barcelona...]

Ollama: En Barcelona las temperaturas estarán entre 17.5°C y 21.3°C,
parcialmente nublado con 15% de probabilidad de lluvia.

Tu: salir
Adios!
```

---

## 🔍 Verificar Instalación

### Test completo:

```bash
# 1. Verificar Python
python3 --version

# 2. Verificar paquetes
python3 -c "import ollama; import requests; print('OK')"

# 3. Verificar Ollama
curl http://localhost:11434/api/version

# 4. Verificar modelo
ollama list | grep llama3.1

# 5. Probar la tool
python3 ollama_tool_standalone.py --test
```

---

## 📝 Script de Instalación Automática

Guarda esto como `instalar_tool.sh` en el servidor:

```bash
#!/bin/bash

echo "=================================================="
echo "Instalando Tool de Temperatura para Ollama"
echo "=================================================="
echo ""

# 1. Verificar Python
echo "[1/5] Verificando Python..."
if command -v python3 &> /dev/null; then
    echo "✓ Python3 encontrado: $(python3 --version)"
else
    echo "✗ Python3 no encontrado. Instalalo primero."
    exit 1
fi

# 2. Instalar dependencias
echo ""
echo "[2/5] Instalando dependencias..."
pip3 install ollama requests
if [ $? -eq 0 ]; then
    echo "✓ Dependencias instaladas"
else
    echo "✗ Error al instalar dependencias"
    exit 1
fi

# 3. Verificar Ollama
echo ""
echo "[3/5] Verificando Ollama..."
if pgrep -x "ollama" > /dev/null; then
    echo "✓ Ollama está corriendo"
else
    echo "⚠ Ollama no está corriendo"
    echo "  Ejecuta: ollama serve"
fi

# 4. Verificar modelo
echo ""
echo "[4/5] Verificando modelo llama3.1..."
if ollama list | grep -q "llama3.1"; then
    echo "✓ Modelo llama3.1 encontrado"
else
    echo "⚠ Modelo llama3.1 no encontrado"
    echo "  Descargando modelo (esto puede tardar)..."
    ollama pull llama3.1
fi

# 5. Probar la tool
echo ""
echo "[5/5] Probando la tool..."
if [ -f "ollama_tool_standalone.py" ]; then
    python3 ollama_tool_standalone.py --test
    echo ""
    echo "=================================================="
    echo "✓ Instalación completada"
    echo "=================================================="
    echo ""
    echo "Para usar, ejecuta:"
    echo "  python3 ollama_tool_standalone.py"
else
    echo "✗ Archivo ollama_tool_standalone.py no encontrado"
    echo "  Cópialo al servidor primero"
fi
```

Luego ejecuta:

```bash
chmod +x instalar_tool.sh
./instalar_tool.sh
```

---

## 🐛 Solución de Problemas

### Error: "ModuleNotFoundError: No module named 'ollama'"

```bash
pip3 install ollama
# o
python3 -m pip install ollama
```

### Error: "Connection refused"

Ollama no está corriendo:
```bash
# Iniciar Ollama
ollama serve

# En segundo plano
nohup ollama serve > /dev/null 2>&1 &
```

### Error: "Model not found"

```bash
ollama pull llama3.1
```

### La tool no llama a la función

Verifica que el modelo soporta function calling:
```bash
# Usa llama3.1 (recomendado)
ollama pull llama3.1
```

---

## 🔐 Permisos

Si tienes problemas de permisos:

```bash
# Dar permisos de ejecución
chmod +x ollama_tool_standalone.py

# Ejecutar
./ollama_tool_standalone.py
```

---

## 🌐 Configuración para Diferentes Modelos

Si quieres usar otro modelo, edita el archivo:

```python
# Línea ~235 aproximadamente
response = ollama.chat(
    model='llama3.1',  # <-- Cambia aquí
    messages=messages,
    tools=[TOOL_DEFINITION]
)
```

Modelos compatibles:
- `llama3.1` ✅ Recomendado
- `llama3.2` ✅
- `mistral` ✅
- `mixtral` ✅
- `qwen2.5` ✅

---

## 📊 Resumen de Comandos

### En tu PC Windows:
```powershell
# Copiar archivo al servidor
scp ollama_tool_standalone.py usuario@servidor:/home/usuario/
```

### En el servidor Linux:
```bash
# Instalar dependencias
pip3 install ollama requests

# Verificar Ollama
ollama serve

# Descargar modelo
ollama pull llama3.1

# Ejecutar tool
python3 ollama_tool_standalone.py
```

---

## ✅ Checklist Final

- [ ] Archivo `ollama_tool_standalone.py` copiado al servidor
- [ ] Dependencias instaladas (`pip3 install ollama requests`)
- [ ] Ollama corriendo (`ollama serve`)
- [ ] Modelo descargado (`ollama pull llama3.1`)
- [ ] Tool ejecutándose (`python3 ollama_tool_standalone.py`)
- [ ] Primera pregunta realizada y respondida

---

## 🎉 ¡Listo!

Una vez completados todos los pasos, tendrás tu asistente de temperatura funcionando en el servidor Ollama.

**Archivo a copiar:** `ollama_tool_standalone.py`
**Tamaño:** ~8 KB
**Dependencias:** ollama, requests
**Tiempo de instalación:** ~5 minutos

---

## 📞 Preguntas Frecuentes

**P: ¿Necesito conexión a internet en el servidor?**
R: Sí, para descargar el modelo de Ollama y para que la tool consulte las APIs de clima.

**P: ¿Puedo usar otro modelo que no sea llama3.1?**
R: Sí, cualquier modelo que soporte function calling (llama3.2, mistral, mixtral, etc.)

**P: ¿Funciona en Windows Server?**
R: Sí, los comandos son similares pero usa `python` en lugar de `python3`.

**P: ¿Cuánta RAM necesita?**
R: Depende del modelo de Ollama (llama3.1 necesita ~4-8GB).

**P: ¿Puedo tener múltiples usuarios usando la tool?**
R: Sí, cada usuario puede ejecutar su propia instancia del script.

---

**Última actualización:** 15/10/2025
**Estado:** ✅ Probado y funcionando
