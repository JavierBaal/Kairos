#!/usr/bin/env python3
"""
Kairos Intelligence System - Launcher Script
Este script inicia la aplicación Kairos Intelligence System.
"""

import sys
import os
import subprocess
import platform

# Nota: Las siguientes importaciones son para verificar si las dependencias están instaladas.
# Pylance puede mostrar advertencias, pero esto es normal ya que estamos verificando
# dinámicamente si las dependencias están disponibles.
# pylint: disable=import-error
# pyright: reportMissingImports=false

def check_python_version():
    """Verifica que la versión de Python sea compatible"""
    import sys
    python_version = sys.version_info
    
    if python_version.major < 3 or (python_version.major == 3 and python_version.minor < 10):
        print(f"✗ Versión de Python incompatible: {sys.version}")
        print("  CrewAI requiere Python 3.10 o superior.")
        print(f"  Tu versión actual es Python {python_version.major}.{python_version.minor}.{python_version.micro}")
        return False
    
    print(f"✓ Versión de Python compatible: {sys.version}")
    return True

def check_dependencies():
    """Verifica que todas las dependencias estén instaladas"""
    missing_deps = []
    
    # Verificar versión de Python primero
    if not check_python_version():
        print("\nDebes actualizar Python a la versión 3.10 o superior para usar CrewAI.")
        print("Puedes descargar la última versión desde: https://www.python.org/downloads/")
        return False, ["python-upgrade"]
    
    # Verificar PyQt6
    try:
        # Esta importación puede generar advertencias en Pylance, pero es intencional
        # para verificar si la dependencia está instalada
        import PyQt6  # type: ignore
        print("✓ PyQt6 está instalado")
    except ImportError:
        missing_deps.append("PyQt6")
        print("✗ PyQt6 no está instalado")
    
    # Verificar yaml
    try:
        # Esta importación puede generar advertencias en Pylance, pero es intencional
        import yaml  # type: ignore
        print("✓ PyYAML está instalado")
    except ImportError:
        missing_deps.append("pyyaml")
        print("✗ PyYAML no está instalado")
    
    # Verificar crewai
    try:
        # Esta importación puede generar advertencias en Pylance, pero es intencional
        import crewai  # type: ignore
        print("✓ CrewAI está instalado")
    except ImportError:
        missing_deps.append("crewai")
        print("✗ CrewAI no está instalado")
    except TypeError as e:
        # Capturar el error específico de versión de Python incompatible
        if "unsupported operand type(s) for |" in str(e):
            print("✗ Error al importar CrewAI: Versión de Python incompatible")
            print("  CrewAI requiere Python 3.10 o superior debido al uso del operador '|' para tipos.")
            return False, ["python-upgrade"]
        else:
            # Otro error de tipo
            print(f"✗ Error al importar CrewAI: {e}")
            return False, ["crewai-error"]
    
    # Nota: crewai-tools ya no es necesario
    # try:
    #     import crewai_tools
    #     print("✓ CrewAI-Tools está instalado")
    # except ImportError:
    #     missing_deps.append("crewai-tools")
    #     print("✗ CrewAI-Tools no está instalado")
    
    return len(missing_deps) == 0, missing_deps

def install_dependencies(missing_deps=None):
    """Instala las dependencias necesarias"""
    print("\nInstalando dependencias...")
    
    if missing_deps:
        # Verificar si necesitamos actualizar Python
        if "python-upgrade" in missing_deps:
            print("\n⚠️ ACCIÓN REQUERIDA: Actualización de Python ⚠️")
            print("CrewAI requiere Python 3.10 o superior.")
            print("Por favor, descarga e instala la última versión de Python desde:")
            print("https://www.python.org/downloads/")
            print("\nDespués de actualizar Python, vuelve a ejecutar este script.")
            return False
            
        # Instalar solo las dependencias faltantes
        for dep in missing_deps:
            if dep in ["python-upgrade", "crewai-error"]:
                continue  # Estos son marcadores especiales, no paquetes reales
                
            print(f"Instalando {dep}...")
            try:
                subprocess.check_call([sys.executable, "-m", "pip", "install", dep])
                print(f"✓ {dep} instalado correctamente")
            except subprocess.CalledProcessError:
                print(f"✗ Error al instalar {dep}")
                return False
        return True
    else:
        # Instalar todas las dependencias desde requirements.txt
        try:
            subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
            print("✓ Todas las dependencias instaladas correctamente")
            return True
        except subprocess.CalledProcessError:
            print("✗ Error al instalar dependencias desde requirements.txt")
            print("\nPuedes intentar instalarlas manualmente con los siguientes comandos:")
            print("pip install PyQt6")
            print("pip install pyyaml")
            print("pip install crewai")
            return False

def ensure_config_directories():
    """Asegura que existan los directorios de configuración necesarios"""
    os.makedirs("config", exist_ok=True)
    os.makedirs("config/templates", exist_ok=True)
    os.makedirs("results", exist_ok=True)

def run_application(simple_mode=False):
    """Ejecuta la aplicación principal"""
    script = "main_simple.py" if simple_mode else "main.py"
    print(f"Iniciando Kairos Intelligence System{' (Modo Básico)' if simple_mode else ''}...")
    
    # En Windows, usa pythonw.exe para evitar la ventana de consola
    if platform.system() == "Windows":
        try:
            subprocess.Popen([sys.executable, script])
        except Exception as e:
            print(f"Error al iniciar la aplicación: {e}")
            return False
    else:
        try:
            subprocess.Popen([sys.executable, script])
        except Exception as e:
            print(f"Error al iniciar la aplicación: {e}")
            return False
    
    return True

def main():
    """Función principal"""
    print("=== Kairos Intelligence System ===")
    print("Verificando dependencias...\n")
    
    # Verificar dependencias
    deps_ok, missing_deps = check_dependencies()
    
    # Determinar si debemos usar el modo simple
    use_simple_mode = False
    
    if not deps_ok:
        if "python-upgrade" in missing_deps:
            # Versión de Python incompatible, ofrecer modo simple
            print("\nDetectada versión de Python incompatible con CrewAI.")
            print("Puedes ejecutar Kairos en modo básico, que no requiere CrewAI,")
            print("o actualizar Python a la versión 3.10 o superior para acceder a todas las funcionalidades.")
            print("\n¿Deseas ejecutar Kairos en modo básico? (s/n)")
            choice = input().lower()
            if choice == 's' or choice == 'y':
                use_simple_mode = True
            else:
                print("\nPor favor, actualiza Python y vuelve a ejecutar este script.")
                return
        else:
            # Otras dependencias faltantes
            print("\nFaltan algunas dependencias necesarias para ejecutar Kairos.")
            print("¿Deseas instalarlas ahora? (s/n)")
            choice = input().lower()
            if choice == 's' or choice == 'y':
                if not install_dependencies(missing_deps):
                    print("\nNo se pudieron instalar todas las dependencias.")
                    print("Por favor, instálalas manualmente y vuelve a intentarlo.")
                    return
            else:
                print("\nNo se pueden ejecutar sin las dependencias necesarias. Saliendo...")
                return
    
    if not use_simple_mode:
        print("\nTodas las dependencias están instaladas correctamente.")
    
    # Asegurar directorios de configuración
    ensure_config_directories()
    
    # Ejecutar aplicación
    run_application(simple_mode=use_simple_mode)
    
    print("Aplicación iniciada. Puedes cerrar esta ventana.")

if __name__ == "__main__":
    main()
