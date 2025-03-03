# Sistema de diseño inspirado en el diseño moderno de Kairos
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

# Tipografía - Usando Inter
FONT_FAMILY = "Inter, -apple-system, system-ui, sans-serif"

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
    "light": 300,
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
    "xs": 4,
    "sm": 6,
    "md": 8,
    "lg": 12,
    "xl": 16,
    "full": 9999,
}

# Sistema de colores HSL refinado (basado en el diseño de referencia)
COLORS = {
    # Fondos (basados en --background, --card, etc.)
    "background": {
        "primary": "hsl(230, 20%, 13%)",     # --background
        "card": "hsla(230, 30%, 17%, 0.8)",  # --card
        "secondary": "hsl(236, 20%, 25%)",    # --secondary
        "muted": "hsl(224, 25%, 23%)",       # --muted
        "elevated": "hsl(230, 30%, 17%)",     # --popover
    },
    
    # Texto (basado en --foreground y variantes)
    "text": {
        "primary": "hsl(210, 40%, 98%)",     # --foreground
        "secondary": "hsl(215, 20%, 70%)",    # --muted-foreground
        "muted": "hsl(215, 20%, 65%)",       # Versión más clara de muted
    },
    
    # Acentos y Estados (basados en --primary, --accent, etc.)
    "accent": {
        "primary": "hsl(204, 100%, 63%)",    # --primary
        "orange": "hsl(24, 94%, 53%)",       # --orange
        "red": "hsl(352, 86%, 57%)",         # --red
        "success": "hsl(174, 75%, 53%)",     # --accent
    },
    
    # Bordes (basados en --border y variantes)
    "border": {
        "default": "hsl(230, 15%, 20%)",     # --border
        "secondary": "hsla(230, 20%, 22%)",   # --sidebar-border
        "hover": "hsl(230, 15%, 25%)",       # Versión más clara para hover
        "primary": "hsla(204, 100%, 63%, 0.3)", # --primary con transparencia
        "orange": "hsla(24, 94%, 53%, 0.3)",   # --orange con transparencia
        "red": "hsla(352, 86%, 57%, 0.3)",     # --red con transparencia
    },
}

# Sombras refinadas
SHADOWS = {
    "sm": "0 2px 4px rgba(0, 0, 0, 0.1)",
    "md": "0 5px 15px rgba(0, 0, 0, 0.2)",
    "lg": "0 5px 30px rgba(0, 0, 0, 0.2)",
    "primary": "0 0 15px rgba(56, 182, 255, 0.5)",    # Shadow del step-indicator-active
    "orange": "0 5px 15px rgba(249, 115, 22, 0.3)",   # Shadow del button-orange
    "red": "0 5px 15px rgba(234, 56, 76, 0.3)",      # Shadow del button-red
}

# Transiciones
TRANSITIONS = {
    "fast": "150ms",
    "normal": "300ms",
    "slow": "500ms",
}

# Estilos de Componentes
COMPONENT_STYLES = {
    # Glass Panel (basado en .glass-panel)
    "panel": {
        "default": f"""
            background-color: {COLORS["background"]["card"]};
            backdrop-filter: blur(8px);
            border: 1px solid hsla(236, 20%, 25%, 0.3);
            border-radius: {BORDER_RADIUS["xl"]}px;
            box-shadow: {SHADOWS["lg"]};
        """,
    },
    
    # Botones (basados en .button-* clases)
    "button": {
        "primary": f"""
            background-color: {COLORS["accent"]["primary"]};
            color: {COLORS["background"]["primary"]};
            padding: 10px 20px;
            border-radius: {BORDER_RADIUS["lg"]}px;
            font-weight: {FONT_WEIGHT["medium"]};
            box-shadow: {SHADOWS["primary"]};
            transition: all {TRANSITIONS["normal"]};
        """,
        "orange": f"""
            background-color: {COLORS["accent"]["orange"]};
            color: {COLORS["background"]["primary"]};
            padding: 10px 20px;
            border-radius: {BORDER_RADIUS["lg"]}px;
            font-weight: {FONT_WEIGHT["medium"]};
            box-shadow: {SHADOWS["orange"]};
            transition: all {TRANSITIONS["normal"]};
        """,
        "red": f"""
            background-color: {COLORS["accent"]["red"]};
            color: {COLORS["text"]["primary"]};
            padding: 10px 20px;
            border-radius: {BORDER_RADIUS["lg"]}px;
            font-weight: {FONT_WEIGHT["medium"]};
            box-shadow: {SHADOWS["red"]};
            transition: all {TRANSITIONS["normal"]};
        """,
    },
    
    # Tarjetas de Agente (basadas en .agent-card-*)
    "agent_card": {
        "default": f"""
            {COMPONENT_STYLES["panel"]["default"]}
            padding: {SPACING["lg"]}px;
            transition: all {TRANSITIONS["normal"]};
        """,
        "orange": f"""
            {COMPONENT_STYLES["panel"]["default"]}
            padding: {SPACING["lg"]}px;
            border-color: {COLORS["border"]["orange"]};
            transition: all {TRANSITIONS["normal"]};
        """,
        "red": f"""
            {COMPONENT_STYLES["panel"]["default"]}
            padding: {SPACING["lg"]}px;
            border-color: {COLORS["border"]["red"]};
            transition: all {TRANSITIONS["normal"]};
        """,
    },
    
    # Indicadores de Paso (basados en .step-indicator-*)
    "step": {
        "default": f"""
            width: 48px;
            height: 48px;
            border: 2px solid {COLORS["border"]["default"]};
            border-radius: {BORDER_RADIUS["full"]}px;
            color: {COLORS["text"]["secondary"]};
            font-weight: {FONT_WEIGHT["semibold"]};
            transition: all {TRANSITIONS["normal"]};
        """,
        "active": f"""
            border-color: {COLORS["accent"]["primary"]};
            background-color: {COLORS["accent"]["primary"]};
            color: {COLORS["background"]["primary"]};
            box-shadow: {SHADOWS["primary"]};
        """,
        "completed": f"""
            border-color: {COLORS["accent"]["primary"]};
            background-color: {COLORS["accent"]["primary"]}20;
            color: {COLORS["accent"]["primary"]};
        """,
    },
    
    # Campo de entrada (basado en .input-field)
    "input": {
        "default": f"""
            background-color: {COLORS["background"]["muted"]}80;
            border: 1px solid {COLORS["border"]["default"]};
            border-radius: {BORDER_RADIUS["lg"]}px;
            padding: {SPACING["sm"]}px {SPACING["md"]}px;
            color: {COLORS["text"]["primary"]};
            transition: all {TRANSITIONS["fast"]};
        """,
        "focus": f"""
            border-color: {COLORS["accent"]["primary"]};
            box-shadow: 0 0 0 2px {COLORS["accent"]["primary"]}40;
            outline: none;
        """,
    },
}
