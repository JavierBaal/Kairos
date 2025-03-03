import os
import sys
import platform
import subprocess
import json
from pathlib import Path
from datetime import datetime
import traceback

def get_system_info():
    """Recopila información del sistema."""
    info = {
        "system": platform.system(),
        "release": platform.release(),
        "version": platform.version(),
        "machine": platform.machine(),
        "processor": platform.processor(),
        "python_version": sys.version,
        "python_path": sys.executable,
        "pwd": os.getcwd(),
        "env_path": os.environ.get("PATH", ""),
        "timestamp": datetime.now().isoformat(),
    }
    return info

def get_pip_packages():
    """Obtiene la lista de paquetes instalados."""
    try:
        result = subprocess.run(
            [sys.executable, "-m", "pip", "list", "--format=json"],
            capture_output=True,
            text=True
        )
        return json.loads(result.stdout)
    except Exception as e:
        return {"error": str(e)}

def check_qt_installation():
    """Verifica la instalación de PyQt."""
    qt_info = {
        "pyqt_installed": False,
        "qt_version": None,
        "plugin_paths": [],
        "errors": []
    }
    
    try:
        import PyQt6
        qt_info["pyqt_installed"] = True
        qt_info["qt_version"] = PyQt6.__version__
        
        from PyQt6.QtWidgets import QApplication
        app = QApplication.instance() or QApplication([])
        qt_info["plugin_paths"] = app.libraryPaths()
        
    except Exception as e:
        qt_info["errors"].append(str(e))
    
    return qt_info

def check_project_structure():
    """Verifica la estructura del proyecto."""
    root_dir = Path(__file__).parent.parent
    structure = {
        "root": str(root_dir),
        "directories": [],
        "files": [],
        "missing": []
    }
    
    required_paths = [
        "ui",
        "ui/components",
        "run_scripts",
        "main_simple.py",
        "ui/__init__.py",
        "ui/theme.py",
        "ui/design_system.py",
        "ui/components/__init__.py",
        "ui/components/agent_card.py",
        "ui/components/step_progress.py",
        "ui/components/collaboration_controls.py",
    ]
    
    for path in required_paths:
        full_path = root_dir / path
        if full_path.exists():
            if full_path.is_dir():
                structure["directories"].append(path)
            else:
                structure["files"].append(path)
        else:
            structure["missing"].append(path)
    
    return structure

def check_font_availability():
    """Verifica la disponibilidad de fuentes."""
    font_info = {
        "system_fonts": [],
        "inter_available": False,
        "fallback_fonts": ["system-ui", "-apple-system", "Segoe UI", "Roboto", "Arial"]
    }
    
    if platform.system() == "Windows":
        import winreg
        try:
            with winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, r"SOFTWARE\Microsoft\Windows NT\CurrentVersion\Fonts") as key:
                i = 0
                while True:
                    try:
                        name, value, _ = winreg.EnumValue(key, i)
                        if "Inter" in name:
                            font_info["inter_available"] = True
                        font_info["system_fonts"].append(name)
                        i += 1
                    except WindowsError:
                        break
        except Exception as e:
            font_info["error"] = str(e)
    
    return font_info

def print_report_summary(report):
    """Imprime un resumen del reporte de diagnóstico."""
    print("\n=== Reporte de Diagnóstico de Kairos ===\n")
    
    # Sistema
    sys_info = report["system_info"]
    print("Sistema:")
    print(f"  OS: {sys_info['system']} {sys_info['release']}")
    print(f"  Python: {sys_info['python_version'].split()[0]}")
    
    # Qt
    qt = report["qt_installation"]
    print("\nPyQt:")
    print(f"  Instalado: {'✓' if qt['pyqt_installed'] else '❌'}")
    if qt['qt_version']:
        print(f"  Versión: {qt['qt_version']}")
    if qt['errors']:
        print(f"  Errores: {', '.join(qt['errors'])}")
    
    # Estructura del proyecto
    structure = report["project_structure"]
    print("\nEstructura del Proyecto:")
    print(f"  Directorios OK: {len(structure['directories'])}")
    print(f"  Archivos OK: {len(structure['files'])}")
    if structure['missing']:
        print("  Faltantes:")
        for item in structure['missing']:
            print(f"    - {item}")
    
    # Fuentes
    fonts = report["font_info"]
    print("\nFuentes:")
    print(f"  Inter disponible: {'✓' if fonts['inter_available'] else '❌'}")
    if not fonts['inter_available']:
        print("  Fuentes de respaldo disponibles:")
        for font in fonts['fallback_fonts']:
            print(f"    - {font}")

def generate_diagnostic_report():
    """Genera un informe de diagnóstico completo."""
    report = {
        "system_info": get_system_info(),
        "pip_packages": get_pip_packages(),
        "qt_installation": check_qt_installation(),
        "project_structure": check_project_structure(),
        "font_info": check_font_availability()
    }
    
    # Guardar reporte
    report_path = Path(__file__).parent / "diagnostic_report.json"
    with open(report_path, "w", encoding="utf-8") as f:
        json.dump(report, f, indent=2, ensure_ascii=False)
    
    return report, report_path

if __name__ == "__main__":
    try:
        report, report_path = generate_diagnostic_report()
        print_report_summary(report)
        print(f"\nReporte completo guardado en: {report_path}")
        sys.exit(0)
    except Exception as e:
        print(f"Error al generar diagnóstico: {e}")
        traceback.print_exc()
        sys.exit(1)
