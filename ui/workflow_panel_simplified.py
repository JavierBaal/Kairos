from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QFrame, QScrollArea
)
from PyQt6.QtCore import Qt

from .components.step_progress import StepProgress
from .components.agent_card import AgentCard
from .components.collaboration_controls import CollaborationControls

class WorkflowPanelSimplified(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setup_ui()
    
    def setup_ui(self):
        # Layout principal
        layout = QVBoxLayout(self)
        layout.setContentsMargins(32, 32, 32, 32)
        layout.setSpacing(32)
        
        # Panel principal con efecto glass
        main_panel = QFrame()
        main_panel.setProperty("glass", True)
        main_panel_layout = QVBoxLayout()
        main_panel_layout.setSpacing(24)
        main_panel.setLayout(main_panel_layout)
        
        # Indicador de pasos en la parte superior
        steps = ["CONFIGURAR", "EJECUTAR", "RESULTADOS"]
        self.step_progress = StepProgress(steps)
        layout.addWidget(self.step_progress)
        
        # Controles de colaboración
        self.collaboration_controls = CollaborationControls()
        main_panel_layout.addWidget(self.collaboration_controls)
        
        # Área de agentes con scroll
        agents_scroll = QScrollArea()
        agents_scroll.setWidgetResizable(True)
        agents_scroll.setFrameShape(QFrame.Shape.NoFrame)
        
        agents_container = QWidget()
        agents_layout = QHBoxLayout()
        agents_layout.setSpacing(16)
        agents_container.setLayout(agents_layout)
        
        # Ejemplo de agentes
        agents_data = [
            ("Investigador", "Analiza datos y tendencias", "default"),
            ("Estratega", "Desarrolla estrategias competitivas", "orange"),
            ("Comunicador", "Genera reportes y presentaciones", "red"),
        ]
        
        for name, desc, variant in agents_data:
            agent_card = AgentCard(name, desc, variant)
            agents_layout.addWidget(agent_card)
        
        agents_layout.addStretch()
        agents_scroll.setWidget(agents_container)
        main_panel_layout.addWidget(agents_scroll)
        
        # Añadir el panel principal al layout
        layout.addWidget(main_panel)
        
        # Configurar estilos y tamaños
        self.setMinimumWidth(800)
        self.setMinimumHeight(600)
