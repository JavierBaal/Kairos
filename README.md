# Kairos Intelligence System

<p align="center">
  <img src="docs/images/logo.png" alt="Kairos Intelligence System Logo" width="200"/>
</p>

## Descripción

Kairos Intelligence System es una plataforma avanzada para la creación, gestión y ejecución de equipos de agentes de IA. Permite a usuarios sin conocimientos técnicos aprovechar el poder de los sistemas multiagente a través de una interfaz gráfica intuitiva y plantillas predefinidas para casos de uso específicos.

## Características Principales

- **Interfaz de Flujo de Trabajo Horizontal**: Diseñada para usuarios no técnicos, con un proceso paso a paso intuitivo
- **Plantillas Premium Predefinidas**: Configuraciones listas para usar en casos de uso específicos
- **Tema Profesional Estilo JetBrains**: Interfaz moderna con tema oscuro por defecto
- **Gestión Visual de Equipos**: Crea y conecta especialistas de IA visualmente
- **Compatibilidad con CrewAI**: Aprovecha el poder del framework CrewAI sin escribir código

## Plantillas Incluidas

### BlackHat Intelligence System
Equipo especializado en análisis competitivo y espionaje de mercado, que incluye:
- Analista de Mercado
- Investigador Competitivo
- Estratega
- Cazador de Oportunidades

Ideal para descubrir oportunidades de mercado ocultas y analizar competidores.

## Requisitos

- Python 3.8 o superior
- PyQt6
- CrewAI y sus dependencias

## Instalación

1. Clona el repositorio:
```bash
git clone https://github.com/yourusername/kairos.git
cd kairos
```

2. Instala las dependencias:
```bash
pip install -r requirements.txt
```

## Uso

### Método Simple
Ejecuta el script de inicio:
```bash
python run_kairos.py
```

### Método Alternativo
Ejecuta directamente la aplicación principal:
```bash
python main.py
```

## Guía Rápida

1. **Paso 1: FORMAR** - Selecciona una plantilla predefinida o crea tu propio equipo desde cero
2. **Paso 2: DEFINIR** - Configura los especialistas con roles, objetivos y capacidades específicas
3. **Paso 3: CONECTAR** - Establece relaciones entre especialistas para definir el flujo de trabajo
4. **Paso 4: ACTIVAR** - Ejecuta el equipo y observa cómo trabajan juntos
5. **Paso 5: RESULTADOS** - Revisa y utiliza los resultados generados por el equipo

## Modos de Interfaz

Kairos ofrece dos modos de interfaz:

- **Moderna (Flujo de Trabajo)**: Interfaz horizontal paso a paso, ideal para nuevos usuarios
- **Tradicional (Pestañas)**: Interfaz basada en pestañas para usuarios avanzados

Puedes cambiar entre modos desde el menú "Interfaz".

## Personalización

### Temas
Kairos incluye temas claro y oscuro (predeterminado). Puedes cambiar el tema desde el menú "Ver" → "Cambiar Tema".

### Plantillas Personalizadas
Puedes crear tus propias plantillas añadiendo archivos YAML en el directorio `config/templates/`.

## Contribuciones

Las contribuciones son bienvenidas. Por favor, sigue estos pasos:

1. Haz un fork del repositorio
2. Crea una rama para tu característica (`git checkout -b feature/caracteristica-increible`)
3. Haz commit de tus cambios (`git commit -m 'Añadir alguna característica increíble'`)
4. Haz push a la rama (`git push origin feature/caracteristica-increible`)
5. Abre un Pull Request

## Licencia

Este proyecto está licenciado bajo la Licencia MIT - ver el archivo LICENSE para más detalles.

## Agradecimientos

- CrewAI - El framework que inspiró esta GUI
- PyQt6 - El framework de GUI utilizado
- JetBrains - Inspiración para el diseño de la interfaz
