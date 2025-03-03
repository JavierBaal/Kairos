# Sistema de Diseño Kairos

## Fundamentos

### Grid y Espaciado
El sistema utiliza una base de 8px (GRID_BASE) para mantener consistencia en todo el diseño:
- xxs: 4px (GRID_BASE / 2)
- xs: 8px (GRID_BASE)
- sm: 16px (GRID_BASE * 2)
- md: 24px (GRID_BASE * 3)
- lg: 32px (GRID_BASE * 4)
- xl: 48px (GRID_BASE * 6)
- xxl: 64px (GRID_BASE * 8)

### Tipografía
Fuente principal: Inter
```
FONT_SIZE = {
    "xs": 12px,
    "sm": 13px,
    "md": 14px,
    "lg": 16px,
    "xl": 20px,
    "xxl": 24px,
    "xxxl": 32px,
}

FONT_WEIGHT = {
    "light": 300,
    "regular": 400,
    "medium": 500,
    "semibold": 600,
    "bold": 700,
}
```

### Colores
Sistema de colores en HSL para mejor control:

#### Fondos
- Primary: hsl(222, 20%, 9%) - Fondo principal oscuro
- Secondary: hsl(223, 16%, 16%) - Paneles y contenido
- Tertiary: hsl(223, 14%, 20%) - Barras y elementos terciarios
- Elevated: hsla(223, 16%, 22%, 0.8) - Elementos elevados con transparencia

#### Texto
- Primary: hsl(220, 40%, 98%) - Texto principal nítido
- Secondary: hsl(220, 15%, 70%) - Texto secundario suave
- Muted: hsl(220, 10%, 55%) - Texto apagado

#### Acentos
- Primary: hsl(204, 100%, 63%) - Azul brillante
- Orange: hsl(20, 90%, 60%) - Naranja vibrante
- Red: hsl(355, 90%, 65%) - Rojo suave
- Success: hsl(145, 80%, 45%) - Verde éxito

### Efectos

#### Sombras
```
SHADOWS = {
    "sm": "0 2px 4px rgba(0, 0, 0, 0.1)",
    "md": "0 5px 15px rgba(0, 0, 0, 0.2)",
    "lg": "0 5px 30px rgba(0, 0, 0, 0.2)",
    "primary": "0 5px 15px rgba(56, 182, 255, 0.3)",
    "primary-hover": "0 5px 20px rgba(56, 182, 255, 0.5)"
}
```

#### Transiciones
```
TRANSITIONS = {
    "fast": "150ms",
    "normal": "300ms",
    "slow": "500ms"
}
```

## Componentes

### Botones
Tres variantes principales con estados:
1. Primary (Azul)
2. Orange
3. Red

Características:
- Altura: 40px
- Padding: 20px horizontal
- Bordes redondeados: 6px
- Sombras con resplandor según variante
- Transición suave en hover

### Tarjetas
Efecto glass con:
- Fondo semi-transparente
- Borde sutil
- Blur backdrop
- Transición en hover
- Sombra elevada en hover

### Inputs
- Altura: 40px
- Padding: 16px
- Borde redondeado: 6px
- Estado focus con resplandor del color primario
- Transición suave

### Progress Bar
- Altura: 4px
- Bordes completamente redondeados
- Transición suave del progreso
- Color primario para la barra de progreso

## Diseño Responsivo

Todos los componentes utilizan medidas relativas:
- Espaciado basado en grid de 8px
- Tamaños de fuente escalables
- Elementos flexibles que se adaptan al contenedor

## Efectos y Transiciones

### Hover
- Cambio sutil de sombra
- Cambio de color de borde
- Resplandor según el tipo de elemento

### Focus
- Anillo de foco con color primario
- Resplandor suave
- Cambio de fondo a elevated

### Animaciones
Todas las transiciones son suaves y naturales:
- Fast: 150ms para cambios pequeños
- Normal: 300ms para la mayoría de interacciones
- Slow: 500ms para transiciones más dramáticas

## Accesibilidad

- Alto contraste entre texto y fondo
- Estados claros y visibles
- Jerarquía visual clara
- Elementos interactivos fácilmente identificables
