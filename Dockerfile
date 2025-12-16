FROM debian:13

# Instalar dependencias del sistema
RUN apt-get update && apt-get install -y \
    python3 \
    python3-pip \
    python3-venv \
    curl \
    nodejs \
    npm \
    jq \
    && rm -rf /var/lib/apt/lists/*

# Instalar Ollama
RUN curl -fsSL https://ollama.com/install.sh | sh

# Crear directorio de trabajo
WORKDIR /app

# Copiar requirements.txt
COPY requirements.txt .

# Crear entorno virtual de Python
RUN python3 -m venv /ollama-agente

# Activar entorno virtual e instalar dependencias
RUN /ollama-agente/bin/pip install --upgrade pip && \
    /ollama-agente/bin/pip install -r requirements.txt

RUN rm /etc/localtime && \
    ln -s /usr/share/zoneinfo/Europe/Madrid /etc/localtime 

# Copiar y configurar script de entrada
COPY docker-entrypoint.sh /docker-entrypoint.sh
RUN chmod +x /docker-entrypoint.sh

# Agregar activación del entorno virtual al inicio del contenedor
RUN echo 'source /ollama-agente/bin/activate' >> /root/.bashrc

RUN echo '#!/bin/bash' > /usr/local/bin/python \
    && echo 'source /ollama-agente/bin/activate' >> /usr/local/bin/python \
    && echo 'exec python3 "$@"' >> /usr/local/bin/python

RUN chmod +x /usr/local/bin/python

# Exponer puerto de Ollama (por defecto 11434)
EXPOSE 11434
EXPOSE 5000

# Comando por defecto
CMD ["bash", "/docker-entrypoint.sh"]
