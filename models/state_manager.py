"""
Kairos Intelligence System - State Manager
Este módulo proporciona un gestor de estado centralizado para la aplicación.
"""

from typing import Dict, Any, List, Callable, Optional
import threading

class StateManager:
    """Gestor de estado centralizado para Kairos."""
    
    _instance = None
    _lock = threading.Lock()
    
    def __new__(cls):
        with cls._lock:
            if cls._instance is None:
                cls._instance = super(StateManager, cls).__new__(cls)
                cls._instance._initialize()
            return cls._instance
    
    def _initialize(self):
        """Inicializar el gestor de estado."""
        self._state = {
            "agents": [],
            "tasks": [],
            "crews": [],
            "monitoring": {
                "active_agents": {},
                "total_cost": 0.0,
                "cost_limit": None
            }
        }
        self._observers = {}
    
    def get_state(self, key: str) -> Any:
        """Obtener un valor del estado."""
        if key in self._state:
            return self._state[key]
        return None
    
    def set_state(self, key: str, value: Any) -> None:
        """Establecer un valor en el estado y notificar a los observadores."""
        self._state[key] = value
        self._notify_observers(key)
    
    def update_state(self, key: str, value: Any) -> None:
        """Actualizar un valor en el estado y notificar a los observadores."""
        if key in self._state:
            if isinstance(self._state[key], dict) and isinstance(value, dict):
                self._state[key].update(value)
            elif isinstance(self._state[key], list) and isinstance(value, list):
                self._state[key].extend(value)
            else:
                self._state[key] = value
            self._notify_observers(key)
    
    def register_observer(self, key: str, callback: Callable) -> None:
        """Registrar un observador para un cambio de estado específico."""
        if key not in self._observers:
            self._observers[key] = []
        self._observers[key].append(callback)
    
    def unregister_observer(self, key: str, callback: Callable) -> None:
        """Eliminar un observador."""
        if key in self._observers and callback in self._observers[key]:
            self._observers[key].remove(callback)
    
    def _notify_observers(self, key: str) -> None:
        """Notificar a los observadores de un cambio de estado."""
        if key in self._observers:
            for callback in self._observers[key]:
                callback(self._state[key])

def get_state_manager():
    """Singleton getter for StateManager"""
    if StateManager._instance is None:
        StateManager._instance = StateManager()
    return StateManager._instance