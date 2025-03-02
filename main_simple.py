#!/usr/bin/env python3
"""
Kairos Intelligence System - Versión Simplificada
Esta versión no requiere CrewAI y funciona con Python 3.9+
"""

import sys
import os
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QTabWidget, QMenuBar, 
    QMenu, QStatusBar, QStyle, QStackedWidget, QMessageBox,
    QLabel, QVBoxLayout, QWidget
)
from PyQt6.QtGui import QAction, QIcon
from PyQt6.QtCore import QSize
from ui.theme import Theme
from ui.workflow_panel_simple import WorkflowPanelSimple

class MainWindowSimple(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Kairos Intelligence System (Modo Básico)")
        self.setMinimumSize(1200, 700)
        
        # Initialize theme - default to dark mode
        self.dark_mode = True
        self.apply_theme()
        
        # Create menu bar
        self.create_menu_bar()
        
        # Create status bar
        self.statusBar = QStatusBar()
        self.setStatusBar(self.statusBar)
        
        # Create central widget with tabs
        self.tabs = QTabWidget()
        self.setCentralWidget(self.tabs)
        
        # Add tabs
        self.setup_tabs()
        
        # Show welcome message
        self.statusBar.showMessage("Bienvenido a Kairos Intelligence System (Modo Básico)", 5000)
        
        # Show compatibility warning
        QMessageBox.warning(
            self, 
            "Modo Básico Activado", 
            "Estás ejecutando Kairos en modo básico debido a la versión de Python.\n\n"
            "CrewAI requiere Python 3.10 o superior, pero estás usando una versión anterior.\n\n"
            "En este modo, puedes ver la interfaz pero no ejecutar equipos de agentes.\n\n"
            "Para acceder a todas las funcionalidades, actualiza Python a la versión 3.10 o superior."
        )
    
    def setup_tabs(self):
        """Set up the tabs in the main window"""
        
        # Tab 1: Agentes
        agent_tab = QWidget()
        agent_layout = QVBoxLayout(agent_tab)
        agent_label = QLabel("Panel de Agentes (Modo Básico)")
        agent_label.setStyleSheet("font-size: 18px; font-weight: bold;")
        agent_layout.addWidget(agent_label)
        agent_layout.addWidget(QLabel("Esta es una versión simplificada que no requiere CrewAI."))
        self.tabs.addTab(agent_tab, "Agentes")
        
        # Tab 2: Tareas
        task_tab = QWidget()
        task_layout = QVBoxLayout(task_tab)
        task_label = QLabel("Panel de Tareas (Modo Básico)")
        task_label.setStyleSheet("font-size: 18px; font-weight: bold;")
        task_layout.addWidget(task_label)
        task_layout.addWidget(QLabel("Esta es una versión simplificada que no requiere CrewAI."))
        self.tabs.addTab(task_tab, "Tareas")
        
        # Tab 3: Equipos
        crew_tab = QWidget()
        crew_layout = QVBoxLayout(crew_tab)
        crew_label = QLabel("Panel de Equipos (Modo Básico)")
        crew_label.setStyleSheet("font-size: 18px; font-weight: bold;")
        crew_layout.addWidget(crew_label)
        crew_layout.addWidget(QLabel("Esta es una versión simplificada que no requiere CrewAI."))
        self.tabs.addTab(crew_tab, "Equipos")
        
        # Tab 4: Flujo de Trabajo
        workflow_tab = WorkflowPanelSimple()
        self.tabs.addTab(workflow_tab, "Flujo de Trabajo")
        
        # Tab 5: Configuración
        config_tab = QWidget()
        config_layout = QVBoxLayout(config_tab)
        config_label = QLabel("Panel de Configuración (Modo Básico)")
        config_label.setStyleSheet("font-size: 18px; font-weight: bold;")
        config_layout.addWidget(config_label)
        config_layout.addWidget(QLabel("Esta es una versión simplificada que no requiere CrewAI."))
        self.tabs.addTab(config_tab, "Configuración")
    
    def get_icon(self, name):
        # Use system icons when available
        if name == "theme":
            return self.style().standardIcon(QStyle.StandardPixmap.SP_DialogResetButton)
        return QIcon()
    
    def create_menu_bar(self):
        menubar = self.menuBar()
        
        # File menu
        file_menu = QMenu("Archivo", self)
        exit_action = QAction("Salir", self)
        exit_action.triggered.connect(self.close)
        file_menu.addAction(exit_action)
        
        # View menu
        view_menu = QMenu("Ver", self)
        theme_action = QAction(self.get_icon("theme"), "Cambiar Tema", self)
        theme_action.triggered.connect(self.toggle_theme)
        view_menu.addAction(theme_action)
        
        # Help menu
        help_menu = QMenu("Ayuda", self)
        about_action = QAction("Acerca de", self)
        about_action.triggered.connect(self.show_about)
        help_menu.addAction(about_action)
        
        menubar.addMenu(file_menu)
        menubar.addMenu(view_menu)
        menubar.addMenu(help_menu)
    
    def apply_theme(self):
        app = QApplication.instance()
        app.setPalette(Theme.get_palette(self.dark_mode))
        app.setStyleSheet(Theme.get_stylesheet(self.dark_mode))
    
    def toggle_theme(self):
        self.dark_mode = not self.dark_mode
        self.apply_theme()
        theme_name = "Oscuro" if self.dark_mode else "Claro"
        self.statusBar.showMessage(f"Cambiado a tema {theme_name}", 3000)
    
    def show_about(self):
        QMessageBox.about(
            self, 
            "Acerca de Kairos", 
            "<h3>Kairos Intelligence System</h3>"
            "<p>Versión: 1.0 (Modo Básico)</p>"
            "<p>Kairos es una plataforma para la creación y gestión de equipos de agentes de IA.</p>"
            "<p><b>Nota:</b> Estás ejecutando la versión básica debido a la compatibilidad de Python.</p>"
            "<p>Para acceder a todas las funcionalidades, actualiza a Python 3.10 o superior.</p>"
        )

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindowSimple()
    window.show()
    sys.exit(app.exec())
