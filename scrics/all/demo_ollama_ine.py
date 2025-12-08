#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Demo rapida del sistema de consulta de poblacion INE con Ollama
Ejecuta algunos ejemplos predefinidos
"""

from ollama_ine import chat_con_herramientas


def demo():
    """
    Ejecuta una demostracion con preguntas predefinidas
    """
    print("=" * 70)
    print("DEMO - CONSULTA DE POBLACION INE CON OLLAMA")
    print("=" * 70)
    print()
    print("Esta demo ejecutara varias consultas de ejemplo para mostrar")
    print("como funciona la integracion de Ollama con la API del INE.")
    print()
    print("=" * 70)
    
    # Preguntas de ejemplo
    preguntas = [
        "¿Cuántos habitantes tenía Madrid en 2021?",
        "Dame la población de Barcelona en 2020",
        "¿Cuál era la población de Murcia en 2019?",
        "Compara Sevilla y Valencia en 2020",
    ]
    
    for i, pregunta in enumerate(preguntas, 1):
        print()
        print(f"\n{'='*70}")
        print(f"EJEMPLO {i}/{len(preguntas)}")
        print('='*70)
        print()
        
        try:
            chat_con_herramientas(pregunta, verbose=True)
        except Exception as e:
            print(f"[ERROR] {e}")
        
        if i < len(preguntas):
            print("\nPresiona Enter para continuar...")
            input()
    
    print()
    print("=" * 70)
    print("DEMO COMPLETADA")
    print("=" * 70)
    print()
    print("Para usar el modo interactivo, ejecuta:")
    print("  python ollama_ine.py")
    print()


if __name__ == "__main__":
    demo()
