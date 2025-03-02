from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
    QPushButton, QFrame, QScrollArea, QSizePolicy,
    QGridLayout, QGroupBox, QSpacerItem, QStackedWidget,
    QSplitter, QDialog, QLineEdit, QFormLayout, QDialogButtonBox, QMessageBox
)
from PyQt6.QtCore import Qt, QSize, pyqtSignal, pyqtSlot
from PyQt6.QtGui import QIcon, QPixmap, QColor, QPainter, QPen, QBrush
from ui.template_panel import TemplatePanel
from ui.agent_monitor import AgentMonitorPanel
from langchain_integration.agent_monitor_adapter import get_monitor_manager

class StepIndicator(QWidget):
    """Widget que muestra un paso en el flujo de trabajo con número y etiqueta"""
    
    clicked = pyqtSignal(int)  # Señal emitida cuando se hace clic en el paso
    
    def __init__(self, step_number, step_name, is_active=False, is_completed=False, parent=None):
        super().__init__(parent)
        self.step_number = step_number
        self.step_name = step_name
        self.is_active = is_active
        self.is_completed = is_completed
        self.setObjectName("stepIndicator")
        self.init_ui()
        
    def init_ui(self):
        layout = QVBoxLayout(self)
        
        # Número de paso con círculo
        self.number_label = QLabel(str(self.step_number))
        self.number_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.number_label.setFixedSize(36, 36)
        self.number_label.setStyleSheet(f"""
            background-color: {"#4dabf7" if self.is_active else "#3c3f41"};
            color: white;
            border-radius: 18px;
            font-weight: bold;
            font-size: 16px;
        """)
        
        # Nombre del paso
        self.name_label = QLabel(self.step_name)
        self.name_label.setObjectName("stepLabelActive" if self.is_active else "stepLabel")
        self.name_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        layout.addWidget(self.number_label, 0, Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.name_label, 0, Qt.AlignmentFlag.AlignCenter)
        
        # Hacer widget clickeable
        self.setCursor(Qt.CursorShape.PointingHandCursor)
        
    def mousePressEvent(self, event):
        self.clicked.emit(self.step_number)
        super().mousePressEvent(event)
        
    def set_active(self, active):
        self.is_active = active
        self.number_label.setStyleSheet(f"""
            background-color: {"#4dabf7" if active else "#3c3f41"};
            color: white;
            border-radius: 18px;
            font-weight: bold;
            font-size: 16px;
        """)
        self.name_label.setObjectName("stepLabelActive" if active else "stepLabel")
        # Forzar actualización de estilo
        self.name_label.setStyleSheet("")
        self.name_label.style().unpolish(self.name_label)
        self.name_label.style().polish(self.name_label)
        
    def set_completed(self, completed):
        self.is_completed = completed
        # Actualizar estilo para estado completado
        if completed:
            self.number_label.setStyleSheet("""
                background-color: #5aaa4f;
                color: white;
                border-radius: 18px;
                font-weight: bold;
                font-size: 16px;
            """)


class ConfigurationPanel(QWidget):
    """Panel para configurar agentes y equipos"""
    
    template_selected = pyqtSignal(object)  # Señal emitida cuando se selecciona una plantilla
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.init_ui()
        
    def init_ui(self):
        layout = QVBoxLayout(self)
        
        # Título
        title = QLabel("CONFIGURACIÓN")
        title.setStyleSheet("font-weight: bold; font-size: 18px;")
        
        # Splitter para dividir el panel en dos secciones
        splitter = QSplitter(Qt.Orientation.Horizontal)
        
        # Panel izquierdo - Plantillas
        self.template_panel = TemplatePanel()
        self.template_panel.template_applied.connect(self.on_template_selected)
        
        # Panel derecho - Configuración de equipo
        team_config = QWidget()
        team_config_layout = QVBoxLayout(team_config)
        
        # Título de configuración
        team_title = QLabel("CONFIGURACIÓN DE EQUIPO")
        team_title.setStyleSheet("font-weight: bold; font-size: 16px;")
        
        # Área de configuración
        config_area = QGroupBox("Parámetros")
        config_layout = QVBoxLayout(config_area)
        
        # Placeholder para parámetros (se llenará dinámicamente según la plantilla)
        self.params_widget = QWidget()
        self.params_layout = QVBoxLayout(self.params_widget)
        self.params_layout.addWidget(QLabel("Selecciona una plantilla para configurar los parámetros"))
        
        # Botones de acción
        buttons_layout = QHBoxLayout()
        save_button = QPushButton("Guardar Configuración")
        next_button = QPushButton("Continuar a Ejecución")
        next_button.setObjectName("primaryButton")
        
        buttons_layout.addWidget(save_button)
        buttons_layout.addWidget(next_button)
        
        # Añadir todo al layout de configuración
        config_layout.addWidget(self.params_widget)
        
        # Añadir componentes al layout del panel derecho
        team_config_layout.addWidget(team_title)
        team_config_layout.addWidget(config_area)
        team_config_layout.addLayout(buttons_layout)
        
        # Añadir paneles al splitter
        splitter.addWidget(self.template_panel)
        splitter.addWidget(team_config)
        splitter.setStretchFactor(0, 1)
        splitter.setStretchFactor(1, 2)
        
        # Añadir componentes al layout principal
        layout.addWidget(title)
        layout.addWidget(splitter)
        
    def on_template_selected(self, template):
        """Manejar la selección de una plantilla"""
        self.template_selected.emit(template)
        
        # Actualizar panel de parámetros
        self.update_params_panel(template)
        
    def update_params_panel(self, template):
        """Actualizar el panel de parámetros según la plantilla seleccionada"""
        # Limpiar panel actual
        while self.params_layout.count():
            item = self.params_layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()
        
        # Añadir parámetros según la plantilla
        self.params_layout.addWidget(QLabel(f"<b>Plantilla:</b> {template.name}"))
        self.params_layout.addWidget(QLabel(f"<b>Descripción:</b> {template.description}"))
        
        # Aquí se añadirían campos de entrada para los parámetros específicos
        # Por ahora, solo mostramos un mensaje
        self.params_layout.addWidget(QLabel("Parámetros de configuración:"))
        
        # Ejemplo de parámetros (en una implementación real, estos vendrían de la plantilla)
        self.params_layout.addWidget(QLabel("• Mercado objetivo: [Campo de texto]"))
        self.params_layout.addWidget(QLabel("• Competidores principales: [Lista]"))
        self.params_layout.addWidget(QLabel("• Profundidad de análisis: [Selector]"))
        
        # Añadir espacio al final
        self.params_layout.addStretch(1)


class ExecutionPanel(QWidget):
    """Panel para ejecutar y monitorizar agentes"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.init_ui()
        
    def init_ui(self):
        layout = QVBoxLayout(self)
        
        # Título
        title = QLabel("EJECUCIÓN")
        title.setStyleSheet("font-weight: bold; font-size: 18px;")
        
        # Splitter para dividir el panel en dos secciones
        splitter = QSplitter(Qt.Orientation.Vertical)
        
        # Panel superior - Controles de ejecución
        execution_controls = QWidget()
        controls_layout = QVBoxLayout(execution_controls)
        
        # Configuración de ejecución
        settings_group = QGroupBox("Configuración de Ejecución")
        settings_layout = QHBoxLayout(settings_group)
        
        # Configuración de API Key
        api_key_layout = QVBoxLayout()
        api_key_layout.addWidget(QLabel("API Key:"))
        api_key_status = QLabel("✓ Configurada")
        api_key_status.setStyleSheet("color: #4dabf7;")
        api_key_button = QPushButton("Cambiar API Key")
        api_key_layout.addWidget(api_key_status)
        api_key_layout.addWidget(api_key_button)
        
        # Configuración de límite de costo
        cost_limit_layout = QVBoxLayout()
        cost_limit_layout.addWidget(QLabel("Límite de Costo:"))
        self.cost_limit_status = QLabel("No establecido")
        self.cost_limit_button = QPushButton("Establecer Límite")
        self.cost_limit_button.clicked.connect(self.set_cost_limit)
        cost_limit_layout.addWidget(self.cost_limit_status)
        cost_limit_layout.addWidget(self.cost_limit_button)
        
        # Configuración de modelo
        model_layout = QVBoxLayout()
        model_layout.addWidget(QLabel("Modelo:"))
        model_label = QLabel("GPT-3.5 Turbo")
        model_button = QPushButton("Cambiar Modelo")
        model_layout.addWidget(model_label)
        model_layout.addWidget(model_button)
        
        # Añadir todas las configuraciones al grupo
        settings_layout.addLayout(api_key_layout)
        settings_layout.addLayout(cost_limit_layout)
        settings_layout.addLayout(model_layout)
        
        # Botones de ejecución
        buttons_layout = QHBoxLayout()
        self.start_button = QPushButton("Iniciar Ejecución")
        self.start_button.setObjectName("primaryButton")
        self.start_button.clicked.connect(self.start_execution)
        self.pause_button = QPushButton("Pausar Todos")
        self.pause_button.setEnabled(False)
        self.pause_button.clicked.connect(self.pause_all_agents)
        self.stop_button = QPushButton("Detener Ejecución")
        self.stop_button.setEnabled(False)
        self.stop_button.clicked.connect(self.stop_execution)
        
        buttons_layout.addWidget(self.start_button)
        buttons_layout.addWidget(self.pause_button)
        buttons_layout.addWidget(self.stop_button)
        
        # Añadir todos los controles al panel superior
        controls_layout.addWidget(settings_group)
        controls_layout.addLayout(buttons_layout)
        
        # Panel inferior - Monitorización de agentes
        self.agent_monitor_panel = AgentMonitorPanel()
        
        # Configurar el gestor de monitorización
        self.monitor_manager = get_monitor_manager()
        self.monitor_manager.set_ui_panel(self.agent_monitor_panel)
        
        # Añadir paneles al splitter
        splitter.addWidget(execution_controls)
        splitter.addWidget(self.agent_monitor_panel)
        splitter.setStretchFactor(0, 1)
        splitter.setStretchFactor(1, 3)
        
        # Añadir componentes al layout principal
        layout.addWidget(title)
        layout.addWidget(splitter)
        
    @pyqtSlot()
    def set_cost_limit(self):
        """Establecer un límite de costo para la ejecución."""
        # Crear un diálogo para ingresar el límite
        dialog = QDialog(self)
        dialog.setWindowTitle("Establecer Límite de Costo")
        dialog.setMinimumWidth(300)
        
        # Crear layout
        layout = QFormLayout(dialog)
        
        # Crear campo de entrada
        cost_input = QLineEdit()
        cost_input.setPlaceholderText("Ejemplo: 2.0")
        layout.addRow("Límite de costo ($):", cost_input)
        
        # Crear botones
        button_box = QDialogButtonBox(
            QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel
        )
        button_box.accepted.connect(dialog.accept)
        button_box.rejected.connect(dialog.reject)
        layout.addRow(button_box)
        
        # Mostrar diálogo
        if dialog.exec() == QDialog.DialogCode.Accepted:
            try:
                cost_limit = float(cost_input.text())
                if cost_limit <= 0:
                    raise ValueError("El límite debe ser mayor que cero")
                
                # Establecer límite
                self.monitor_manager.set_cost_limit(cost_limit)
                
                # Actualizar estado
                self.cost_limit_status.setText(f"${cost_limit:.2f}")
                self.cost_limit_status.setStyleSheet("color: #4dabf7;")
                
                # Mostrar mensaje de confirmación
                QMessageBox.information(
                    self,
                    "Límite Establecido",
                    f"Se ha establecido un límite de costo de ${cost_limit:.2f}."
                )
            except ValueError as e:
                # Mostrar mensaje de error
                QMessageBox.warning(
                    self,
                    "Error",
                    f"Por favor, ingrese un número válido mayor que cero. Error: {str(e)}"
                )
    
    @pyqtSlot()
    def start_execution(self):
        """Iniciar la ejecución de los agentes."""
        # En una implementación real, aquí se crearían y ejecutarían los agentes
        # Para esta demostración, solo simularemos la actividad
        
        # Cambiar estado de los botones
        self.start_button.setEnabled(False)
        self.pause_button.setEnabled(True)
        self.stop_button.setEnabled(True)
        
        # Simular agentes para la demostración
        self.simulate_agents()
        
        # Mostrar mensaje
        QMessageBox.information(
            self,
            "Ejecución Iniciada",
            "La ejecución de los agentes ha comenzado. Puedes monitorizar su progreso en el panel inferior."
        )
    
    def simulate_agents(self):
        """Simular agentes para la demostración."""
        # Añadir algunos agentes de ejemplo al panel de monitorización
        self.agent_monitor_panel.add_agent_monitor(
            "researcher", "Investigador de Mercado", "Analista de Datos"
        )
        self.agent_monitor_panel.add_agent_monitor(
            "writer", "Redactor de Contenido", "Escritor Creativo"
        )
        self.agent_monitor_panel.add_agent_monitor(
            "analyst", "Estratega de Marketing", "Planificador"
        )
        
        # Simular algunas métricas iniciales
        self.agent_monitor_panel.update_agent_cost("researcher", 0.05)
        self.agent_monitor_panel.update_agent_tokens("researcher", 250)
        self.agent_monitor_panel.update_agent_progress("researcher", 10)
        self.agent_monitor_panel.update_agent_status("researcher", "Iniciando investigación...")
        
        self.agent_monitor_panel.update_agent_cost("writer", 0.03)
        self.agent_monitor_panel.update_agent_tokens("writer", 150)
        self.agent_monitor_panel.update_agent_progress("writer", 5)
        self.agent_monitor_panel.update_agent_status("writer", "Preparando estructura...")
        
        self.agent_monitor_panel.update_agent_cost("analyst", 0.02)
        self.agent_monitor_panel.update_agent_tokens("analyst", 100)
        self.agent_monitor_panel.update_agent_progress("analyst", 3)
        self.agent_monitor_panel.update_agent_status("analyst", "Analizando datos iniciales...")
    
    @pyqtSlot()
    def pause_all_agents(self):
        """Pausar todos los agentes en ejecución."""
        # En una implementación real, aquí se pausarían los agentes
        # Para esta demostración, solo actualizaremos el estado
        
        # Actualizar estado de los agentes
        for agent_id in self.agent_monitor_panel.agent_monitors:
            self.agent_monitor_panel.update_agent_status(agent_id, "Pausado")
        
        # Cambiar texto del botón
        if self.pause_button.text() == "Pausar Todos":
            self.pause_button.setText("Reanudar Todos")
        else:
            self.pause_button.setText("Pausar Todos")
            # Actualizar estado de los agentes al reanudar
            self.agent_monitor_panel.update_agent_status("researcher", "Continuando investigación...")
            self.agent_monitor_panel.update_agent_status("writer", "Redactando contenido...")
            self.agent_monitor_panel.update_agent_status("analyst", "Analizando tendencias...")
    
    @pyqtSlot()
    def stop_execution(self):
        """Detener la ejecución de los agentes."""
        # En una implementación real, aquí se detendrían los agentes
        # Para esta demostración, solo actualizaremos el estado
        
        # Actualizar estado de los agentes
        for agent_id in self.agent_monitor_panel.agent_monitors:
            self.agent_monitor_panel.update_agent_status(agent_id, "Detenido")
            self.agent_monitor_panel.update_agent_progress(agent_id, 100)
        
        # Cambiar estado de los botones
        self.start_button.setEnabled(True)
        self.pause_button.setEnabled(False)
        self.stop_button.setEnabled(False)
        self.pause_button.setText("Pausar Todos")
        
        # Mostrar mensaje
        QMessageBox.information(
            self,
            "Ejecución Detenida",
            "La ejecución de los agentes ha sido detenida."
        )


class ResultsPanel(QWidget):
    """Panel para visualizar y exportar resultados"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.init_ui()
        
    def init_ui(self):
        layout = QVBoxLayout(self)
        
        # Título
        title = QLabel("RESULTADOS")
        title.setStyleSheet("font-weight: bold; font-size: 18px;")
        
        # Splitter para dividir el panel en dos secciones
        splitter = QSplitter(Qt.Orientation.Horizontal)
        
        # Panel izquierdo - Lista de resultados
        results_list = QWidget()
        results_list_layout = QVBoxLayout(results_list)
        
        # Título de lista
        list_title = QLabel("DOCUMENTOS GENERADOS")
        list_title.setStyleSheet("font-weight: bold; font-size: 16px;")
        
        # Lista de resultados (simulada)
        results_group = QGroupBox("Archivos")
        results_group_layout = QVBoxLayout(results_group)
        
        # Simular algunos resultados
        results = [
            ("competitor_analysis.md", "Análisis de Competidores"),
            ("market_trends.md", "Análisis de Tendencias"),
            ("opportunities.md", "Oportunidades Identificadas"),
            ("strategic_plan.md", "Plan Estratégico")
        ]
        
        for filename, description in results:
            item = QPushButton(f"{description} ({filename})")
            item.setStyleSheet("text-align: left; padding: 10px;")
            results_group_layout.addWidget(item)
        
        # Añadir componentes al layout de lista
        results_list_layout.addWidget(list_title)
        results_list_layout.addWidget(results_group)
        
        # Panel derecho - Visualización de resultado
        result_view = QWidget()
        result_view_layout = QVBoxLayout(result_view)
        
        # Título de visualización
        view_title = QLabel("VISTA PREVIA")
        view_title.setStyleSheet("font-weight: bold; font-size: 16px;")
        
        # Área de visualización
        preview_area = QGroupBox("Contenido")
        preview_layout = QVBoxLayout(preview_area)
        
        # Contenido de ejemplo
        preview_content = QLabel("""
        <h2>Análisis de Competidores</h2>
        
        <h3>Competidores Principales</h3>
        <ul>
            <li><b>Competidor A</b>: Líder en el mercado con 45% de cuota</li>
            <li><b>Competidor B</b>: Enfoque en segmento premium</li>
            <li><b>Competidor C</b>: Estrategia agresiva de precios</li>
        </ul>
        
        <h3>Fortalezas y Debilidades</h3>
        <p>El análisis DAFO revela oportunidades significativas en el segmento de...</p>
        
        <h3>Estrategias de Marketing</h3>
        <p>Los competidores están invirtiendo principalmente en canales digitales, con énfasis en...</p>
        """)
        preview_content.setWordWrap(True)
        preview_layout.addWidget(preview_content)
        
        # Botones de acción
        buttons_layout = QHBoxLayout()
        export_button = QPushButton("Exportar Todos")
        export_button.setObjectName("primaryButton")
        view_button = QPushButton("Abrir en Editor")
        share_button = QPushButton("Compartir")
        
        buttons_layout.addWidget(export_button)
        buttons_layout.addWidget(view_button)
        buttons_layout.addWidget(share_button)
        
        # Añadir componentes al layout de visualización
        result_view_layout.addWidget(view_title)
        result_view_layout.addWidget(preview_area)
        result_view_layout.addLayout(buttons_layout)
        
        # Añadir paneles al splitter
        splitter.addWidget(results_list)
        splitter.addWidget(result_view)
        splitter.setStretchFactor(0, 1)
        splitter.setStretchFactor(1, 2)
        
        # Añadir componentes al layout principal
        layout.addWidget(title)
        layout.addWidget(splitter)


class WorkflowPanelSimplified(QWidget):
    """Panel principal que implementa la interfaz de flujo de trabajo horizontal simplificada"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.current_step = 1
        self.init_ui()
        
    def init_ui(self):
        main_layout = QVBoxLayout(self)
        
        # Indicador de pasos
        steps_widget = QWidget()
        steps_layout = QHBoxLayout(steps_widget)
        
        self.step_indicators = []
        steps = [
            (1, "CONFIGURAR"),
            (2, "EJECUTAR"),
            (3, "RESULTADOS")
        ]
        
        for step_num, step_name in steps:
            indicator = StepIndicator(step_num, step_name, is_active=(step_num == self.current_step))
            indicator.clicked.connect(self.set_current_step)
            steps_layout.addWidget(indicator)
            self.step_indicators.append(indicator)
        
        # Área de contenido - usando stacked widget para diferentes pasos
        self.content_stack = QStackedWidget()
        
        # Paso 1: Configuración
        self.configuration_panel = ConfigurationPanel()
        
        # Paso 2: Ejecución
        self.execution_panel = ExecutionPanel()
        
        # Paso 3: Resultados
        self.results_panel = ResultsPanel()
        
        # Añadir todos los pasos al stack
        self.content_stack.addWidget(self.configuration_panel)  # Índice 0 - Paso 1
        self.content_stack.addWidget(self.execution_panel)      # Índice 1 - Paso 2
        self.content_stack.addWidget(self.results_panel)        # Índice 2 - Paso 3
        
        # Establecer paso actual
        self.content_stack.setCurrentIndex(0)
        
        # Añadir todos los componentes al layout principal
        main_layout.addWidget(steps_widget)
        main_layout.addWidget(self.content_stack, 1)
        
        # Conectar señales
        self.configuration_panel.template_selected.connect(self.on_template_selected)
        
    def set_current_step(self, step_num):
        """Cambiar el paso activo actual"""
        if 1 <= step_num <= len(self.step_indicators):
            # Actualizar indicadores de paso
            for i, indicator in enumerate(self.step_indicators):
                indicator.set_active(i + 1 == step_num)
                
                # Marcar pasos anteriores como completados
                if i + 1 < step_num:
                    indicator.set_completed(True)
                
            self.current_step = step_num
            
            # Actualizar stack de contenido
            self.content_stack.setCurrentIndex(step_num - 1)
    
    def on_template_selected(self, template):
        """Manejar la selección de una plantilla"""
        # Aquí se podría implementar lógica adicional
        # Por ejemplo, cargar configuraciones específicas de la plantilla
        pass
