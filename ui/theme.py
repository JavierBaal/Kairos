from PyQt6.QtGui import QPalette, QColor
from PyQt6.QtCore import Qt

class Theme:
    # Color palette - Inspired by modern UI design and Kairos concept art
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
            "selected": "#4dabf7",
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
            "selected": "#2b7cd1",
        },
        "mixed": {
            # Base colors - Dark backgrounds with light content areas
            "background": "#16162e",  # Más oscuro para mejor contraste
            "background_secondary": "#f9f9f9",  # Más claro para mejor legibilidad
            "background_tertiary": "#e8e8e8",
            "text": "#202020",  # Más oscuro para mejor legibilidad
            "text_secondary": "#5a5a68",  # Más oscuro para mejor contraste
            "text_on_dark": "#ffffff",
            "text_secondary_on_dark": "#d0d0d8",  # Más claro para mejor legibilidad

            # Accent colors - Vibrant gradients
            "primary": "#6a3de8",
            "primary_dark": "#5035b0",
            "secondary": "#ff5a5f",
            "tertiary": "#00c2a8",
            "error": "#ff3b5b",
            "warning": "#ffbd3d",
            "info": "#3d8aff",
            
            # Gradient colors
            "gradient_purple": "#6a3de8",
            "gradient_blue": "#3d8aff",
            "gradient_coral": "#ff5a5f",
            "gradient_orange": "#ff8f59",
            "gradient_teal": "#00c2a8",
            
            # UI elements
            "border": "#e0e0e0",
            "border_dark": "#383860",  # Más oscuro para mejor contraste
            "surface_light": "#ffffff",
            "surface_dark": "#1e1e38",  # Más oscuro para mejor contraste
            "hover_light": "#f0f0f0",
            "hover_dark": "#2a2a4d",  # Ajustado para mejor contraste
            "selected": "#6a3de8",
        }
    }

    # Gradients
    GRADIENTS = {
        "dark": {
            "primary_button": "qlineargradient(x1:0, y1:0, x2:0, y2:1, stop:0 #4dabf7, stop:1 #3d8bd7)",
            "secondary_button": "qlineargradient(x1:0, y1:0, x2:0, y2:1, stop:0 #3c3f41, stop:1 #323537)",
            "main_panel": "qlineargradient(x1:0, y1:0, x2:0, y2:1, stop:0 #2b2d30, stop:1 #252729)",
            "app_background": "qlineargradient(x1:0, y1:0, x2:1, y2:1, stop:0 #1e1f22, stop:1 #191a1d)",
        },
        "light": {
            "primary_button": "qlineargradient(x1:0, y1:0, x2:0, y2:1, stop:0 #3b8be3, stop:1 #2b7cd1)",
            "secondary_button": "qlineargradient(x1:0, y1:0, x2:0, y2:1, stop:0 #f0f0f0, stop:1 #e7e7e7)",
            "main_panel": "qlineargradient(x1:0, y1:0, x2:0, y2:1, stop:0 #ffffff, stop:1 #f7f7f7)",
            "app_background": "qlineargradient(x1:0, y1:0, x2:1, y2:1, stop:0 #f7f8fa, stop:1 #f0f1f3)",
        },
        "mixed": {
            # Vibrant gradients inspired by the reference images
            "primary_button": "qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 #6a3de8, stop:1 #3d8aff)",
            "secondary_button": "qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 #ff5a5f, stop:1 #ff8f59)",
            "tertiary_button": "qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 #00c2a8, stop:1 #5aaa4f)",
            
            # Background gradients - Más sutiles y elegantes
            "app_background": "qlineargradient(x1:0, y1:0, x2:1, y2:1, stop:0 #16162e, stop:1 #1e1e38)",
            "main_panel_light": "qlineargradient(x1:0, y1:0, x2:0, y2:1, stop:0 #ffffff, stop:1 #f5f5f5)",
            "main_panel_dark": "qlineargradient(x1:0, y1:0, x2:0, y2:1, stop:0 #1e1e38, stop:1 #16162e)",
            
            # Accent gradients - Más suaves para mejor ergonomía visual
            "accent_purple_blue": "qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 #6a3de8, stop:1 #3d8aff)",
            "accent_coral_orange": "qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 #ff5a5f, stop:1 #ff8f59)",
            "accent_teal_green": "qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 #00c2a8, stop:1 #5aaa4f)",
        }
    }

    @staticmethod
    def get_palette(theme_mode="mixed"):
        palette = QPalette()
        
        if theme_mode not in ["dark", "light", "mixed"]:
            theme_mode = "mixed"  # Default to mixed theme
            
        colors = Theme.COLORS[theme_mode]

        # Set up palette colors
        if theme_mode == "mixed":
            # Mixed theme uses dark background with light content areas
            palette.setColor(QPalette.ColorRole.Window, QColor(colors["background"]))
            palette.setColor(QPalette.ColorRole.WindowText, QColor(colors["text_on_dark"]))
            palette.setColor(QPalette.ColorRole.Base, QColor(colors["background_secondary"]))
            palette.setColor(QPalette.ColorRole.AlternateBase, QColor(colors["background_tertiary"]))
            palette.setColor(QPalette.ColorRole.ToolTipBase, QColor(colors["surface_dark"]))
            palette.setColor(QPalette.ColorRole.ToolTipText, QColor(colors["text_on_dark"]))
            palette.setColor(QPalette.ColorRole.Text, QColor(colors["text"]))
            palette.setColor(QPalette.ColorRole.Button, QColor(colors["surface_light"]))
            palette.setColor(QPalette.ColorRole.ButtonText, QColor(colors["text"]))
            palette.setColor(QPalette.ColorRole.BrightText, QColor(colors["text_on_dark"]))
            palette.setColor(QPalette.ColorRole.Link, QColor(colors["primary"]))
            palette.setColor(QPalette.ColorRole.Highlight, QColor(colors["primary"]))
            palette.setColor(QPalette.ColorRole.HighlightedText, QColor("#ffffff"))
        else:
            # Standard dark/light themes
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
    def get_stylesheet(theme_mode="mixed"):
        if theme_mode not in ["dark", "light", "mixed"]:
            theme_mode = "mixed"  # Default to mixed theme
            
        colors = Theme.COLORS[theme_mode]
        gradients = Theme.GRADIENTS[theme_mode]

        if theme_mode == "mixed":
            return f"""
                /* General Application Style */
                QWidget {{
                    font-family: 'Segoe UI', 'Arial', sans-serif;
                    font-size: 14px;
                    color: {colors["text"]};
                    letter-spacing: 0.2px;
                }}

                QMainWindow {{
                    background: {gradients["app_background"]};
                }}

                /* Buttons with gradients */
                QPushButton {{
                    background: {gradients["secondary_button"]};
                    color: white;
                    border: none;
                    border-radius: 6px;
                    padding: 10px 20px;
                    font-weight: 600;
                    letter-spacing: 0.5px;
                }}

                QPushButton:hover {{
                    opacity: 0.9;
                }}

                QPushButton:pressed {{
                    opacity: 0.8;
                }}

                QPushButton#primaryButton {{
                    background: {gradients["primary_button"]};
                    color: white;
                    font-weight: bold;
                }}

                QPushButton#tertiaryButton {{
                    background: {gradients["tertiary_button"]};
                    color: white;
                    font-weight: bold;
                }}

                /* Panels with mixed styling */
                QGroupBox {{
                    background: {gradients["main_panel_light"]};
                    border: 1px solid {colors["border"]};
                    border-radius: 12px;
                    margin-top: 12px;
                    padding-top: 16px;
                    font-weight: bold;
                    color: {colors["text"]};
                }}

                QGroupBox::title {{
                    subcontrol-origin: margin;
                    subcontrol-position: top left;
                    padding: 0 6px;
                    color: {colors["text"]};
                }}

                QGroupBox#darkPanel {{
                    background: {gradients["main_panel_dark"]};
                    border: 1px solid {colors["border_dark"]};
                    color: {colors["text_on_dark"]};
                }}

                QGroupBox#darkPanel QLabel {{
                    color: {colors["text_on_dark"]};
                }}

                /* Tabs with modern styling */
                QTabWidget::pane {{
                    border: 1px solid {colors["border"]};
                    background-color: {colors["background_secondary"]};
                    border-radius: 12px;
                }}

                QTabBar::tab {{
                    background-color: {colors["surface_dark"]};
                    color: {colors["text_on_dark"]};
                    padding: 12px 24px;
                    margin-right: 4px;
                    border-top-left-radius: 8px;
                    border-top-right-radius: 8px;
                    border: none;
                }}

                QTabBar::tab:selected {{
                    background: {gradients["primary_button"]};
                    color: white;
                    font-weight: bold;
                }}

                QTabBar::tab:hover:!selected {{
                    background-color: {colors["hover_dark"]};
                }}

                /* Form elements with consistent styling */
                QLineEdit, QTextEdit, QPlainTextEdit {{
                    background-color: white;
                    color: {colors["text"]};
                    border: 1px solid {colors["border"]};
                    border-radius: 8px;
                    padding: 12px;
                    selection-background-color: {colors["primary"]};
                    font-size: 15px;
                }}

                QLineEdit:focus, QTextEdit:focus, QPlainTextEdit:focus {{
                    border: 1px solid {colors["primary"]};
                }}

                /* Dropdown styling */
                QComboBox {{
                    background-color: white;
                    color: {colors["text"]};
                    border: 1px solid {colors["border"]};
                    border-radius: 8px;
                    padding: 10px;
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
                    border-top-right-radius: 8px;
                    border-bottom-right-radius: 8px;
                }}

                QComboBox QAbstractItemView {{
                    background-color: white;
                    color: {colors["text"]};
                    border: 1px solid {colors["border"]};
                    selection-background-color: {colors["primary"]};
                    selection-color: white;
                    outline: 0;
                }}

                /* List styling */
                QListWidget {{
                    background-color: white;
                    color: {colors["text"]};
                    border: 1px solid {colors["border"]};
                    border-radius: 8px;
                    outline: 0;
                    padding: 4px;
                }}

                QListWidget::item {{
                    padding: 10px;
                    border-radius: 4px;
                    margin: 2px;
                }}

                QListWidget::item:selected {{
                    background: {gradients["primary_button"]};
                    color: white;
                }}

                QListWidget::item:hover:!selected {{
                    background-color: {colors["hover_light"]};
                }}

                /* Dark-themed list for agent monitoring */
                QListWidget#darkList {{
                    background-color: {colors["surface_dark"]};
                    color: {colors["text_on_dark"]};
                    border: 1px solid {colors["border_dark"]};
                }}

                QListWidget#darkList::item {{
                    background-color: rgba(255, 255, 255, 0.05);
                    border-radius: 6px;
                }}

                QListWidget#darkList::item:selected {{
                    background: {gradients["primary_button"]};
                }}

                QListWidget#darkList::item:hover:!selected {{
                    background-color: rgba(255, 255, 255, 0.1);
                }}

                /* Checkbox styling */
                QCheckBox {{
                    color: {colors["text"]};
                    spacing: 8px;
                }}

                QCheckBox::indicator {{
                    width: 20px;
                    height: 20px;
                    border-radius: 4px;
                    border: 1px solid {colors["border"]};
                    background-color: white;
                }}

                QCheckBox::indicator:checked {{
                    background: {gradients["primary_button"]};
                    border: none;
                }}

                QCheckBox::indicator:hover {{
                    border-color: {colors["primary"]};
                }}

                /* Menu styling */
                QMenuBar {{
                    background-color: {colors["surface_dark"]};
                    color: {colors["text_on_dark"]};
                    border: none;
                }}

                QMenuBar::item {{
                    padding: 10px 15px;
                    background: transparent;
                    border-radius: 6px;
                }}

                QMenuBar::item:selected {{
                    background: {gradients["primary_button"]};
                    color: white;
                }}

                QMenu {{
                    background-color: {colors["surface_dark"]};
                    color: {colors["text_on_dark"]};
                    border: 1px solid {colors["border_dark"]};
                    border-radius: 8px;
                    padding: 5px;
                }}

                QMenu::item {{
                    padding: 10px 30px 10px 20px;
                    border-radius: 4px;
                    margin: 3px;
                }}

                QMenu::item:selected {{
                    background: {gradients["primary_button"]};
                    color: white;
                }}

                /* Status bar styling */
                QStatusBar {{
                    background-color: {colors["surface_dark"]};
                    color: {colors["text_on_dark"]};
                    border: none;
                }}

                /* Scrollbar styling - Más delgados para mejor ergonomía */
                QScrollBar:vertical {{
                    background-color: transparent;
                    width: 6px;
                    margin: 0;
                }}

                QScrollBar::handle:vertical {{
                    background: {gradients["accent_purple_blue"]};
                    min-height: 20px;
                    border-radius: 3px;
                    margin: 1px;
                }}

                QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {{
                    height: 0px;
                }}

                QScrollBar:horizontal {{
                    background-color: transparent;
                    height: 6px;
                    margin: 0;
                }}

                QScrollBar::handle:horizontal {{
                    background: {gradients["accent_purple_blue"]};
                    min-width: 20px;
                    border-radius: 3px;
                    margin: 1px;
                }}

                QScrollBar::add-line:horizontal, QScrollBar::sub-line:horizontal {{
                    width: 0px;
                }}

                /* Step indicators */
                QWidget#stepIndicator {{
                    background-color: {colors["surface_dark"]};
                    border-radius: 25px;
                    padding: 0px;
                }}

                QLabel#stepNumber {{
                    color: white;
                    font-weight: bold;
                    font-size: 18px;
                    background: {gradients["accent_purple_blue"]};
                    border-radius: 20px;
                    min-width: 40px;
                    min-height: 40px;
                    padding: 0px;
                    qproperty-alignment: AlignCenter;
                }}

                QLabel#stepNumberInactive {{
                    color: white;
                    font-weight: bold;
                    font-size: 18px;
                    background-color: rgba(255, 255, 255, 0.2);
                    border-radius: 20px;
                    min-width: 40px;
                    min-height: 40px;
                    padding: 0px;
                    qproperty-alignment: AlignCenter;
                }}

                QLabel#stepLabel {{
                    color: {colors["text_secondary_on_dark"]};
                    font-weight: bold;
                    font-size: 14px;
                }}

                QLabel#stepLabelActive {{
                    color: white;
                    font-weight: bold;
                    font-size: 14px;
                }}

                /* Horizontal workflow panels */
                QWidget#workflowPanel {{
                    background-color: {colors["background_secondary"]};
                    border-radius: 12px;
                    border: 1px solid {colors["border"]};
                }}

                /* Specialist cards */
                QFrame#specialistCard {{
                    background-color: white;
                    border-radius: 12px;
                    border: 1px solid {colors["border"]};
                    padding: 15px;
                }}

                QFrame#specialistCard:hover {{
                    border: 1px solid {colors["primary"]};
                    background-color: {colors["hover_light"]};
                }}

                QLabel#specialistTitle {{
                    font-weight: bold;
                    color: {colors["text"]};
                    font-size: 18px;
                }}

                QLabel#specialistDescription {{
                    color: {colors["text_secondary"]};
                    font-size: 14px;
                }}

                /* Agent monitoring components - Mejorados para mejor legibilidad */
                QWidget#agentMonitor {{
                    background: {gradients["main_panel_dark"]};
                    border-radius: 12px;
                    padding: 15px;
                }}

                QLabel#agentName {{
                    color: white;
                    font-weight: bold;
                    font-size: 18px;
                    letter-spacing: 0.5px;
                }}

                QLabel#agentRole {{
                    color: {colors["text_secondary_on_dark"]};
                    font-style: italic;
                    font-size: 15px;
                }}

                QLabel#costLabel, QLabel#tokenLabel, QLabel#progressLabel, QLabel#statusLabel {{
                    color: {colors["text_secondary_on_dark"]};
                    font-size: 14px;
                    font-weight: 500;
                }}

                QLabel#costValue, QLabel#tokenValue, QLabel#progressValue, QLabel#statusValue {{
                    color: white;
                    font-weight: bold;
                    font-size: 16px;
                }}

                /* Progress bar styling - Más delgadas para mejor contraste visual */
                QProgressBar {{
                    border: none;
                    border-radius: 2px;
                    background-color: rgba(255, 255, 255, 0.1);
                    height: 4px;
                    text-align: center;
                }}

                QProgressBar::chunk {{
                    background: {gradients["accent_coral_orange"]};
                    border-radius: 2px;
                }}

                /* Cost monitoring panel */
                QWidget#costPanel {{
                    background: {gradients["main_panel_dark"]};
                    border-radius: 12px;
                    padding: 20px;
                }}

                QLabel#costTitle {{
                    color: white;
                    font-weight: bold;
                    font-size: 20px;
                    letter-spacing: 0.5px;
                }}

                QLabel#costTotal {{
                    color: white;
                    font-weight: bold;
                    font-size: 28px;
                }}

                QLabel#tokenCount {{
                    color: {colors["text_secondary_on_dark"]};
                    font-size: 15px;
                }}

                /* Charts and visualizations */
                QWidget#chartWidget {{
                    background-color: {colors["surface_dark"]};
                    border-radius: 12px;
                    padding: 15px;
                }}

                /* Drag and drop areas */
                QWidget#dropArea {{
                    background-color: rgba(255, 255, 255, 0.05);
                    border: 1px dashed rgba(255, 255, 255, 0.2);
                    border-radius: 12px;
                    padding: 30px;
                }}

                QWidget#dropArea:hover {{
                    background-color: rgba(255, 255, 255, 0.1);
                    border: 1px dashed {colors["primary"]};
                }}

                QLabel#dropLabel {{
                    color: {colors["text_secondary_on_dark"]};
                    font-size: 16px;
                    font-style: italic;
                    qproperty-alignment: AlignCenter;
                }}
            """
        else:
            # Return the original dark/light theme stylesheet
            return """
                /* General Application Style */
                QWidget {
                    font-family: 'JetBrains Mono', 'Segoe UI', 'Arial';
                    font-size: 14px;
                    color: #ffffff;
                }

                QMainWindow {
                    background: qlineargradient(x1:0, y1:0, x2:1, y2:1, stop:0 #1e1f22, stop:1 #191a1d);
                }

                /* Buttons with gradients */
                QPushButton {
                    background: qlineargradient(x1:0, y1:0, x2:0, y2:1, stop:0 #3c3f41, stop:1 #323537);
                    color: #ffffff;
                    border: none;
                    border-radius: 4px;
                    padding: 8px 16px;
                    font-weight: 500;
                }

                QPushButton:hover {
                    background-color: #4e5254;
                }

                QPushButton:pressed {
                    background-color: #3c3f41;
                }

                QPushButton#primaryButton {
                    background: qlineargradient(x1:0, y1:0, x2:0, y2:1, stop:0 #4dabf7, stop:1 #3d8bd7);
                    color: white;
                    font-weight: bold;
                }

                /* Panels with gradients */
                QGroupBox {
                    background: qlineargradient(x1:0, y1:0, x2:0, y2:1, stop:0 #2b2d30, stop:1 #252729);
                    border: 1px solid #5a5d5f;
                    border-radius: 6px;
                    margin-top: 12px;
                    padding-top: 16px;
                    font-weight: bold;
                }

                QGroupBox::title {
                    subcontrol-origin: margin;
                    subcontrol-position: top left;
                    padding: 0 6px;
                    color: #ffffff;
                }
            """
