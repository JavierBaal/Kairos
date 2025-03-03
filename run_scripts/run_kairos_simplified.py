import os
import sys
import traceback
from pathlib import Path

def setup_environment():
    """Configura el entorno de ejecución."""
    try:
        # Obtener ruta del directorio raíz del proyecto
        root_dir = str(Path(__file__).parent.parent.absolute())
        print(f"Directorio raíz: {root_dir}")
        
        # Cambiar al directorio raíz
        os.chdir(root_dir)
        
        # Añadir directorio raíz al path de Python
        if root_dir not in sys.path:
            sys.path.insert(0, root_dir)
            print(f"Añadido al PATH: {root_dir}")
        
        # Verificar las variables de entorno de PyQt
        pyqt_paths = [
            os.path.join(root_dir, "venv", "Lib", "site-packages", "PyQt6", "Qt6", "plugins"),
            os.path.join(sys.prefix, "Lib", "site-packages", "PyQt6", "Qt6", "plugins"),
        ]
        
        for path in pyqt_paths:
            if os.path.exists(path) and path not in os.environ.get("QT_PLUGIN_PATH", ""):
                os.environ["QT_PLUGIN_PATH"] = path + os.pathsep + os.environ.get("QT_PLUGIN_PATH", "")
                print(f"Añadida ruta de plugins Qt: {path}")
        
        return True
        
    except Exception as e:
        print(f"Error al configurar el entorno: {e}")
        traceback.print_exc()
        return False

def run_application():
    """Ejecuta la aplicación principal."""
    try:
        print("\nIniciando aplicación...")
        from main_simple import main
        return main()
    except Exception as e:
        print(f"\nError al iniciar la aplicación: {e}")
        traceback.print_exc()
        return 1

def main():
    """Función principal de ejecución."""
    print("\n=== Kairos Intelligence System ===")
    print(f"Python {sys.version}")
    
    if not setup_environment():
        print("\nError: No se pudo configurar el entorno correctamente")
        return 1
    
    print("\nEntorno configurado correctamente")
    print("--------------------------------")
    
    return run_application()

if __name__ == "__main__":
    try:
        sys.exit(main())
    except KeyboardInterrupt:
        print("\nAplicación terminada por el usuario")
        sys.exit(0)
    except Exception as e:
        print(f"\nError fatal: {e}")
        traceback.print_exc()
        sys.exit(1)
