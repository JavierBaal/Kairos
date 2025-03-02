#!/usr/bin/env python3
"""
Kairos Intelligence System - Demo de Monitorización de Agentes LangChain
Este script muestra cómo utilizar el sistema de monitorización con agentes de LangChain.
"""

import sys
import os
import time
import threading
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QVBoxLayout, QWidget, QLabel, QPushButton, QHBoxLayout,
    QDialog, QLineEdit, QFormLayout, QDialogButtonBox, QMessageBox
)
from PyQt6.QtCore import Qt, pyqtSlot, QTimer, pyqtSignal

# Asegurarse de que podemos importar desde el directorio padre
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from ui.theme import Theme
from ui.agent_monitor import AgentMonitorPanel
from langchain_integration.agent_monitor_adapter import get_monitor_manager, create_monitored_kairos_agent
from langchain_prototype.agent_example import search_web, read_file, write_file, KairosTask, KairosCrew

class LangChainMonitorDemo(QMainWindow):
    """Ventana de demostración para la monitorización de agentes LangChain."""
    
    # Señales para actualizar la UI desde el hilo de simulación
    update_status_signal = pyqtSignal(str, str)
    update_progress_signal = pyqtSignal(str, int)
    update_tokens_signal = pyqtSignal(str, int)
    update_cost_signal = pyqtSignal(str, float)
    simulation_finished_signal = pyqtSignal()
    add_agent_signal = pyqtSignal(str, str, str)
    
    def __init__(self):
        super().__init__()
        
        # Conectar señales con slots
        self.update_status_signal.connect(self.update_agent_status)
        self.update_progress_signal.connect(self.update_agent_progress)
        self.update_tokens_signal.connect(self.update_agent_tokens)
        self.update_cost_signal.connect(self.update_agent_cost)
        self.simulation_finished_signal.connect(self.on_simulation_finished)
        self.add_agent_signal.connect(self.add_agent_monitor)
        
        # Configurar la ventana
        self.setWindowTitle("Kairos - Monitorización de Agentes LangChain")
        self.resize(1200, 800)
        
        # Crear widget central
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # Crear layout principal
        main_layout = QVBoxLayout(central_widget)
        
        # Título
        title_label = QLabel("Kairos Intelligence System - Monitorización de Agentes LangChain")
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title_label.setStyleSheet("font-size: 24px; font-weight: bold; color: white; margin: 20px;")
        main_layout.addWidget(title_label)
        
        # Botones de control
        control_layout = QHBoxLayout()
        
        self.start_button = QPushButton("Iniciar Simulación")
        self.start_button.setObjectName("primaryButton")
        self.start_button.clicked.connect(self.start_simulation)
        control_layout.addWidget(self.start_button)
        
        self.set_limit_button = QPushButton("Establecer Límite de Costo")
        self.set_limit_button.clicked.connect(self.set_cost_limit)
        control_layout.addWidget(self.set_limit_button)
        
        main_layout.addLayout(control_layout)
        
        # Crear panel de monitorización
        self.monitor_panel = AgentMonitorPanel()
        main_layout.addWidget(self.monitor_panel)
        
        # Obtener gestor de monitorización y configurarlo
        self.monitor_manager = get_monitor_manager()
        self.monitor_manager.set_ui_panel(self.monitor_panel)
        
        # Inicializar variables
        self.simulation_running = False
        self.simulation_thread = None
    
    @pyqtSlot()
    def start_simulation(self):
        """Iniciar la simulación de agentes LangChain."""
        if self.simulation_running:
            return
        
        self.simulation_running = True
        self.start_button.setText("Simulación en Curso...")
        self.start_button.setEnabled(False)
        
        # Crear los agentes en el hilo principal antes de iniciar la simulación
        self.setup_agents()
        
        # Crear y ejecutar la simulación en un hilo separado
        self.simulation_thread = threading.Thread(target=self.run_simulation)
        self.simulation_thread.daemon = True
        self.simulation_thread.start()
    
    def setup_agents(self):
        """Configurar los agentes en el hilo principal."""
        # Crear los monitores de agentes en el hilo principal
        self.add_agent_monitor("researcher", "Alex", "Investigador de mercado")
        self.add_agent_monitor("writer", "Sam", "Redactor de contenido")
        self.add_agent_monitor("analyst", "Taylor", "Analista de datos")
    
    @pyqtSlot()
    def set_cost_limit(self):
        """Establecer un límite de costo para la simulación."""
        # Crear un diálogo para ingresar el límite
        dialog = QDialog(self)
        dialog.setWindowTitle("Establecer Límite de Costo")
        dialog.setMinimumWidth(300)
        
        # Crear layout
        layout = QFormLayout(dialog)
        
        # Crear campo de entrada
        cost_input = QLineEdit()
        cost_input.setPlaceholderText("Ejemplo: 2.0")
        layout.addRow("Límite de costo ($):", cost_input)
        
        # Crear botones
        button_box = QDialogButtonBox(
            QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel
        )
        button_box.accepted.connect(dialog.accept)
        button_box.rejected.connect(dialog.reject)
        layout.addRow(button_box)
        
        # Mostrar diálogo
        if dialog.exec() == QDialog.DialogCode.Accepted:
            try:
                cost_limit = float(cost_input.text())
                if cost_limit <= 0:
                    raise ValueError("El límite debe ser mayor que cero")
                
                # Establecer límite
                self.monitor_manager.set_cost_limit(cost_limit)
                
                # Mostrar mensaje de confirmación
                QMessageBox.information(
                    self,
                    "Límite Establecido",
                    f"Se ha establecido un límite de costo de ${cost_limit:.2f}."
                )
            except ValueError as e:
                # Mostrar mensaje de error
                QMessageBox.warning(
                    self,
                    "Error",
                    f"Por favor, ingrese un número válido mayor que cero. Error: {str(e)}"
                )
    
    def run_simulation(self):
        """Ejecutar la simulación de agentes LangChain."""
        try:
            # En una aplicación real, aquí crearíamos agentes reales de LangChain
            # Para esta demostración, solo simularemos la actividad sin necesidad de API key
            
            # Nota: Para crear agentes reales, descomentar el siguiente código y configurar la API key
            """
            researcher = create_monitored_kairos_agent(
                name="Alex",
                role="Investigador de mercado",
                goal="Encontrar información relevante sobre tendencias de mercado",
                backstory="Tienes años de experiencia analizando datos de mercado y tendencias.",
                verbose=True,
                tools=[search_web],
                llm_model="gpt-3.5-turbo",
                agent_id="researcher"
            )
            
            writer = create_monitored_kairos_agent(
                name="Sam",
                role="Redactor de contenido",
                goal="Crear contenido persuasivo basado en datos de investigación",
                backstory="Eres un escritor experimentado especializado en marketing.",
                verbose=True,
                tools=[read_file, write_file],
                llm_model="gpt-3.5-turbo",
                agent_id="writer"
            )
            
            analyst = create_monitored_kairos_agent(
                name="Taylor",
                role="Analista de datos",
                goal="Analizar datos y extraer insights valiosos",
                backstory="Eres un experto en análisis de datos con experiencia en visualización.",
                verbose=True,
                tools=[read_file],
                llm_model="gpt-3.5-turbo",
                agent_id="analyst"
            )
            """
            
            # En una aplicación real, estos agentes ejecutarían tareas reales
            # Para esta demostración, simularemos su actividad
            
            # Simular actividad del investigador
            self.simulate_agent_activity(
                agent_id="researcher",
                name="Alex",
                role="Investigador de mercado",
                steps=[
                    {"status": "Iniciando investigación de mercado...", "progress": 5, "tokens": 100, "cost": 0.02},
                    {"status": "Buscando tendencias actuales...", "progress": 15, "tokens": 300, "cost": 0.06},
                    {"status": "Analizando resultados de búsqueda...", "progress": 30, "tokens": 600, "cost": 0.12},
                    {"status": "Recopilando datos relevantes...", "progress": 50, "tokens": 1200, "cost": 0.24},
                    {"status": "Organizando información encontrada...", "progress": 75, "tokens": 1800, "cost": 0.36},
                    {"status": "Finalizando informe de investigación...", "progress": 90, "tokens": 2200, "cost": 0.44},
                    {"status": "Investigación completada", "progress": 100, "tokens": 2500, "cost": 0.50}
                ]
            )
            
            # Simular actividad del redactor
            self.simulate_agent_activity(
                agent_id="writer",
                name="Sam",
                role="Redactor de contenido",
                steps=[
                    {"status": "Revisando datos de investigación...", "progress": 5, "tokens": 150, "cost": 0.03},
                    {"status": "Planificando estructura del contenido...", "progress": 20, "tokens": 400, "cost": 0.08},
                    {"status": "Redactando introducción...", "progress": 35, "tokens": 800, "cost": 0.16},
                    {"status": "Desarrollando argumentos principales...", "progress": 55, "tokens": 1500, "cost": 0.30},
                    {"status": "Añadiendo ejemplos y casos de estudio...", "progress": 70, "tokens": 2000, "cost": 0.40},
                    {"status": "Redactando conclusiones...", "progress": 85, "tokens": 2400, "cost": 0.48},
                    {"status": "Revisando y puliendo el texto...", "progress": 95, "tokens": 2700, "cost": 0.54},
                    {"status": "Contenido completado", "progress": 100, "tokens": 3000, "cost": 0.60}
                ]
            )
            
            # Simular actividad del analista
            self.simulate_agent_activity(
                agent_id="analyst",
                name="Taylor",
                role="Analista de datos",
                steps=[
                    {"status": "Preparando herramientas de análisis...", "progress": 5, "tokens": 120, "cost": 0.024},
                    {"status": "Importando datos para análisis...", "progress": 15, "tokens": 350, "cost": 0.07},
                    {"status": "Limpiando y normalizando datos...", "progress": 30, "tokens": 700, "cost": 0.14},
                    {"status": "Realizando análisis estadístico...", "progress": 50, "tokens": 1300, "cost": 0.26},
                    {"status": "Identificando patrones y tendencias...", "progress": 65, "tokens": 1800, "cost": 0.36},
                    {"status": "Generando visualizaciones...", "progress": 80, "tokens": 2200, "cost": 0.44},
                    {"status": "Preparando informe de insights...", "progress": 90, "tokens": 2500, "cost": 0.50},
                    {"status": "Análisis completado", "progress": 100, "tokens": 2800, "cost": 0.56}
                ]
            )
            
        except Exception as e:
            print(f"Error en la simulación: {str(e)}")
        finally:
            # Emitir señal para restablecer estado de la UI
            self.simulation_finished_signal.emit()
    
    def simulate_agent_activity(self, agent_id, name, role, steps):
        """
        Simular la actividad de un agente con pasos predefinidos.
        
        Args:
            agent_id: ID del agente
            name: Nombre del agente
            role: Rol del agente
            steps: Lista de pasos con estado, progreso, tokens y costo
        """
        
        # Simular cada paso
        for step in steps:
            # Verificar si la simulación debe detenerse
            if not self.simulation_running:
                break
            
            # Emitir señales para actualizar métricas en el hilo principal
            self.update_status_signal.emit(agent_id, step["status"])
            self.update_progress_signal.emit(agent_id, step["progress"])
            self.update_tokens_signal.emit(agent_id, step["tokens"])
            self.update_cost_signal.emit(agent_id, step["cost"])
            
            # Pausa entre pasos
            time.sleep(2)
    
    @pyqtSlot(str, str, str)
    def add_agent_monitor(self, agent_id, name, role):
        """Añadir un monitor de agente al panel."""
        if agent_id not in self.monitor_panel.agent_monitors:
            self.monitor_panel.add_agent_monitor(agent_id, name, role)
    
    @pyqtSlot(str, str)
    def update_agent_status(self, agent_id, status):
        """Actualizar el estado de un agente."""
        if agent_id in self.monitor_panel.agent_monitors:
            self.monitor_panel.update_agent_status(agent_id, status)
    
    @pyqtSlot(str, int)
    def update_agent_progress(self, agent_id, progress):
        """Actualizar el progreso de un agente."""
        if agent_id in self.monitor_panel.agent_monitors:
            self.monitor_panel.update_agent_progress(agent_id, progress)
    
    @pyqtSlot(str, int)
    def update_agent_tokens(self, agent_id, tokens):
        """Actualizar los tokens de un agente."""
        if agent_id in self.monitor_panel.agent_monitors:
            self.monitor_panel.update_agent_tokens(agent_id, tokens)
    
    @pyqtSlot(str, float)
    def update_agent_cost(self, agent_id, cost):
        """Actualizar el costo de un agente."""
        if agent_id in self.monitor_panel.agent_monitors:
            self.monitor_panel.update_agent_cost(agent_id, cost)
    
    @pyqtSlot()
    def on_simulation_finished(self):
        """Manejar la finalización de la simulación."""
        self.simulation_running = False
        self.start_button.setText("Iniciar Simulación")
        self.start_button.setEnabled(True)


def main():
    """Función principal."""
    print("Iniciando demostración de monitorización de agentes LangChain...")
    print("Si no ves una ventana, verifica que no esté minimizada o detrás de otras ventanas.")
    
    # Crear aplicación
    app = QApplication(sys.argv)
    
    # Aplicar tema mixto
    app.setPalette(Theme.get_palette("mixed"))
    app.setStyleSheet(Theme.get_stylesheet("mixed"))
    
    # Crear y mostrar ventana
    demo = LangChainMonitorDemo()
    demo.show()
    
    print("Ventana de demostración creada y mostrada.")
    print("Presiona Ctrl+C en esta ventana para cerrar la aplicación.")
    
    # Ejecutar aplicación
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
