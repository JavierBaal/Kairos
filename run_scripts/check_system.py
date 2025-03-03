import os
import sys
import shutil
from pathlib import Path
import importlib.util
import traceback
import subprocess

def run_pip_install(package):
    """Intenta instalar un paquete usando pip."""
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "--no-cache-dir", package])
        return True
    except subprocess.CalledProcessError:
        return False

def check_and_fix_python_version():
    """Verifica la versión de Python."""
    print(f"Python version: {sys.version}")
    if sys.version_info < (3, 8):
        print("❌ Se requiere Python 3.8 o superior")
        return False
    print("✓ Versión de Python OK")
    return True

def check_and_fix_dependency(module_name, package_name=None):
    """Verifica si un módulo puede ser importado y trata de instalarlo si no está."""
    if package_name is None:
        package_name = module_name

    try:
        module = importlib.import_module(module_name)
        version = getattr(module, '__version__', 'desconocida')
        print(f"✓ {package_name}: OK (versión {version})")
        return True
    except ImportError:
        print(f"❌ {package_name} no encontrado. Intentando instalar...")
        if run_pip_install(package_name):
            try:
                importlib.import_module(module_name)
                print(f"✓ {package_name} instalado correctamente")
                return True
            except ImportError:
                print(f"❌ No se pudo importar {package_name} después de instalarlo")
                return False
        else:
            print(f"❌ No se pudo instalar {package_name}")
            return False

def ensure_directory_exists(path):
    """Crea un directorio si no existe."""
    if not path.exists():
        try:
            path.mkdir(parents=True)
            print(f"✓ Directorio creado: {path}")
            return True
        except Exception as e:
            print(f"❌ No se pudo crear el directorio {path}: {e}")
            return False
    return True

def check_and_fix_project_structure():
    """Verifica y trata de arreglar la estructura del proyecto."""
    root_dir = Path(__file__).parent.parent
    required_dirs = ['ui', 'ui/components']
    required_files = [
        'main_simple.py',
        'ui/__init__.py',
        'ui/theme.py',
        'ui/design_system.py',
        'ui/components/__init__.py',
        'ui/components/agent_card.py',
        'ui/components/step_progress.py',
        'ui/components/collaboration_controls.py',
    ]
    
    print("\nVerificando estructura del proyecto:")
    all_ok = True
    
    # Verificar y crear directorios
    for dir_name in required_dirs:
        dir_path = root_dir / dir_name
        if not dir_path.is_dir():
            all_ok = ensure_directory_exists(dir_path) and all_ok
        else:
            print(f"✓ Directorio OK: {dir_name}")
    
    # Verificar archivos
    for file_path in required_files:
        full_path = root_dir / file_path
        if not full_path.is_file():
            print(f"❌ Archivo no encontrado: {file_path}")
            all_ok = False
        else:
            print(f"✓ Archivo OK: {file_path}")
    
    return all_ok

def check_qt_plugins():
    """Verifica la disponibilidad de plugins de Qt."""
    try:
        from PyQt6.QtWidgets import QApplication
        app = QApplication.instance() or QApplication([])
        paths = app.libraryPaths()
        print("\nRutas de plugins de Qt:")
        for path in paths:
            print(f"  - {path}")
        return True
    except Exception as e:
        print(f"\n❌ Error al verificar plugins de Qt: {e}")
        return False

def check_system():
    """Realiza todas las verificaciones del sistema e intenta arreglar problemas."""
    try:
        print("=== Verificación del Sistema ===\n")
        
        checks = [
            ("Versión de Python", check_and_fix_python_version),
            ("PyQt6", lambda: check_and_fix_dependency('PyQt6')),
            ("colour", lambda: check_and_fix_dependency('colour')),
            ("Plugins de Qt", check_qt_plugins),
            ("Estructura del proyecto", check_and_fix_project_structure),
        ]
        
        all_ok = True
        for name, check_func in checks:
            print(f"\nVerificando {name}...")
            try:
                if not check_func():
                    all_ok = False
                    print(f"❌ Fallo en: {name}")
            except Exception as e:
                all_ok = False
                print(f"❌ Error en {name}: {e}")
                traceback.print_exc()
        
        if not all_ok:
            print("\n❌ Se encontraron problemas en la verificación")
            return False
            
        print("\n✅ Todas las verificaciones completadas con éxito")
        return True
        
    except Exception as e:
        print(f"\nError durante la verificación: {e}")
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = check_system()
    if not success:
        print("\nSugerencias de solución:")
        print("1. Ejecute 'install.bat' para reinstalar las dependencias")
        print("2. Verifique que Python 3.8 o superior esté instalado")
        print("3. Asegúrese de tener acceso a Internet para descargar paquetes")
    sys.exit(0 if success else 1)
