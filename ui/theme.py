from PyQt6.QtGui import QPalette, QColor
from PyQt6.QtCore import Qt

class Theme:
    # Color palette
    COLORS = {
        "dark": {
            "background": "#1e1e2e",
            "surface": "#2d2d3d",
            "primary": "#7c4dff",  # Vibrant purple
            "secondary": "#03dac6", # Teal
            "accent": "#ff4081",    # Pink
            "error": "#cf6679",
            "text": "#ffffff",
            "text_secondary": "#b0b0b0",
            "border": "#454555"
        },
        "light": {
            "background": "#f5f5f7",
            "surface": "#ffffff",
            "primary": "#6200ee",  # Deep purple
            "secondary": "#03dac6", # Teal
            "accent": "#ff4081",    # Pink
            "error": "#b00020",
            "text": "#202020",
            "text_secondary": "#707070",
            "border": "#e0e0e0"
        }
    }
    
    @staticmethod
    def get_palette(dark_mode=False):
        palette = QPalette()
        colors = Theme.COLORS["dark"] if dark_mode else Theme.COLORS["light"]
        
        palette.setColor(QPalette.ColorRole.Window, QColor(colors["background"]))
        palette.setColor(QPalette.ColorRole.WindowText, QColor(colors["text"]))
        palette.setColor(QPalette.ColorRole.Base, QColor(colors["surface"]))
        palette.setColor(QPalette.ColorRole.AlternateBase, QColor(colors["background"]))
        palette.setColor(QPalette.ColorRole.ToolTipBase, QColor(colors["surface"]))
        palette.setColor(QPalette.ColorRole.ToolTipText, QColor(colors["text"]))
        palette.setColor(QPalette.ColorRole.Text, QColor(colors["text"]))
        palette.setColor(QPalette.ColorRole.Button, QColor(colors["surface"]))
        palette.setColor(QPalette.ColorRole.ButtonText, QColor(colors["text"]))
        palette.setColor(QPalette.ColorRole.Link, QColor(colors["primary"]))
        palette.setColor(QPalette.ColorRole.Highlight, QColor(colors["primary"]))
        palette.setColor(QPalette.ColorRole.HighlightedText, QColor(colors["text"]))
        
        return palette

    @staticmethod
    def get_stylesheet(dark_mode=False):
        colors = Theme.COLORS["dark"] if dark_mode else Theme.COLORS["light"]
        
        return f"""
            QMainWindow {{
                background-color: {colors["background"]};
            }}
            QTabWidget::pane {{
                border: 1px solid {colors["border"]};
                background-color: {colors["surface"]};
                border-radius: 8px;
            }}
            QTabBar::tab {{
                background-color: {colors["surface"]};
                color: {colors["text"]};
                padding: 10px 20px;
                margin-right: 2px;
                border-top-left-radius: 6px;
                border-top-right-radius: 6px;
                border: 1px solid {colors["border"]};
                border-bottom: none;
            }}
            QTabBar::tab:selected {{
                background-color: {colors["primary"]};
                color: white;
                font-weight: bold;
            }}
            QTabBar::tab:hover:!selected {{
                background-color: {colors["background"]};
                border-color: {colors["primary"]};
            }}
            QPushButton {{
                background-color: {colors["primary"]};
                color: white;
                border: none;
                padding: 10px 15px;
                border-radius: 6px;
                font-weight: bold;
            }}
            QPushButton:hover {{
                background-color: {QColor(colors["primary"]).lighter(115).name()};
                box-shadow: 0 2px 5px rgba(0, 0, 0, 0.2);
            }}
            QPushButton:pressed {{
                background-color: {QColor(colors["primary"]).darker(115).name()};
            }}
            QLineEdit, QTextEdit {{
                background-color: {colors["surface"]};
                border: 2px solid {colors["border"]};
                color: {colors["text"]};
                padding: 8px;
                border-radius: 6px;
            }}
            QLineEdit:focus, QTextEdit:focus {{
                border-color: {colors["primary"]};
            }}
            QComboBox {{
                background-color: {colors["surface"]};
                border: 2px solid {colors["border"]};
                color: {colors["text"]};
                padding: 8px;
                border-radius: 6px;
                min-width: 6em;
            }}
            QComboBox:focus {{
                border-color: {colors["primary"]};
            }}
            QComboBox::drop-down {{
                subcontrol-origin: padding;
                subcontrol-position: top right;
                width: 20px;
                border-left-width: 1px;
                border-left-color: {colors["border"]};
                border-left-style: solid;
                border-top-right-radius: 6px;
                border-bottom-right-radius: 6px;
            }}
            QListWidget {{
                background-color: {colors["surface"]};
                border: 2px solid {colors["border"]};
                border-radius: 6px;
                padding: 5px;
            }}
            QListWidget::item {{
                padding: 8px;
                border-radius: 4px;
                margin: 2px;
            }}
            QListWidget::item:selected {{
                background-color: {colors["primary"]};
                color: white;
            }}
            QListWidget::item:hover:!selected {{
                background-color: {colors["background"]};
            }}
            QCheckBox {{
                color: {colors["text"]};
                spacing: 8px;
            }}
            QCheckBox::indicator {{
                width: 18px;
                height: 18px;
                border-radius: 4px;
                border: 2px solid {colors["border"]};
            }}
            QCheckBox::indicator:checked {{
                background-color: {colors["primary"]};
                border-color: {colors["primary"]};
                image: url(:/icons/check.png);
            }}
            QMenuBar {{
                background-color: {colors["surface"]};
                color: {colors["text"]};
                border-bottom: 1px solid {colors["border"]};
            }}
            QMenuBar::item {{
                padding: 8px 12px;
                background: transparent;
            }}
            QMenuBar::item:selected {{
                background-color: {colors["primary"]};
                color: white;
                border-radius: 4px;
            }}
            QMenu {{
                background-color: {colors["surface"]};
                color: {colors["text"]};
                border: 1px solid {colors["border"]};
                border-radius: 6px;
                padding: 5px;
            }}
            QMenu::item {{
                padding: 8px 25px 8px 20px;
                border-radius: 4px;
                margin: 2px;
            }}
            QMenu::item:selected {{
                background-color: {colors["primary"]};
                color: white;
            }}
            QStatusBar {{
                background-color: {colors["surface"]};
                color: {colors["text"]};
                border-top: 1px solid {colors["border"]};
            }}
        """