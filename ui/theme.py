from PyQt6.QtGui import QPalette, QColor, QFont
from PyQt6.QtCore import Qt

from .design_system import (
    COLORS,
    GRADIENTS,
    COMPONENT_STYLES,
    FONT_FAMILY,
    FONT_SIZE,
    SPACING,
    BORDER_RADIUS
)

class Theme:
    @staticmethod
    def get_palette():
        palette = QPalette()
        
        # Colores de fondo
        palette.setColor(QPalette.ColorRole.Window, QColor(COLORS["background"]["primary"]))
        palette.setColor(QPalette.ColorRole.Base, QColor(COLORS["background"]["secondary"]))
        palette.setColor(QPalette.ColorRole.AlternateBase, QColor(COLORS["background"]["tertiary"]))
        
        # Colores de texto
        palette.setColor(QPalette.ColorRole.WindowText, QColor(COLORS["text"]["primary"]))
        palette.setColor(QPalette.ColorRole.Text, QColor(COLORS["text"]["primary"]))
        palette.setColor(QPalette.ColorRole.PlaceholderText, QColor(COLORS["text"]["hint"]))
        palette.setColor(QPalette.ColorRole.BrightText, QColor(COLORS["text"]["primary"]))
        
        # Colores de botones
        palette.setColor(QPalette.ColorRole.Button, QColor(COLORS["background"]["tertiary"]))
        palette.setColor(QPalette.ColorRole.ButtonText, QColor(COLORS["text"]["primary"]))
        
        # Colores de selección
        palette.setColor(QPalette.ColorRole.Highlight, QColor(COLORS["accent"]["primary"]))
        palette.setColor(QPalette.ColorRole.HighlightedText, QColor(COLORS["text"]["primary"]))
        
        # Colores deshabilitados
        palette.setColor(QPalette.ColorGroup.Disabled, QPalette.ColorRole.Text, QColor(COLORS["text"]["disabled"]))
        palette.setColor(QPalette.ColorGroup.Disabled, QPalette.ColorRole.ButtonText, QColor(COLORS["text"]["disabled"]))
        palette.setColor(QPalette.ColorGroup.Disabled, QPalette.ColorRole.WindowText, QColor(COLORS["text"]["disabled"]))
        
        return palette

    @staticmethod
    def get_stylesheet():
        return f"""
        /* Estilo Global */
        * {{
            font-family: {FONT_FAMILY};
        }}
        
        /* QMainWindow y QDialog */
        QMainWindow, QDialog {{
            background-color: {COLORS["background"]["primary"]};
            color: {COLORS["text"]["primary"]};
        }}
        
        /* Botones */
        QPushButton {{
            {COMPONENT_STYLES["button"]["secondary"]}
        }}
        
        QPushButton:hover {{
            background: qlineargradient(x1:0, y1:0, x2:0, y2:1, 
                                      stop:0 #4e5157, stop:1 #45474c);
            border: 1px solid {COLORS["border"]["hover"]};
        }}
        
        QPushButton:pressed {{
            background: {COLORS["state"]["pressed"]};
        }}
        
        QPushButton:disabled {{
            background: {COLORS["background"]["secondary"]};
            color: {COLORS["text"]["disabled"]};
            border: 1px solid {COLORS["border"]["default"]};
        }}
        
        QPushButton[primary="true"] {{
            {COMPONENT_STYLES["button"]["primary"]}
        }}
        
        QPushButton[success="true"] {{
            {COMPONENT_STYLES["button"]["success"]}
        }}
        
        /* Campos de entrada */
        QLineEdit, QTextEdit, QPlainTextEdit {{
            {COMPONENT_STYLES["input"]["default"]}
        }}
        
        QLineEdit:focus, QTextEdit:focus, QPlainTextEdit:focus {{
            {COMPONENT_STYLES["input"]["focused"]}
        }}
        
        QLineEdit:disabled, QTextEdit:disabled, QPlainTextEdit:disabled {{
            background: {COLORS["background"]["secondary"]};
            color: {COLORS["text"]["disabled"]};
            border: 1px solid {COLORS["border"]["default"]};
        }}
        
        /* Paneles */
        QFrame[frameShape="6"], QFrame[panel="true"] {{
            {COMPONENT_STYLES["panel"]["default"]}
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
            background: {COLORS["background"]["tertiary"]};
            color: {COLORS["text"]["primary"]};
        }}
        
        QMenuBar::item:selected {{
            background: {COLORS["state"]["selected"]};
        }}
        
        QMenu {{
            {COMPONENT_STYLES["menu"]["default"]}
        }}
        
        QMenu::item {{
            {COMPONENT_STYLES["menu"]["item"]}
        }}
        
        QMenu::item:selected {{
            background: {COLORS["state"]["selected"]};
        }}
        
        /* Pestañas */
        QTabBar::tab {{
            {COMPONENT_STYLES["tab"]["default"]}
        }}
        
        QTabBar::tab:selected {{
            {COMPONENT_STYLES["tab"]["selected"]}
        }}
        
        QTabBar::tab:hover {{
            background: {COLORS["state"]["hover"]};
        }}
        
        /* Scrollbars */
        QScrollBar:vertical {{
            background: {COLORS["background"]["secondary"]};
            width: 12px;
            margin: 0;
        }}
        
        QScrollBar::handle:vertical {{
            background: {COLORS["background"]["tertiary"]};
            min-height: 20px;
            border-radius: {BORDER_RADIUS["sm"]}px;
        }}
        
        QScrollBar::handle:vertical:hover {{
            background: {COLORS["state"]["hover"]};
        }}
        
        QScrollBar:horizontal {{
            background: {COLORS["background"]["secondary"]};
            height: 12px;
            margin: 0;
        }}
        
        QScrollBar::handle:horizontal {{
            background: {COLORS["background"]["tertiary"]};
            min-width: 20px;
            border-radius: {BORDER_RADIUS["sm"]}px;
        }}
        
        QScrollBar::handle:horizontal:hover {{
            background: {COLORS["state"]["hover"]};
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
            border: 1px solid {COLORS["border"]["hover"]};
        }}
        
        QComboBox::drop-down {{
            border: none;
            padding-right: {SPACING["xs"]}px;
        }}
        
        QComboBox::down-arrow {{
            image: url(resources/icons/chevron-down.svg);
            width: 12px;
            height: 12px;
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
            border: 1px solid {COLORS["border"]["default"]};
            border-radius: {BORDER_RADIUS["md"]}px;
            padding: {SPACING["lg"]}px;
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
            background: {GRADIENTS["button"]["primary"]};
            border-radius: {BORDER_RADIUS["xs"]}px;
        }}
        
        /* Tables */
        QTableView {{
            background: {COLORS["background"]["secondary"]};
            border: 1px solid {COLORS["border"]["default"]};
        }}
        
        QTableView::item {{
            padding: {SPACING["xs"]}px;
        }}
        
        QTableView::item:selected {{
            background: {COLORS["state"]["selected"]};
        }}
        
        QHeaderView::section {{
            background: {COLORS["background"]["tertiary"]};
            color: {COLORS["text"]["secondary"]};
            padding: {SPACING["sm"]}px;
            border: none;
            border-right: 1px solid {COLORS["border"]["default"]};
            border-bottom: 1px solid {COLORS["border"]["default"]};
        }}
        
        /* Trees y Listas */
        QTreeView, QListView {{
            background: {COLORS["background"]["secondary"]};
            border: 1px solid {COLORS["border"]["default"]};
        }}
        
        QTreeView::item, QListView::item {{
            padding: {SPACING["xs"]}px;
        }}
        
        QTreeView::item:selected, QListView::item:selected {{
            background: {COLORS["state"]["selected"]};
        }}
        
        QTreeView::branch {{
            background: transparent;
        }}
        
        /* Tooltips */
        QToolTip {{
            background: {COLORS["background"]["elevated"]};
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
