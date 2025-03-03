from PyQt6.QtWidgets import QFrame, QVBoxLayout, QLabel, QWidget
from PyQt6.QtCore import Qt

class AgentCard(QFrame):
    def __init__(self, name, description, variant="default", parent=None):
        super().__init__(parent)
        
        # Configurar el frame
        self.setProperty("card", True)
        self.setFixedSize(200, 200)
        
        # Configurar el estilo según la variante
        self.variant = variant
        self.setProperty(variant, True)
        
        # Layout principal
        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.setLayout(layout)
        
        # Círculo con inicial
        self.circle = self._create_circle(name[0])
        layout.addWidget(self.circle, alignment=Qt.AlignmentFlag.AlignCenter)
        
        # Nombre
        name_label = QLabel(name)
        name_label.setProperty("heading", True)
        name_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(name_label)
        
        # Descripción
        desc_label = QLabel(description)
        desc_label.setProperty("text-muted", True)
        desc_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        desc_label.setWordWrap(True)
        layout.addWidget(desc_label)
        
        # Efecto hover
        self.setMouseTracking(True)

    def _create_circle(self, letter):
        # Widget circular contenedor
        outer_circle = QWidget()
        outer_circle.setFixedSize(64, 64)
        outer_circle.setProperty("circle-outer", True)
        outer_circle.setProperty(f"circle-outer-{self.variant}", True)
        
        # Widget circular interno con la letra
        inner_circle = QLabel(letter.upper())
        inner_circle.setFixedSize(40, 40)
        inner_circle.setAlignment(Qt.AlignmentFlag.AlignCenter)
        inner_circle.setProperty("circle-inner", True)
        inner_circle.setProperty(f"circle-inner-{self.variant}", True)
        
        # Layout para centrar el círculo interno
        layout = QVBoxLayout(outer_circle)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.addWidget(inner_circle, alignment=Qt.AlignmentFlag.AlignCenter)
        
        return outer_circle

    def enterEvent(self, event):
        """Efecto al pasar el mouse por encima."""
        self.setProperty("hover", True)
        self.style().unpolish(self)
        self.style().polish(self)
        super().enterEvent(event)

    def leaveEvent(self, event):
        """Efecto al quitar el mouse."""
        self.setProperty("hover", False)
        self.style().unpolish(self)
        self.style().polish(self)
        super().leaveEvent(event)
