from PyQt6.QtGui import QPalette, QColor, QFont
from PyQt6.QtCore import Qt
from colour import Color

from .design_system import (
    COLORS,
    COMPONENT_STYLES,
    FONT_FAMILY,
    FONT_SIZE,
    FONT_WEIGHT,
    SPACING,
    BORDER_RADIUS,
    SHADOWS,
    TRANSITIONS,
)

class Theme:
    @staticmethod
    def _parse_hsl(hsl_str):
        """Convierte una cadena HSL en un objeto QColor."""
        if not hsl_str or not hsl_str.startswith("hsl"):
            return None
        
        try:
            # Eliminar 'hsl' o 'hsla' y paréntesis
            values = hsl_str.split("(")[1].split(")")[0].split(",")
            
            # Parsear valores
            h = float(values[0])
            s = float(values[1].strip().rstrip("%")) / 100
            l = float(values[2].strip().rstrip("%")) / 100
            
            # Usar colour para la conversión HSL -> RGB
            rgb = Color(hsl=(h/360, s, l)).rgb
            
            # Crear QColor
            return QColor.fromRgbF(rgb[0], rgb[1], rgb[2])
        except Exception as e:
            print(f"Error al parsear color HSL '{hsl_str}': {e}")
            # Retornar un color por defecto en caso de error
            return QColor(53, 53, 53)  # Un gris oscuro como fallback

    @staticmethod
    def get_palette():
        palette = QPalette()
        
        # Fondos principales
        palette.setColor(QPalette.ColorRole.Window, Theme._parse_hsl(COLORS["background"]["primary"]))
        palette.setColor(QPalette.ColorRole.Base, Theme._parse_hsl(COLORS["background"]["card"]))
        palette.setColor(QPalette.ColorRole.AlternateBase, Theme._parse_hsl(COLORS["background"]["secondary"]))
        
        # Textos
        palette.setColor(QPalette.ColorRole.WindowText, Theme._parse_hsl(COLORS["text"]["primary"]))
        palette.setColor(QPalette.ColorRole.Text, Theme._parse_hsl(COLORS["text"]["primary"]))
        palette.setColor(QPalette.ColorRole.PlaceholderText, Theme._parse_hsl(COLORS["text"]["muted"]))
        
        # Botones
        palette.setColor(QPalette.ColorRole.Button, Theme._parse_hsl(COLORS["accent"]["primary"]))
        palette.setColor(QPalette.ColorRole.ButtonText, Theme._parse_hsl(COLORS["text"]["primary"]))
        
        # Selección
        palette.setColor(QPalette.ColorRole.Highlight, Theme._parse_hsl(COLORS["accent"]["primary"]))
        palette.setColor(QPalette.ColorRole.HighlightedText, Theme._parse_hsl(COLORS["background"]["primary"]))
        
        # Estados deshabilitados
        palette.setColor(QPalette.ColorGroup.Disabled, QPalette.ColorRole.Text, 
                        Theme._parse_hsl(COLORS["text"]["muted"]))
        palette.setColor(QPalette.ColorGroup.Disabled, QPalette.ColorRole.ButtonText,
                        Theme._parse_hsl(COLORS["text"]["muted"]))
        
        return palette

    @staticmethod
    def get_stylesheet():
        return f"""
        * {{
            font-family: {FONT_FAMILY};
            font-size: {FONT_SIZE["md"]}px;
            color: {COLORS["text"]["primary"]};
        }}
        
        QWidget {{
            background-color: transparent;
            font-family: system-ui, -apple-system, sans-serif;
        }}
        
        QMainWindow, QDialog {{
            background-color: {COLORS["background"]["primary"]};
        }}
        
        /* Glass Panel */
        QFrame[glass="true"] {{
            {COMPONENT_STYLES["panel"]["default"]}
        }}
        
        /* Botones */
        QPushButton {{
            {COMPONENT_STYLES["button"]["primary"]}
            margin: {SPACING["xs"]}px;
            min-width: {SPACING["xxl"]}px;
        }}
        
        QPushButton:hover {{
            box-shadow: {SHADOWS["primary"]};
            opacity: 0.9;
        }}
        
        QPushButton[orange="true"] {{
            {COMPONENT_STYLES["button"]["orange"]}
        }}
        
        QPushButton[orange="true"]:hover {{
            box-shadow: {SHADOWS["orange"]};
            opacity: 0.9;
        }}
        
        QPushButton[red="true"] {{
            {COMPONENT_STYLES["button"]["red"]}
        }}
        
        QPushButton[red="true"]:hover {{
            box-shadow: {SHADOWS["red"]};
            opacity: 0.9;
        }}
        
        QPushButton:disabled {{
            background-color: {COLORS["background"]["muted"]};
            color: {COLORS["text"]["muted"]};
            box-shadow: none;
            opacity: 0.5;
        }}
        
        /* Tarjetas de Agente */
        QFrame[agent-card="true"] {{
            {COMPONENT_STYLES["agent_card"]["default"]}
        }}
        
        QFrame[agent-card="true"][orange="true"] {{
            {COMPONENT_STYLES["agent_card"]["orange"]}
        }}
        
        QFrame[agent-card="true"][red="true"] {{
            {COMPONENT_STYLES["agent_card"]["red"]}
        }}
        
        QFrame[agent-card="true"][hover="true"] {{
            box-shadow: {SHADOWS["lg"]};
        }}
        
        /* Indicadores de Paso */
        QLabel[step-indicator="true"] {{
            {COMPONENT_STYLES["step"]["default"]}
        }}
        
        QLabel[step-indicator="true"][active="true"] {{
            {COMPONENT_STYLES["step"]["active"]}
        }}
        
        QLabel[step-indicator="true"][completed="true"] {{
            {COMPONENT_STYLES["step"]["completed"]}
        }}
        
        /* Líneas conectoras entre pasos */
        QWidget[step-connector="true"] {{
            background-color: {COLORS["border"]["default"]};
            max-height: 2px;
            margin-top: {SPACING["xl"]}px;
        }}
        
        /* Campos de entrada */
        QLineEdit, QTextEdit, QPlainTextEdit {{
            {COMPONENT_STYLES["input"]["default"]}
        }}
        
        QLineEdit:focus, QTextEdit:focus, QPlainTextEdit:focus {{
            {COMPONENT_STYLES["input"]["focus"]}
        }}
        
        /* Etiquetas con variantes */
        QLabel {{
            color: {COLORS["text"]["primary"]};
        }}
        
        QLabel[secondary="true"] {{
            color: {COLORS["text"]["secondary"]};
            font-weight: {FONT_WEIGHT["regular"]};
        }}
        
        QLabel[heading="true"] {{
            color: {COLORS["text"]["primary"]};
            font-weight: {FONT_WEIGHT["semibold"]};
            font-size: {FONT_SIZE["lg"]}px;
            margin-bottom: {SPACING["xs"]}px;
        }}
        
        QLabel[subheading="true"] {{
            color: {COLORS["text"]["secondary"]};
            font-weight: {FONT_WEIGHT["medium"]};
            font-size: {FONT_SIZE["md"]}px;
        }}
        
        /* Scrollbars refinadas */
        QScrollBar:vertical {{
            background-color: {COLORS["background"]["primary"]};
            width: 6px;
            margin: 0;
        }}
        
        QScrollBar::handle:vertical {{
            background-color: {COLORS["background"]["muted"]};
            min-height: 20px;
            border-radius: {BORDER_RADIUS["full"]}px;
        }}
        
        QScrollBar::handle:vertical:hover {{
            background-color: {COLORS["accent"]["primary"]};
        }}
        
        QScrollBar:horizontal {{
            background-color: {COLORS["background"]["primary"]};
            height: 6px;
            margin: 0;
        }}
        
        QScrollBar::handle:horizontal {{
            background-color: {COLORS["background"]["muted"]};
            min-width: 20px;
            border-radius: {BORDER_RADIUS["full"]}px;
        }}
        
        QScrollBar::handle:horizontal:hover {{
            background-color: {COLORS["accent"]["primary"]};
        }}
        
        QScrollBar::add-line, QScrollBar::sub-line {{
            width: 0;
            height: 0;
        }}
        
        /* Menús y Tooltips */
        QMenu {{
            background-color: {COLORS["background"]["elevated"]};
            border: 1px solid {COLORS["border"]["default"]};
            border-radius: {BORDER_RADIUS["md"]}px;
            padding: {SPACING["xs"]}px 0;
        }}
        
        QMenu::item {{
            padding: {SPACING["xs"]}px {SPACING["md"]}px;
            color: {COLORS["text"]["primary"]};
        }}
        
        QMenu::item:selected {{
            background-color: {COLORS["background"]["secondary"]};
        }}
        
        QToolTip {{
            background-color: {COLORS["background"]["elevated"]};
            color: {COLORS["text"]["primary"]};
            border: 1px solid {COLORS["border"]["default"]};
            border-radius: {BORDER_RADIUS["sm"]}px;
            padding: {SPACING["xs"]}px {SPACING["sm"]}px;
        }}
        
        /* Progress bar */
        QProgressBar {{
            border: none;
            background-color: {COLORS["background"]["muted"]};
            height: 4px;
            border-radius: {BORDER_RADIUS["full"]}px;
        }}
        
        QProgressBar::chunk {{
            background-color: {COLORS["accent"]["primary"]};
            border-radius: {BORDER_RADIUS["full"]}px;
        }}
    """

    @staticmethod
    def apply_to_app(app):
        """Aplica el tema completo a la aplicación."""
        app.setStyle("Fusion")  # Base limpia
        app.setPalette(Theme.get_palette())
        app.setStyleSheet(Theme.get_stylesheet())
        
        # Configura la fuente por defecto del sistema como fallback
        font = QFont("system-ui")  # Usar system-ui como fuente fallback
        font.setPixelSize(FONT_SIZE["md"])
        font.setWeight(FONT_WEIGHT["regular"])
        app.setFont(font)
