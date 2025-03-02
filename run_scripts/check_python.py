#!/usr/bin/env python3
"""
Script para verificar la versión de Python y las rutas de instalación
"""

import sys
import os
import subprocess
import platform

def get_python_path():
    """Obtiene la ruta del ejecutable de Python actual"""
    return sys.executable

def get_python_version():
    """Obtiene la versión de Python actual"""
    return sys.version

def list_installed_pythons():
    """Intenta listar todas las instalaciones de Python en el sistema"""
    pythons = []
    
    # En Windows, buscar en el registro
    if platform.system() == "Windows":
        try:
            import winreg
            for version in ["3.9", "3.10", "3.11", "3.12"]:
                try:
                    key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, f"SOFTWARE\\Python\\PythonCore\\{version}\\InstallPath")
                    path, _ = winreg.QueryValueEx(key, "")
                    exe_path = os.path.join(path, "python.exe")
                    if os.path.exists(exe_path):
                        try:
                            # Intentar ejecutar python --version
                            result = subprocess.check_output([exe_path, "--version"], stderr=subprocess.STDOUT, text=True)
                            pythons.append((exe_path, result.strip()))
                        except:
                            pythons.append((exe_path, f"Python {version}"))
                except:
                    pass
        except:
            pass
    
    # Buscar en PATH
    try:
        paths = os.environ["PATH"].split(os.pathsep)
        for path in paths:
            for name in ["python", "python3", "python3.9", "python3.10", "python3.11", "python3.12"]:
                exe = name + (".exe" if platform.system() == "Windows" else "")
                exe_path = os.path.join(path, exe)
                if os.path.exists(exe_path) and os.path.isfile(exe_path):
                    try:
                        # Intentar ejecutar python --version
                        result = subprocess.check_output([exe_path, "--version"], stderr=subprocess.STDOUT, text=True)
                        if (exe_path, result.strip()) not in pythons:
                            pythons.append((exe_path, result.strip()))
                    except:
                        pass
    except:
        pass
    
    return pythons

def main():
    """Función principal"""
    print("=== Información de Python ===\n")
    
    # Mostrar versión actual
    print(f"Versión de Python actual: {get_python_version()}")
    print(f"Ruta del ejecutable: {get_python_path()}\n")
    
    # Verificar si la versión es compatible con CrewAI
    python_version = sys.version_info
    if python_version.major < 3 or (python_version.major == 3 and python_version.minor < 10):
        print("⚠️ Esta versión de Python NO es compatible con CrewAI.")
        print("CrewAI requiere Python 3.10 o superior debido al uso del operador '|' para tipos.\n")
    else:
        print("✓ Esta versión de Python ES compatible con CrewAI.\n")
    
    # Listar otras instalaciones de Python
    print("Buscando otras instalaciones de Python en el sistema...")
    pythons = list_installed_pythons()
    
    if pythons:
        print("\nInstalaciones de Python encontradas:")
        for i, (path, version) in enumerate(pythons, 1):
            print(f"{i}. {version} - {path}")
            
        print("\nSi tienes Python 3.10 o superior instalado pero no se está utilizando,")
        print("puedes especificar la ruta completa al ejecutar el script:")
        print("C:\\ruta\\a\\python310\\python.exe run_kairos.py")
    else:
        print("\nNo se encontraron otras instalaciones de Python.")
        print("Si tienes Python 3.10 o superior instalado pero no se detectó,")
        print("puedes especificar la ruta completa al ejecutar el script.")
    
    print("\nPara instalar la última versión de Python, visita:")
    print("https://www.python.org/downloads/")

if __name__ == "__main__":
    main()
