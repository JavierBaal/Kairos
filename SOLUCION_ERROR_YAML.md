# Solución al Error de Carga de Crews en Kairos

## Descripción del Error

Al ejecutar `run_kairos_with_monitoring.bat`, se producía el siguiente error:

```
Failed to load crews: could not determine a constructor for the tag 'tag:yaml.org,2002:python/object:models.crew_model.CrewModel'. in 'config/crews.yaml', line 3, column 5
```

## Causa del Error

El error se debía a que el archivo `config/crews.yaml` utilizaba etiquetas YAML específicas de Python (`!!python/object:models.crew_model.CrewModel`) para deserializar objetos Python directamente desde el YAML. Sin embargo, el código en `ui/crew_panel.py` estaba utilizando `yaml.safe_load()` para cargar los equipos, que por razones de seguridad no puede manejar estas etiquetas específicas de Python.

## Solución Implementada

Se modificó el archivo `config/crews.yaml` para que utilice un formato YAML estándar sin etiquetas específicas de Python. El nuevo formato es más seguro y compatible con `yaml.safe_load()`.

### Antes:

```yaml
Equipo de Inteligencia Competitiva BlackHat:
  agents:
  - !!python/object:models.agent_model.AgentModel
    allow_delegation: true
    backstory: "Analista con 15 años de experiencia en investigación de mercados y big data..."
    # ...
  # ...
```

### Después:

```yaml
Equipo de Inteligencia Competitiva BlackHat:
  description: "Equipo especializado en análisis competitivo, espionaje de mercado y descubrimiento de oportunidades ocultas"
  agents:
    - Analista de Mercado
    - Investigador Competitivo
    - Estratega
    - Cazador de Oportunidades
  tasks:
    - Análisis de Competidores
    - Análisis de Tendencias
    - Identificación de Oportunidades
    - Plan Estratégico
  process: hierarchical
  verbose: true
```

## Recomendaciones para el Futuro

1. **Evitar el uso de `yaml.load()` sin un loader específico**: Esta función puede ser peligrosa ya que permite la ejecución de código arbitrario. En su lugar, utilizar siempre `yaml.safe_load()` o `yaml.load()` con un loader personalizado que restrinja las etiquetas permitidas.

2. **Mantener consistencia en la serialización/deserialización**: Asegurarse de que el código que guarda los archivos YAML y el código que los carga utilicen el mismo enfoque. Si se utiliza `yaml.safe_load()` para cargar, no se deben incluir etiquetas específicas de Python al guardar.

3. **Documentar el formato de los archivos de configuración**: Incluir comentarios en los archivos de configuración que expliquen su estructura y formato esperado, para evitar confusiones en el futuro.
