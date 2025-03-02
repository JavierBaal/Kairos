import sys
import os
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QTabWidget, QMenuBar, 
    QMenu, QStatusBar, QStyle, QStackedWidget, QMessageBox
)
from PyQt6.QtGui import QAction, QIcon
from PyQt6.QtCore import QSize
from ui.task_panel import TaskPanel
from ui.agent_panel import AgentPanel
# from ui.crew_panel import CrewPanel  # Comentamos esta línea
from ui.langchain_team_panel import LangChainTeamPanel  # Importamos el nuevo panel
from ui.workflow_panel import WorkflowPanel
from ui.monitor_panel import MonitorPanel  # Nuevo panel de monitorización
from ui.theme import Theme
from models.template_model import TemplateModel
from models.state_manager import get_state_manager  # Gestor de estado centralizado
from langchain_integration.agent_monitor_adapter import get_monitor_manager  # Gestor de monitorización

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Kairos Intelligence System")
        self.setMinimumSize(1200, 700)  # Increased size for horizontal layout
        
        # Initialize state manager
        self.state_manager = get_state_manager()
        
        # Initialize monitor manager
        self.monitor_manager = get_monitor_manager()
        
# Initialize theme
        self.apply_theme()
        
        # Create menu bar
        self.create_menu_bar()
        
        # Create status bar
        self.statusBar = QStatusBar()
        self.setStatusBar(self.statusBar)
        
        # Create stacked widget for different interfaces
        self.stacked_widget = QStackedWidget()
        self.setCentralWidget(self.stacked_widget)
        
        # Create traditional tabbed interface (legacy)
        self.tabs = QTabWidget()
        
        # Create panels
        self.agent_panel = AgentPanel()
        self.task_panel = TaskPanel()
        # self.crew_panel = CrewPanel()  # Comentamos esta línea
        self.langchain_team_panel = LangChainTeamPanel(self.state_manager)  # Creamos el nuevo panel
        self.monitor_panel = MonitorPanel()
        
        # Add tabs with icons
        self.tabs.addTab(self.agent_panel, self.get_icon("person"), "Especialistas")
        self.tabs.addTab(self.task_panel, self.get_icon("task"), "Objetivos")
        self.tabs.addTab(self.langchain_team_panel, self.get_icon("group"), "Equipos")  # Usamos el nuevo panel
        self.tabs.addTab(self.monitor_panel, self.get_icon("monitor"), "Monitorización")
        
        # Connect signals for traditional interface
        self.tabs.currentChanged.connect(self.tab_changed)
        
        # Create new workflow interface
        self.workflow_panel = WorkflowPanel()
        
        # Add both interfaces to stacked widget
        self.stacked_widget.addWidget(self.workflow_panel)  # Index 0 - New interface
        self.stacked_widget.addWidget(self.tabs)            # Index 1 - Traditional interface
        
        # Default to new workflow interface
        self.stacked_widget.setCurrentIndex(0)
        
        # Connect monitor manager to UI
        self.monitor_manager.set_ui_panel(self.monitor_panel)
        
        # Register state observers
        self.register_state_observers()
        
        # Show welcome message
        self.statusBar.showMessage("Bienvenido a Kairos Intelligence System", 5000)

    def get_icon(self, name):
        # Use system icons when available
        if name == "person":
            return self.style().standardIcon(QStyle.StandardPixmap.SP_DialogApplyButton)
        elif name == "task":
            return self.style().standardIcon(QStyle.StandardPixmap.SP_FileDialogDetailedView)
        elif name == "group":
            return self.style().standardIcon(QStyle.StandardPixmap.SP_DialogHelpButton)
        elif name == "theme":
            return self.style().standardIcon(QStyle.StandardPixmap.SP_DialogResetButton)
        elif name == "interface":
            return self.style().standardIcon(QStyle.StandardPixmap.SP_ComputerIcon)
        elif name == "monitor":
            return self.style().standardIcon(QStyle.StandardPixmap.SP_ComputerIcon)
        return QIcon()
    
    def register_state_observers(self):
        """Registrar observadores para cambios de estado"""
        # Actualizar panel de agentes cuando cambian los agentes
        self.state_manager.register_observer("agents", self.agent_panel.update_from_state)
        
        # Actualizar panel de tareas cuando cambian las tareas o los agentes
        self.state_manager.register_observer("tasks", self.task_panel.update_from_state)
        self.state_manager.register_observer("agents", self.task_panel.update_agents_from_state)
        
        # Actualizar panel de equipos cuando cambian los equipos, tareas o agentes
        self.state_manager.register_observer("teams", self.langchain_team_panel.update_from_state)
        # Ya no necesitamos estas líneas:
        # self.state_manager.register_observer("crews", self.crew_panel.update_from_state)
        # self.state_manager.register_observer("tasks", self.crew_panel.update_tasks_from_state)
        # self.state_manager.register_observer("agents", self.crew_panel.update_agents_from_state)
        
        # Actualizar panel de monitorización cuando cambia el estado de monitorización
        self.state_manager.register_observer("monitoring", self.monitor_panel.update_from_state)

    def create_menu_bar(self):
        menubar = self.menuBar()
        
        # File menu
        file_menu = QMenu("Archivo", self)
        exit_action = QAction(self.get_icon("exit"), "Salir", self)
        exit_action.triggered.connect(self.close)
        file_menu.addAction(exit_action)
        
        # View menu
        view_menu = QMenu("Ver", self)
        theme_action = QAction(self.get_icon("theme"), "Cambiar Tema", self)
        theme_action.triggered.connect(self.toggle_theme)
        view_menu.addAction(theme_action)
        
        # Interface menu
        interface_menu = QMenu("Interfaz", self)
        modern_action = QAction("Moderna (Flujo de Trabajo)", self)
        modern_action.triggered.connect(lambda: self.stacked_widget.setCurrentIndex(0))
        traditional_action = QAction("Tradicional (Pestañas)", self)
        traditional_action.triggered.connect(lambda: self.stacked_widget.setCurrentIndex(1))
        interface_menu.addAction(modern_action)
        interface_menu.addAction(traditional_action)
        
        menubar.addMenu(file_menu)
        menubar.addMenu(view_menu)
        menubar.addMenu(interface_menu)
    
    def apply_theme(self):
        app = QApplication.instance()
        Theme.apply_to_app(app)
    
    def toggle_theme(self):
        # Ahora usamos un tema único tipo JetBrains
        self.apply_theme()
        self.statusBar.showMessage("Tema JetBrains aplicado", 3000)
        
    def tab_changed(self, index):
        # When switching to Tasks tab, update available agents
        if index == 1:  # Tasks tab
            self.task_panel.update_agents(self.agent_panel.get_agents())
        # Ya no necesitamos esta parte:
        # When switching to Crews tab, update available agents and tasks
        # elif index == 2:  # Crews tab
        #     self.crew_panel.update_agents(self.agent_panel.get_agents())
        #     self.crew_panel.update_tasks(self.task_panel.tasks)
    
    def sync_data(self):
        """Sync data between traditional interface and workflow interface"""
        # Update workflow panel with agents from agent panel
        self.workflow_panel.populate_specialist_library(self.agent_panel.get_agents())
        
        # Connect template application signal
        self.workflow_panel.template_panel.template_applied.connect(self.apply_template)
        
    def apply_template(self, template):
        """Apply a template to the traditional interface panels"""
        try:
            # Apply template to traditional panels
            success = template.apply_template(
                self.agent_panel,
                self.task_panel,
                self.langchain_team_panel  # Updated to use new panel
            )
            
            if success:
                QMessageBox.information(
                    self, 
                    "Plantilla Aplicada", 
                    f"La plantilla '{template.name}' ha sido aplicada correctamente."
                )
                
                # Ensure config directory exists
                os.makedirs("config", exist_ok=True)
                
                # Save changes to config files
                self.agent_panel.save_agents()
                self.task_panel.save_tasks()
                
                # Update workflow panel
                self.sync_data()
            else:
                QMessageBox.warning(
                    self, 
                    "Error", 
                    "No se pudo aplicar la plantilla. Verifica la configuración."
                )
        except Exception as e:
            QMessageBox.critical(
                self, 
                "Error", 
                f"Error al aplicar la plantilla: {str(e)}"
            )
    
    def closeEvent(self, event):
        self.agent_panel.save_agents()
        self.task_panel.save_tasks()
        # self.crew_panel.save_crews()  # Ya no necesitamos esto
        event.accept()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    
    # Sync data after showing window
    window.sync_data()
    
    sys.exit(app.exec())
