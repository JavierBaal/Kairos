from PyQt6.QtWidgets import QWidget, QHBoxLayout, QPushButton, QVBoxLayout, QLabel
from PyQt6.QtCore import Qt

class CollaborationControls(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self._setup_ui()
    
    def _setup_ui(self):
        layout = QHBoxLayout()
        layout.setSpacing(16)
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.setLayout(layout)
        
        # Botón Configurar
        config_section = self._create_section(
            "Configurar",
            "Configura los agentes y tareas",
            "primary"
        )
        layout.addWidget(config_section)
        
        # Botón Ejecutar
        execute_section = self._create_section(
            "Ejecutar",
            "Inicia la colaboración",
            "orange"
        )
        layout.addWidget(execute_section)
        
        # Botón Resultados
        results_section = self._create_section(
            "Resultados",
            "Revisa los resultados",
            "red"
        )
        layout.addWidget(results_section)
        
    def _create_section(self, title, description, variant):
        container = QWidget()
        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        container.setLayout(layout)
        
        button = QPushButton(title)
        button.setProperty(variant, True)
        button.setFixedHeight(40)
        layout.addWidget(button, alignment=Qt.AlignmentFlag.AlignCenter)
        
        desc_label = QLabel(description)
        desc_label.setProperty("text-muted", True)
        desc_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        desc_label.setWordWrap(True)
        layout.addWidget(desc_label)
        
        return container
