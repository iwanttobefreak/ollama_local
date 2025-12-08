# 🔌 Usar MCPs de Node.js con Ollama

## ¿Ollama soporta MCP nativamente?

**NO.** Ollama usa "function calling" básico, **NO el protocolo MCP completo**.

Pero **SÍ puedes usar MCPs de Node.js** con estos métodos:

---

## 🎯 3 Métodos para usar MCPs con Ollama

### Método 1: Adapter Python → MCP Node.js ⭐ RECOMENDADO

**Cómo funciona:**
```
Usuario → Ollama → Python Tool → subprocess → MCP Node.js → Resultado
```

**Ventajas:**
- ✅ Usa MCPs oficiales de Anthropic
- ✅ No modificas tu código de Ollama
- ✅ Fácil de mantener

**Desventajas:**
- ⚠️ Requiere Node.js instalado
- ⚠️ Un poco más lento (subprocess)

**Ya creado:** `tools/mcp_adapter.py`

---

### Método 2: Traducir MCP a Python Tool

**Cómo funciona:**
```
MCP Node.js (código) → Traducir a Python → Tool Python nativo
```

**Ventajas:**
- ✅ 100% Python, sin Node.js
- ✅ Más rápido (nativo)
- ✅ Fácil debug

**Desventajas:**
- ⚠️ Tienes que traducir el código
- ⚠️ Mantener actualizaciones manualmente

**Ejemplo:** Puedo traducir el MCP de Git de Node.js a Python puro

---

### Método 3: Proxy MCP Server

**Cómo funciona:**
```
Ollama → HTTP API → MCP Server (Node.js) → Resultado
```

**Ventajas:**
- ✅ Separa servicios (microservicios)
- ✅ Puede correr en otro servidor
- ✅ Reutilizable por múltiples clientes

**Desventajas:**
- ⚠️ Más complejo (servidor HTTP)
- ⚠️ Overhead de red

---

## 🚀 Implementación Práctica

### Paso 1: Instalar Node.js (si no lo tienes)

```bash
# Ubuntu/Debian
curl -fsSL https://deb.nodesource.com/setup_20.x | sudo -E bash -
sudo apt-get install -y nodejs

# Verificar
node --version  # v20.x.x
npm --version   # 10.x.x
```

### Paso 2: Instalar MCPs oficiales

```bash
# MCP de Git (comandos git básicos)
npm install -g @modelcontextprotocol/server-git

# MCP de GitHub (API de GitHub)
npm install -g @modelcontextprotocol/server-github

# MCP de Filesystem (leer/escribir archivos)
npm install -g @modelcontextprotocol/server-filesystem

# Verificar
npx @modelcontextprotocol/server-git --version
```

### Paso 3: Integrar con tu sistema Ollama

**Opción A: Usar el adapter** (`mcp_adapter.py` ya creado)

1. Importar en `ollama_multi_tools.py`:
```python
from mcp_adapter import (
    git_status_mcp,
    github_repo_info_mcp,
    GIT_STATUS_TOOL,
    GITHUB_REPO_INFO_TOOL,
    KEYWORDS as MCP_KEYWORDS
)

# Añadir a available_functions
available_functions = {
    'obtener_pronostico_temperatura': obtener_pronostico_temperatura,
    'clonar_repositorio_git': clonar_repositorio_git,
    'git_status_mcp': git_status_mcp,  # ← Nueva
    'github_repo_info_mcp': github_repo_info_mcp,  # ← Nueva
}

# Añadir a tools_registry
tools_registry = [
    # ... existentes ...
    {
        'definition': GIT_STATUS_TOOL,
        'keywords': MCP_KEYWORDS,
        'name': 'git-status'
    },
    {
        'definition': GITHUB_REPO_INFO_TOOL,
        'keywords': MCP_KEYWORDS,
        'name': 'github-info'
    }
]
```

2. ¡Listo! Ahora puedes:
```bash
python ollama_multi_tools.py
>>> ¿Cuál es el estado de mi repositorio?
[Usa git_status_mcp → llama MCP de Node.js → devuelve resultado]

>>> Dame info del repo microsoft/vscode en GitHub
[Usa github_repo_info_mcp → llama MCP GitHub → devuelve estrellas, forks, etc.]
```

---

## 📦 MCPs Disponibles (Oficiales de Anthropic)

### 1. **@modelcontextprotocol/server-git**
```bash
npm install -g @modelcontextprotocol/server-git
```

**Tools disponibles:**
- `git_status` - Estado del repo
- `git_diff` - Ver diferencias
- `git_log` - Historial de commits  
- `git_show` - Ver commit específico
- `git_add` - Añadir archivos al stage
- `git_commit` - Crear commit
- `git_push` - Subir cambios
- `git_pull` - Bajar cambios

---

### 2. **@modelcontextprotocol/server-github**
```bash
npm install -g @modelcontextprotocol/server-github
```

**Tools disponibles:**
- `get_repository` - Info del repo
- `search_repositories` - Buscar repos
- `list_commits` - Ver commits
- `get_issue` - Info de issue
- `create_issue` - Crear issue
- `create_pull_request` - Crear PR
- `list_pull_requests` - Listar PRs

**Requiere:** GitHub Token (crear en https://github.com/settings/tokens)

---

### 3. **@modelcontextprotocol/server-filesystem**
```bash
npm install -g @modelcontextprotocol/server-filesystem
```

**Tools disponibles:**
- `read_file` - Leer archivo
- `write_file` - Escribir archivo
- `list_directory` - Listar directorio
- `create_directory` - Crear carpeta
- `move_file` - Mover archivo
- `search_files` - Buscar archivos

---

### 4. **@modelcontextprotocol/server-brave-search**
```bash
npm install -g @modelcontextprotocol/server-brave-search
```

**Tools disponibles:**
- `brave_web_search` - Buscar en web
- `brave_local_search` - Buscar localmente

**Requiere:** Brave Search API Key

---

## 🧪 Ejemplo Completo

### Usar Git Status MCP:

```python
# En ollama_multi_tools.py después de añadir mcp_adapter

>>> ¿Qué archivos he modificado en mi repo?
```

**Detrás de escena:**
1. Ollama detecta que necesita info de Git
2. Llama a `git_status_mcp(repo_path='.')`
3. Python ejecuta: `npx @modelcontextprotocol/server-git`
4. MCP de Node.js ejecuta: `git status --porcelain`
5. Devuelve: "Modified: 3 files, Untracked: 2 files..."
6. Ollama presenta resultado al usuario

---

## ⚡ Optimización: Cache de MCPs

Si usas MCPs frecuentemente, puedes:

1. **Mantener MCP corriendo** (servidor persistente)
2. **Usar MCP Python SDK** en lugar de subprocess
3. **Traducir MCPs críticos** a Python nativo

---

## 🎯 Recomendación Final

**Para tu caso (Ollama + Python):**

### Corto plazo:
✅ Usa `mcp_adapter.py` (ya creado)
✅ Instala MCPs oficiales de Anthropic
✅ Empieza con Git y GitHub MCPs

### Largo plazo:
✅ Traduce MCPs más usados a Python nativo
✅ Crea tus propias tools Python especializadas
✅ Considera migrar a MCP Python SDK si necesitas más MCPs

---

## 📝 Próximos pasos

1. **Instala Node.js** en el servidor:
   ```bash
   curl -fsSL https://deb.nodesource.com/setup_20.x | sudo -E bash -
   sudo apt-get install -y nodejs
   ```

2. **Instala MCPs oficiales**:
   ```bash
   npm install -g @modelcontextprotocol/server-git
   npm install -g @modelcontextprotocol/server-github
   ```

3. **Integra mcp_adapter.py** en `ollama_multi_tools.py`

4. **Prueba**:
   ```bash
   python ollama_multi_tools.py
   >>> Dame el estado de mi repositorio git
   ```

---

## 🔗 Referencias

- **MCP Servers (Anthropic):** https://github.com/modelcontextprotocol/servers
- **MCP Spec:** https://modelcontextprotocol.io
- **Awesome MCP:** https://github.com/punkpeye/awesome-mcp

---

**¿Quieres que integre `mcp_adapter.py` en tu `ollama_multi_tools.py`?** 🚀

Te puedo:
1. ✅ Hacer la integración completa
2. ✅ Crear más adapters para otros MCPs
3. ✅ O traducir MCPs específicos a Python puro

**Dime cuál prefieres!** 💡
