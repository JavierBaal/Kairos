# Kairos con LangChain

Este directorio contiene la implementación de Kairos utilizando LangChain como alternativa a CrewAI. Esta versión ofrece mayor estabilidad, mejor documentación y compatibilidad con Python 3.9+.

## Ventajas de LangChain

- **Mayor compatibilidad**: Funciona con Python 3.9 o superior (CrewAI requiere 3.10+)
- **Sin dependencia de Rust**: No requiere compilar extensiones nativas
- **Mejor documentación**: Documentación más completa y ejemplos
- **Comunidad más grande**: Mayor soporte y recursos disponibles
- **Actualizaciones frecuentes**: Mantenimiento activo y mejoras continuas

## Estructura de Clases

La implementación de LangChain para Kairos incluye clases equivalentes a las de CrewAI:

1. **KairosAgent**: Equivalente a `Agent` en CrewAI
   - Representa un agente con un rol, objetivo y conjunto de herramientas
   - Utiliza LangChain para crear y ejecutar agentes

2. **KairosTask**: Equivalente a `Task` en CrewAI
   - Representa una tarea que debe realizar un agente
   - Incluye descripción, agente asignado y contexto

3. **KairosCrew**: Equivalente a `Crew` en CrewAI
   - Representa un equipo de agentes que trabajan juntos
   - Ejecuta tareas en secuencia o en paralelo

## Herramientas Incluidas

La implementación incluye varias herramientas predefinidas:

- **search_web**: Busca información en la web
- **read_file**: Lee el contenido de un archivo
- **write_file**: Escribe contenido en un archivo

## Cómo Usar

### 1. Crear Agentes

```python
from langchain_prototype.agent_example import KairosAgent

researcher = KairosAgent(
    name="Alex",
    role="Investigador de mercado",
    goal="Encontrar información relevante sobre tendencias de mercado",
    backstory="Tienes años de experiencia analizando datos de mercado y tendencias.",
    verbose=True,
    tools=[search_web],
    llm_model="gpt-3.5-turbo"
)
```

### 2. Crear Tareas

```python
from langchain_prototype.agent_example import KairosTask

research_task = KairosTask(
    description="Investiga las tendencias actuales en inteligencia artificial para empresas.",
    agent=researcher,
    expected_output="Un resumen de las tendencias actuales en IA empresarial."
)
```

### 3. Crear y Ejecutar un Equipo

```python
from langchain_prototype.agent_example import KairosCrew

crew = KairosCrew(
    agents=[researcher, writer],
    tasks=[research_task, writing_task],
    verbose=True
)

results = crew.run()
```

## Integración con la Interfaz de Usuario

Para integrar completamente LangChain con la interfaz de usuario de Kairos:

1. Importar las clases de LangChain en los paneles correspondientes:
   ```python
   from langchain_prototype.agent_example import KairosAgent, KairosTask, KairosCrew
   ```

2. Reemplazar las llamadas a CrewAI por las equivalentes de LangChain:
   ```python
   # Antes (CrewAI)
   agent = Agent(...)
   
   # Después (LangChain)
   agent = KairosAgent(...)
   ```

3. Actualizar los métodos de ejecución para usar la nueva implementación.

## Requisitos

- Python 3.9 o superior
- LangChain y sus dependencias (instalables con `install_langchain.bat`)
- API key de OpenAI (para usar con los modelos de OpenAI)

## Configuración de la API Key

Para usar LangChain con modelos de OpenAI, necesitas configurar tu API key:

```python
import os
os.environ["OPENAI_API_KEY"] = "tu-api-key-aquí"
```

O ejecutar el script `run_langchain_prototype.bat` que te pedirá la API key.

## Próximos Pasos

1. Implementar más herramientas específicas para Kairos
2. Integrar completamente con la interfaz de usuario
3. Añadir soporte para más modelos de lenguaje
4. Implementar ejecución paralela de tareas
