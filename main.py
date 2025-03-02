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
from ui.crew_panel import CrewPanel
from ui.workflow_panel import WorkflowPanel
from ui.theme import Theme
from models.template_model import TemplateModel

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Kairos Intelligence System")
        self.setMinimumSize(1200, 700)  # Increased size for horizontal layout
        
        # Initialize theme - default to dark mode
        self.dark_mode = True
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
        self.crew_panel = CrewPanel()
        
        # Add tabs with icons
        self.tabs.addTab(self.agent_panel, self.get_icon("person"), "Especialistas")
        self.tabs.addTab(self.task_panel, self.get_icon("task"), "Objetivos")
        self.tabs.addTab(self.crew_panel, self.get_icon("group"), "Equipos")
        
        # Connect signals for traditional interface
        self.tabs.currentChanged.connect(self.tab_changed)
        
        # Create new workflow interface
        self.workflow_panel = WorkflowPanel()
        
        # Add both interfaces to stacked widget
        self.stacked_widget.addWidget(self.workflow_panel)  # Index 0 - New interface
        self.stacked_widget.addWidget(self.tabs)            # Index 1 - Traditional interface
        
        # Default to new workflow interface
        self.stacked_widget.setCurrentIndex(0)
        
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
        return QIcon()
    
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
        app.setPalette(Theme.get_palette(self.dark_mode))
        app.setStyleSheet(Theme.get_stylesheet(self.dark_mode))
    
    def toggle_theme(self):
        self.dark_mode = not self.dark_mode
        self.apply_theme()
        theme_name = "Oscuro" if self.dark_mode else "Claro"
        self.statusBar.showMessage(f"Cambiado a tema {theme_name}", 3000)
        
    def tab_changed(self, index):
        # When switching to Tasks tab, update available agents
        if index == 1:  # Tasks tab
            self.task_panel.update_agents(self.agent_panel.get_agents())
        # When switching to Crews tab, update available agents and tasks
        elif index == 2:  # Crews tab
            self.crew_panel.update_agents(self.agent_panel.get_agents())
            self.crew_panel.update_tasks(self.task_panel.tasks)
    
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
                self.crew_panel
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
                self.crew_panel.save_crews()
                
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
        self.crew_panel.save_crews()
        event.accept()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    
    # Sync data after showing window
    window.sync_data()
    
    sys.exit(app.exec())
