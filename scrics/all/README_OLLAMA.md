# Herramienta de Consulta de Población INE para Ollama

Script de Python que permite a modelos de lenguaje (como Ollama) consultar datos oficiales de población de España directamente desde el Instituto Nacional de Estadística (INE).

## ✨ Características

- ✅ **Consulta en tiempo real** - Datos directos desde www.ine.es (SIN datos hardcodeados)
- ✅ **Datos oficiales** - Instituto Nacional de Estadística de España
- ✅ **Fácil integración** - Funciona directamente con Ollama
- ✅ **Cobertura completa** - Todas las provincias y capitales de España
- ✅ **Histórico amplio** - Datos desde 1996 hasta 2021
- ✅ **Formato UTF-8** - Sin caracteres especiales problemáticos

## 📋 Requisitos

```powershell
# Python 3.8 o superior
python --version

# Ollama instalado y corriendo
ollama --version
```

## 🚀 Instalación

### 1. Instalar dependencias

```powershell
pip install ollama requests
```

### 2. Descargar un modelo compatible con Ollama

```powershell
ollama pull llama3.2
```

Los modelos recomendados que soportan function calling:
- `llama3.2` (recomendado)
- `mistral`
- `qwen2.5`

### 3. Verificar que Ollama está corriendo

```powershell
# Si no está corriendo, iniciarlo:
ollama serve
```

## 💻 Uso

### Modo Interactivo (Conversación)

```powershell
cd C:\Users\joseantonio.legidoma\copilot\apis
python ollama_ine.py
```

Ejemplo de conversación:

```
Tu: ¿Cuántos habitantes tenía Madrid en 2021?

[Ollama llama a: consultar_poblacion_ine]
[Argumentos: {'lugar': 'Madrid', 'año': 2021}]

[Resultado de la consulta:]
Poblacion de Madrid en 2021:
- Lugar: Madrid. Total. Total habitantes. Personas.
- Codigo INE: DPOP12922
- Poblacion: 6,751,251 habitantes
- Fuente: INE (www.ine.es)

Ollama: Según los datos oficiales del INE, Madrid tenía 6,751,251 
habitantes en el año 2021.

---

Tu: Compara Barcelona y Sevilla en 2020

[Ollama llama a: consultar_poblacion_ine]
[Argumentos: {'lugar': 'Barcelona', 'año': 2020}]
...
[Ollama llama a: consultar_poblacion_ine]
[Argumentos: {'lugar': 'Sevilla', 'año': 2020}]
...

Ollama: En 2020, Barcelona tenía 5,743,402 habitantes y Sevilla 
1,950,219 habitantes. Barcelona tenía aproximadamente 3.8 millones 
más de habitantes que Sevilla, siendo casi 3 veces más grande.
```

### Modo Pregunta Única

```powershell
python ollama_ine.py "¿Cuántos habitantes tenía Murcia en 2019?"
```

### Usar desde otro script Python

```python
from ollama_ine import chat_con_herramientas

# Hacer una pregunta
respuesta = chat_con_herramientas(
    "¿Cuál era la población de Valencia en 2020?",
    modelo='llama3.2',
    verbose=True
)

print(respuesta)
```

## 📊 Ejemplos de consultas

```
✅ ¿Cuántos habitantes tenía Madrid en 2021?
✅ Dame la población de Barcelona en 2020
✅ Compara la población de Sevilla y Valencia en 2019
✅ ¿Cuál es la tendencia de población de Murcia entre 2015 y 2021?
✅ ¿Qué provincia tenía más habitantes en 2020: Málaga o Zaragoza?
✅ Lista la población de las 5 ciudades más grandes de España en 2021
```

## 📁 Archivos

```
apis/
├── ine_poblacion.py          # Script standalone (sin Ollama)
├── ollama_ine.py             # Cliente Ollama SIMPLE (RECOMENDADO)
├── mcp_ine_server.py         # Servidor MCP (avanzado)
├── test_mcp_ine.py           # Tests del servidor MCP
├── GUIA_OLLAMA.md            # Guía detallada de integración
└── README_OLLAMA.md          # Este archivo
```

## 🎯 Casos de uso

1. **Análisis demográfico conversacional**
   ```
   Tu: ¿Cómo ha evolucionado la población de Madrid desde 2015?
   ```

2. **Comparaciones entre ciudades**
   ```
   Tu: Compara el crecimiento de población entre Barcelona y Valencia 
        desde 2010 hasta 2020
   ```

3. **Consultas específicas**
   ```
   Tu: ¿Cuántos habitantes tenía Salamanca en 2018?
   ```

4. **Análisis regional**
   ```
   Tu: Dame la población de todas las capitales andaluzas en 2021
   ```

## 🔧 Configuración avanzada

### Cambiar el modelo de Ollama

Edita `ollama_ine.py` y modifica:

```python
def modo_conversacion(modelo: str = 'llama3.2'):  # Cambiar aquí
```

O pásalo al llamar la función:

```python
chat_con_herramientas(pregunta, modelo='mistral')
```

### Ajustar el timeout de consulta

En `ollama_ine.py`, función `consultar_poblacion_ine`:

```python
response = requests.get(url, headers=headers, timeout=30)  # Cambiar timeout
```

## 📝 Datos disponibles

- **Cobertura geográfica:** Todas las provincias de España y capitales principales
- **Rango temporal:** 1996 - 2021
- **Fuente:** Instituto Nacional de Estadística (INE)
- **Tabla:** 2852 - Población por municipios, sexo y año
- **URL:** https://www.ine.es/jaxiT3/Tabla.htm?t=2852

## ❓ Troubleshooting

### Error: "ollama module not found"
```powershell
pip install ollama
```

### Error: "Connection refused" o "Ollama not running"
```powershell
# Iniciar Ollama
ollama serve
```

### El modelo no responde o da errores
```powershell
# Verificar que el modelo está descargado
ollama list

# Descargar si es necesario
ollama pull llama3.2
```

### No encuentra datos para un municipio pequeño

La API del INE solo incluye provincias y capitales principales. Para municipios pequeños, consulta directamente en:
https://www.ine.es/jaxiT3/Tabla.htm?t=2852

### Error: "No se encontró el año 2023"

Los datos del INE llegan hasta 2021. Para años posteriores, consulta la web del INE directamente.

## 🆚 Comparación de opciones

| Característica | ine_poblacion.py | ollama_ine.py | mcp_ine_server.py |
|----------------|------------------|---------------|-------------------|
| Requiere Ollama | ❌ | ✅ | ✅ |
| Requiere MCP | ❌ | ❌ | ✅ |
| Conversacional | ❌ | ✅ | ✅ |
| Fácil de usar | ✅✅✅ | ✅✅ | ✅ |
| Recomendado para | CLI simple | **Ollama local** | Integraciones |

**Recomendación:** Usa `ollama_ine.py` para integración con Ollama (más simple y funcional).

## 📚 Recursos

- **INE:** https://www.ine.es
- **Ollama:** https://ollama.ai
- **Ollama Python SDK:** https://github.com/ollama/ollama-python
- **MCP:** https://modelcontextprotocol.io

## 📄 Licencia

Script de uso libre para consultas al INE.
Datos del INE sujetos a las condiciones de uso del Instituto Nacional de Estadística.

## 👤 Autor

Creado para facilitar el acceso a datos demográficos oficiales de España mediante IA conversacional.

---

**Nota:** Este script NO almacena datos. Cada consulta se realiza en tiempo real al INE.
