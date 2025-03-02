#!/usr/bin/env python3
"""
Kairos Intelligence System - Agent Monitor Widget
Este módulo implementa un widget para monitorizar agentes y sus costos.
"""

from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QProgressBar,
    QPushButton, QFrame, QSizePolicy, QSpacerItem, QScrollArea
)
from PyQt6.QtCore import Qt, pyqtSignal, pyqtSlot, QTimer
from PyQt6.QtGui import QIcon, QPixmap

class AgentMonitorWidget(QWidget):
    """Widget para monitorizar un agente y su costo."""
    
    # Señales
    pause_requested = pyqtSignal(str)  # ID del agente
    resume_requested = pyqtSignal(str)  # ID del agente
    modify_requested = pyqtSignal(str)  # ID del agente
    
    def __init__(self, agent_id, agent_name, agent_role, parent=None):
        super().__init__(parent)
        self.agent_id = agent_id
        self.agent_name = agent_name
        self.agent_role = agent_role
        self.is_paused = False
        self.cost = 0.0
        self.tokens = 0
        self.progress = 0
        
        # Configurar el widget
        self.setObjectName("agentMonitor")
        self.setup_ui()
        
    def setup_ui(self):
        """Configurar la interfaz de usuario del widget."""
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(15, 15, 15, 15)
        main_layout.setSpacing(10)
        
        # Encabezado: Nombre y rol del agente
        header_layout = QHBoxLayout()
        
        # Icono del agente (placeholder)
        self.agent_icon = QLabel()
        self.agent_icon.setFixedSize(40, 40)
        self.agent_icon.setStyleSheet("background-color: rgba(255, 255, 255, 0.1); border-radius: 20px;")
        header_layout.addWidget(self.agent_icon)
        
        # Información del agente
        agent_info_layout = QVBoxLayout()
        self.name_label = QLabel(self.agent_name)
        self.name_label.setObjectName("agentName")
        self.role_label = QLabel(self.agent_role)
        self.role_label.setObjectName("agentRole")
        
        agent_info_layout.addWidget(self.name_label)
        agent_info_layout.addWidget(self.role_label)
        header_layout.addLayout(agent_info_layout)
        
        # Botones de control
        control_layout = QHBoxLayout()
        
        self.pause_button = QPushButton()
        self.pause_button.setFixedSize(30, 30)
        self.pause_button.setToolTip("Pausar agente")
        self.pause_button.clicked.connect(self.toggle_pause)
        
        self.modify_button = QPushButton()
        self.modify_button.setFixedSize(30, 30)
        self.modify_button.setToolTip("Modificar agente")
        self.modify_button.clicked.connect(self.request_modify)
        
        control_layout.addWidget(self.pause_button)
        control_layout.addWidget(self.modify_button)
        header_layout.addLayout(control_layout)
        
        main_layout.addLayout(header_layout)
        
        # Separador
        separator = QFrame()
        separator.setFrameShape(QFrame.Shape.HLine)
        separator.setFrameShadow(QFrame.Shadow.Sunken)
        separator.setStyleSheet("background-color: rgba(255, 255, 255, 0.1);")
        main_layout.addWidget(separator)
        
        # Progreso
        progress_layout = QVBoxLayout()
        progress_header = QHBoxLayout()
        
        progress_label = QLabel("Progreso:")
        progress_label.setObjectName("progressLabel")
        progress_header.addWidget(progress_label)
        
        self.progress_value = QLabel("0%")
        self.progress_value.setObjectName("progressValue")
        self.progress_value.setAlignment(Qt.AlignmentFlag.AlignRight)
        progress_header.addWidget(self.progress_value)
        
        progress_layout.addLayout(progress_header)
        
        self.progress_bar = QProgressBar()
        self.progress_bar.setRange(0, 100)
        self.progress_bar.setValue(0)
        self.progress_bar.setTextVisible(False)
        progress_layout.addWidget(self.progress_bar)
        
        main_layout.addLayout(progress_layout)
        
        # Información de costo
        cost_layout = QHBoxLayout()
        
        cost_info_layout = QVBoxLayout()
        cost_label = QLabel("Costo:")
        cost_label.setObjectName("costLabel")
        self.cost_value = QLabel("$0.00")
        self.cost_value.setObjectName("costValue")
        
        cost_info_layout.addWidget(cost_label)
        cost_info_layout.addWidget(self.cost_value)
        cost_layout.addLayout(cost_info_layout)
        
        token_info_layout = QVBoxLayout()
        token_label = QLabel("Tokens:")
        token_label.setObjectName("tokenLabel")
        self.token_value = QLabel("0")
        self.token_value.setObjectName("tokenValue")
        
        token_info_layout.addWidget(token_label)
        token_info_layout.addWidget(self.token_value)
        cost_layout.addLayout(token_info_layout)
        
        main_layout.addLayout(cost_layout)
        
        # Estado actual
        status_layout = QHBoxLayout()
        status_label = QLabel("Estado:")
        status_label.setObjectName("statusLabel")
        self.status_value = QLabel("Esperando...")
        self.status_value.setObjectName("statusValue")
        
        status_layout.addWidget(status_label)
        status_layout.addWidget(self.status_value)
        status_layout.addStretch()
        
        main_layout.addLayout(status_layout)
        
        # Configurar estilos
        self.update_ui_state()
    
    def update_ui_state(self):
        """Actualizar el estado visual de los botones según el estado del agente."""
        if self.is_paused:
            self.pause_button.setText("▶")  # Icono de reproducción
            self.pause_button.setToolTip("Reanudar agente")
            self.status_value.setText("Pausado")
        else:
            self.pause_button.setText("⏸")  # Icono de pausa
            self.pause_button.setToolTip("Pausar agente")
            self.status_value.setText("Ejecutando...")
    
    @pyqtSlot()
    def toggle_pause(self):
        """Alternar entre pausar y reanudar el agente."""
        self.is_paused = not self.is_paused
        self.update_ui_state()
        
        if self.is_paused:
            self.pause_requested.emit(self.agent_id)
        else:
            self.resume_requested.emit(self.agent_id)
    
    @pyqtSlot()
    def request_modify(self):
        """Solicitar modificación del agente."""
        self.modify_requested.emit(self.agent_id)
    
    @pyqtSlot(float)
    def update_cost(self, cost):
        """Actualizar el costo del agente."""
        self.cost = cost
        self.cost_value.setText(f"${cost:.4f}")
    
    @pyqtSlot(int)
    def update_tokens(self, tokens):
        """Actualizar el conteo de tokens del agente."""
        self.tokens = tokens
        self.token_value.setText(f"{tokens}")
    
    @pyqtSlot(int)
    def update_progress(self, progress):
        """Actualizar el progreso del agente."""
        self.progress = progress
        self.progress_bar.setValue(progress)
        self.progress_value.setText(f"{progress}%")
    
    @pyqtSlot(str)
    def update_status(self, status):
        """Actualizar el estado del agente."""
        self.status_value.setText(status)


class CostMonitorWidget(QWidget):
    """Widget para monitorizar el costo total de todos los agentes."""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.total_cost = 0.0
        self.total_tokens = 0
        self.max_cost = None  # Límite de costo (opcional)
        
        # Configurar el widget
        self.setObjectName("costPanel")
        self.setup_ui()
    
    def setup_ui(self):
        """Configurar la interfaz de usuario del widget."""
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(15, 15, 15, 15)
        main_layout.setSpacing(10)
        
        # Título
        title_label = QLabel("Monitor de Costos")
        title_label.setObjectName("costTitle")
        main_layout.addWidget(title_label)
        
        # Costo total
        cost_layout = QHBoxLayout()
        
        cost_label = QLabel("Costo Total:")
        cost_label.setObjectName("costLabel")
        cost_layout.addWidget(cost_label)
        
        self.cost_value = QLabel("$0.00")
        self.cost_value.setObjectName("costTotal")
        self.cost_value.setAlignment(Qt.AlignmentFlag.AlignRight)
        cost_layout.addWidget(self.cost_value)
        
        main_layout.addLayout(cost_layout)
        
        # Tokens totales
        token_layout = QHBoxLayout()
        
        token_label = QLabel("Tokens Totales:")
        token_label.setObjectName("tokenLabel")
        token_layout.addWidget(token_label)
        
        self.token_value = QLabel("0")
        self.token_value.setObjectName("tokenCount")
        self.token_value.setAlignment(Qt.AlignmentFlag.AlignRight)
        token_layout.addWidget(self.token_value)
        
        main_layout.addLayout(token_layout)
        
        # Límite de costo (si está configurado)
        self.limit_layout = QHBoxLayout()
        
        self.limit_label = QLabel("Límite de Costo:")
        self.limit_label.setObjectName("limitLabel")
        self.limit_layout.addWidget(self.limit_label)
        
        self.limit_value = QLabel("No establecido")
        self.limit_value.setObjectName("limitValue")
        self.limit_value.setAlignment(Qt.AlignmentFlag.AlignRight)
        self.limit_layout.addWidget(self.limit_value)
        
        main_layout.addLayout(self.limit_layout)
        
        # Barra de progreso para el límite
        self.limit_progress = QProgressBar()
        self.limit_progress.setRange(0, 100)
        self.limit_progress.setValue(0)
        self.limit_progress.setTextVisible(False)
        self.limit_progress.setVisible(False)  # Oculto por defecto
        main_layout.addWidget(self.limit_progress)
        
        # Separador
        separator = QFrame()
        separator.setFrameShape(QFrame.Shape.HLine)
        separator.setFrameShadow(QFrame.Shadow.Sunken)
        separator.setStyleSheet("background-color: rgba(255, 255, 255, 0.1);")
        main_layout.addWidget(separator)
        
        # Botón para establecer límite
        self.set_limit_button = QPushButton("Establecer Límite")
        self.set_limit_button.clicked.connect(self.request_set_limit)
        main_layout.addWidget(self.set_limit_button)
        
        # Espacio flexible
        main_layout.addStretch()
    
    @pyqtSlot(float)
    def update_total_cost(self, cost):
        """Actualizar el costo total."""
        self.total_cost = cost
        self.cost_value.setText(f"${cost:.4f}")
        
        # Actualizar progreso si hay límite
        if self.max_cost:
            progress = min(int((cost / self.max_cost) * 100), 100)
            self.limit_progress.setValue(progress)
            
            # Cambiar color según el porcentaje
            if progress > 90:
                self.limit_progress.setStyleSheet("QProgressBar::chunk { background: #ff3b5b; }")
            elif progress > 75:
                self.limit_progress.setStyleSheet("QProgressBar::chunk { background: #ffbd3d; }")
    
    @pyqtSlot(int)
    def update_total_tokens(self, tokens):
        """Actualizar el conteo total de tokens."""
        self.total_tokens = tokens
        self.token_value.setText(f"{tokens:,}")
    
    @pyqtSlot(float)
    def set_cost_limit(self, limit):
        """Establecer un límite de costo."""
        self.max_cost = limit
        self.limit_value.setText(f"${limit:.2f}")
        self.limit_progress.setVisible(True)
        
        # Actualizar progreso
        if self.total_cost > 0:
            progress = min(int((self.total_cost / limit) * 100), 100)
            self.limit_progress.setValue(progress)
    
    @pyqtSlot()
    def request_set_limit(self):
        """Solicitar al usuario que establezca un límite de costo."""
        # Esta función debería mostrar un diálogo para ingresar el límite
        # Por ahora, simplemente establecemos un valor de ejemplo
        self.set_cost_limit(10.0)


class AgentMonitorPanel(QWidget):
    """Panel que contiene múltiples monitores de agentes y un monitor de costo total."""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.agent_monitors = {}  # Diccionario de monitores de agentes por ID
        
        # Configurar el widget
        self.setup_ui()
    
    def setup_ui(self):
        """Configurar la interfaz de usuario del panel."""
        main_layout = QHBoxLayout(self)
        main_layout.setContentsMargins(10, 10, 10, 10)
        main_layout.setSpacing(10)
        
        # Panel izquierdo: Monitores de agentes
        self.agents_layout = QVBoxLayout()
        self.agents_widget = QWidget()
        self.agents_widget.setLayout(self.agents_layout)
        
        # Hacer que el panel de agentes sea desplazable si hay muchos
        self.agents_scroll = QScrollArea()
        self.agents_scroll.setWidgetResizable(True)
        self.agents_scroll.setWidget(self.agents_widget)
        
        # Panel derecho: Monitor de costo
        self.cost_monitor = CostMonitorWidget()
        
        # Añadir widgets al layout principal
        main_layout.addWidget(self.agents_scroll, 7)  # 70% del espacio
        main_layout.addWidget(self.cost_monitor, 3)   # 30% del espacio
    
    def add_agent_monitor(self, agent_id, agent_name, agent_role):
        """Añadir un nuevo monitor de agente al panel."""
        if agent_id in self.agent_monitors:
            return  # Evitar duplicados
        
        monitor = AgentMonitorWidget(agent_id, agent_name, agent_role)
        self.agent_monitors[agent_id] = monitor
        self.agents_layout.addWidget(monitor)
        
        # Conectar señales
        monitor.pause_requested.connect(self.on_agent_pause_requested)
        monitor.resume_requested.connect(self.on_agent_resume_requested)
        monitor.modify_requested.connect(self.on_agent_modify_requested)
        
        return monitor
    
    def remove_agent_monitor(self, agent_id):
        """Eliminar un monitor de agente del panel."""
        if agent_id not in self.agent_monitors:
            return
        
        monitor = self.agent_monitors.pop(agent_id)
        self.agents_layout.removeWidget(monitor)
        monitor.deleteLater()
    
    def update_agent_cost(self, agent_id, cost):
        """Actualizar el costo de un agente específico."""
        if agent_id in self.agent_monitors:
            self.agent_monitors[agent_id].update_cost(cost)
            
            # Actualizar costo total
            total_cost = sum(monitor.cost for monitor in self.agent_monitors.values())
            self.cost_monitor.update_total_cost(total_cost)
    
    def update_agent_tokens(self, agent_id, tokens):
        """Actualizar los tokens de un agente específico."""
        if agent_id in self.agent_monitors:
            self.agent_monitors[agent_id].update_tokens(tokens)
            
            # Actualizar tokens totales
            total_tokens = sum(monitor.tokens for monitor in self.agent_monitors.values())
            self.cost_monitor.update_total_tokens(total_tokens)
    
    def update_agent_progress(self, agent_id, progress):
        """Actualizar el progreso de un agente específico."""
        if agent_id in self.agent_monitors:
            self.agent_monitors[agent_id].update_progress(progress)
    
    def update_agent_status(self, agent_id, status):
        """Actualizar el estado de un agente específico."""
        if agent_id in self.agent_monitors:
            self.agent_monitors[agent_id].update_status(status)
    
    @pyqtSlot(str)
    def on_agent_pause_requested(self, agent_id):
        """Manejar la solicitud de pausa de un agente."""
        print(f"Pausa solicitada para el agente {agent_id}")
        # Aquí se implementaría la lógica para pausar el agente
    
    @pyqtSlot(str)
    def on_agent_resume_requested(self, agent_id):
        """Manejar la solicitud de reanudación de un agente."""
        print(f"Reanudación solicitada para el agente {agent_id}")
        # Aquí se implementaría la lógica para reanudar el agente
    
    @pyqtSlot(str)
    def on_agent_modify_requested(self, agent_id):
        """Manejar la solicitud de modificación de un agente."""
        print(f"Modificación solicitada para el agente {agent_id}")
        # Aquí se implementaría la lógica para mostrar un diálogo de modificación


# Ejemplo de uso
if __name__ == "__main__":
    import sys
    from PyQt6.QtWidgets import QApplication
    
    app = QApplication(sys.argv)
    
    # Aplicar tema oscuro
    app.setStyle("Fusion")
    
    # Crear panel de monitorización
    panel = AgentMonitorPanel()
    
    # Añadir algunos agentes de ejemplo
    panel.add_agent_monitor("agent1", "Investigador de Mercado", "Analista de Datos")
    panel.add_agent_monitor("agent2", "Redactor de Contenido", "Escritor Creativo")
    panel.add_agent_monitor("agent3", "Estratega de Marketing", "Planificador")
    
    # Simular actualizaciones
    panel.update_agent_cost("agent1", 0.25)
    panel.update_agent_tokens("agent1", 1250)
    panel.update_agent_progress("agent1", 45)
    
    panel.update_agent_cost("agent2", 0.15)
    panel.update_agent_tokens("agent2", 750)
    panel.update_agent_progress("agent2", 30)
    
    panel.update_agent_cost("agent3", 0.05)
    panel.update_agent_tokens("agent3", 250)
    panel.update_agent_progress("agent3", 10)
    
    # Mostrar panel
    panel.setWindowTitle("Monitorización de Agentes")
    panel.resize(800, 600)
    panel.show()
    
    sys.exit(app.exec())
