# Docker Ollama con API Flask

Este contenedor ejecuta automáticamente Ollama serve y la API Flask de conversaciones al iniciar.

## 🚀 Inicio Automático

### Opción 1: Usando el script de gestión (recomendado)
```bash
cd /Users/T054810/ollama_local
./manage_docker.sh
```

### Opción 2: Comando manual
```bash
docker run --rm -d --name ollama \
  -p 11434:11434 -p 5000:5000 \
  --memory="16g" \
  -v /Users/T054810/ollama_local/scrics:/scrics \
  -v /Users/T054810/ia/ollama/usr_local_lib:/usr/local/lib \
  -v /Users/T054810/ia/ollama/root_ollama:/root/.ollama \
  -ti ollama
```

## 📊 Servicios Automáticos

Al iniciar el contenedor, automáticamente se ejecutan:

1. **Ollama Serve** - API de Ollama en puerto 11434
2. **API Flask** - Servidor de conversaciones en puerto 5000

## 🔍 Verificación

```bash
# Ver logs del contenedor
docker logs ollama

# Verificar servicios
curl http://localhost:11434/api/version
curl http://localhost:5000

# Probar la API
curl -X POST http://localhost:5000/preguntar \
     -H "Content-Type: application/json" \
     -d '{"persona":"jandro", "pregunta":"¿Hola?"}'
```

## 🛠️ Gestión del Contenedor

### Ver estado
```bash
docker ps | grep ollama
```

### Ver logs en tiempo real
```bash
docker logs -f ollama
```

### Entrar al contenedor
```bash
docker exec -it ollama bash
```

### Detener contenedor
```bash
docker stop ollama
```

## 🔧 Solución de Problemas

### Servicios no responden
```bash
# Reiniciar servicios dentro del contenedor
docker exec ollama bash -c "pkill -f 'ollama serve' && pkill -f 'api_ollama_server'"
# Los servicios se reiniciarán automáticamente
```

### Actualizar código
```bash
# Si modificas api_ollama_server.py:
cd /Users/T054810/ollama_local
./manage_docker.sh  # Esto detiene el anterior y crea uno nuevo
```

### Ver procesos corriendo
```bash
docker exec ollama ps aux
```

## 📁 Estructura

```
/scrics/chats/
├── api_ollama_server.py    # API Flask (se ejecuta automáticamente)
├── historial/              # Historiales de conversación
└── contextos/              # Contextos de personajes

/ollama-agente/             # Entorno virtual Python
/root/.ollama/              # Modelos de Ollama (volumen mapeado)
```

## ⚙️ Configuración

- **Puerto Ollama**: 11434
- **Puerto Flask API**: 5000
- **Modelo por defecto**: llama3.1:8b
- **Memoria límite**: 16GB
- **Supervisor**: Reinicio automático de servicios caídos

## 📂 Volúmenes Mapeados

- **Código**: `/Users/T054810/ollama_local/scrics:/scrics`
- **Binarios**: `/Users/T054810/ia/ollama/usr_local_lib:/usr/local/lib`
- **Modelos**: `/Users/T054810/ia/ollama/root_ollama:/root/.ollama`

Una vez dentro del contenedor, el entorno virtual ya está activado:

```bash
# El entorno virtual está activado automáticamente
source /ollama-agente/bin/activate  # (ya activado por defecto)

# Verificar instalación
python3 --version
pip list
ollama --version

# Ejecutar scripts de la lección
cd /app
python3 mcp_client_temperatura.py
```

## Estructura del contenedor

```
/ollama-agente/          # Entorno virtual Python
/app/                     # Archivos del proyecto
/usr/local/bin/ollama    # Binario de Ollama
```

## Solución de problemas

### Ollama no responde
```bash
# Verificar que Ollama está corriendo
curl http://localhost:11434/api/version

# Reiniciar Ollama manualmente
ollama serve
```

### Dependencias Python faltantes
```bash
# Activar entorno virtual
source /ollama-agente/bin/activate

# Reinstalar dependencias
pip install -r requirements.txt
```

### Puerto ocupado
```bash
# Usar un puerto diferente
docker run -d -p 11435:11434 ollama-python-env
```