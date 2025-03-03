import sys
import traceback
from PyQt6.QtWidgets import QApplication, QMainWindow
from PyQt6.QtCore import QTimer

class MainWindow(QMainWindow):
    def __init__(self):
        print("Iniciando MainWindow...")
        super().__init__()
        self.init_ui()
    
    def init_ui(self):
        """Inicializa la interfaz de usuario."""
        print("Configurando interfaz de usuario...")
        self.setWindowTitle('Kairos Intelligence System')
        self.setMinimumSize(1024, 768)
        
        try:
            print("Importando módulos UI...")
            from ui.workflow_panel_simplified import WorkflowPanelSimplified
            from ui.theme import Theme
            
            print("Aplicando tema...")
            Theme.apply_to_app(QApplication.instance())
            
            print("Creando panel de workflow...")
            self.workflow_panel = WorkflowPanelSimplified()
            self.setCentralWidget(self.workflow_panel)
            
            print("Interfaz configurada correctamente.")
            
        except Exception as e:
            print(f"Error al inicializar UI: {e}")
            traceback.print_exc()
            raise

def main():
    try:
        print("\nIniciando aplicación Kairos...")
        print(f"Python {sys.version}")
        print(f"Qt Path: {QApplication.libraryPaths()}")
        
        # Crear aplicación
        app = QApplication(sys.argv)
        
        # Crear y mostrar la ventana principal
        window = MainWindow()
        window.show()
        
        print("\nAplicación iniciada correctamente.")
        print("----------------------------------------")
        
        # Ejecutar aplicación
        return app.exec()
        
    except Exception as e:
        print(f"\nError fatal al iniciar la aplicación: {e}")
        traceback.print_exc()
        return 1

if __name__ == "__main__":
    sys.exit(main())
