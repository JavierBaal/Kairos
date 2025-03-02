"""
Kairos Intelligence System - Componente de Tarjeta
Este módulo proporciona un componente de tarjeta para mejorar la organización visual.
"""

from PyQt6.QtWidgets import QFrame, QVBoxLayout, QLabel, QHBoxLayout, QWidget
from PyQt6.QtCore import Qt, pyqtSignal

class Card(QFrame):
    """Componente de tarjeta para mejorar la organización visual."""
    
    clicked = pyqtSignal()
    
    def __init__(self, title="", icon=None, parent=None):
        super().__init__(parent)
        
        # Configurar el estilo de la tarjeta
        self.setObjectName("card")
        self.setFrameShape(QFrame.Shape.StyledPanel)
        self.setFrameShadow(QFrame.Shadow.Raised)
        self.setCursor(Qt.CursorShape.PointingHandCursor)
        
        # Crear layout principal
        self.main_layout = QVBoxLayout(self)
        self.main_layout.setContentsMargins(12, 12, 12, 12)
        self.main_layout.setSpacing(8)
        
        # Crear encabezado
        if title or icon:
            header_layout = QHBoxLayout()
            header_layout.setContentsMargins(0, 0, 0, 0)
            header_layout.setSpacing(8)
            
            # Añadir icono si existe
            if icon:
                header_layout.addWidget(icon)
            
            # Añadir título
            if title:
                title_label = QLabel(title)
                title_label.setObjectName("cardTitle")
                title_label.setStyleSheet("font-weight: bold; font-size: 14px;")
                header_layout.addWidget(title_label)
            
            # Añadir espacio flexible
            header_layout.addStretch()
            
            # Añadir encabezado al layout principal
            self.main_layout.addLayout(header_layout)
        
        # Crear contenedor para el contenido
        self.content_widget = QWidget()
        self.content_layout = QVBoxLayout(self.content_widget)
        self.content_layout.setContentsMargins(0, 0, 0, 0)
        self.content_layout.setSpacing(8)
        
        # Añadir contenedor al layout principal
        self.main_layout.addWidget(self.content_widget)
    
    def add_widget(self, widget):
        """Añadir un widget al contenido de la tarjeta."""
        self.content_layout.addWidget(widget)
    
    def add_layout(self, layout