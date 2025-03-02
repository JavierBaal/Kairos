#!/usr/bin/env python3
"""
Ejemplo de implementación de agentes con LangChain para Kairos
Este script muestra cómo crear agentes y ejecutar tareas usando LangChain
como alternativa a CrewAI.
"""

from langchain.agents import AgentExecutor, create_openai_functions_agent
from langchain.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.messages import SystemMessage
from langchain_openai import ChatOpenAI
from langchain.tools import tool
from langchain.tools.render import format_tool_to_openai_function
from typing import List, Dict, Any, Optional
import os

# Configuración de la API key (en un entorno real, usar variables de entorno)
# os.environ["OPENAI_API_KEY"] = "tu-api-key-aquí"

# Definición de herramientas personalizadas
@tool
def search_web(query: str) -> str:
    """Busca información en la web sobre un tema específico."""
    # En una implementación real, esto conectaría con un motor de búsqueda
    return f"Resultados de búsqueda para: {query}"

@tool
def read_file(file_path: str) -> str:
    """Lee el contenido de un archivo."""
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            return file.read()
    except Exception as e:
        return f"Error al leer el archivo: {str(e)}"

@tool
def write_file(file_path: str, content: str) -> str:
    """Escribe contenido en un archivo."""
    try:
        with open(file_path, 'w', encoding='utf-8') as file:
            file.write(content)
        return f"Archivo guardado correctamente en {file_path}"
    except Exception as e:
        return f"Error al escribir el archivo: {str(e)}"

# Clase para representar un agente (equivalente a Agent en CrewAI)
class KairosAgent:
    def __init__(
        self,
        name: str,
        role: str,
        goal: str,
        backstory: str = "",
        verbose: bool = False,
        tools: Optional[List[Any]] = None,
        llm_model: str = "gpt-3.5-turbo"
    ):
        self.name = name
        self.role = role
        self.goal = goal
        self.backstory = backstory
        self.verbose = verbose
        self.tools = tools if tools is not None else []
        
        # Configurar el modelo de lenguaje
        self.llm = ChatOpenAI(model=llm_model, temperature=0.7)
        
        # Crear el agente
        self._create_agent()
    
    def _create_agent(self):
        """Crea el agente de LangChain con las herramientas y configuración especificadas."""
        # Convertir herramientas al formato de OpenAI
        openai_tools = [format_tool_to_openai_function(t) for t in self.tools]
        
        # Crear el prompt del agente
        system_message = f"""
        Eres {self.name}, {self.role}.
        Tu objetivo es: {self.goal}
        
        Backstory: {self.backstory}
        
        Responde siempre desde la perspectiva de tu rol.
        """
        
        prompt = ChatPromptTemplate.from_messages(
            [
                SystemMessage(content=system_message),
                MessagesPlaceholder(variable_name="chat_history"),
                ("human", "{input}"),
                MessagesPlaceholder(variable_name="agent_scratchpad"),
            ]
        )
        
        # Crear el agente
        agent = create_openai_functions_agent(self.llm, self.tools, prompt)
        
        # Crear el ejecutor del agente
        self.agent_executor = AgentExecutor(
            agent=agent,
            tools=self.tools,
            verbose=self.verbose,
            handle_parsing_errors=True
        )
    
    def execute_task(self, task_description: str, context: Optional[Dict[str, Any]] = None) -> str:
        """Ejecuta una tarea con el agente."""
        context_dict = context if context is not None else {}
        context_dict["chat_history"] = []
        
        # Ejecutar la tarea
        result = self.agent_executor.invoke(
            {"input": task_description, **context_dict}
        )
        
        return result.get("output", "No se pudo completar la tarea.")

# Clase para representar una tarea (equivalente a Task en CrewAI)
class KairosTask:
    def __init__(
        self,
        description: str,
        agent: KairosAgent,
        expected_output: str = "",
        context: Optional[Dict[str, Any]] = None
    ):
        self.description = description
        self.agent = agent
        self.expected_output = expected_output
        self.context = context if context is not None else {}
    
    def execute(self) -> str:
        """Ejecuta la tarea utilizando el agente asignado."""
        return self.agent.execute_task(self.description, self.context)

# Clase para representar un equipo (equivalente a Crew en CrewAI)
class KairosCrew:
    def __init__(
        self,
        agents: List[KairosAgent],
        tasks: List[KairosTask],
        verbose: bool = False
    ):
        self.agents = agents
        self.tasks = tasks
        self.verbose = verbose
        self.results = []
    
    def run(self) -> List[str]:
        """Ejecuta todas las tareas en secuencia."""
        self.results = []
        
        for i, task in enumerate(self.tasks):
            if self.verbose:
                print(f"\n--- Ejecutando tarea {i+1}/{len(self.tasks)} ---")
                print(f"Descripción: {task.description}")
                print(f"Agente: {task.agent.name} ({task.agent.role})")
            
            result = task.execute()
            self.results.append(result)
            
            if self.verbose:
                print(f"\nResultado: {result}")
        
        return self.results

# Ejemplo de uso
def main():
    # Crear agentes
    researcher = KairosAgent(
        name="Alex",
        role="Investigador de mercado",
        goal="Encontrar información relevante sobre tendencias de mercado",
        backstory="Tienes años de experiencia analizando datos de mercado y tendencias.",
        verbose=True,
        tools=[search_web],
        llm_model="gpt-3.5-turbo"
    )
    
    writer = KairosAgent(
        name="Sam",
        role="Redactor de contenido",
        goal="Crear contenido persuasivo basado en datos de investigación",
        backstory="Eres un escritor experimentado especializado en marketing.",
        verbose=True,
        tools=[read_file, write_file],
        llm_model="gpt-3.5-turbo"
    )
    
    # Crear tareas
    research_task = KairosTask(
        description="Investiga las tendencias actuales en inteligencia artificial para empresas.",
        agent=researcher,
        expected_output="Un resumen de las tendencias actuales en IA empresarial."
    )
    
    writing_task = KairosTask(
        description="Escribe un artículo de blog sobre cómo las empresas pueden aprovechar la IA.",
        agent=writer,
        expected_output="Un artículo de blog completo sobre IA empresarial."
    )
    
    # Crear equipo
    crew = KairosCrew(
        agents=[researcher, writer],
        tasks=[research_task, writing_task],
        verbose=True
    )
    
    # Ejecutar equipo
    print("Ejecutando equipo de agentes con LangChain...")
    results = crew.run()
    
    print("\n=== Resultados finales ===")
    for i, result in enumerate(results):
        print(f"\nResultado de tarea {i+1}:")
        print(result)

if __name__ == "__main__":
    # Comenta esta línea si no tienes una API key configurada
    print("Para ejecutar este ejemplo, descomenta la línea 'main()' y configura tu API key de OpenAI.")
    # main()
