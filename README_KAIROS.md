# Kairos Intelligence System

Kairos es una plataforma para la creación y gestión de equipos de agentes de IA. Este documento proporciona información sobre cómo ejecutar, configurar y distribuir Kairos.

## Opciones de Ejecución

Kairos ofrece varias opciones para ejecutar la aplicación, dependiendo de tus necesidades y configuración:

### 1. Ejecución con CrewAI (Original)

- **Requisitos**: Python 3.10 o superior
- **Instalación**: Ejecuta `install_dependencies.bat` y selecciona tu versión de Python
- **Ejecución**: Usa `run_kairos.bat`, `run_kairos_with_python312.bat` o `run_kairos_with_python313.bat`

### 2. Ejecución con LangChain (Recomendado)

- **Requisitos**: Python 3.9 o superior
- **Instalación**: Ejecuta `install_langchain.bat` y selecciona tu versión de Python
- **Ejecución**: Usa `run_langchain_prototype.bat`
- **Ventajas**: Mayor estabilidad, mejor documentación, menos problemas de dependencias

### 3. Modo Básico (Sin CrewAI/LangChain)

- **Requisitos**: Python 3.9 o superior
- **Ejecución**: Selecciona la opción 1 en `run_kairos.bat` para ejecutar en modo básico
- **Limitaciones**: No incluye funcionalidad de agentes, solo interfaz de usuario

## Opciones de Distribución

Kairos puede distribuirse de varias formas para facilitar su uso por diferentes tipos de usuarios:

### 1. Ejecutable Independiente

- **Creación**: Ejecuta `package_kairos.bat` y sigue las instrucciones
- **Ventajas**: No requiere Python instalado, fácil de distribuir
- **Opciones**: Puedes empaquetar la versión con LangChain o la versión básica

### 2. Instalador para Windows

- **Requisitos**: NSIS instalado (https://nsis.sourceforge.io/Download)
- **Creación**: Selecciona la opción 1 o 3 en el empaquetador
- **Resultado**: Un archivo .exe que instala Kairos en el sistema

### 3. Versión Portable (ZIP)

- **Creación**: Selecciona la opción 2 o 3 en el empaquetador
- **Resultado**: Un archivo ZIP que contiene Kairos listo para usar sin instalación
- **Uso**: Extrae el ZIP y ejecuta el archivo .exe o el batch incluido

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

## Comparación de Frameworks

| Característica | CrewAI | LangChain |
|----------------|--------|-----------|
| Estabilidad | Menor (proyecto más nuevo) | Mayor (proyecto maduro) |
| Documentación | Limitada | Extensa |
| Comunidad | Pequeña pero creciente | Grande y activa |
| Requisitos | Python 3.10+, Rust | Python 3.9+ |
| Facilidad de uso | API simple | API más compleja pero flexible |
| Herramientas | Limitadas | Extensas |

## Próximos Pasos

1. **Migración completa a LangChain**: Actualizar toda la interfaz de usuario para trabajar con LangChain
2. **Versión web**: Desarrollar una versión web de Kairos para acceso desde cualquier dispositivo
3. **Más herramientas**: Implementar herramientas adicionales específicas para Kairos
4. **Mejoras de UI/UX**: Mejorar la experiencia de usuario y la interfaz gráfica

## Recursos Adicionales

- [Documentación de LangChain](https://python.langchain.com/docs/get_started/introduction)
- [Ejemplos de LangChain](https://python.langchain.com/docs/use_cases)
- [Guía de Agentes en LangChain](https://python.langchain.com/docs/modules/agents/)
- [Documentación de PyInstaller](https://pyinstaller.org/en/stable/)
- [Documentación de NSIS](https://nsis.sourceforge.io/Docs/)
