# Sistema de Diseño de Kairos

## Introducción

El Sistema de Diseño de Kairos es una biblioteca de componentes, estilos y patrones que proporciona una experiencia visual coherente y ergonómica para la aplicación. Basado en principios de ergonomía cognitiva y utilizando la proporción áurea (1.618) como base para layouts y espaciados, este sistema garantiza una interfaz intuitiva, profesional y visualmente atractiva.

## Principios de Diseño

### 1. Ergonomía Cognitiva

El diseño prioriza la facilidad de uso y la claridad visual, reduciendo la carga cognitiva del usuario mediante:

- Contraste adecuado entre texto y fondo (ratio mínimo 4.5:1)
- Jerarquía visual clara con tamaños de texto normalizados
- Espaciado consistente basado en un grid de 8px
- Elementos interactivos claramente identificables

### 2. Proporción Áurea

La proporción áurea (1.618) se utiliza como base para:

- División de layouts (61.8% / 38.2%)
- Relaciones de tamaño entre elementos
- Espaciados y márgenes
- Proporciones de componentes

### 3. Consistencia Visual

El sistema mantiene consistencia a través de:

- Paleta de colores unificada
- Sistema tipográfico coherente
- Componentes reutilizables con comportamientos predecibles
- Patrones de interacción estandarizados

## Estructura del Sistema

El sistema de diseño se implementa en dos archivos principales:

1. `ui/design_system.py`: Define constantes, proporciones y estilos base
2. `ui/theme.py`: Implementa el sistema en la aplicación mediante QPalette y hojas de estilo

### Componentes Principales

#### Grid Base

```python
GRID_BASE = 8  # Unidad base en píxeles
```

Todo el espaciado y dimensiones se basan en múltiplos de esta unidad para mantener consistencia visual.

#### Espaciados

```python
SPACING = {
    "xxs": GRID_BASE / 2,  # 4px
    "xs": GRID_BASE,       # 8px
    "sm": GRID_BASE * 2,   # 16px
    "md": GRID_BASE * 3,   # 24px
    "lg": GRID_BASE * 4,   # 32px
    "xl": GRID_BASE * 6,   # 48px
    "xxl": GRID_BASE * 8,  # 64px
}
```

#### Radios de Borde

```python
BORDER_RADIUS = {
    "xs": 4,
    "sm": 6,
    "md": 8,
    "lg": 12,
    "xl": 16,
    "pill": 999,  # Para botones tipo "pill"
    "circle": 999,  # Para elementos circulares
}
```

#### Tipografía

```python
FONT_SIZE = {
    "xs": 12,
    "sm": 14,
    "md": 16,
    "lg": 20,
    "xl": 24,
    "xxl": 32,
    "xxxl": 48,
}

FONT_WEIGHT = {
    "regular": 400,
    "medium": 500,
    "semibold": 600,
    "bold": 700,
}
```

#### Paleta de Colores

La paleta utiliza un enfoque de tema mixto con fondos oscuros y áreas de contenido claras:

```python
COLORS = {
    # Colores Base
    "background": {
        "primary": "#16162e",     # Fondo principal (oscuro)
        "secondary": "#f9f9f9",   # Fondo secundario (claro)
        "tertiary": "#1e1e38",    # Fondo terciario (oscuro alternativo)
        "accent": "#f5f5f7",      # Fondo de acento (muy claro)
    },
    
    # Texto
    "text": {
        "primary": "#202020",     # Texto principal sobre fondos claros
        "secondary": "#5a5a68",   # Texto secundario sobre fondos claros
        "on_dark": "#ffffff",     # Texto principal sobre fondos oscuros
        "on_dark_secondary": "#d0d0d8",  # Texto secundario sobre fondos oscuros
    },
    
    # Colores de Acento
    "accent": {
        "purple": "#6a3de8",      # Acento principal
        "blue": "#3d8aff",        # Acento secundario
        "coral": "#ff5a5f",       # Acento terciario
        "orange": "#ff8f59",      # Acento cuaternario
        "teal": "#00c2a8",        # Acento quinario
        "green": "#5aaa4f",       # Acento para éxito
    },
    
    # Estados
    "state": {
        "success": "#5aaa4f",     # Éxito
        "error": "#ff3b5b",       # Error
        "warning": "#ffbd3d",     # Advertencia
        "info": "#3d8aff",        # Información
    },
}
```

#### Gradientes

```python
GRADIENTS = {
    # Botones
    "button": {
        "primary": "qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 #6a3de8, stop:1 #3d8aff)",
        "secondary": "qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 #ff5a5f, stop:1 #ff8f59)",
        "tertiary": "qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 #00c2a8, stop:1 #5aaa4f)",
    },
    
    # Fondos
    "background": {
        "app": "qlineargradient(x1:0, y1:0, x2:1, y2:1, stop:0 #16162e, stop:1 #1e1e38)",
        "panel_light": "qlineargradient(x1:0, y1:0, x2:0, y2:1, stop:0 #ffffff, stop:1 #f5f5f5)",
        "panel_dark": "qlineargradient(x1:0, y1:0, x2:0, y2:1, stop:0 #1e1e38, stop:1 #16162e)",
    },
}
```

#### Proporciones Áureas para Layouts

```python
GOLDEN_LAYOUT = {
    "main_content": 1 / GOLDEN_RATIO,  # ~0.618 (61.8%)
    "sidebar": 1 - (1 / GOLDEN_RATIO),  # ~0.382 (38.2%)
    "header_height": GRID_BASE * 8,  # 64px
    "footer_height": GRID_BASE * 6,  # 48px
}
```

## Componentes UI

### Botones

El sistema define varios estilos de botones:

1. **Primario**: Gradiente púrpura-azul para acciones principales
2. **Secundario**: Gradiente coral-naranja para acciones secundarias
3. **Terciario**: Gradiente teal-verde para acciones terciarias
4. **Texto**: Sin fondo, solo texto en color de acento
5. **Outline**: Borde en color de acento sin fondo

```python
COMPONENT_STYLES = {
    "button": {
        "primary": f"""
            background: {GRADIENTS["button"]["primary"]};
            color: {COLORS["text"]["on_dark"]};
            border: none;
            border-radius: {BORDER_RADIUS["md"]}px;
            padding: {COMPONENT_DIMENSIONS["button"]["padding"]["md"]};
            font-weight: {FONT_WEIGHT["bold"]};
            font-size: {FONT_SIZE["md"]}px;
            height: {COMPONENT_DIMENSIONS["button"]["height"]["md"]}px;
        """,
        # Otros estilos...
    },
}
```

### Tarjetas

Dos estilos principales de tarjetas:

1. **Light**: Fondo claro con texto oscuro
2. **Dark**: Fondo oscuro con texto claro

```python
COMPONENT_STYLES = {
    "card": {
        "light": f"""
            background-color: {COLORS["surface"]["light"]};
            border: 1px solid {COLORS["border"]["light"]};
            border-radius: {BORDER_RADIUS["lg"]}px;
            padding: {COMPONENT_DIMENSIONS["card"]["padding"]}px;
        """,
        "dark": f"""
            background-color: {COLORS["surface"]["dark"]};
            border: 1px solid {COLORS["border"]["dark"]};
            border-radius: {BORDER_RADIUS["lg"]}px;
            padding: {COMPONENT_DIMENSIONS["card"]["padding"]}px;
            color: {COLORS["text"]["on_dark"]};
        """,
    },
}
```

### Barras de Progreso

Barras de progreso delgadas (4px) para mejor contraste visual:

```python
COMPONENT_STYLES = {
    "progress_bar": {
        "default": f"""
            border: none;
            border-radius: {BORDER_RADIUS["xs"]}px;
            background-color: rgba(255, 255, 255, 0.1);
            height: {COMPONENT_DIMENSIONS["progress_bar"]["height"]["sm"]}px;
            text-align: center;
        """,
        "chunk": f"""
            background: {GRADIENTS["accent"]["coral_orange"]};
            border-radius: {BORDER_RADIUS["xs"]}px;
        """,
    },
}
```

## Implementación

### Uso en Componentes

Para utilizar el sistema de diseño en componentes PyQt:

```python
from ui.theme import Theme
from ui.design_system import COLORS, SPACING, BORDER_RADIUS

# Aplicar tema a la aplicación
app.setPalette(Theme.get_palette())
app.setStyleSheet(Theme.get_stylesheet())

# Usar constantes en componentes específicos
my_label.setStyleSheet(f"""
    color: {COLORS["accent"]["purple"]};
    font-size: {FONT_SIZE["lg"]}px;
    margin: {SPACING["md"]}px;
""")
```

### Extensión del Sistema

Para añadir nuevos componentes o estilos:

1. Definir constantes en `ui/design_system.py`
2. Implementar estilos en `ui/theme.py`
3. Documentar en este archivo

## Mejores Prácticas

1. **Consistencia**: Usar siempre constantes del sistema de diseño en lugar de valores hardcodeados
2. **Extensibilidad**: Añadir nuevos componentes siguiendo los patrones existentes
3. **Documentación**: Documentar nuevos componentes o modificaciones
4. **Accesibilidad**: Mantener ratios de contraste adecuados para texto
5. **Responsividad**: Diseñar componentes que se adapten a diferentes tamaños de pantalla

## Ejemplos Visuales

### Botones

- **Primario**: Gradiente púrpura-azul, texto blanco
- **Secundario**: Gradiente coral-naranja, texto blanco
- **Terciario**: Gradiente teal-verde, texto blanco

### Tarjetas

- **Light**: Fondo blanco, borde gris claro, texto oscuro
- **Dark**: Fondo azul oscuro, borde azul medio, texto blanco

### Indicadores de Paso

- **Activo**: Círculo con gradiente púrpura-azul, número blanco
- **Inactivo**: Círculo gris semitransparente, número blanco

## Conclusión

El Sistema de Diseño de Kairos proporciona una base sólida para crear una interfaz de usuario coherente, profesional y ergonómica. Al seguir estos principios y utilizar los componentes definidos, se garantiza una experiencia de usuario consistente y de alta calidad en toda la aplicación.
