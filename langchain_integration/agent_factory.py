"""
Factory class for creating LangChain agents
"""
from langchain.agents import AgentType, initialize_agent
from langchain.chat_models import ChatOpenAI
from langchain.tools import BaseTool

class AgentFactory:
    """
    Factory class for creating LangChain agents with different configurations
    """
    
    def __init__(self):
        """Initialize the agent factory"""
        pass
    
    def create_agent(self, name, role, model="gpt-3.5-turbo", tools=None, temperature=0.7):
        """
        Create a LangChain agent with the specified configuration
        
        Args:
            name (str): Name of the agent
            role (str): Role/description of the agent
            model (str): Model to use (default: gpt-3.5-turbo)
            tools (list): List of tools to provide to the agent
            temperature (float): Temperature for generation (0.0-1.0)
            
        Returns:
            Agent: A configured LangChain agent
        """
        # Create the language model
        llm = ChatOpenAI(
            model=model,
            temperature=temperature
        )
        
        # Create tools list if provided
        agent_tools = []
        if tools:
            # Here you would convert the tool configurations to actual LangChain tools
            # For now, we'll just use a placeholder implementation
            pass
        
        # Create the agent
        # If no tools are provided, create a conversational agent
        if not agent_tools:
            # For agents without tools, we'll just return the LLM with the role in the system message
            return {
                "name": name,
                "role": role,
                "llm": llm,
                "type": "conversational"
            }
        else:
            # For agents with tools, initialize a proper agent
            agent = initialize_agent(
                agent_tools,
                llm,
                agent=AgentType.CHAT_CONVERSATIONAL_REACT_DESCRIPTION,
                verbose=True
            )
            
            return {
                "name": name,
                "role": role,
                "agent": agent,
                "type": "tool_using"
            }