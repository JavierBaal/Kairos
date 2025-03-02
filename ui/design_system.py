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
    "tooltip": "0 2px 4px rgba(0, 0, 0, 0.2)",
    "dropdown": "0 4px 8px rgba(0, 0, 0, 0.25)",
    "card": "0 1px 3px rgba(0, 0, 0, 0.2)",
    "modal": "0 8px 16px rgba(0, 0, 0, 0.35)",
    "elevated": "0 2px 6px rgba(0, 0, 0, 0.3)",
}

# Colores - Estilo JetBrains Mejorado
COLORS = {
    # Fondos principales
    "background": {
        "primary": "#1e1f22",     # Fondo principal más oscuro y rico
        "secondary": "#2b2d30",    # Paneles y áreas de contenido
        "tertiary": "#333639",     # Barras de herramientas y headers
        "elevated": "#393b40",     # Elementos elevados
    },
    
    # Texto
    "text": {
        "primary": "#dfe1e5",      # Texto principal más suave
        "secondary": "#9da0a8",    # Texto secundario más vibrante
        "disabled": "#6f737a",     # Texto deshabilitado
        "hint": "#787a80",         # Texto de ayuda/placeholder
    },
    
    # Acentos Vibrantes
    "accent": {
        "primary": "#4dabf7",      # Azul brillante (como IntelliJ)
        "purple": "#b392f0",       # Púrpura vibrante
        "green": "#85e89d",        # Verde menta
        "coral": "#ff7b72",        # Coral vibrante
        "yellow": "#ffdf5d",       # Amarillo brillante
        "orange": "#ffa657",       # Naranja cálido
    },
    
    # Estados
    "state": {
        "hover": "#383b3f",        # Fondo hover más suave
        "selected": "#2f3237",     # Selección más sutil
        "pressed": "#26282c",      # Estado presionado
        "focused": "#2979ff",      # Borde focus más brillante
    },
    
    # Bordes
    "border": {
        "default": "#3b3e43",      # Bordes más visibles
        "light": "#43474d",        # Bordes claros
        "focus": "#2979ff",        # Borde de focus
        "separator": "#35383c",    # Separadores sutiles
    },
    
    # Feedback
    "feedback": {
        "success": "#4caf50",      # Verde éxito
        "error": "#ff5370",        # Rojo error
        "warning": "#ffcb6b",      # Amarillo advertencia
        "info": "#82aaff",         # Azul información
    },
}

# Gradientes Refinados
GRADIENTS = {
    # Botones
    "button": {
        "primary": "qlineargradient(x1:0, y1:0, x2:0, y2:1, stop:0 #4dabf7, stop:1 #2979ff)",
        "secondary": "qlineargradient(x1:0, y1:0, x2:0, y2:1, stop:0 #454649, stop:1 #3a3b3f)",
        "success": "qlineargradient(x1:0, y1:0, x2:0, y2:1, stop:0 #5cb860, stop:1 #4caf50)",
    },
    
    # Fondos
    "background": {
        "app": "qlineargradient(x1:0, y1:0, x2:1, y2:1, stop:0 #1e1f22, stop:1 #252629)",
        "header": "qlineargradient(x1:0, y1:0, x2:0, y2:1, stop:0 #383b3f, stop:1 #2b2d30)",
        "toolbar": "qlineargradient(x1:0, y1:0, x2:0, y2:1, stop:0 #333639, stop:1 #2b2d30)",
    },
    
    # Acentos
    "accent": {
        "blue": "qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 #4dabf7, stop:1 #2979ff)",
        "purple": "qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 #b392f0, stop:1 #9277d9)",
        "success": "qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 #85e89d, stop:1 #4caf50)",
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

# Layout
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
            border-radius: {BORDER_RADIUS["md"]}px;
            padding: {COMPONENT_DIMENSIONS["button"]["padding"]["md"]};
            font-family: {FONT_FAMILY};
            font-size: {FONT_SIZE["md"]}px;
            font-weight: {FONT_WEIGHT["medium"]};
            height: {COMPONENT_DIMENSIONS["button"]["height"]["md"]}px;
            box-shadow: {SHADOWS["card"]};
        """,
        "secondary": f"""
            background: {GRADIENTS["button"]["secondary"]};
            color: {COLORS["text"]["primary"]};
            border: 1px solid {COLORS["border"]["default"]};
            border-radius: {BORDER_RADIUS["md"]}px;
            padding: {COMPONENT_DIMENSIONS["button"]["padding"]["md"]};
            font-family: {FONT_FAMILY};
            font-size: {FONT_SIZE["md"]}px;
            font-weight: {FONT_WEIGHT["medium"]};
            height: {COMPONENT_DIMENSIONS["button"]["height"]["md"]}px;
            box-shadow: {SHADOWS["card"]};
        """,
        "success": f"""
            background: {GRADIENTS["button"]["success"]};
            color: {COLORS["text"]["primary"]};
            border: 1px solid {COLORS["border"]["default"]};
            border-radius: {BORDER_RADIUS["md"]}px;
            padding: {COMPONENT_DIMENSIONS["button"]["padding"]["md"]};
            font-family: {FONT_FAMILY};
            font-size: {FONT_SIZE["md"]}px;
            font-weight: {FONT_WEIGHT["medium"]};
            height: {COMPONENT_DIMENSIONS["button"]["height"]["md"]}px;
            box-shadow: {SHADOWS["card"]};
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
            box-shadow: {SHADOWS["elevated"]};
        """,
        "hover": f"""
            border: 1px solid {COLORS["border"]["light"]};
            background: {COLORS["background"]["elevated"]};
        """,
    },
    
    # Paneles y tarjetas
    "panel": {
        "default": f"""
            background: {COLORS["background"]["secondary"]};
            border: 1px solid {COLORS["border"]["default"]};
            border-radius: {BORDER_RADIUS["lg"]}px;
            padding: {SPACING["md"]}px;
            box-shadow: {SHADOWS["card"]};
        """,
        "elevated": f"""
            background: {COLORS["background"]["elevated"]};
            border: 1px solid {COLORS["border"]["light"]};
            border-radius: {BORDER_RADIUS["lg"]}px;
            padding: {SPACING["md"]}px;
            box-shadow: {SHADOWS["elevated"]};
        """,
    },
    
    # Barras de herramientas
    "toolbar": {
        "default": f"""
            background: {GRADIENTS["background"]["toolbar"]};
            border-bottom: 1px solid {COLORS["border"]["default"]};
            min-height: {GOLDEN_LAYOUT["toolbar_height"]}px;
            padding: 0 {SPACING["sm"]}px;
            box-shadow: {SHADOWS["card"]};
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
            box-shadow: {SHADOWS["card"]};
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
    
    # Pestañas
    "tab": {
        "default": f"""
            background: transparent;
            color: {COLORS["text"]["secondary"]};
            border: none;
            padding: {SPACING["sm"]}px {SPACING["md"]}px;
            font-size: {FONT_SIZE["md"]}px;
            border-bottom: 2px solid transparent;
        """,
        "selected": f"""
            color: {COLORS["text"]["primary"]};
            background: {COLORS["background"]["elevated"]};
            border-bottom: 2px solid {COLORS["accent"]["primary"]};
        """,
        "hover": f"""
            background: {COLORS["state"]["hover"]};
            color: {COLORS["text"]["primary"]};
        """,
    },
    
    # Menús
    "menu": {
        "default": f"""
            background: {COLORS["background"]["elevated"]};
            border: 1px solid {COLORS["border"]["default"]};
            border-radius: {BORDER_RADIUS["md"]}px;
            padding: {SPACING["xs"]}px 0;
            box-shadow: {SHADOWS["dropdown"]};
        """,
        "item": f"""
            padding: {SPACING["xs"]}px {SPACING["md"]}px;
            color: {COLORS["text"]["primary"]};
            font-size: {FONT_SIZE["md"]}px;
        """,
        "item_selected": f"""
            background: {COLORS["state"]["selected"]};
            color: {COLORS["text"]["primary"]};
        """,
    },
}
