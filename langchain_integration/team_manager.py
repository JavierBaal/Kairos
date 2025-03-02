from langchain.agents import initialize_agent, AgentType
from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate

class TeamManager:
    """
    Gestor de equipos de agentes LangChain.
    Proporciona métodos para ejecutar diferentes tipos de equipos.
    """
    
    def __init__(self):
        pass
    
    def run_sequential_team(self, agents, objective, verbose=True):
        """
        Ejecuta un equipo de agentes de forma secuencial.
        Cada agente trabaja sobre el resultado del anterior.
        
        Args:
            agents (list): Lista de agentes LangChain
            objective (str): Objetivo del equipo
            verbose (bool): Si se debe mostrar información detallada
            
        Returns:
            str: Resultado final del equipo
        """
        current_result = objective
        full_output = f"Objetivo: {objective}\n\n"
        
        for i, agent in enumerate(agents):
            if verbose:
                full_output += f"\n--- Agente {i+1}: {agent.name} ({agent.role}) ---\n"
            
            # El agente trabaja sobre el resultado actual
            result = agent.run(current_result)
            current_result = result
            
            if verbose:
                full_output += f"Resultado: {result}\n"
        
        if verbose:
            full_output += f"\n--- Resultado Final ---\n{current_result}"
            return full_output
        else:
            return current_result
    
    def run_hierarchical_team(self, agents, objective, verbose=True):
        """
        Ejecuta un equipo de agentes de forma jerárquica.
        El primer agente actúa como líder y delega tareas a los demás.
        
        Args:
            agents (list): Lista de agentes LangChain
            objective (str): Objetivo del equipo
            verbose (bool): Si se debe mostrar información detallada
            
        Returns:
            str: Resultado final del equipo
        """
        if not agents:
            return "No hay agentes en el equipo"
        
        full_output = f"Objetivo: {objective}\n\n"
        
        # El primer agente es el líder
        leader = agents[0]
        team_members = agents[1:] if len(agents) > 1 else []
        
        if verbose:
            full_output += f"Líder: {leader.name} ({leader.role})\n"
            full_output += f"Miembros del equipo: {', '.join([a.name for a in team_members])}\n\n"
        
        # El líder analiza el objetivo y crea subtareas
        leader_prompt = f"""
        Eres el líder de un equipo. Tu objetivo es: {objective}
        
        Divide este objetivo en subtareas específicas para tu equipo.
        Para cada subtarea, especifica:
        1. Descripción clara de la tarea
        2. Resultado esperado
        
        Formato:
        Subtarea 1: [descripción]
        Resultado esperado: [resultado]
        
        Subtarea 2: [descripción]
        Resultado esperado: [resultado]
        
        ...y así sucesivamente.
        """
        
        subtasks_plan = leader.run(leader_prompt)
        
        if verbose:
            full_output += f"--- Plan del Líder ---\n{subtasks_plan}\n\n"
        
        # Extraer subtareas (implementación simplificada)
        subtasks = []
        current_task = ""
        for line in subtasks_plan.split('\n'):
            if line.startswith("Subtarea"):
                if current_task:
                    subtasks.append(current_task)
                current_task = line + "\n"
            elif line.strip():
                current_task += line + "\n"
        
        if current_task:
            subtasks.append(current_task)
        
        # Asignar subtareas a los miembros del equipo
        results = []
        
        for i, subtask in enumerate(subtasks):
            # Asignar cíclicamente si hay menos miembros que tareas
            member_index = i % len(team_members) if team_members else 0
            
            if team_members:
                agent = team_members[member_index]
                if verbose:
                    full_output += f"--- Subtarea {i+1} asignada a {agent.name} ---\n"
                    full_output += f"{subtask}\n"
                
                result = agent