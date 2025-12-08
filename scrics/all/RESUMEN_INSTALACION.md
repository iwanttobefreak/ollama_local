# 🚀 RESUMEN EJECUTIVO - Tool de Temperatura para Ollama Remoto

## 📌 LO QUE NECESITAS HACER (3 PASOS SIMPLES)

### 1️⃣ COPIAR EL ARCHIVO AL SERVIDOR

**Archivo a copiar:** `ollama_tool_standalone.py`  
**Ubicación actual:** `C:\Users\joseantonio.legidoma\copilot\apis\ollama_tool_standalone.py`

**Opción rápida (SCP desde PowerShell):**
```powershell
scp C:\Users\joseantonio.legidoma\copilot\apis\ollama_tool_standalone.py usuario@tu-servidor:/home/usuario/
```

---

### 2️⃣ INSTALAR EN EL SERVIDOR

Conéctate al servidor por SSH y ejecuta:

```bash
# Instalar paquetes de Python
pip3 install ollama requests

# Descargar modelo (si no lo tienes)
ollama pull llama3.1
```

---

### 3️⃣ EJECUTAR LA TOOL

```bash
# Ejecutar chat interactivo
python3 ollama_tool_standalone.py
```

**¡Y LISTO!** Ya puedes chatear sobre el tiempo.

---

## 💬 EJEMPLO DE USO

```
Tu: ¿Qué tiempo hará mañana en Madrid?

[Consultando Madrid...]

Ollama: Mañana en Madrid tendremos temperaturas entre 13.9°C y 23.8°C, 
con cielo nublado y 18% de probabilidad de lluvia.

Tu: ¿Y en Barcelona?

[Consultando Barcelona...]

Ollama: En Barcelona las temperaturas serán de 17.5°C a 21.3°C...
```

---

## 📋 COMANDO COMPLETO DE INSTALACIÓN (COPIAR Y PEGAR)

En el servidor, ejecuta todo esto de una vez:

```bash
# Instalar dependencias
pip3 install ollama requests && \

# Verificar que Ollama está corriendo (si no, iniciarlo)
pgrep ollama || (echo "Iniciando Ollama..." && nohup ollama serve > /dev/null 2>&1 &) && \

# Descargar modelo si no existe
ollama list | grep -q llama3.1 || ollama pull llama3.1 && \

# Ejecutar la tool
python3 ollama_tool_standalone.py
```

---

## ✅ VERIFICACIÓN RÁPIDA

```bash
# Todo en uno
python3 -c "import ollama, requests; print('Paquetes OK')" && \
ollama list | grep llama3.1 && \
echo "Todo listo para ejecutar!"
```

---

## 🎯 CARACTERÍSTICAS DE ESTA TOOL

- ✅ **UN SOLO ARCHIVO** - Todo incluido, no necesita más archivos
- ✅ **CUALQUIER CIUDAD** - Madrid, Barcelona, Mataró, pueblos pequeños, etc.
- ✅ **SIN DATOS HARDCODEADOS** - Búsqueda dinámica
- ✅ **SIN API_KEY** - Usa servicios gratuitos
- ✅ **CHAT NATURAL** - Habla normalmente con Ollama
- ✅ **16 DÍAS DE PRONÓSTICO** - Todo el que necesites

---

## 📁 ARCHIVO ÚNICO

**ollama_tool_standalone.py**
- Tamaño: ~8 KB
- Incluye: Todo lo necesario
- Dependencias externas: ollama, requests
- Funciona: De forma independiente

---

## 🚨 SI TIENES PROBLEMAS

### Ollama no responde
```bash
ollama serve
```

### Modelo no encontrado
```bash
ollama pull llama3.1
```

### Paquetes no instalados
```bash
pip3 install ollama requests
```

---

## 📞 SOPORTE RÁPIDO

| Problema | Solución |
|----------|----------|
| No encuentra el módulo ollama | `pip3 install ollama` |
| Connection refused | `ollama serve` |
| Model not found | `ollama pull llama3.1` |
| No funciona en Python 2 | Usa `python3` |

---

## 🎓 PREGUNTAS QUE PUEDES HACER

- "¿Qué tiempo hará mañana en Madrid?"
- "Pronóstico de 5 días para Barcelona"
- "¿Lloverá en Sevilla esta semana?"
- "¿Dónde hará mejor tiempo: Madrid o Barcelona?"
- "Temperatura en Mataró para el fin de semana"

---

## ⏱️ TIEMPO ESTIMADO

- **Copiar archivo:** 1 minuto
- **Instalar dependencias:** 2 minutos
- **Descargar modelo (si no lo tienes):** 5-10 minutos
- **Primera prueba:** 1 minuto

**TOTAL:** ~5-15 minutos

---

## 🎉 RESULTADO FINAL

Tendrás un chat con Ollama que puede responder preguntas sobre el tiempo en cualquier ciudad de España, usando datos en tiempo real.

**Simple. Rápido. Funciona.**

---

## 📝 CHECKLIST

```
[ ] Archivo ollama_tool_standalone.py copiado al servidor
[ ] pip3 install ollama requests ejecutado
[ ] ollama serve corriendo
[ ] ollama pull llama3.1 completado
[ ] python3 ollama_tool_standalone.py ejecutado
[ ] Primera pregunta realizada
```

---

**Archivo a copiar:** `ollama_tool_standalone.py`  
**Comando para ejecutar:** `python3 ollama_tool_standalone.py`  
**Estado:** ✅ Listo para usar
