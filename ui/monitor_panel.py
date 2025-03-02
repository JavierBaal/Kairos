"""
Kairos Intelligence System - Panel de Monitorización
Este módulo proporciona una interfaz para monitorizar agentes de LangChain.
"""

from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, 
    QScrollArea, QFrame, QProgressBar, QSplitter, QGridLayout
)
from PyQt6.QtCore import Qt, pyqtSlot
from PyQt6.QtGui import QFont

class AgentMonitorWidget(QFrame):
    """Widget para mostrar información de monitorización de un agente."""
    
    def __init__(self, agent_id, agent_name, agent_role, parent=None):
        super().__init__(parent)
        self.agent_id = agent_id
        
        # Configurar estilo
        self.setFrameShape(QFrame.Shape.StyledPanel)
        self.setFrameShadow(QFrame.Shadow.Raised)
        self.setObjectName("monitorCard")
        
        # Crear layout principal
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(12, 12, 12, 12)
        main_layout.setSpacing(8)
        
        # Encabezado con nombre y rol
        header_layout = QHBoxLayout()
        
        # Nombre del agente
        name_label = QLabel(agent_name)
        name_label.setFont(QFont("Segoe UI", 12, QFont.Weight.Bold))
        header_layout.addWidget(name_label)
        
        # Rol del agente
        role_label = QLabel(f"({agent_role})")
        role_label.setObjectName("roleLabel")
        header_layout.addWidget(role_label)
        
        # Espacio flexible
        header_layout.addStretch()
        
        # Añadir encabezado al layout principal
        main_layout.addLayout(header_layout)
        
        # Grid para métricas
        metrics_grid = QGridLayout()
        metrics_grid.setColumnStretch(1, 1)  # La segunda columna se estira
        
        # Estado
        metrics_grid.addWidget(QLabel("Estado:"), 0, 0)
        self.status_label = QLabel("Inicializando...")
        self.status_label.setObjectName("statusLabel")
        metrics_grid.addWidget(self.status_label, 0, 1)
        
        # Progreso
        metrics_grid.addWidget(QLabel("Progreso:"), 1, 0)
        progress_layout = QHBoxLayout()
        self.progress_bar = QProgressBar()
        self.progress_bar.setRange(0, 100)
        self.progress_bar.setValue(0)
        self.progress_bar.setTextVisible(True)
        progress_layout.addWidget(self.progress_bar)
        self.progress_label = QLabel("0%")
        progress_layout.addWidget(self.progress_label)
        metrics_grid.addLayout(progress_layout, 1, 1)
        
        # Tokens
        metrics_grid.addWidget(QLabel("Tokens:"), 2, 0)
        self.tokens_label = QLabel("0")
        metrics_grid.addWidget(self.tokens_label, 2, 1)
        
        # Costo
        metrics_grid.addWidget(QLabel("Costo:"), 3, 0)
        self.cost_label = QLabel("$0.00")
        metrics_grid.addWidget(self.cost_label, 3, 1)
        
        # Añadir grid de métricas al layout principal
        main_layout.addLayout(metrics_grid)
    
    def update_status(self, status):
        """Actualizar el estado del agente."""
        self.status_label.setText(status)
    
    def update_progress(self, progress):
        """Actualizar el progreso del agente."""
        self.progress_bar.setValue(progress)
        self.progress_label.setText(f"{progress}%")
    
    def update_tokens(self, tokens):
        """Actualizar el contador de tokens del agente."""
        self.tokens_label.setText(f"{tokens:,}")
    
    def update_cost(self, cost):
        """Actualizar el costo del agente."""
        self.cost_label.setText(f"${cost:.2f}")


class MonitorPanel(QWidget):
    """Panel para monitorizar agentes de LangChain."""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        
        # Crear layout principal
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(16, 16, 16, 16)
        main_layout.setSpacing(16)
        
        # Título
        title_label = QLabel("Monitorización de Agentes")
        title_label.setFont(QFont("Segoe UI", 16, QFont.Weight.Bold))
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        main_layout.addWidget(title_label)
        
        # Panel de control
        control_layout = QHBoxLayout()
        
        # Información general
        info_layout = QVBoxLayout()
        
        # Costo total
        cost_layout = QHBoxLayout()
        cost_layout.addWidget(QLabel("Costo Total:"))
        self.total_cost_label = QLabel("$0.00")
        self.total_cost_label.setFont(QFont("Segoe UI", 12, QFont.Weight.Bold))
        cost_layout.addWidget(self.total_cost_label)
        cost_layout.addStretch()
        info_layout.addLayout(cost_layout)
        
        # Límite de costo
        limit_layout = QHBoxLayout()
        limit_layout.addWidget(QLabel("Límite de Costo:"))
        self.cost_limit_label = QLabel("No establecido")
        limit_layout.addWidget(self.cost_limit_label)
        limit_layout.addStretch()
        info_layout.addLayout(limit_layout)
        
        control_layout.addLayout(info_layout)
        control_layout.addStretch()
        
        # Botones de control
        button_layout = QHBoxLayout()
        
        self.set_limit_button = QPushButton("Establecer Límite")
        self.set_limit_button.setObjectName("primaryButton")
        button_layout.addWidget(self.set_limit_button)
        
        self.reset_button = QPushButton("Reiniciar Contadores")
        button_layout.addWidget(self.reset_button)
        
        control_layout.addLayout(button_layout)
        
        main_layout.addLayout(control_layout)
        
        # Área de desplazamiento para los agentes
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setFrameShape(QFrame.Shape.NoFrame)
        
        # Contenedor para los widgets de agentes
        self.agents_container = QWidget()
        self.agents_layout = QVBoxLayout(self.agents_container)
        self.agents_layout.setContentsMargins(0, 0, 0, 0)
        self.agents_layout.setSpacing(16)
        self.agents_layout.addStretch()  # Para que los widgets se alineen en la parte superior
        
        scroll_area.setWidget(self.agents_container)
        main_layout.addWidget(scroll_area)
        
        # Diccionario para almacenar los widgets de agentes
        self.agent_widgets = {}
    
    def add_agent(self, agent_id, agent_name, agent_role):
        """Añadir un nuevo agente al panel de monitorización."""
        if agent_id in self.agent_widgets:
            return
        
        # Crear widget para el agente
        agent_widget = AgentMonitorWidget(agent_id, agent_name, agent_role)
        
        # Añadir al layout antes del stretch
        self.agents_layout.insertWidget(self.agents_layout.count() - 1, agent_widget)
        
        # Almacenar referencia
        self.agent_widgets[agent_id] = agent_widget
    
    def update_agent_status(self, agent_id, status):
        """Actualizar el estado de un agente."""
        if agent_id in self.agent_widgets:
            self.agent_widgets[agent_id].update_status(status)
    
    def update_agent_progress(self, agent_id, progress):
        """Actualizar el progreso de un agente."""
        if agent_id in self.agent_widgets:
            self.agent_widgets[agent_id].update_progress(progress)
    
    def update_agent_tokens(self, agent_id, tokens):
        """Actualizar los tokens de un agente."""
        if agent_id in self.agent_widgets:
            self.agent_widgets[agent_id].update_tokens(tokens)
    
    def update_agent_cost(self, agent_id, cost):
        """Actualizar el costo de un agente."""
        if agent_id in self.agent_widgets:
            self.agent_widgets[agent_id].update_cost(cost)
    
    def update_total_cost(self, total_cost):
        """Actualizar el costo total."""
        self.total_cost_label.setText(f"${total_cost:.2f}")
    
    def update_cost_limit(self, limit):
        """Actualizar el límite de costo."""
        if limit is None:
            self.cost_limit_label.setText("No establecido")
        else:
            self.cost_limit_label.setText(f"${limit:.2f}")
    
    def update_from_state(self, monitoring_state):
        """Actualizar el panel desde el estado de monitorización."""
        # Actualizar costo total
        if "total_cost" in monitoring_state:
            self.update_total_cost(monitoring_state["total_cost"])
        
        # Actualizar límite de costo
        if "cost_limit" in monitoring_state:
            self.update_cost_limit(monitoring_state["cost_limit"])
        
        # Actualizar agentes activos
        if "active_agents" in monitoring_state:
            for agent_id, agent_data in monitoring_state["active_agents"].items():
                # Añadir agente si no existe
                if agent_id not in self.agent_widgets and "name" in agent_data and "role" in agent_data:
                    self.add_agent(agent_id, agent_data["name"], agent_data["role"])
                
                # Actualizar métricas
                if "status" in agent_data:
                    self.update_agent_status(agent_id, agent_data["status"])
                if "progress" in agent_data:
                    self.update_agent_progress(agent_id, agent_data["progress"])
                if "tokens" in agent_data:
                    self.update_agent_tokens(agent_id, agent_data["tokens"])
                if "cost" in agent_data:
                    self.update_agent_cost(agent_id, agent_data["cost"])