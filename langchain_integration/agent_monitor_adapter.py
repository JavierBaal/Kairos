#!/usr/bin/env python3
"""
Kairos Intelligence System - LangChain Agent Monitor Adapter
Este módulo proporciona un adaptador para monitorizar agentes de LangChain.
"""

import time
import uuid
import threading
from typing import Dict, Any, Optional, List, Callable, Union
from functools import wraps

from langchain.agents import AgentExecutor
from langchain_openai import ChatOpenAI
from langchain_core.callbacks import BaseCallbackHandler
from langchain_core.messages import BaseMessage

# Precios aproximados por 1000 tokens (actualizar según cambios de OpenAI)
MODEL_COSTS = {
    "gpt-3.5-turbo": {"input": 0.0015, "output": 0.002},
    "gpt-4": {"input": 0.03, "output": 0.06},
    "gpt-4-turbo": {"input": 0.01, "output": 0.03},
    "gpt-4o": {"input": 0.01, "output": 0.03},
    # Añadir más modelos según sea necesario
}

# Valor predeterminado para modelos desconocidos
DEFAULT_COST = {"input": 0.002, "output": 0.002}


class AgentMonitorCallback(BaseCallbackHandler):
    """
    Callback handler para monitorizar agentes de LangChain.
    Captura métricas como tokens, costos y tiempos de respuesta.
    """
    
    def __init__(self, agent_id: str, agent_name: str, agent_role: str, 
                 update_callback: Optional[Callable] = None):
        """
        Inicializar el callback handler.
        
        Args:
            agent_id: ID único del agente
            agent_name: Nombre del agente
            agent_role: Rol del agente
            update_callback: Función para actualizar la UI con las métricas
        """
        self.agent_id = agent_id
        self.agent_name = agent_name
        self.agent_role = agent_role
        self.update_callback = update_callback
        
        # Métricas
        self.total_tokens = 0
        self.input_tokens = 0
        self.output_tokens = 0
        self.total_cost = 0.0
        self.start_time = None
        self.current_model = "gpt-3.5-turbo"  # Modelo predeterminado
        self.progress = 0
        self.status = "Inicializando..."
        
        # Historial de llamadas
        self.call_history = []
    
    def on_llm_start(self, serialized: Dict[str, Any], prompts: List[str], **kwargs: Any) -> None:
        """Llamado cuando comienza una llamada al LLM."""
        self.start_time = time.time()
        self.status = "Procesando consulta..."
        
        # Extraer el modelo si está disponible
        if "invocation_params" in kwargs and "model" in kwargs["invocation_params"]:
            self.current_model = kwargs["invocation_params"]["model"]
        
        self._update_ui()
    
    def on_llm_end(self, response: Any, **kwargs: Any) -> None:
        """Llamado cuando finaliza una llamada al LLM."""
        duration = time.time() - self.start_time if self.start_time else 0
        
        # Extraer tokens si están disponibles
        if hasattr(response, "llm_output") and response.llm_output:
            llm_output = response.llm_output
            if "token_usage" in llm_output:
                token_usage = llm_output["token_usage"]
                prompt_tokens = token_usage.get("prompt_tokens", 0)
                completion_tokens = token_usage.get("completion_tokens", 0)
                
                self.input_tokens += prompt_tokens
                self.output_tokens += completion_tokens
                self.total_tokens = self.input_tokens + self.output_tokens
                
                # Calcular costo
                model_cost = MODEL_COSTS.get(self.current_model, DEFAULT_COST)
                input_cost = (prompt_tokens / 1000) * model_cost["input"]
                output_cost = (completion_tokens / 1000) * model_cost["output"]
                call_cost = input_cost + output_cost
                self.total_cost += call_cost
                
                # Registrar la llamada
                self.call_history.append({
                    "timestamp": time.time(),
                    "model": self.current_model,
                    "input_tokens": prompt_tokens,
                    "output_tokens": completion_tokens,
                    "cost": call_cost,
                    "duration": duration
                })
        
        self.status = "Procesando resultados..."
        self._update_ui()
    
    def on_llm_error(self, error: Exception, **kwargs: Any) -> None:
        """Llamado cuando ocurre un error en una llamada al LLM."""
        self.status = f"Error: {str(error)}"
        self._update_ui()
    
    def on_chain_start(self, serialized: Dict[str, Any], inputs: Dict[str, Any], **kwargs: Any) -> None:
        """Llamado cuando comienza una cadena."""
        self.status = "Iniciando cadena de razonamiento..."
        self._update_ui()
    
    def on_chain_end(self, outputs: Dict[str, Any], **kwargs: Any) -> None:
        """Llamado cuando finaliza una cadena."""
        self.status = "Cadena completada"
        self._update_ui()
    
    def on_agent_action(self, action: Dict[str, Any], **kwargs: Any) -> None:
        """Llamado cuando un agente decide tomar una acción."""
        tool = action.get("tool", "desconocida")
        self.status = f"Ejecutando herramienta: {tool}"
        self._update_ui()
    
    def on_agent_finish(self, finish: Dict[str, Any], **kwargs: Any) -> None:
        """Llamado cuando un agente termina su ejecución."""
        self.status = "Tarea completada"
        self.progress = 100
        self._update_ui()
    
    def on_tool_start(self, serialized: Dict[str, Any], input_str: str, **kwargs: Any) -> None:
        """Llamado cuando comienza la ejecución de una herramienta."""
        tool_name = serialized.get("name", "desconocida")
        self.status = f"Iniciando herramienta: {tool_name}"
        self._update_ui()
    
    def on_tool_end(self, output: str, **kwargs: Any) -> None:
        """Llamado cuando finaliza la ejecución de una herramienta."""
        self.status = "Procesando resultado de herramienta"
        self._update_ui()
    
    def on_tool_error(self, error: Exception, **kwargs: Any) -> None:
        """Llamado cuando ocurre un error en una herramienta."""
        self.status = f"Error en herramienta: {str(error)}"
        self._update_ui()
    
    def on_text(self, text: str, **kwargs: Any) -> None:
        """Llamado cuando se genera texto."""
        # Actualizar progreso basado en heurísticas
        # Por ejemplo, si detectamos ciertos patrones en el texto
        if "pensando" in text.lower() or "thinking" in text.lower():
            self.progress = max(10, self.progress)
        elif "buscando" in text.lower() or "searching" in text.lower():
            self.progress = max(30, self.progress)
        elif "analizando" in text.lower() or "analyzing" in text.lower():
            self.progress = max(50, self.progress)
        elif "generando" in text.lower() or "generating" in text.lower():
            self.progress = max(70, self.progress)
        elif "finalizando" in text.lower() or "finalizing" in text.lower():
            self.progress = max(90, self.progress)
        
        self._update_ui()
    
    def update_progress(self, progress: int) -> None:
        """Actualizar manualmente el progreso del agente."""
        self.progress = min(max(0, progress), 100)
        self._update_ui()
    
    def update_status(self, status: str) -> None:
        """Actualizar manualmente el estado del agente."""
        self.status = status
        self._update_ui()
    
    def _update_ui(self) -> None:
        """Actualizar la interfaz de usuario con las métricas actuales."""
        if self.update_callback:
            self.update_callback(
                agent_id=self.agent_id,
                cost=self.total_cost,
                tokens=self.total_tokens,
                progress=self.progress,
                status=self.status
            )


class MonitoredAgentExecutor:
    """
    Wrapper para AgentExecutor que añade monitorización.
    """
    
    def __init__(self, agent_executor: AgentExecutor, agent_name: str, agent_role: str, 
                 agent_id: Optional[str] = None, update_callback: Optional[Callable] = None):
        """
        Inicializar el ejecutor de agente monitorizado.
        
        Args:
            agent_executor: El ejecutor de agente de LangChain
            agent_name: Nombre del agente
            agent_role: Rol del agente
            agent_id: ID único del agente (opcional, se genera uno si no se proporciona)
            update_callback: Función para actualizar la UI con las métricas
        """
        self.agent_executor = agent_executor
        self.agent_name = agent_name
        self.agent_role = agent_role
        self.agent_id = agent_id or str(uuid.uuid4())
        
        # Crear callback de monitorización
        self.monitor = AgentMonitorCallback(
            agent_id=self.agent_id,
            agent_name=self.agent_name,
            agent_role=self.agent_role,
            update_callback=update_callback
        )
        
        # Añadir callback al ejecutor
        if not hasattr(self.agent_executor, "callbacks") or self.agent_executor.callbacks is None:
            self.agent_executor.callbacks = [self.monitor]
        else:
            self.agent_executor.callbacks.append(self.monitor)
    
    def invoke(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Invocar el ejecutor de agente con monitorización.
        
        Args:
            input_data: Datos de entrada para el agente
        
        Returns:
            Resultado del agente
        """
        # Actualizar estado
        self.monitor.update_status("Iniciando tarea...")
        self.monitor.update_progress(5)
        
        try:
            # Ejecutar agente
            result = self.agent_executor.invoke(input_data)
            
            # Actualizar estado final
            self.monitor.update_status("Tarea completada")
            self.monitor.update_progress(100)
            
            return result
        except Exception as e:
            # Manejar errores
            self.monitor.update_status(f"Error: {str(e)}")
            raise
    
    def arun(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Versión asíncrona de invoke.
        
        Args:
            input_data: Datos de entrada para el agente
        
        Returns:
            Resultado del agente
        """
        # Crear una función para ejecutar en un hilo separado
        def run_in_thread():
            return self.invoke(input_data)
        
        # Crear y iniciar el hilo
        thread = threading.Thread(target=run_in_thread)
        thread.start()
        
        # Devolver una referencia al hilo para que el llamador pueda esperar si lo desea
        return {"thread": thread, "agent_id": self.agent_id}


class MonitoredChatOpenAI(ChatOpenAI):
    """
    Versión monitorizada de ChatOpenAI que registra tokens y costos.
    """
    
    def __init__(self, agent_id: str, agent_name: str, agent_role: str, 
                 update_callback: Optional[Callable] = None, **kwargs):
        """
        Inicializar el modelo ChatOpenAI monitorizado.
        
        Args:
            agent_id: ID único del agente
            agent_name: Nombre del agente
            agent_role: Rol del agente
            update_callback: Función para actualizar la UI con las métricas
            **kwargs: Argumentos para ChatOpenAI
        """
        super().__init__(**kwargs)
        
        # Crear callback de monitorización
        self.monitor = AgentMonitorCallback(
            agent_id=agent_id,
            agent_name=agent_name,
            agent_role=agent_role,
            update_callback=update_callback
        )
        
        # Añadir callback al modelo
        if not hasattr(self, "callbacks") or self.callbacks is None:
            self.callbacks = [self.monitor]
        else:
            self.callbacks.append(self.monitor)
    
    def invoke(self, messages: List[BaseMessage], **kwargs) -> Any:
        """
        Invocar el modelo con monitorización.
        
        Args:
            messages: Lista de mensajes para el modelo
            **kwargs: Argumentos adicionales
        
        Returns:
            Respuesta del modelo
        """
        # Actualizar estado
        self.monitor.update_status("Generando respuesta...")
        
        # Invocar el modelo
        return super().invoke(messages, **kwargs)


class AgentMonitorManager:
    """
    Gestor para monitorizar múltiples agentes y actualizar la UI.
    """
    
    def __init__(self, ui_panel=None):
        """
        Inicializar el gestor de monitorización.
        
        Args:
            ui_panel: Panel de UI para mostrar la monitorización (opcional)
        """
        self.ui_panel = ui_panel
        self.agents = {}  # Diccionario de agentes monitorizados por ID
        self.cost_limit = None  # Límite de costo global
        self.paused_agents = set()  # Conjunto de IDs de agentes pausados
    
    def set_ui_panel(self, ui_panel):
        """
        Establecer el panel de UI para la monitorización.
        
        Args:
            ui_panel: Panel de UI para mostrar la monitorización
        """
        self.ui_panel = ui_panel
    
    def create_monitored_agent(self, agent_executor: AgentExecutor, agent_name: str, agent_role: str, 
                              agent_id: Optional[str] = None) -> MonitoredAgentExecutor:
        """
        Crear un agente monitorizado.
        
        Args:
            agent_executor: El ejecutor de agente de LangChain
            agent_name: Nombre del agente
            agent_role: Rol del agente
            agent_id: ID único del agente (opcional, se genera uno si no se proporciona)
        
        Returns:
            Agente monitorizado
        """
        # Crear agente monitorizado
        monitored_agent = MonitoredAgentExecutor(
            agent_executor=agent_executor,
            agent_name=agent_name,
            agent_role=agent_role,
            agent_id=agent_id,
            update_callback=self.update_agent_metrics
        )
        
        # Registrar agente
        self.agents[monitored_agent.agent_id] = monitored_agent
        
        # Añadir a la UI si está disponible
        if self.ui_panel:
            self.ui_panel.add_agent_monitor(
                agent_id=monitored_agent.agent_id,
                agent_name=agent_name,
                agent_role=agent_role
            )
        
        return monitored_agent
    
    def create_monitored_llm(self, agent_name: str, agent_role: str, 
                            agent_id: Optional[str] = None, **kwargs) -> MonitoredChatOpenAI:
        """
        Crear un modelo LLM monitorizado.
        
        Args:
            agent_name: Nombre del agente
            agent_role: Rol del agente
            agent_id: ID único del agente (opcional, se genera uno si no se proporciona)
            **kwargs: Argumentos para ChatOpenAI
        
        Returns:
            Modelo LLM monitorizado
        """
        # Generar ID si no se proporciona
        agent_id = agent_id or str(uuid.uuid4())
        
        # Crear modelo monitorizado
        monitored_llm = MonitoredChatOpenAI(
            agent_id=agent_id,
            agent_name=agent_name,
            agent_role=agent_role,
            update_callback=self.update_agent_metrics,
            **kwargs
        )
        
        # Añadir a la UI si está disponible
        if self.ui_panel:
            self.ui_panel.add_agent_monitor(
                agent_id=agent_id,
                agent_name=agent_name,
                agent_role=agent_role
            )
        
        return monitored_llm
    
    def update_agent_metrics(self, agent_id: str, cost: float, tokens: int, 
                            progress: int, status: str) -> None:
        """
        Actualizar las métricas de un agente en la UI.
        
        Args:
            agent_id: ID del agente
            cost: Costo acumulado
            tokens: Tokens totales
            progress: Progreso (0-100)
            status: Estado actual
        """
        if not self.ui_panel:
            return
        
        # Verificar si se excede el límite de costo
        if self.cost_limit is not None:
            total_cost = sum(agent.monitor.total_cost for agent in self.agents.values())
            if total_cost > self.cost_limit and agent_id not in self.paused_agents:
                # Pausar el agente si excede el límite
                self.pause_agent(agent_id)
                status = "Pausado: límite de costo excedido"
        
        # Actualizar UI
        self.ui_panel.update_agent_cost(agent_id, cost)
        self.ui_panel.update_agent_tokens(agent_id, tokens)
        self.ui_panel.update_agent_progress(agent_id, progress)
        self.ui_panel.update_agent_status(agent_id, status)
    
    def set_cost_limit(self, limit: float) -> None:
        """
        Establecer un límite de costo global.
        
        Args:
            limit: Límite de costo en dólares
        """
        self.cost_limit = limit
        
        # Actualizar UI si está disponible
        if self.ui_panel and hasattr(self.ui_panel, "cost_monitor"):
            self.ui_panel.cost_monitor.set_cost_limit(limit)
    
    def pause_agent(self, agent_id: str) -> None:
        """
        Pausar un agente.
        
        Args:
            agent_id: ID del agente a pausar
        """
        if agent_id in self.agents:
            self.paused_agents.add(agent_id)
            
            # Actualizar UI
            if self.ui_panel:
                self.ui_panel.update_agent_status(agent_id, "Pausado")
    
    def resume_agent(self, agent_id: str) -> None:
        """
        Reanudar un agente pausado.
        
        Args:
            agent_id: ID del agente a reanudar
        """
        if agent_id in self.paused_agents:
            self.paused_agents.remove(agent_id)
            
            # Actualizar UI
            if self.ui_panel and agent_id in self.agents:
                self.ui_panel.update_agent_status(agent_id, "Reanudado")
    
    def get_total_cost(self) -> float:
        """
        Obtener el costo total de todos los agentes.
        
        Returns:
            Costo total en dólares
        """
        return sum(agent.monitor.total_cost for agent in self.agents.values())
    
    def get_total_tokens(self) -> int:
        """
        Obtener el total de tokens de todos los agentes.
        
        Returns:
            Total de tokens
        """
        return sum(agent.monitor.total_tokens for agent in self.agents.values())


# Instancia global del gestor de monitorización
monitor_manager = AgentMonitorManager()


def get_monitor_manager() -> AgentMonitorManager:
    """
    Obtener la instancia global del gestor de monitorización.
    
    Returns:
        Gestor de monitorización
    """
    return monitor_manager


# Funciones de utilidad para integrar con KairosAgent de langchain_prototype

def create_monitored_kairos_agent(name: str, role: str, goal: str, backstory: str = "",
                                 verbose: bool = False, tools: Optional[List[Any]] = None,
                                 llm_model: str = "gpt-3.5-turbo", agent_id: Optional[str] = None):
    """
    Crear un KairosAgent monitorizado.
    
    Args:
        name: Nombre del agente
        role: Rol del agente
        goal: Objetivo del agente
        backstory: Historia de fondo del agente
        verbose: Si se debe mostrar información detallada
        tools: Lista de herramientas para el agente
        llm_model: Modelo de lenguaje a utilizar
        agent_id: ID único del agente (opcional)
    
    Returns:
        KairosAgent monitorizado
    """
    # Importar KairosAgent aquí para evitar dependencias circulares
    from langchain_prototype.agent_example import KairosAgent
    
    # Crear LLM monitorizado
    monitored_llm = monitor_manager.create_monitored_llm(
        agent_name=name,
        agent_role=role,
        agent_id=agent_id,
        model=llm_model,
        temperature=0.7
    )
    
    # Crear KairosAgent con el LLM monitorizado
    agent = KairosAgent(
        name=name,
        role=role,
        goal=goal,
        backstory=backstory,
        verbose=verbose,
        tools=tools,
        llm_model=llm_model
    )
    
    # Reemplazar el LLM con la versión monitorizada
    agent.llm = monitored_llm
    
    # Recrear el agente con el nuevo LLM
    agent._create_agent()
    
    return agent


# Ejemplo de uso
if __name__ == "__main__":
    import sys
    from PyQt6.QtWidgets import QApplication
    from ui.agent_monitor import AgentMonitorPanel
    from ui.theme import Theme
    
    # Crear aplicación
    app = QApplication(sys.argv)
    
    # Aplicar tema
    app.setPalette(Theme.get_palette("mixed"))
    app.setStyleSheet(Theme.get_stylesheet("mixed"))
    
    # Crear panel de monitorización
    panel = AgentMonitorPanel()
    
    # Configurar gestor de monitorización
    monitor_manager.set_ui_panel(panel)
    monitor_manager.set_cost_limit(5.0)
    
    # Simular agentes (en una aplicación real, estos serían agentes reales)
    for i in range(3):
        agent_id = f"agent{i+1}"
        agent_name = f"Agente {i+1}"
        agent_role = f"Rol {i+1}"
        
        # Añadir agente a la UI
        panel.add_agent_monitor(agent_id, agent_name, agent_role)
        
        # Simular actualizaciones
        panel.update_agent_cost(agent_id, 0.1 * (i+1))
        panel.update_agent_tokens(agent_id, 500 * (i+1))
        panel.update_agent_progress(agent_id, 20 * (i+1))
        panel.update_agent_status(agent_id, f"Trabajando en tarea {i+1}")
    
    # Mostrar panel
    panel.setWindowTitle("Monitorización de Agentes LangChain")
    panel.resize(800, 600)
    panel.show()
    
    sys.exit(app.exec())
