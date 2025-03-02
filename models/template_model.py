import os
import yaml
from models.agent_model import AgentModel
from models.task_model import TaskModel
from models.crew_model import CrewModel

class TemplateModel:
    """Modelo para gestionar plantillas predefinidas"""
    
    def __init__(self, template_id="", name="", description="", specialists=None, objectives=None, 
                 process="sequential", verbose=True, workflow=None, instructions=""):
        self.template_id = template_id
        self.name = name
        self.description = description
        self.specialists = specialists or {}
        self.objectives = objectives or {}
        self.process = process
        self.verbose = verbose
        self.workflow = workflow or {}
        self.instructions = instructions
    
    @staticmethod
    def load_templates():
        """Carga todas las plantillas disponibles en el directorio de plantillas"""
        templates = {}
        templates_dir = "config/templates"
        
        # Crear directorio si no existe
        os.makedirs(templates_dir, exist_ok=True)
        
        # Buscar archivos YAML en el directorio de plantillas
        for filename in os.listdir(templates_dir):
            if filename.endswith(".yaml") or filename.endswith(".yml"):
                template_path = os.path.join(templates_dir, filename)
                template_id = os.path.splitext(filename)[0]
                
                try:
                    with open(template_path, "r", encoding="utf-8") as f:
                        template_data = yaml.safe_load(f)
                    
                    # Crear modelo de plantilla
                    template = TemplateModel(
                        template_id=template_id,
                        name=template_data.get("name", ""),
                        description=template_data.get("description", ""),
                        specialists=template_data.get("specialists", {}),
                        objectives=template_data.get("objectives", {}),
                        process=template_data.get("process", "sequential"),
                        verbose=template_data.get("verbose", True),
                        workflow=template_data.get("workflow", {}),
                        instructions=template_data.get("instructions", "")
                    )
                    
                    templates[template_id] = template
                except Exception as e:
                    print(f"Error al cargar plantilla {template_id}: {str(e)}")
        
        return templates
    
    def create_agents(self):
        """Crea objetos AgentModel a partir de los especialistas de la plantilla"""
        agents = {}
        
        for agent_id, agent_data in self.specialists.items():
            agent = AgentModel(
                name=agent_data.get("name", ""),
                role=agent_data.get("role", ""),
                goal=agent_data.get("goal", ""),
                backstory=agent_data.get("backstory", ""),
                verbose=agent_data.get("verbose", True),
                allow_delegation=agent_data.get("allow_delegation", False),
                tools=agent_data.get("tools", [])
            )
            
            agents[agent.name] = agent
        
        return agents
    
    def create_tasks(self):
        """Crea objetos TaskModel a partir de los objetivos de la plantilla"""
        tasks = {}
        
        for task_id, task_data in self.objectives.items():
            task = TaskModel(
                name=task_data.get("name", ""),
                description=task_data.get("description", ""),
                expected_output=task_data.get("expected_output", ""),
                agent=task_data.get("agent", ""),
                output_file=task_data.get("output_file", "")
            )
            
            tasks[task.name] = task
        
        return tasks
    
    def create_crew(self, agents, tasks):
        """Crea un objeto CrewModel con los agentes y tareas proporcionados"""
        crew = CrewModel(
            name=self.name,
            description=self.description,
            agents=list(agents.values()),
            tasks=list(tasks.values()),
            process=self.process,
            verbose=self.verbose
        )
        
        return crew
    
    def apply_template(self, agent_panel, task_panel, crew_panel):
        """Aplica la plantilla a los paneles de la interfaz"""
        # Crear agentes
        agents = self.create_agents()
        
        # Actualizar panel de agentes
        agent_panel.agents = agents
        agent_panel.agent_list.clear()
        for name in agents.keys():
            agent_panel.agent_list.addItem(name)
        
        # Crear tareas
        tasks = self.create_tasks()
        
        # Actualizar panel de tareas
        task_panel.tasks = tasks
        task_panel.task_list.clear()
        for name in tasks.keys():
            task_panel.task_list.addItem(name)
        
        # Actualizar panel de equipos
        crew = self.create_crew(agents, tasks)
        crew_panel.crews = {crew.name: crew}
        crew_panel.crew_list.clear()
        crew_panel.crew_list.addItem(crew.name)
        
        return True
