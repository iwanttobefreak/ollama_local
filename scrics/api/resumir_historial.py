#!/usr/bin/env python3
# resumir_historial.py
#
# Uso:
#     python resumir_historial.py <persona>

import os
import sys
import json
import shutil
from datetime import datetime
import requests

HIST_DIR = "historial"
MODEL = "llama3.1:latest"
OLLAMA_URL = "http://localhost:11434/v1/chat/completions"

def leer_historial(path):
    if not os.path.exists(path):
        return ""
    with open(path, "r", encoding="utf-8") as f:
        return f.read().strip()

def generar_resumen(texto):
    """
    Pide a Ollama un resumen claro y conciso del historial completo.
    NO debe incluir instrucciones, disculpas ni pedir contexto.
    """
    prompt = f"""
Eres un asistente que resume historiales de conversación.

Resumen SOLO del siguiente historial:

--------------------------------
{texto}
--------------------------------

Instrucciones:
- Haz un resumen breve y claro.
- No digas que falta contexto.
- No pidas más información.
- No menciones que no entiendes algo.
- No añadas explicaciones del proceso.
- NO DIGAS "Aquí está el resumen", solo entrega el contenido.

DEVUELVE ÚNICAMENTE EL RESUMEN, NADA MÁS.
"""

    payload = {
        "model": MODEL,
        "messages": [
            {"role": "system", "content": "Eres un asistente que resume sin añadir explicaciones."},
            {"role": "user", "content": prompt}
        ]
    }

    resp = requests.post(OLLAMA_URL, json=payload)
    if resp.status_code != 200:
        print("❌ Error llamando a Ollama:", resp.text)
        return None

    try:
        data = resp.json()
        return data["choices"][0]["message"]["content"].strip()
    except Exception:
        print("❌ Error parseando JSON:", resp.text)
        return None

def escribir_historial_resumido(persona, resumen):
    path = os.path.join(HIST_DIR, f"{persona}_history.txt")

    contenido = (
        f"Usuario: Resumen del historial previo\n"
        f"{persona.capitalize()}: {resumen}\n"
    )

    with open(path, "w", encoding="utf-8") as f:
        f.write(contenido)

    print(f"✔ Historial resumido escrito en {path}")

def backup_historial(path):
    fecha = datetime.now().strftime("%Y%m%d_%H%M%S")
    destino = f"{path}_{fecha}"
    shutil.move(path, destino)
    print(f"✔ Backup creado: {destino}")

def main():
    if len(sys.argv) != 2:
        print("Uso: python resumir_historial.py <persona>")
        sys.exit(1)

    persona = sys.argv[1].lower()
    path_hist = os.path.join(HIST_DIR, f"{persona}_history.txt")

    historial = leer_historial(path_hist)

    if historial.strip() == "":
        print("⚠ Historial vacío, nada que resumir.")
        sys.exit(0)

    # Crear copia de seguridad
    backup_historial(path_hist)

    # Resumir
    resumen = generar_resumen(historial)
    if not resumen:
        print("❌ No se pudo generar resumen.")
        sys.exit(1)

    # Escribir el nuevo historial
    escribir_historial_resumido(persona, resumen)

if __name__ == "__main__":
    main()

