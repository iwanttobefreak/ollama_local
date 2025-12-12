Entramos de forma interactiva para lanzar comandos:
```
docker exec -ti ollama bash
```

Si queremos hacer acciones, el LLM nos dice que no puede:
```
ollama run llama3.1:8b

>>> ¿Me puedes crear el fichero /tmp/prueba.txt?
No, no puedo crear un archivo en tu sistema de archivos. ¿En qué puedo ayudarte con respecto a crear un archivo de
texto?
```

En este caso vamos a arranca un MCP server que contiene un conjunto de herramientas especificas para un conjunto de utilidades. Por ejemplo para utilides de ficheros.

Primero instalamos un conector entre LLM y los MCP servers:
```
pip install ollama-mcp-bridge
```

Ahora instalamos el MCP server de:
https://github.com/modelcontextprotocol/servers/tree/main/src/filesystem

Se puede usar con docker o npx. Vamos a probar con npx

Instalamos npx:
```
apt-get update
apt-get install nodejs npm
```

Tenemos el fichero **scrics/tools/mcp-bridge-config.json** que hace de conector entre LLM y MCP:
```python
{
  "mcpServers": {
    "filesystem": {
      "command": "npx",
      "args": [
        "-y",
        "@modelcontextprotocol/server-filesystem",
        "/tmp"
      ]
    }
  }
}
```
Lo ejecutamos con:
```bash
ollama-mcp-bridge --config /app/scrics/tools/mcp-bridge-config-filesystem.json
```
Vemos que la primera vez se descarga el MCP server. Se queda escuchando en el puerto 8000 (modificarlo en el fichero). Vemos también que carga las tools del MCP server:
```
2025-12-11 10:03:25.856 | INFO     | ollama_mcp_bridge.mcp_manager:_connect_server:66 - Connected to 'filesystem' with 14 tools
```

Ahora abrimos otra consola de ollama:
```
docker exec -ti ollama bash
````

Levantamos el chat con mcp-server
python /app/scrics/tools/mcp-chat-filesystem.py

Ahora le pedimos lo mismo que antes y nos crea el fichero:
```bash
>>> ¿Me puedes crear el fichero /tmp/prueba.txt?
[RESPUESTA MCP]
{"model":"qwen2.5:latest","created_at":"2025-12-11T14:26:54.79427683Z","message":{"role":"assistant","content":"He creado el archivo `/tmp/prueba.txt` para ti. No has proporcionado ningún contenido, así que el archivo se creará pero estará vacío. Si deseas escribir algún texto en él, puedes indicármelo y lo haré. ¿Necesitas agregar algún contenido al archivo?"},"done":true,"done_reason":"stop","total_duration":4846533696,"load_duration":57815419,"prompt_eval_count":1689,"prompt_eval_duration":1355663480,"eval_count":64,"eval_duration":3387944979}

[RESPUESTA FORMATEADA]
He creado el archivo `/tmp/prueba.txt` para ti. No has proporcionado ningún contenido, así que el archivo se creará pero estará vacío. Si deseas escribir algún texto en él, puedes indicármelo y lo haré. ¿Necesitas agregar algún contenido al archivo?
```

Le podemos preguntar que herramientas tiene disponibles:
```
>>> ¿Cuantas tools tienes disponibles?
[RESPUESTA MCP]
{"model":"qwen2.5:latest","created_at":"2025-12-11T14:23:15.60276718Z","message":{"role":"assistant","content":"Tengo disponibles 12 herramientas. Aquí está la lista con sus nombres:\n\n1. filesystem.read_text_file\n2. filesystem.write_file\n3. filesystem.edit_file\n4. filesystem.create_directory\n5. filesystem.list_directory\n6. filesystem.list_directory_with_sizes\n7. filesystem.directory_tree\n8. filesystem.move_file\n9. filesystem.search_files\n10. filesystem.get_file_info\n11. filesystem.read_media_file\n12. filesystem.read_multiple_files\n\nCada una de estas herramientas tiene un propósito específico para ayudar con diferentes tareas relacionadas con el sistema de archivos."},"done":true,"done_reason":"stop","total_duration":64743332070,"load_duration":2230084553,"prompt_eval_count":1633,"prompt_eval_duration":55669300366,"eval_count":126,"eval_duration":6799383551}

[RESPUESTA FORMATEADA]
Tengo disponibles 12 herramientas. Aquí está la lista con sus nombres:

1. filesystem.read_text_file
2. filesystem.write_file
3. filesystem.edit_file
4. filesystem.create_directory
5. filesystem.list_directory
6. filesystem.list_directory_with_sizes
7. filesystem.directory_tree
8. filesystem.move_file
9. filesystem.search_files
10. filesystem.get_file_info
11. filesystem.read_media_file
12. filesystem.read_multiple_files

Cada una de estas herramientas tiene un propósito específico para ayudar con diferentes tareas relacionadas con el sistema de archivos.
```

Herramientas para repositorios GIT:
https://github.com/modelcontextprotocol/servers/tree/main/src/git

Instlamos uvx:
```
pip install uv
```

Lanzamos el conector entre LLM y MCP server
```
ollama-mcp-bridge --config /app/scrics/tools/mcp-bridge-config-git.json
```
Vemos que la primera vez nos instala las herramientas para el MCP server

Ahora en otra ventana abrimos el chat:
```
docker exec -ti ollama bash
```

Preguntamos que herramientas tiene ahora:
```
>>> enumerame las herramientas de git que tienes disponibles
[RESPUESTA MCP]
{"model":"qwen2.5:latest","created_at":"2025-12-11T14:45:31.628047421Z","message":{"role":"assistant","content":"Las herramientas de Git disponibles a través de mí son las siguientes:\n\n1. `git.git_status`: Muestra el estado del árbol de trabajo.\n2. `git.git_diff_unstaged`: Muestra los cambios en el directorio de trabajo que aún no han sido marcados para un commit.\n3. `git.git_diff_staged`: Muestra los cambios que están listos para ser commiteados (marcados para un commit).\n4. `git.git_diff`: Muestra las diferencias entre ramas o commits específicos.\n5. `git.git_commit`: Registra los cambios en el repositorio.\n6. `git.git_add`: Agrega el contenido de archivos al área de preparación.\n7. `git.git_reset`: Desmarca todos los cambios marcados para un commit.\n8. `git.git_log`: Muestra los logs de comit.\n9. `git.git_create_branch`: Crea una nueva rama a partir de una rama base (opcional).\n10. `git.git_checkout`: Cambia de rama actual.\n11. `git.git_show`: Muestra el contenido de un commit específico.\n12. `git.git_branch`: Lista las ramas Git.\n\nEstas herramientas cubren una variedad de tareas comunes en el uso de Git, desde el seguimiento y marcar cambios hasta la gestión de diferentes ramas y commits."},"done":true,"done_reason":"stop","total_duration":16172482439,"load_duration":65436544,"prompt_eval_count":1110,"prompt_eval_duration":558160928,"eval_count":291,"eval_duration":15456992642}

[RESPUESTA FORMATEADA]
Las herramientas de Git disponibles a través de mí son las siguientes:

1. `git.git_status`: Muestra el estado del árbol de trabajo.
2. `git.git_diff_unstaged`: Muestra los cambios en el directorio de trabajo que aún no han sido marcados para un commit.
3. `git.git_diff_staged`: Muestra los cambios que están listos para ser commiteados (marcados para un commit).
4. `git.git_diff`: Muestra las diferencias entre ramas o commits específicos.
5. `git.git_commit`: Registra los cambios en el repositorio.
6. `git.git_add`: Agrega el contenido de archivos al área de preparación.
7. `git.git_reset`: Desmarca todos los cambios marcados para un commit.
8. `git.git_log`: Muestra los logs de comit.
9. `git.git_create_branch`: Crea una nueva rama a partir de una rama base (opcional).
10. `git.git_checkout`: Cambia de rama actual.
11. `git.git_show`: Muestra el contenido de un commit específico.
12. `git.git_branch`: Lista las ramas Git.

Estas herramientas cubren una variedad de tareas comunes en el uso de Git, desde el seguimiento y marcar cambios hasta la gestión de diferentes ramas y commits.
```

Pero si le preguntamos por crear un fichero en el filesystem nos dice que no puede porque no tiene cargado el otro MCP server pero te da respuesta que tiene que ver con git:
```
>>> Crea el fichero /tmp/git.txt
[RESPUESTA MCP]
{"model":"qwen2.5:latest","created_at":"2025-12-11T15:07:53.454907769Z","message":{"role":"assistant","content":"To create the file `/tmp/git.txt`, we will first need to initialize a Git repository in that directory if it doesn't already exist. Then, we can add and commit an empty file to track its creation.\n\nLet's start by initializing a new Git repository in `/tmp/` (assuming you want the repo there), and create `git.txt` inside it.\n"},"done":true,"done_reason":"stop","total_duration":45151043964,"load_duration":2511449073,"prompt_eval_count":1109,"prompt_eval_duration":37494787239,"eval_count":98,"eval_duration":5108953980}

[RESPUESTA FORMATEADA]
To create the file `/tmp/git.txt`, we will first need to initialize a Git repository in that directory if it doesn't already exist. Then, we can add and commit an empty file to track its creation.

Let's start by initializing a new Git repository in `/tmp/` (assuming you want the repo there), and create `git.txt` inside it.
````

Podemos añadir los dos MCP servers al conector, con el fichero 