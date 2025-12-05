# 📚 Lección 2: Resumen Visual

## 🎯 Objetivo de la Lección

Aprender a usar **MCP (Model Context Protocol)** para crear servidores de herramientas reutilizables que pueden conectarse con LLMs como Ollama.

---

## 📁 Archivos Creados

```
leccion02/
│
├── 📘 Documentación
│   ├── README.md           → Guía principal de la lección
│   ├── INSTALACION.md      → Guía paso a paso de instalación
│   ├── COMPARACION.md      → Diferencias Lección 1 vs 2
│   └── RESUMEN.md          → Este archivo (resumen visual)
│
├── 🟢 Ejemplo Básico (Sin Ollama)
│   ├── mcp_server_minimo.py    → Servidor MCP simple
│   └── mcp_client_minimo.py    → Cliente para probar
│
├── 🔵 Ejemplo Completo (Con Ollama)
│   ├── mcp_server_temperatura.py    → Servidor con datos reales
│   └── mcp_client_temperatura.py    → Cliente con IA
│
└── 🛠️ Utilidades
    ├── requirements.txt      → Dependencias Python
    └── test_leccion02.sh     → Script de prueba interactivo
```

---

## 🚦 Flujo de Trabajo

### Ejemplo Mínimo (Básico)

```
1️⃣ Usuario ejecuta:
   python3 mcp_client_minimo.py

2️⃣ Cliente inicia servidor:
   mcp_server_minimo.py

3️⃣ Cliente se conecta al servidor vía MCP

4️⃣ Cliente lista herramientas disponibles:
   - saludar (devuelve un saludo)

5️⃣ Cliente llama a la herramienta:
   session.call_tool("saludar", {"nombre": "María"})

6️⃣ Servidor ejecuta y responde:
   "¡Hola María! Bienvenido al servidor MCP."

7️⃣ Cliente muestra el resultado
```

### Ejemplo Completo (Con IA)

```
1️⃣ Usuario ejecuta:
   python3 mcp_client_temperatura.py

2️⃣ Cliente inicia servidor MCP:
   mcp_server_temperatura.py

3️⃣ Usuario pregunta:
   "¿Qué temperatura hará mañana en Madrid?"

4️⃣ Cliente envía pregunta a Ollama (LLM)

5️⃣ Ollama analiza y decide usar la herramienta:
   obtener_temperatura(ciudad="Madrid", dias=3)

6️⃣ Cliente llama al servidor MCP

7️⃣ Servidor ejecuta:
   script_pronostico_temperatura.py Madrid 3

8️⃣ Script consulta Open-Meteo API

9️⃣ Datos regresan al servidor → cliente → Ollama

🔟 Ollama procesa y responde en lenguaje natural:
   "Mañana en Madrid la temperatura estará entre..."
```

---

## 🔑 Conceptos Clave

### MCP = Model Context Protocol

**¿Qué es?**
Un protocolo estándar para que los LLMs se conecten con herramientas externas.

**Componentes:**
- 🖥️ **Servidor MCP**: Expone herramientas (tools)
- 📱 **Cliente MCP**: Se conecta al servidor
- 🤖 **LLM**: Usa las herramientas para responder

### Diferencia con Lección 1

| Aspecto | Lección 1 | Lección 2 |
|---------|-----------|-----------|
| **Arquitectura** | Monolítica | Cliente-Servidor |
| **Código** | Todo en un archivo | Separado en servidor/cliente |
| **Reutilización** | Baja | Alta |
| **Escalabilidad** | Limitada | Excelente |
| **Complejidad** | Simple | Moderada |

---

## 🎓 Lo que Aprendiste

✅ **Conceptos:**
- Qué es MCP y para qué sirve
- Diferencia entre tools directas y MCP servers
- Arquitectura cliente-servidor para LLMs

✅ **Práctica:**
- Crear un servidor MCP básico
- Conectar un cliente a un servidor MCP
- Integrar MCP con Ollama
- Exponer herramientas reutilizables

✅ **Habilidades:**
- Definir herramientas con `@server.list_tools()`
- Implementar lógica con `@server.call_tool()`
- Conectar cliente y servidor con MCP
- Convertir tools MCP a formato Ollama

---

## 🚀 Ejemplos de Uso

### Caso 1: Asistente Meteorológico

```
Usuario: "¿Lloverá mañana en Barcelona?"
         ↓
      Ollama LLM
         ↓
    MCP Server → script_temperatura.py → Open-Meteo API
         ↓
      Respuesta: "Probabilidad de lluvia: 8%"
```

### Caso 2: Sistema Multi-Aplicación

```
                    MCP Server Temperatura
                           ↑
        ┌──────────────────┼──────────────────┐
        ↓                  ↓                  ↓
    App Web          App Móvil         Bot Telegram
```

Un solo servidor, múltiples clientes.

---

## 📊 Comparación de Complejidad

### Ejemplo Básico (30 líneas)

```python
# Servidor
server = Server("ejemplo")

@server.list_tools()
async def handle_list_tools():
    return [Tool(name="saludar", ...)]

@server.call_tool()
async def handle_call_tool(name, args):
    return [TextContent(text=f"¡Hola {args['nombre']}!")]
```

### Ejemplo Completo (150 líneas)

- Servidor MCP completo
- Cliente con Ollama integrado
- Manejo de errores
- Chat interactivo
- Conversión de formats

---

## 🔧 Comandos Rápidos

```bash
# Instalar todo
cd lecciones/leccion02
pip install -r requirements.txt

# Probar básico (sin Ollama)
python3 mcp_client_minimo.py

# Probar completo (con Ollama)
python3 mcp_client_temperatura.py

# Usar script interactivo
./test_leccion02.sh
```

---

## 🐛 Troubleshooting Rápido

| Problema | Solución |
|----------|----------|
| `ImportError: mcp` | `pip install mcp` |
| `ImportError: ollama` | `pip install ollama` |
| `Connection refused` | Ejecuta desde directorio `leccion02` |
| `Model not found` | `docker exec ollama ollama pull llama3.2:3b` |
| `Docker ollama not running` | `docker start ollama` |

---

## 📚 Siguientes Pasos

1. ✅ **Completar Lección 2**
   - Ejecutar ejemplo básico
   - Ejecutar ejemplo completo
   - Entender el flujo MCP

2. 🔧 **Experimentar**
   - Añadir más herramientas al servidor
   - Cambiar el modelo de Ollama
   - Modificar el prompt del sistema

3. 🚀 **Crear tu propio proyecto**
   - Servidor MCP con tus APIs
   - Integrar con bases de datos
   - Conectar múltiples clientes

4. 📖 **Aprender más**
   - [Documentación MCP](https://modelcontextprotocol.io/)
   - [Ejemplos oficiales](https://github.com/modelcontextprotocol/servers)
   - Lección 3 (próximamente)

---

## 💡 Tips Finales

### Para Aprender
1. Empieza con el ejemplo mínimo
2. Lee el código línea por línea
3. Modifica y prueba
4. Pasa al ejemplo completo

### Para Desarrollar
1. Usa MCP cuando tengas múltiples clientes
2. Mantén los servidores simples
3. Documenta bien tus herramientas
4. Maneja errores apropiadamente

### Para Producción
1. Añade autenticación
2. Implementa logging
3. Usa variables de entorno
4. Considera usar HTTP en vez de stdio

---

## 🎉 ¡Felicitaciones!

Has completado la Lección 2 y ahora sabes:
- ✅ Qué es MCP y cómo funciona
- ✅ Crear servidores MCP
- ✅ Conectar clientes a servidores
- ✅ Integrar MCP con Ollama
- ✅ Diferencias arquitectónicas con Lección 1

**¡Estás listo para crear tus propios servidores MCP!** 🚀

---

## 📞 Recursos de Ayuda

- **Documentación:** Revisa `README.md` para detalles
- **Instalación:** Lee `INSTALACION.md` paso a paso
- **Comparación:** Ver `COMPARACION.md` para entender diferencias
- **Código:** Todos los ejemplos están comentados

**¿Dudas?** Revisa los ejemplos línea por línea y prueba modificarlos.
