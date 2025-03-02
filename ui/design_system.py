# Sistema de diseño inspirado en JetBrains IDEs
from math import sqrt

# Constantes base
GOLDEN_RATIO = (1 + sqrt(5)) / 2  # ≈ 1.618
GRID_BASE = 8

# Espaciado
SPACING = {
    "xxs": GRID_BASE / 2,  # 4px
    "xs": GRID_BASE,       # 8px
    "sm": GRID_BASE * 2,   # 16px
    "md": GRID_BASE * 3,   # 24px
    "lg": GRID_BASE * 4,   # 32px
    "xl": GRID_BASE * 6,   # 48px
    "xxl": GRID_BASE * 8,  # 64px
}

# Tipografía
FONT_FAMILY = "Segoe UI, -apple-system, system-ui, sans-serif"

FONT_SIZE = {
    "xs": 12,
    "sm": 13,
    "md": 14,
    "lg": 16,
    "xl": 20,
    "xxl": 24,
    "xxxl": 32,
}

FONT_WEIGHT = {
    "regular": 400,
    "medium": 500,
    "semibold": 600,
    "bold": 700,
}

LINE_HEIGHT = {
    "tight": 1.2,
    "normal": 1.5,
    "relaxed": 1.65,
}

# Bordes y Radios
BORDER_RADIUS = {
    "xs": 3,
    "sm": 4,
    "md": 6,
    "lg": 8,
    "xl": 12,
    "rounded": 999,
}

BORDER_WIDTH = {
    "none": 0,
    "thin": 1,
    "normal": 2,
    "thick": 3,
}

# Sombras
SHADOWS = {
    "tooltip": "0 2px 4px rgba(0, 0, 0, 0.1)",
    "dropdown": "0 4px 8px rgba(0, 0, 0, 0.15)",
    "card": "0 1px 3px rgba(0, 0, 0, 0.12)",
    "modal": "0 8px 16px rgba(0, 0, 0, 0.25)",
}

# Colores - Estilo JetBrains
COLORS = {
    # Fondos principales
    "background": {
        "primary": "#2b2b2b",    # Fondo principal oscuro
        "secondary": "#323232",   # Paneles y áreas de contenido
        "tertiary": "#3c3f41",   # Barras de herramientas y headers
        "elevated": "#404040",    # Elementos elevados
    },
    
    # Texto
    "text": {
        "primary": "#ffffff",     # Texto principal sobre oscuro
        "secondary": "#a7a7a7",   # Texto secundario sobre oscuro
        "disabled": "#777777",    # Texto deshabilitado
        "hint": "#666666",        # Texto de ayuda/placeholder
    },
    
    # Acentos
    "accent": {
        "primary": "#3592c4",     # Azul principal (como en IntelliJ)
        "success": "#499c54",     # Verde para éxito
        "warning": "#be9117",     # Amarillo para advertencias
        "error": "#c75450",       # Rojo para errores
        "purple": "#9876aa",      # Púrpura para keywords
        "orange": "#cc7832",      # Naranja para strings
    },
    
    # Bordes
    "border": {
        "default": "#323232",     # Bordes por defecto
        "active": "#4c708c",      # Bordes cuando activo
        "hover": "#2f65ca",       # Bordes en hover
        "separator": "#2d2d2d",   # Líneas separadoras
    },
    
    # Estados
    "state": {
        "selected": "#2d2f32",    # Fondo seleccionado
        "hover": "#353739",       # Fondo en hover
        "pressed": "#2b2d2f",     # Fondo presionado
        "focused": "#103366",     # Borde enfocado
    },
}

# Gradientes
GRADIENTS = {
    # Botones
    "button": {
        "primary": "qlineargradient(x1:0, y1:0, x2:0, y2:1, stop:0 #365880, stop:1 #2c4b69)",
        "secondary": "qlineargradient(x1:0, y1:0, x2:0, y2:1, stop:0 #4e5157, stop:1 #393b40)",
        "success": "qlineargradient(x1:0, y1:0, x2:0, y2:1, stop:0 #499c54, stop:1 #3d8047)",
    },
    
    # Fondos
    "background": {
        "toolbar": "qlineargradient(x1:0, y1:0, x2:0, y2:1, stop:0 #3c3f41, stop:1 #323232)",
        "header": "qlineargradient(x1:0, y1:0, x2:0, y2:1, stop:0 #365880, stop:1 #2c4b69)",
    },
}

# Dimensiones de Componentes
COMPONENT_DIMENSIONS = {
    "button": {
        "height": {
            "sm": GRID_BASE * 3,    # 24px
            "md": GRID_BASE * 4,    # 32px
            "lg": GRID_BASE * 5,    # 40px
        },
        "padding": {
            "sm": f"{SPACING['xs']}px {SPACING['sm']}px",  # 8px 16px
            "md": f"{SPACING['sm']}px {SPACING['md']}px",  # 16px 24px
            "lg": f"{SPACING['md']}px {SPACING['lg']}px",  # 24px 32px
        },
    },
    
    "input": {
        "height": GRID_BASE * 4,     # 32px
        "padding": SPACING["sm"],    # 16px
    },
    
    "icon": {
        "sm": GRID_BASE * 2,         # 16px
        "md": GRID_BASE * 3,         # 24px
        "lg": GRID_BASE * 4,         # 32px
    },
}

# Layout Basado en Proporción Áurea
GOLDEN_LAYOUT = {
    "main_content": 1 / GOLDEN_RATIO,        # ~0.618 (61.8%)
    "sidebar": 1 - (1 / GOLDEN_RATIO),       # ~0.382 (38.2%)
    "header_height": GRID_BASE * 7,          # 56px
    "toolbar_height": GRID_BASE * 5,         # 40px
    "status_bar_height": GRID_BASE * 3,      # 24px
}

# Estilos de Componentes
COMPONENT_STYLES = {
    # Botones
    "button": {
        "primary": f"""
            background: {GRADIENTS["button"]["primary"]};
            color: {COLORS["text"]["primary"]};
            border: 1px solid {COLORS["border"]["default"]};
            border-radius: {BORDER_RADIUS["sm"]}px;
            padding: {COMPONENT_DIMENSIONS["button"]["padding"]["md"]};
            font-family: {FONT_FAMILY};
            font-size: {FONT_SIZE["md"]}px;
            font-weight: {FONT_WEIGHT["medium"]};
            height: {COMPONENT_DIMENSIONS["button"]["height"]["md"]}px;
        """,
        "secondary": f"""
            background: {GRADIENTS["button"]["secondary"]};
            color: {COLORS["text"]["primary"]};
            border: 1px solid {COLORS["border"]["default"]};
            border-radius: {BORDER_RADIUS["sm"]}px;
            padding: {COMPONENT_DIMENSIONS["button"]["padding"]["md"]};
            font-family: {FONT_FAMILY};
            font-size: {FONT_SIZE["md"]}px;
            font-weight: {FONT_WEIGHT["medium"]};
            height: {COMPONENT_DIMENSIONS["button"]["height"]["md"]}px;
        """,
        "success": f"""
            background: {GRADIENTS["button"]["success"]};
            color: {COLORS["text"]["primary"]};
            border: 1px solid {COLORS["border"]["default"]};
            border-radius: {BORDER_RADIUS["sm"]}px;
            padding: {COMPONENT_DIMENSIONS["button"]["padding"]["md"]};
            font-family: {FONT_FAMILY};
            font-size: {FONT_SIZE["md"]}px;
            font-weight: {FONT_WEIGHT["medium"]};
            height: {COMPONENT_DIMENSIONS["button"]["height"]["md"]}px;
        """,
    },
    
    # Campos de entrada
    "input": {
        "default": f"""
            background: {COLORS["background"]["secondary"]};
            color: {COLORS["text"]["primary"]};
            border: 1px solid {COLORS["border"]["default"]};
            border-radius: {BORDER_RADIUS["sm"]}px;
            padding: {SPACING["sm"]}px;
            font-family: {FONT_FAMILY};
            font-size: {FONT_SIZE["md"]}px;
            height: {COMPONENT_DIMENSIONS["input"]["height"]}px;
        """,
        "focused": f"""
            border: 1px solid {COLORS["accent"]["primary"]};
            background: {COLORS["background"]["elevated"]};
        """,
    },
    
    # Paneles y tarjetas
    "panel": {
        "default": f"""
            background: {COLORS["background"]["secondary"]};
            border: 1px solid {COLORS["border"]["default"]};
            border-radius: {BORDER_RADIUS["md"]}px;
            padding: {SPACING["md"]}px;
        """,
    },
    
    # Barras de herramientas
    "toolbar": {
        "default": f"""
            background: {GRADIENTS["background"]["toolbar"]};
            border-bottom: 1px solid {COLORS["border"]["default"]};
            min-height: {GOLDEN_LAYOUT["toolbar_height"]}px;
            padding: 0 {SPACING["sm"]}px;
        """,
    },
    
    # Encabezados
    "header": {
        "default": f"""
            background: {GRADIENTS["background"]["header"]};
            color: {COLORS["text"]["primary"]};
            padding: {SPACING["md"]}px;
            font-size: {FONT_SIZE["lg"]}px;
            font-weight: {FONT_WEIGHT["semibold"]};
            min-height: {GOLDEN_LAYOUT["header_height"]}px;
        """,
    },
    
    # Barra de estado
    "statusbar": {
        "default": f"""
            background: {COLORS["background"]["tertiary"]};
            color: {COLORS["text"]["secondary"]};
            border-top: 1px solid {COLORS["border"]["default"]};
            min-height: {GOLDEN_LAYOUT["status_bar_height"]}px;
            padding: 0 {SPACING["sm"]}px;
            font-size: {FONT_SIZE["sm"]}px;
        """,
    },
    
    # Menús y desplegables
    "menu": {
        "default": f"""
            background: {COLORS["background"]["secondary"]};
            border: 1px solid {COLORS["border"]["default"]};
            border-radius: {BORDER_RADIUS["sm"]}px;
            padding: {SPACING["xs"]}px 0;
        """,
        "item": f"""
            padding: {SPACING["xs"]}px {SPACING["md"]}px;
            color: {COLORS["text"]["primary"]};
            font-size: {FONT_SIZE["md"]}px;
        """,
    },
    
    # Pestañas
    "tab": {
        "default": f"""
            background: transparent;
            color: {COLORS["text"]["secondary"]};
            border: none;
            padding: {SPACING["sm"]}px {SPACING["md"]}px;
            font-size: {FONT_SIZE["md"]}px;
        """,
        "selected": f"""
            background: {COLORS["state"]["selected"]};
            color: {COLORS["text"]["primary"]};
            border-bottom: 2px solid {COLORS["accent"]["primary"]};
        """,
    },
}
