from PyQt6.QtGui import QPalette, QColor
from PyQt6.QtCore import Qt

class Theme:
    # Color palette - JetBrains inspired
    COLORS = {
        "dark": {
            # Base colors
            "background": "#1e1f22",
            "background_secondary": "#2b2d30",
            "background_tertiary": "#3c3f41",
            "text": "#ffffff",
            "text_secondary": "#a9b7c6",
            
            # Accent colors
            "primary": "#4dabf7",
            "primary_dark": "#3d8bd7",
            "secondary": "#f07178",
            "tertiary": "#c3e88d",
            "error": "#ff5370",
            "warning": "#ffcb6b",
            "info": "#82aaff",
            
            # UI elements
            "border": "#5a5d5f",
            "surface": "#2b2d30",
            "hover": "#4e5254",
            "selected": "#4dabf7"
        },
        "light": {
            # Base colors
            "background": "#f7f8fa",
            "background_secondary": "#ffffff",
            "background_tertiary": "#e7e7e7",
            "text": "#2c2c2c",
            "text_secondary": "#6f737a",
            
            # Accent colors
            "primary": "#2b7cd1",
            "primary_dark": "#1e63a9",
            "secondary": "#e05a66",
            "tertiary": "#5aaa4f",
            "error": "#d32f2f",
            "warning": "#ed9c24",
            "info": "#3b7dd8",
            
            # UI elements
            "border": "#d1d1d1",
            "surface": "#ffffff",
            "hover": "#e9e9e9",
            "selected": "#2b7cd1"
        }
    }
    
    # Gradients
    GRADIENTS = {
        "dark": {
            "primary_button": "qlineargradient(x1:0, y1:0, x2:0, y2:1, stop:0 #4dabf7, stop:1 #3d8bd7)",
            "secondary_button": "qlineargradient(x1:0, y1:0, x2:0, y2:1, stop:0 #3c3f41, stop:1 #323537)",
            "main_panel": "qlineargradient(x1:0, y1:0, x2:0, y2:1, stop:0 #2b2d30, stop:1 #252729)",
            "app_background": "qlineargradient(x1:0, y1:0, x2:1, y2:1, stop:0 #1e1f22, stop:1 #191a1d)"
        },
        "light": {
            "primary_button": "qlineargradient(x1:0, y1:0, x2:0, y2:1, stop:0 #3b8be3, stop:1 #2b7cd1)",
            "secondary_button": "qlineargradient(x1:0, y1:0, x2:0, y2:1, stop:0 #f0f0f0, stop:1 #e7e7e7)",
            "main_panel": "qlineargradient(x1:0, y1:0, x2:0, y2:1, stop:0 #ffffff, stop:1 #f7f7f7)",
            "app_background": "qlineargradient(x1:0, y1:0, x2:1, y2:1, stop:0 #f7f8fa, stop:1 #f0f1f3)"
        }
    }
    
    @staticmethod
    def get_palette(dark_mode=True):
        palette = QPalette()
        theme = "dark" if dark_mode else "light"
        colors = Theme.COLORS[theme]
        
        # Set up palette colors
        palette.setColor(QPalette.ColorRole.Window, QColor(colors["background"]))
        palette.setColor(QPalette.ColorRole.WindowText, QColor(colors["text"]))
        palette.setColor(QPalette.ColorRole.Base, QColor(colors["background_secondary"]))
        palette.setColor(QPalette.ColorRole.AlternateBase, QColor(colors["background_tertiary"]))
        palette.setColor(QPalette.ColorRole.ToolTipBase, QColor(colors["background_secondary"]))
        palette.setColor(QPalette.ColorRole.ToolTipText, QColor(colors["text"]))
        palette.setColor(QPalette.ColorRole.Text, QColor(colors["text"]))
        palette.setColor(QPalette.ColorRole.Button, QColor(colors["background_secondary"]))
        palette.setColor(QPalette.ColorRole.ButtonText, QColor(colors["text"]))
        palette.setColor(QPalette.ColorRole.BrightText, QColor(colors["text"]))
        palette.setColor(QPalette.ColorRole.Link, QColor(colors["primary"]))
        palette.setColor(QPalette.ColorRole.Highlight, QColor(colors["primary"]))
        palette.setColor(QPalette.ColorRole.HighlightedText, QColor("#ffffff"))
        
        return palette

    @staticmethod
    def get_stylesheet(dark_mode=True):
        theme = "dark" if dark_mode else "light"
        colors = Theme.COLORS[theme]
        gradients = Theme.GRADIENTS[theme]
        
        return f"""
            /* General Application Style */
            QWidget {{
                font-family: 'JetBrains Mono', 'Segoe UI', 'Arial';
                font-size: 14px;
                color: {colors["text"]};
            }}
            
            QMainWindow {{
                background: {gradients["app_background"]};
            }}
            
            /* Buttons with gradients */
            QPushButton {{
                background: {gradients["secondary_button"]};
                color: {colors["text"]};
                border: none;
                border-radius: 4px;
                padding: 8px 16px;
                font-weight: 500;
            }}
            
            QPushButton:hover {{
                background-color: {colors["hover"]};
            }}
            
            QPushButton:pressed {{
                background-color: {colors["background_tertiary"]};
            }}
            
            QPushButton#primaryButton {{
                background: {gradients["primary_button"]};
                color: white;
                font-weight: bold;
            }}
            
            QPushButton#primaryButton:hover {{
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1, 
                                          stop:0 {QColor(colors["primary"]).lighter(115).name()}, 
                                          stop:1 {QColor(colors["primary_dark"]).lighter(115).name()});
            }}
            
            /* Panels with gradients */
            QGroupBox {{
                background: {gradients["main_panel"]};
                border: 1px solid {colors["border"]};
                border-radius: 6px;
                margin-top: 12px;
                padding-top: 16px;
                font-weight: bold;
            }}
            
            QGroupBox::title {{
                subcontrol-origin: margin;
                subcontrol-position: top left;
                padding: 0 6px;
                color: {colors["text"]};
            }}
            
            /* Tabs with modern styling */
            QTabWidget::pane {{
                border: 1px solid {colors["border"]};
                background-color: {colors["background_secondary"]};
                border-radius: 4px;
            }}
            
            QTabBar::tab {{
                background-color: {colors["background"]};
                color: {colors["text_secondary"]};
                padding: 10px 20px;
                margin-right: 2px;
                border-top-left-radius: 4px;
                border-top-right-radius: 4px;
                border: 1px solid {colors["border"]};
                border-bottom: none;
            }}
            
            QTabBar::tab:selected {{
                background-color: {colors["primary"]};
                color: white;
                font-weight: bold;
            }}
            
            QTabBar::tab:hover:!selected {{
                background-color: {colors["hover"]};
                color: {colors["text"]};
            }}
            
            /* Form elements with consistent styling */
            QLineEdit, QTextEdit, QPlainTextEdit {{
                background-color: {colors["background_tertiary"]};
                color: {colors["text"]};
                border: 1px solid {colors["border"]};
                border-radius: 4px;
                padding: 8px;
                selection-background-color: {colors["primary"]};
            }}
            
            QLineEdit:focus, QTextEdit:focus, QPlainTextEdit:focus {{
                border: 1px solid {colors["primary"]};
            }}
            
            /* Dropdown styling */
            QComboBox {{
                background-color: {colors["background_tertiary"]};
                color: {colors["text"]};
                border: 1px solid {colors["border"]};
                border-radius: 4px;
                padding: 8px;
                min-width: 6em;
            }}
            
            QComboBox:focus {{
                border: 1px solid {colors["primary"]};
            }}
            
            QComboBox::drop-down {{
                subcontrol-origin: padding;
                subcontrol-position: top right;
                width: 20px;
                border-left: 1px solid {colors["border"]};
                border-top-right-radius: 4px;
                border-bottom-right-radius: 4px;
            }}
            
            QComboBox QAbstractItemView {{
                background-color: {colors["background_secondary"]};
                color: {colors["text"]};
                border: 1px solid {colors["border"]};
                selection-background-color: {colors["primary"]};
                selection-color: white;
                outline: 0;
            }}
            
            /* List styling */
            QListWidget {{
                background-color: {colors["background_tertiary"]};
                color: {colors["text"]};
                border: 1px solid {colors["border"]};
                border-radius: 4px;
                outline: 0;
                padding: 4px;
            }}
            
            QListWidget::item {{
                padding: 8px;
                border-radius: 2px;
                margin: 2px;
            }}
            
            QListWidget::item:selected {{
                background-color: {colors["primary"]};
                color: white;
            }}
            
            QListWidget::item:hover:!selected {{
                background-color: {colors["hover"]};
            }}
            
            /* Checkbox styling */
            QCheckBox {{
                color: {colors["text"]};
                spacing: 8px;
            }}
            
            QCheckBox::indicator {{
                width: 18px;
                height: 18px;
                border-radius: 3px;
                border: 1px solid {colors["border"]};
                background-color: {colors["background_tertiary"]};
            }}
            
            QCheckBox::indicator:checked {{
                background-color: {colors["primary"]};
                border-color: {colors["primary"]};
            }}
            
            QCheckBox::indicator:hover {{
                border-color: {colors["primary"]};
            }}
            
            /* Menu styling */
            QMenuBar {{
                background-color: {colors["background_secondary"]};
                color: {colors["text"]};
                border-bottom: 1px solid {colors["border"]};
            }}
            
            QMenuBar::item {{
                padding: 8px 12px;
                background: transparent;
                border-radius: 4px;
            }}
            
            QMenuBar::item:selected {{
                background-color: {colors["primary"]};
                color: white;
            }}
            
            QMenu {{
                background-color: {colors["background_secondary"]};
                color: {colors["text"]};
                border: 1px solid {colors["border"]};
                border-radius: 4px;
            }}
            
            QMenu::item {{
                padding: 8px 25px 8px 20px;
                border-radius: 2px;
                margin: 2px;
            }}
            
            QMenu::item:selected {{
                background-color: {colors["primary"]};
                color: white;
            }}
            
            /* Status bar styling */
            QStatusBar {{
                background-color: {colors["background_secondary"]};
                color: {colors["text"]};
                border-top: 1px solid {colors["border"]};
            }}
            
            /* Scrollbar styling */
            QScrollBar:vertical {{
                background-color: {colors["background"]};
                width: 12px;
                margin: 0;
            }}
            
            QScrollBar::handle:vertical {{
                background-color: {colors["background_tertiary"]};
                min-height: 20px;
                border-radius: 6px;
                margin: 2px;
            }}
            
            QScrollBar::handle:vertical:hover {{
                background-color: {colors["hover"]};
            }}
            
            QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {{
                height: 0px;
            }}
            
            QScrollBar:horizontal {{
                background-color: {colors["background"]};
                height: 12px;
                margin: 0;
            }}
            
            QScrollBar::handle:horizontal {{
                background-color: {colors["background_tertiary"]};
                min-width: 20px;
                border-radius: 6px;
                margin: 2px;
            }}
            
            QScrollBar::handle:horizontal:hover {{
                background-color: {colors["hover"]};
            }}
            
            QScrollBar::add-line:horizontal, QScrollBar::sub-line:horizontal {{
                width: 0px;
            }}
            
            /* Step indicators */
            QWidget#stepIndicator {{
                background-color: {colors["background_secondary"]};
                border-radius: 4px;
                padding: 8px;
            }}
            
            QLabel#stepLabel {{
                color: {colors["text_secondary"]};
                font-weight: bold;
            }}
            
            QLabel#stepLabelActive {{
                color: {colors["primary"]};
                font-weight: bold;
            }}
            
            /* Horizontal workflow panels */
            QWidget#workflowPanel {{
                background-color: {colors["background_secondary"]};
                border-radius: 6px;
                border: 1px solid {colors["border"]};
            }}
            
            /* Specialist cards */
            QFrame#specialistCard {{
                background-color: {colors["background_tertiary"]};
                border-radius: 6px;
                border: 1px solid {colors["border"]};
                padding: 8px;
            }}
            
            QFrame#specialistCard:hover {{
                border: 1px solid {colors["primary"]};
                background-color: {colors["hover"]};
            }}
            
            QLabel#specialistTitle {{
                font-weight: bold;
                color: {colors["text"]};
                font-size: 16px;
            }}
            
            QLabel#specialistDescription {{
                color: {colors["text_secondary"]};
            }}
        """
