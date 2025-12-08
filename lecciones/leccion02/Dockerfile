FROM ubuntu:22.04FROM ubuntu:22.04



# Instalar dependencias del sistema# Instalar dependencias del sistema

RUN apt-get update && apt-get install -y \RUN apt-get update && apt-get install -y \

    python3 \    python3 \

    python3-pip \    python3-pip \

    python3-venv \    python3-venv \

    curl \    curl \

    && rm -rf /var/lib/apt/lists/*    && rm -rf /var/lib/apt/lists/*



# Instalar Ollama# Instalar Ollama

RUN curl -fsSL https://ollama.com/install.sh | shRUN curl -fsSL https://ollama.com/install.sh | sh



# Crear directorio de trabajo# Crear directorio de trabajo

WORKDIR /appWORKDIR /app



# Copiar requirements.txt# Copiar requirements.txt

COPY requirements.txt .COPY requirements.txt .



# Crear entorno virtual de Python# Crear entorno virtual de Python

RUN python3 -m venv /ollama-agenteRUN python3 -m venv /ollama-agente



# Activar entorno virtual e instalar dependencias# Activar entorno virtual e instalar dependencias

RUN /ollama-agente/bin/pip install --upgrade pip && \RUN /ollama-agente/bin/pip install --upgrade pip && \

    /ollama-agente/bin/pip install -r requirements.txt    /ollama-agente/bin/pip install -r requirements.txt



# Copiar archivos del proyecto# Copiar archivos del proyecto

COPY . .COPY . .



# Copiar y configurar script de entrada# Copiar y configurar script de entrada

COPY docker-entrypoint.sh /docker-entrypoint.shCOPY docker-entrypoint.sh /docker-entrypoint.sh

RUN chmod +x /docker-entrypoint.shRUN chmod +x /docker-entrypoint.sh



# Exponer puerto de Ollama (por defecto 11434)# Exponer puerto de Ollama (por defecto 11434)

EXPOSE 11434EXPOSE 11434



# Comando por defecto# Comando por defecto

CMD ["/docker-entrypoint.sh"]CMD ["/docker-entrypoint.sh"]