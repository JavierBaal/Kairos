# Kairos Intelligence System

Kairos es una plataforma para la creación y gestión de equipos de agentes de IA. Este documento proporciona información sobre cómo ejecutar, configurar y distribuir Kairos.

## Estructura del Proyecto

El proyecto está organizado en las siguientes carpetas:

- **config/**: Configuración de agentes, tareas y equipos
- **config_files/**: Archivos de configuración del proyecto
- **dist/**: Ejecutables generados por PyInstaller
- **dist_tools/**: Herramientas para empaquetar y distribuir Kairos
- **installers/**: Scripts para instalar dependencias
- **langchain_prototype/**: Implementación de Kairos con LangChain
- **models/**: Modelos de datos
- **run_scripts/**: Scripts para ejecutar Kairos
- **ui/**: Interfaz de usuario

## Scripts Principales

En la raíz del proyecto hay tres scripts principales:

- **run_kairos.bat**: Ejecuta Kairos
- **install.bat**: Instala las dependencias necesarias
- **package.bat**: Empaqueta Kairos como un ejecutable independiente

## Opciones de Ejecución

Kairos ofrece varias opciones para ejecutar la aplicación:

### 1. Ejecución con LangChain (Recomendado)

- **Requisitos**: Python 3.9 o superior
- **Instalación**: Ejecuta `install.bat` y selecciona la opción 1
- **Ejecución**: Usa `run_kairos.bat`
- **Ventajas**: Mayor estabilidad, mejor documentación, menos problemas de dependencias

### 2. Ejecución con CrewAI (Original)

- **Requisitos**: Python 3.10 o superior
- **Instalación**: Ejecuta `install.bat` y selecciona la opción 2
- **Ejecución**: Usa `run_kairos.bat`

### 3. Modo Básico (Sin CrewAI/LangChain)

- **Requisitos**: Python 3.9 o superior
- **Ejecución**: Selecciona la opción correspondiente en `run_kairos.bat`
- **Limitaciones**: No incluye funcionalidad de agentes, solo interfaz de usuario

## Opciones de Distribución

Kairos puede distribuirse de varias formas:

### 1. Ejecutable Independiente

- **Creación**: Ejecuta `package.bat` y sigue las instrucciones
- **Ventajas**: No requiere Python instalado, fácil de distribuir
- **Opciones**: Puedes empaquetar la versión con LangChain o la versión básica

### 2. Instalador para Windows

- **Requisitos**: NSIS instalado (https://nsis.sourceforge.io/Download)
- **Creación**: Selecciona la opción correspondiente en el empaquetador
- **Resultado**: Un archivo .exe que instala Kairos en el sistema

### 3. Versión Portable (ZIP)

- **Creación**: Selecciona la opción correspondiente en el empaquetador
- **Resultado**: Un archivo ZIP que contiene Kairos listo para usar sin instalación

## Solución de Problemas

### Problemas con CrewAI

Si encuentras errores relacionados con CrewAI, prueba estas soluciones:

1. **Error de versión de Python**: Asegúrate de usar Python 3.10 o superior
2. **Error de compilación de tiktoken**: Instala Rust desde https://rustup.rs/
3. **Otros errores de dependencias**: Usa la versión de LangChain o el modo básico

### Problemas con LangChain

Si encuentras errores relacionados con LangChain:

1. **API key no configurada**: Asegúrate de proporcionar una API key de OpenAI válida
2. **Errores de importación**: Verifica que todas las dependencias estén instaladas correctamente

## Recursos Adicionales

Para más información, consulta los siguientes archivos:

- **README_KAIROS.md**: Documentación detallada de Kairos
- **langchain_prototype/README.md**: Guía de migración de CrewAI a LangChain
- **docs/user_guide.md**: Guía de usuario
