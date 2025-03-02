from PyQt6.QtGui import QPalette, QColor, QFont, QLinearGradient, QGradient, QBrush, QVector2D
from PyQt6.QtCore import Qt

from .design_system import (
    COLORS,
    GRADIENTS,
    COMPONENT_STYLES,
    FONT_FAMILY,
    FONT_SIZE,
    SPACING,
    BORDER_RADIUS,
    SHADOWS,
)

class Theme:
    @staticmethod
    def _create_gradient(gradient_str):
        """Convierte una cadena de gradiente en un objeto QLinearGradient."""
        if not gradient_str or not gradient_str.startswith("qlineargradient"):
            return None
        
        # Parsear parámetros del gradiente
        params = gradient_str.split("(")[1].split(")")[0].split(",")
        params = {p.split(":")[0].strip(): p.split(":")[1].strip() for p in params}
        
        # Crear objeto gradiente con coordenadas enteras
        gradient = QLinearGradient(
            0, 0 if params.get("y1", "0") == "0" else 100,
            0 if params.get("x2", "0") == "0" else 100,
            0 if params.get("y2", "0") == "0" else 100
        )
        
        # Añadir stops
        stops = [(float(s.split(" ")[0]), s.split(" ")[1]) for s in params["stop"].split(",")]
        for pos, color in stops:
            gradient.setColorAt(pos, QColor(color))
        
        gradient.setCoordinateMode(QGradient.CoordinateMode.ObjectBoundingMode)
        return gradient

    @staticmethod
    def get_palette():
        palette = QPalette()
        
        # Fondos principales
        palette.setColor(QPalette.ColorRole.Window, QColor(COLORS["background"]["primary"]))
        palette.setColor(QPalette.ColorRole.Base, QColor(COLORS["background"]["secondary"]))
        palette.setColor(QPalette.ColorRole.AlternateBase, QColor(COLORS["background"]["tertiary"]))
        
        # Textos
        palette.setColor(QPalette.ColorRole.WindowText, QColor(COLORS["text"]["primary"]))
        palette.setColor(QPalette.ColorRole.Text, QColor(COLORS["text"]["primary"]))
        palette.setColor(QPalette.ColorRole.PlaceholderText, QColor(COLORS["text"]["hint"]))
        palette.setColor(QPalette.ColorRole.BrightText, QColor(COLORS["text"]["primary"]))
        
        # Botones y controles
        palette.setColor(QPalette.ColorRole.Button, QColor(COLORS["background"]["tertiary"]))
        palette.setColor(QPalette.ColorRole.ButtonText, QColor(COLORS["text"]["primary"]))
        
        # Selección
        palette.setColor(QPalette.ColorRole.Highlight, QColor(COLORS["accent"]["primary"]))
        palette.setColor(QPalette.ColorRole.HighlightedText, QColor(COLORS["text"]["primary"]))
        
        # Estados deshabilitados
        palette.setColor(QPalette.ColorGroup.Disabled, QPalette.ColorRole.Text, 
                        QColor(COLORS["text"]["disabled"]))
        palette.setColor(QPalette.ColorGroup.Disabled, QPalette.ColorRole.ButtonText,
                        QColor(COLORS["text"]["disabled"]))
        palette.setColor(QPalette.ColorGroup.Disabled, QPalette.ColorRole.WindowText,
                        QColor(COLORS["text"]["disabled"]))
        
        return palette

    @staticmethod
    def get_stylesheet():
        return f"""
        /* Estilo Global */
        * {{
            font-family: {FONT_FAMILY};
        }}
        
        QMainWindow, QDialog {{
            background-color: {COLORS["background"]["primary"]};
            color: {COLORS["text"]["primary"]};
        }}
        
        /* Botones */
        QPushButton {{
            {COMPONENT_STYLES["button"]["secondary"]}
            margin: {SPACING["xs"]}px;
        }}
        
        QPushButton:hover {{
            background-color: {COLORS["state"]["hover"]};
            border: 1px solid {COLORS["border"]["light"]};
            box-shadow: {SHADOWS["elevated"]};
        }}
        
        QPushButton:pressed {{
            background-color: {COLORS["state"]["pressed"]};
            border: 1px solid {COLORS["border"]["focus"]};
        }}
        
        QPushButton:disabled {{
            background-color: {COLORS["background"]["secondary"]};
            color: {COLORS["text"]["disabled"]};
            border: 1px solid {COLORS["border"]["default"]};
            box-shadow: none;
        }}
        
        QPushButton[primary="true"] {{
            {COMPONENT_STYLES["button"]["primary"]}
        }}
        
        QPushButton[primary="true"]:hover {{
            border: 1px solid {COLORS["accent"]["primary"]};
            background-color: {COLORS["accent"]["primary"]};
        }}
        
        QPushButton[success="true"] {{
            {COMPONENT_STYLES["button"]["success"]}
        }}
        
        QPushButton[success="true"]:hover {{
            border: 1px solid {COLORS["accent"]["green"]};
            background-color: {COLORS["feedback"]["success"]};
        }}
        
        /* Campos de entrada */
        QLineEdit, QTextEdit, QPlainTextEdit {{
            {COMPONENT_STYLES["input"]["default"]}
        }}
        
        QLineEdit:focus, QTextEdit:focus, QPlainTextEdit:focus {{
            {COMPONENT_STYLES["input"]["focused"]}
        }}
        
        QLineEdit:hover, QTextEdit:hover, QPlainTextEdit:hover {{
            {COMPONENT_STYLES["input"]["hover"]}
        }}
        
        QLineEdit:disabled, QTextEdit:disabled, QPlainTextEdit:disabled {{
            background-color: {COLORS["background"]["secondary"]};
            color: {COLORS["text"]["disabled"]};
            border: 1px solid {COLORS["border"]["default"]};
        }}
        
        /* Paneles */
        QFrame[frameShape="6"], QFrame[panel="true"] {{
            {COMPONENT_STYLES["panel"]["default"]}
        }}
        
        QFrame[elevated="true"] {{
            {COMPONENT_STYLES["panel"]["elevated"]}
        }}
        
        /* Barras de herramientas */
        QToolBar {{
            {COMPONENT_STYLES["toolbar"]["default"]}
        }}
        
        /* Barra de estado */
        QStatusBar {{
            {COMPONENT_STYLES["statusbar"]["default"]}
        }}
        
        /* Menús */
        QMenuBar {{
            background-color: {COLORS["background"]["tertiary"]};
            color: {COLORS["text"]["primary"]};
            border-bottom: 1px solid {COLORS["border"]["default"]};
        }}
        
        QMenuBar::item:selected {{
            background-color: {COLORS["state"]["selected"]};
        }}
        
        QMenu {{
            {COMPONENT_STYLES["menu"]["default"]}
        }}
        
        QMenu::item {{
            {COMPONENT_STYLES["menu"]["item"]}
        }}
        
        QMenu::item:selected {{
            {COMPONENT_STYLES["menu"]["item_selected"]}
        }}
        
        /* Pestañas */
        QTabBar::tab {{
            {COMPONENT_STYLES["tab"]["default"]}
        }}
        
        QTabBar::tab:selected {{
            {COMPONENT_STYLES["tab"]["selected"]}
        }}
        
        QTabBar::tab:hover {{
            {COMPONENT_STYLES["tab"]["hover"]}
        }}
        
        /* Scrollbars */
        QScrollBar:vertical {{
            background-color: {COLORS["background"]["secondary"]};
            width: 12px;
            margin: 0;
        }}
        
        QScrollBar::handle:vertical {{
            background-color: {COLORS["background"]["elevated"]};
            min-height: 20px;
            border-radius: {BORDER_RADIUS["sm"]}px;
            margin: 2px;
        }}
        
        QScrollBar::handle:vertical:hover {{
            background-color: {COLORS["state"]["hover"]};
        }}
        
        QScrollBar:horizontal {{
            background-color: {COLORS["background"]["secondary"]};
            height: 12px;
            margin: 0;
        }}
        
        QScrollBar::handle:horizontal {{
            background-color: {COLORS["background"]["elevated"]};
            min-width: 20px;
            border-radius: {BORDER_RADIUS["sm"]}px;
            margin: 2px;
        }}
        
        QScrollBar::handle:horizontal:hover {{
            background-color: {COLORS["state"]["hover"]};
        }}
        
        QScrollBar::add-line, QScrollBar::sub-line {{
            width: 0;
            height: 0;
        }}
        
        /* Headers y etiquetas */
        QLabel[header="true"] {{
            {COMPONENT_STYLES["header"]["default"]}
        }}
        
        /* Comboboxes */
        QComboBox {{
            {COMPONENT_STYLES["input"]["default"]}
        }}
        
        QComboBox:hover {{
            {COMPONENT_STYLES["input"]["hover"]}
        }}
        
        QComboBox::drop-down {{
            border: none;
            padding-right: {SPACING["xs"]}px;
        }}
        
        QComboBox QAbstractItemView {{
            {COMPONENT_STYLES["menu"]["default"]}
            selection-background-color: {COLORS["state"]["selected"]};
        }}
        
        /* Checkboxes y Radio buttons */
        QCheckBox, QRadioButton {{
            color: {COLORS["text"]["primary"]};
            spacing: {SPACING["xs"]}px;
        }}
        
        QCheckBox:disabled, QRadioButton:disabled {{
            color: {COLORS["text"]["disabled"]};
        }}
        
        /* Grupos */
        QGroupBox {{
            {COMPONENT_STYLES["panel"]["default"]}
            padding-top: {SPACING["xl"]}px;
            margin-top: {SPACING["sm"]}px;
        }}
        
        QGroupBox::title {{
            color: {COLORS["text"]["primary"]};
            subcontrol-origin: margin;
            subcontrol-position: top left;
            padding: 0 {SPACING["xs"]}px;
            background-color: {COLORS["background"]["primary"]};
        }}
        
        /* Progress Bars */
        QProgressBar {{
            border: none;
            border-radius: {BORDER_RADIUS["xs"]}px;
            background-color: {COLORS["background"]["secondary"]};
            height: 4px;
            text-align: center;
        }}
        
        QProgressBar::chunk {{
            background-color: {COLORS["accent"]["primary"]};
            border-radius: {BORDER_RADIUS["xs"]}px;
        }}
        
        /* Trees y Listas */
        QTreeView, QListView {{
            {COMPONENT_STYLES["panel"]["default"]}
            show-decoration-selected: 1;
        }}
        
        QTreeView::item, QListView::item {{
            padding: {SPACING["xs"]}px;
            border-radius: {BORDER_RADIUS["xs"]}px;
        }}
        
        QTreeView::item:selected, QListView::item:selected {{
            background-color: {COLORS["state"]["selected"]};
            color: {COLORS["text"]["primary"]};
        }}
        
        QTreeView::item:hover, QListView::item:hover {{
            background-color: {COLORS["state"]["hover"]};
        }}
        
        QTreeView::branch {{
            background: transparent;
        }}
        
        /* Tooltips */
        QToolTip {{
            background-color: {COLORS["background"]["elevated"]};
            color: {COLORS["text"]["primary"]};
            border: 1px solid {COLORS["border"]["default"]};
            border-radius: {BORDER_RADIUS["sm"]}px;
            padding: {SPACING["xs"]}px {SPACING["sm"]}px;
        }}
    """

    @staticmethod
    def apply_to_app(app):
        """Aplica el tema completo a la aplicación."""
        app.setStyle("Fusion")  # Estilo base limpio
        app.setPalette(Theme.get_palette())
        app.setStyleSheet(Theme.get_stylesheet())
        
        # Configura la fuente por defecto
        font = QFont(FONT_FAMILY.split(",")[0].strip())
        font.setPixelSize(FONT_SIZE["md"])
        app.setFont(font)
