Uso de tools sencillas
¿Que es una tool?
Es una herramienta para que el LLM realice llamadas externas que no conoce como LLM, cosas dinámicas, por ejemplo operaciones matemáticas, consultas del tiempo, programación de TV,.... En general, ejecutar un comando, que puede ser un comando de sistema (un ls), una llamada a una api, .....

Definición básica

```
{
  "type": "function",
  "function": {
    "name": "ejecutar_comando",   <-- nombre de la función, podría ser: consulta_temperatura, suma_numero.....
    "description": "Ejecuta comandos del sistema de forma segura",
    "parameters": {
      "type": "object",
      "properties": {
        "command": {
          "type": "string",
          "description": "El comando a ejecutar (ej: 'ls -la', 'docker ps')"
        },
        "directory": {
          "type": "string",
          "description": "Directorio donde ejecutar el comando (opcional)",
          "default": "/projects"
        }
      },
      "required": ["command"]
    }
  }
}
```

### 🔧 **Desglose Detallado**

#### **1. 📌 `"type": "function"`**
- **💡 Qué es**: Identifica que esto es una función ejecutable
- **🎯 Por qué**: Le dice a Ollama que puede llamar a esta herramienta durante una conversación
- **⚠️ Importante**: Siempre debe ser `"function"` para herramientas de Ollama

#### **2. 🏷️ `"function.name"`**
- **💡 Qué es**: El nombre único e identificador de la función
- **🎯 Por qué**: Ollama usa este nombre para saber qué función invocar
- **✅ Ejemplo**: `"execute_command"`, `"docker_management"`, `"file_operations"`
- **📝 Buenas prácticas**: 
  - Usar snake_case
  - Nombres descriptivos y claros
  - Sin espacios ni caracteres especiales

#### **3. 📄 `"function.description"`**
- **💡 Qué es**: Descripción clara de qué hace la función
- **🎯 Por qué**: Ollama lee esto para decidir cuándo usar la función
- **✅ Ejemplo**: `"Ejecuta comandos del sistema de forma segura"`
- **📝 Buenas prácticas**:
  - Ser específico sobre qué hace
  - Mencionar limitaciones de seguridad
  - Usar lenguaje claro y directo

#### **4. ⚙️ `"function.parameters"`**
- **💡 Qué es**: Define la estructura de datos que acepta la función
- **🎯 Por qué**: Ollama necesita saber qué información enviar a la función
- **✅ Siempre**: `"type": "object"` - es el formato estándar

#### **5. 🎛️ `"parameters.properties"`**
- **💡 Qué es**: Lista detallada de todos los parámetros que acepta la función
- **🎯 Por qué**: Define exactamente qué datos puede enviar Ollama
- **📝 Cada propiedad contiene**:

##### **5.1 📊 `"type"`**
- **💡 Qué es**: Tipo de dato del parámetro
- **✅ Opciones disponibles**:
  - `"string"` - Texto (comandos, rutas, nombres)
  - `"number"` - Números (puertos, IDs, tamaños)
  - `"boolean"` - Verdadero/Falso (flags, opciones)
  - `"array"` - Listas (múltiples archivos, opciones)
  - `"object"` - Objetos complejos (configuraciones)

##### **5.2 📝 `"description"`**
- **💡 Qué es**: Explicación del parámetro específico
- **🎯 Por qué**: Ayuda a Ollama a entender qué valor enviar
- **✅ Ejemplo**: `"El comando a ejecutar (ej: 'ls -la', 'docker ps')"`

##### **5.3 🎯 `"default"` (Opcional)**
- **💡 Qué es**: Valor por defecto si no se especifica
- **🎯 Por qué**: Simplifica el uso de la función
- **✅ Ejemplo**: `"default": "/projects"`

##### **5.4 📋 `"enum"` (Opcional)**
- **💡 Qué es**: Lista de valores permitidos
- **🎯 Por qué**: Restringe las opciones a valores válidos
- **✅ Ejemplo**: `"enum": ["list", "start", "stop", "logs"]`

#### **6. ❗ `"required"`**
- **💡 Qué es**: Array con nombres de parámetros obligatorios
- **🎯 Por qué**: Ollama sabe qué parámetros debe enviar siempre
- **✅ Ejemplo**: `["command"]` - el comando es obligatorio
- **📝 Nota**: Los parámetros con `"default"` no suelen ser required


Prueba 1
Con una tool que tiene integrado la consulta del tiempo
