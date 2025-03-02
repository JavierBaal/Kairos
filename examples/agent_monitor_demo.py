#!/usr/bin/env python3
"""
Kairos Intelligence System - Demo de Monitorización de Agentes
Este script muestra una demostración del panel de monitorización de agentes con el tema mixto.
"""

import sys
import os
import random
import time
from PyQt6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QLabel
from PyQt6.QtCore import QTimer, Qt, pyqtSlot

# Asegurarse de que podemos importar desde el directorio padre
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from ui.theme import Theme
from ui.agent_monitor import AgentMonitorPanel

class AgentMonitorDemo(QMainWindow):
    """Ventana de demostración para el panel de monitorización de agentes."""
    
    def __init__(self):
        super().__init__()
        
        # Configurar la ventana
        self.setWindowTitle("Kairos - Monitorización de Agentes")
        self.resize(1200, 800)
        
        # Crear widget central
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # Crear layout principal
        main_layout = QVBoxLayout(central_widget)
        
        # Título
        title_label = QLabel("Kairos Intelligence System - Panel de Monitorización")
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title_label.setStyleSheet("font-size: 24px; font-weight: bold; color: white; margin: 20px;")
        main_layout.addWidget(title_label)
        
        # Crear panel de monitorización
        self.monitor_panel = AgentMonitorPanel()
        main_layout.addWidget(self.monitor_panel)
        
        # Añadir agentes de ejemplo
        self.setup_demo_agents()
        
        # Configurar timer para simular actualizaciones
        self.update_timer = QTimer(self)
        self.update_timer.timeout.connect(self.simulate_agent_updates)
        self.update_timer.start(1000)  # Actualizar cada segundo
    
    def setup_demo_agents(self):
        """Configurar agentes de demostración."""
        # Definir algunos agentes de ejemplo
        agents = [
            {
                "id": "agent1",
                "name": "Investigador de Mercado",
                "role": "Analista de Datos"
            },
            {
                "id": "agent2",
                "name": "Redactor de Contenido",
                "role": "Escritor Creativo"
            },
            {
                "id": "agent3",
                "name": "Estratega de Marketing",
                "role": "Planificador"
            },
            {
                "id": "agent4",
                "name": "Asistente Ejecutivo",
                "role": "Coordinador"
            },
            {
                "id": "agent5",
                "name": "Analista Financiero",
                "role": "Experto en Finanzas"
            }
        ]
        
        # Añadir agentes al panel
        for agent in agents:
            self.monitor_panel.add_agent_monitor(agent["id"], agent["name"], agent["role"])
            
            # Inicializar con valores aleatorios
            self.monitor_panel.update_agent_cost(agent["id"], random.uniform(0.05, 0.2))
            self.monitor_panel.update_agent_tokens(agent["id"], random.randint(100, 1000))
            self.monitor_panel.update_agent_progress(agent["id"], random.randint(5, 20))
            
            # Establecer estados iniciales
            statuses = ["Analizando datos...", "Generando contenido...", "Planificando estrategia...", 
                       "Coordinando tareas...", "Evaluando opciones..."]
            self.monitor_panel.update_agent_status(agent["id"], random.choice(statuses))
        
        # Establecer un límite de costo
        self.monitor_panel.cost_monitor.set_cost_limit(5.0)
    
    @pyqtSlot()
    def simulate_agent_updates(self):
        """Simular actualizaciones de los agentes."""
        # Actualizar cada agente con valores aleatorios
        for agent_id in self.monitor_panel.agent_monitors:
            # Incrementar costo
            current_cost = self.monitor_panel.agent_monitors[agent_id].cost
            new_cost = current_cost + random.uniform(0.001, 0.01)
            self.monitor_panel.update_agent_cost(agent_id, new_cost)
            
            # Incrementar tokens
            current_tokens = self.monitor_panel.agent_monitors[agent_id].tokens
            new_tokens = current_tokens + random.randint(10, 50)
            self.monitor_panel.update_agent_tokens(agent_id, new_tokens)
            
            # Incrementar progreso
            current_progress = self.monitor_panel.agent_monitors[agent_id].progress
            new_progress = min(current_progress + random.randint(0, 2), 100)
            self.monitor_panel.update_agent_progress(agent_id, new_progress)
            
            # Actualizar estado ocasionalmente
            if random.random() < 0.1:  # 10% de probabilidad
                statuses = [
                    "Analizando datos...",
                    "Generando contenido...",
                    "Planificando estrategia...",
                    "Evaluando opciones...",
                    "Procesando información...",
                    "Consultando fuentes...",
                    "Optimizando resultados...",
                    "Refinando análisis..."
                ]
                self.monitor_panel.update_agent_status(agent_id, random.choice(statuses))
            
            # Simular finalización
            if new_progress >= 100:
                self.monitor_panel.update_agent_status(agent_id, "¡Tarea completada!")
                # Detener actualizaciones para este agente


def main():
    """Función principal."""
    print("Iniciando demostración del monitor de agentes...")
    print("Si no ves una ventana, verifica que no esté minimizada o detrás de otras ventanas.")
    
    # Crear aplicación
    app = QApplication(sys.argv)
    
    # Aplicar tema mixto
    app.setPalette(Theme.get_palette("mixed"))
    app.setStyleSheet(Theme.get_stylesheet("mixed"))
    
    # Crear y mostrar ventana
    demo = AgentMonitorDemo()
    demo.show()
    
    print("Ventana de demostración creada y mostrada.")
    print("Presiona Ctrl+C en esta ventana para cerrar la aplicación.")
    
    # Ejecutar aplicación
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
