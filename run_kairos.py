!/usr/bin/env python3
"""
Kairos Intelligence System - Launcher Script
Este script inicia la aplicación Kairos Intelligence System.
"""

import sys
import os
import subprocess
import platform

def check_dependencies():
    """Verifica que todas las dependencias estén instaladas"""
    try:
        import PyQt6
        import yaml
        return True
    except ImportError as e:
        print(f"Error: Falta dependencia - {e}")
        return False

def install_dependencies():
    """Instala las dependencias necesarias"""
    print("Instalando dependencias...")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        return True
    except subprocess.CalledProcessError:
        print("Error al instalar dependencias. Intenta ejecutar manualmente:")
        print("pip install -r requirements.txt")
        return False

def ensure_config_directories():
    """Asegura que existan los directorios de configuración necesarios"""
    os.makedirs("config", exist_ok=True)
    os.makedirs("config/templates", exist_ok=True)
    os.makedirs("results", exist_ok=True)

def run_application():
    """Ejecuta la aplicación principal"""
    print("Iniciando Kairos Intelligence System...")
    
    # En Windows, usa pythonw.exe para evitar la ventana de consola
    if platform.system() == "Windows":
        try:
            subprocess.Popen([sys.executable, "main.py"])
        except Exception as e:
            print(f"Error al iniciar la aplicación: {e}")
            return False
    else:
        try:
            subprocess.Popen([sys.executable, "main.py"])
        except Exception as e:
            print(f"Error al iniciar la aplicación: {e}")
            return False
    
    return True

def main():
    """Función principal"""
    print("=== Kairos Intelligence System ===")
    
    # Verificar dependencias
    if not check_dependencies():
        print("Faltan dependencias. ¿Deseas instalarlas ahora? (s/n)")
        choice = input().lower()
        if choice == 's' or choice == 'y':
            if not install_dependencies():
                return
        else:
            print("No se pueden instalar las dependencias. Saliendo...")
            return
    
    # Asegurar directorios de configuración
    ensure_config_directories()
    
    # Ejecutar aplicación
    run_application()
    
    print("Aplicación iniciada. Puedes cerrar esta ventana.")

if __name__ == "__main__":
    main()
