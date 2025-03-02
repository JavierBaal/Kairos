# Kairos con LangChain - Prototipo

Este directorio contiene un prototipo de implementación de Kairos utilizando LangChain como alternativa a CrewAI. LangChain es un framework más maduro y estable para la creación de aplicaciones basadas en LLMs, con una comunidad más amplia y mejor soporte.

## Ventajas de LangChain sobre CrewAI

- **Mayor estabilidad**: LangChain es un proyecto más maduro con actualizaciones frecuentes y una comunidad activa.
- **Mejor documentación**: Documentación extensa y ejemplos detallados.
- **Compatibilidad con más modelos**: Soporte para una amplia variedad de modelos y proveedores.
- **Menos problemas de dependencias**: No requiere Rust para la compilación de algunas dependencias.
- **Compatibilidad con Python 3.9+**: Funciona con versiones anteriores de Python, a diferencia de CrewAI que requiere Python 3.10+.

## Estructura del Prototipo

- `agent_example.py`: Implementación de ejemplo que muestra cómo crear agentes, tareas y equipos con LangChain.
- `../requirements_langchain.txt`: Archivo de requisitos para instalar las dependencias de LangChain.
- `../install_langchain.bat`: Script para instalar las dependencias de LangChain.
- `../run_langchain_prototype.bat`: Script para ejecutar el prototipo de LangChain.

## Cómo Usar el Prototipo

1. **Instalar Dependencias**:
   - Ejecuta `install_langchain.bat` y selecciona la versión de Python que deseas usar.
   - El script instalará PyQt6, PyYAML y LangChain.

2. **Ejecutar el Prototipo**:
   - Ejecuta `run_langchain_prototype.bat` y selecciona la versión de Python.
   - Proporciona tu API key de OpenAI cuando se te solicite.
   - El prototipo ejecutará un ejemplo simple de agentes y tareas.

3. **Explorar el Código**:
   - Abre `agent_example.py` para ver cómo se implementan los agentes, tareas y equipos con LangChain.
   - Modifica el código para experimentar con diferentes configuraciones.

## Guía de Migración de CrewAI a LangChain

### 1. Conceptos Equivalentes

| CrewAI | LangChain | Notas |
|--------|-----------|-------|
| `Agent` | `KairosAgent` | Implementado como una clase personalizada que utiliza `AgentExecutor` de LangChain |
| `Task` | `KairosTask` | Implementado como una clase personalizada que ejecuta tareas con un agente |
| `Crew` | `KairosCrew` | Implementado como una clase personalizada que ejecuta tareas en secuencia |
| `Tool` | `@tool` | LangChain utiliza decoradores para definir herramientas |

### 2. Pasos para Migrar

1. **Actualizar requirements.txt**:
   ```
   PyQt6>=6.4.0
   pyyaml>=6.0
   langchain>=0.1.0
   langchain-openai>=0.0.2
   langchain-community>=0.0.10
   langchain-core>=0.1.10
   ```

2. **Migrar Agentes**:
   - Reemplazar `from crewai import Agent` con la clase `KairosAgent` personalizada.
   - Actualizar la creación de agentes para usar el nuevo formato.

3. **Migrar Tareas**:
   - Reemplazar `from crewai import Task` con la clase `KairosTask` personalizada.
   - Actualizar la creación de tareas para usar el nuevo formato.

4. **Migrar Equipos (Crews)**:
   - Reemplazar `from crewai import Crew` con la clase `KairosCrew` personalizada.
   - Actualizar la creación de equipos para usar el nuevo formato.

5. **Migrar Herramientas**:
   - Reemplazar herramientas de CrewAI con herramientas de LangChain usando el decorador `@tool`.

### 3. Ejemplo de Migración

**Código CrewAI Original**:
```python
from crewai import Agent, Task, Crew
from crewai_tools import SerperDevTool

# Crear agente
researcher = Agent(
    role="Investigador de mercado",
    goal="Encontrar información relevante",
    backstory="Tienes experiencia en análisis de mercado",
    verbose=True,
    tools=[SerperDevTool()]
)

# Crear tarea
research_task = Task(
    description="Investiga tendencias de IA",
    agent=researcher
)

# Crear equipo
crew = Crew(
    agents=[researcher],
    tasks=[research_task],
    verbose=True
)

# Ejecutar equipo
result = crew.kickoff()
```

**Código LangChain Migrado**:
```python
from langchain_prototype.agent_example import KairosAgent, KairosTask, KairosCrew
from langchain.tools import tool

@tool
def search_web(query: str) -> str:
    """Busca información en la web."""
    # Implementación de búsqueda
    return f"Resultados para: {query}"

# Crear agente
researcher = KairosAgent(
    name="Investigador",
    role="Investigador de mercado",
    goal="Encontrar información relevante",
    backstory="Tienes experiencia en análisis de mercado",
    verbose=True,
    tools=[search_web]
)

# Crear tarea
research_task = KairosTask(
    description="Investiga tendencias de IA",
    agent=researcher
)

# Crear equipo
crew = KairosCrew(
    agents=[researcher],
    tasks=[research_task],
    verbose=True
)

# Ejecutar equipo
results = crew.run()
```

## Próximos Pasos

1. **Integrar con la Interfaz de Usuario**: Actualizar la interfaz de usuario de Kairos para trabajar con LangChain.
2. **Implementar Más Herramientas**: Añadir más herramientas específicas para Kairos.
3. **Mejorar la Gestión de Memoria**: Implementar memoria compartida entre agentes.
4. **Añadir Soporte para Más Modelos**: Integrar con más proveedores de LLMs.

## Recursos Adicionales

- [Documentación de LangChain](https://python.langchain.com/docs/get_started/introduction)
- [Ejemplos de LangChain](https://python.langchain.com/docs/use_cases)
- [Guía de Agentes en LangChain](https://python.langchain.com/docs/modules/agents/)
