import sys
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QTabWidget, QMenuBar, 
    QMenu, QStatusBar, QStyle
)
from PyQt6.QtGui import QAction, QIcon
from PyQt6.QtCore import QSize
from ui.task_panel import TaskPanel
from ui.agent_panel import AgentPanel
from ui.crew_panel import CrewPanel
from ui.theme import Theme

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("CrewAI GUI")
        self.setMinimumSize(900, 600)
        
        # Initialize theme
        self.dark_mode = False
        self.apply_theme()
        
        # Create menu bar
        self.create_menu_bar()
        
        # Create status bar
        self.statusBar = QStatusBar()
        self.setStatusBar(self.statusBar)
        
        # Create tab widget
        self.tabs = QTabWidget()
        self.setCentralWidget(self.tabs)
        
        # Create panels
        self.agent_panel = AgentPanel()
        self.task_panel = TaskPanel()
        self.crew_panel = CrewPanel()
        
        # Add tabs with icons
        self.tabs.addTab(self.agent_panel, self.get_icon("person"), "Agents")
        self.tabs.addTab(self.task_panel, self.get_icon("task"), "Tasks")
        self.tabs.addTab(self.crew_panel, self.get_icon("group"), "Crews")
        
        # Connect signals
        self.tabs.currentChanged.connect(self.tab_changed)
        
        # Show welcome message
        self.statusBar.showMessage("Welcome to CrewAI GUI", 5000)
    
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
        return QIcon()
    
    def create_menu_bar(self):
        menubar = self.menuBar()
        
        # File menu
        file_menu = QMenu("File", self)
        exit_action = QAction(self.get_icon("exit"), "Exit", self)
        exit_action.triggered.connect(self.close)
        file_menu.addAction(exit_action)
        
        # View menu
        view_menu = QMenu("View", self)
        theme_action = QAction(self.get_icon("theme"), "Toggle Dark Mode", self)
        theme_action.triggered.connect(self.toggle_theme)
        view_menu.addAction(theme_action)
        
        menubar.addMenu(file_menu)
        menubar.addMenu(view_menu)
    
    def apply_theme(self):
        app = QApplication.instance()
        app.setPalette(Theme.get_palette(self.dark_mode))
        app.setStyleSheet(Theme.get_stylesheet(self.dark_mode))
    
    def toggle_theme(self):
        self.dark_mode = not self.dark_mode
        self.apply_theme()
        theme_name = "Dark" if self.dark_mode else "Light"
        self.statusBar.showMessage(f"Switched to {theme_name} theme", 3000)
        
    def tab_changed(self, index):
        # When switching to Tasks tab, update available agents
        if index == 1:  # Tasks tab
            self.task_panel.update_agents(self.agent_panel.get_agents())
        # When switching to Crews tab, update available agents and tasks
        elif index == 2:  # Crews tab
            self.crew_panel.update_agents(self.agent_panel.get_agents())
            self.crew_panel.update_tasks(self.task_panel.tasks)
        
    def closeEvent(self, event):
        self.agent_panel.save_agents()
        self.task_panel.save_tasks()
        self.crew_panel.save_crews()
        event.accept()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())