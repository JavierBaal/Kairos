from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, 
    QTextEdit, QPushButton, QListWidget, QFormLayout, 
    QComboBox, QMessageBox, QInputDialog, QCheckBox,
    QListWidgetItem, QDialog, QDialogButtonBox, QTabWidget
)
from PyQt6.QtCore import Qt, pyqtSignal
import yaml
import os
import sys
import uuid

# Ensure modules are accessible
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
if parent_dir not in sys.path:
    sys.path.append(parent_dir)

from langchain_integration.team_manager import TeamManager
from langchain_integration.agent_factory import AgentFactory

class SelectAgentsDialog(QDialog):
    def __init__(self, available_agents, selected_agents=None):
        super().__init__()
        self.setWindowTitle("Seleccionar Agentes")
        self.resize(500, 400)
        
        layout = QVBoxLayout(self)
        
        # Lista de agentes disponibles
        self.agent_list = QListWidget()
        self.agent_list.setSelectionMode(QListWidget.SelectionMode.MultiSelection)
        
        # Añadir agentes a la lista
        for agent_id, agent_data in available_agents.items():
            agent_name = agent_data.get("name", "Sin nombre")
            agent_role = agent_data.get("role", "Sin rol")
            item = QListWidgetItem(f"{agent_name} ({agent_role})")
            item.setData(Qt.ItemDataRole.UserRole, agent_id)
            self.agent_list.addItem(item)
            
            # Seleccionar agentes previamente seleccionados
            if selected_agents and agent_id in selected_agents:
                item.setSelected(True)
        
        layout.addWidget(QLabel("Selecciona los agentes para este equipo:"))
        layout.addWidget(self.agent_list)
        
        # Botones
        button_box = QDialogButtonBox(QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel)
        button_box.accepted.connect(self.accept)
        button_box.rejected.connect(self.reject)
        layout.addWidget(button_box)
    
    def get_selected_agents(self):
        selected = []
        for i in range(self.agent_list.count()):
            item = self.agent_list.item(i)
            if item.isSelected():
                agent_id = item.data(Qt.ItemDataRole.UserRole)
                selected.append(agent_id)
        return selected

class LangChainTeamPanel(QWidget):
    team_executed = pyqtSignal(str, dict)  # Señal para cuando se ejecuta un equipo
    
    def __init__(self, state_manager):
        super().__init__()
        self.state_manager = state_manager
        self.team_manager = TeamManager()
        self.agent_factory = AgentFactory()
        self.teams = {}
        self.init_ui()
        
    def init_ui(self):
        layout = QHBoxLayout(self)
        
        # Panel izquierdo - Lista de equipos
        left_panel = QWidget()
        left_layout = QVBoxLayout(left_panel)
        
        self.team_list = QListWidget()
        self.team_list.itemClicked.connect(self.load_team)
        
        left_layout.addWidget(QLabel("Equipos:"))
        left_layout.addWidget(self.team_list)
        
        button_layout = QHBoxLayout()
        self.add_button = QPushButton("Nuevo Equipo")
        self.delete_button = QPushButton("Eliminar Equipo")
        self.add_button.clicked.connect(self.add_team)
        self.delete_button.clicked.connect(self.delete_team)
        
        button_layout.addWidget(self.add_button)
        button_layout.addWidget(self.delete_button)
        left_layout.addLayout(button_layout)
        
        # Panel derecho - Detalles del equipo
        right_panel = QTabWidget()
        
        # Pestaña de configuración
        config_tab = QWidget()
        self.config_layout = QFormLayout(config_tab)
        
        self.team_name = QLineEdit()
        self.team_description = QTextEdit()
        
        self.select_agents_button = QPushButton("Seleccionar Agentes")
        self.select_agents_button.clicked.connect(self.select_agents)
        self.agents_label = QLabel("No hay agentes seleccionados")
        
        self.team_type = QComboBox()
        self.team_type.addItems(["Secuencial", "Jerárquico", "Colaborativo"])
        
        self.verbose_checkbox = QCheckBox("Mostrar detalles de ejecución")
        self.verbose_checkbox.setChecked(True)
        
        self.config_layout.addRow("Nombre:", self.team_name)
        self.config_layout.addRow("Descripción:", self.team_description)
        self.config_layout.addRow("Agentes:", self.select_agents_button)
        self.config_layout.addRow("", self.agents_label)
        self.config_layout.addRow("Tipo de equipo:", self.team_type)
        self.config_layout.addRow(self.verbose_checkbox)
        
        # Botones de guardar y ejecutar
        button_layout = QHBoxLayout()
        self.save_button = QPushButton("Guardar Equipo")
        self.run_button = QPushButton("Ejecutar Equipo")
        self.save_button.clicked.connect(self.save_team)
        self.run_button.clicked.connect(self.run_team)
        
        button_layout.addWidget(self.save_button)
        button_layout.addWidget(self.run_button)
        self.config_layout.addRow(button_layout)
        
        # Pestaña de objetivos
        objectives_tab = QWidget()
        objectives_layout = QVBoxLayout(objectives_tab)
        
        self.objective_text = QTextEdit()
        self.objective_text.setPlaceholderText("Describe el objetivo principal del equipo...")
        
        objectives_layout.addWidget(QLabel("Objetivo del equipo:"))
        objectives_layout.addWidget(self.objective_text)
        
        # Pestaña de resultados
        results_tab = QWidget()
        results_layout = QVBoxLayout(results_tab)
        
        self.results_text = QTextEdit()
        self.results_text.setReadOnly(True)
        
        results_layout.addWidget(QLabel("Resultados:"))
        results_layout.addWidget(self.results_text)
        
        # Añadir pestañas
        right_panel.addTab(config_tab, "Configuración")
        right_panel.addTab(objectives_tab, "Objetivos")
        right_panel.addTab(results_tab, "Resultados")
        
        # Añadir paneles al layout principal
        layout.addWidget(left_panel, 1)
        layout.addWidget(right_panel, 2)
        
        # Cargar equipos existentes
        self.load_teams()
        
    def add_team(self):
        name, ok = QInputDialog.getText(self, "Nuevo Equipo", "Nombre del equipo:")
        if ok and name:
            if name in self.teams:
                QMessageBox.warning(self, "Advertencia", "Ya existe un equipo con este nombre")
                return
                
            team_id = str(uuid.uuid4())
            self.teams[team_id] = {
                "id": team_id,
                "name": name,
                "description": "",
                "agents": [],
                "type": "Secuencial",
                "verbose": True,
                "objective": "",
                "results": ""
            }
            
            item = QListWidgetItem(name)
            item.setData(Qt.ItemDataRole.UserRole, team_id)
            self.team_list.addItem(item)
            self.clear_form()
            self.team_name.setText(name)
            
            # Actualizar el estado global
            self.update_state()
    
    def delete_team(self):
        current_item = self.team_list.currentItem()
        if current_item:
            team_id = current_item.data(Qt.ItemDataRole.UserRole)
            team_name = current_item.text()
            
            confirm = QMessageBox.question(
                self, "Confirmar eliminación", 
                f"¿Estás seguro de que deseas eliminar el equipo '{team_name}'?",
                QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
            )
            
            if confirm == QMessageBox.StandardButton.Yes:
                self.teams.pop(team_id, None)
                self.team_list.takeItem(self.team_list.row(current_item))
                self.clear_form()
                
                # Actualizar el estado global
                self.update_state()
    
    def load_team(self, item):
        team_id = item.data(Qt.ItemDataRole.UserRole)
        if team_id in self.teams:
            team = self.teams[team_id]
            
            self.team_name.setText(team["name"])
            self.team_description.setText(team["description"])
            
            # Actualizar etiqueta de agentes
            agents = team["agents"]
            if agents:
                agent_names = []
                for agent_id in agents:
                    agent_state = self.state_manager.get_state("agents", {})
                    if agent_id in agent_state:
                        agent_names.append(agent_state[agent_id].get("name", "Sin nombre"))
                
                self.agents_label.setText(", ".join(agent_names))
            else:
                self.agents_label.setText("No hay agentes seleccionados")
            
            # Establecer tipo de equipo
            index = self.team_type.findText(team["type"])
            if index >= 0:
                self.team_type.setCurrentIndex(index)
            
            # Establecer verbose
            self.verbose_checkbox.setChecked(team["verbose"])
            
            # Establecer objetivo
            self.objective_text.setText(team["objective"])
            
            # Establecer resultados
            self.results_text.setText(team["results"])
    
    def select_agents(self):
        agents_state = self.state_manager.get_state("agents", {})
        if not agents_state:
            QMessageBox.warning(self, "Advertencia", "No hay agentes disponibles. Por favor, crea agentes primero.")
            return
        
        current_item = self.team_list.currentItem()
        if not current_item:
            QMessageBox.warning(self, "Advertencia", "Por favor, selecciona un equipo primero.")
            return
            
        team_id = current_item.data(Qt.ItemDataRole.UserRole)
        team = self.teams[team_id]
        
        dialog = SelectAgentsDialog(agents_state, team["agents"])
        if dialog.exec() == QDialog.DialogCode.Accepted:
            selected_agents = dialog.get_selected_agents()
            team["agents"] = selected_agents
            
            # Actualizar etiqueta de agentes
            agent_names = []
            for agent_id in selected_agents:
                if agent_id in agents_state:
                    agent_names.append(agents_state[agent_id].get("name", "Sin nombre"))
            
            if agent_names:
                self.agents_label.setText(", ".join(agent_names))
            else:
                self.agents_label.setText("No hay agentes seleccionados")
            
            # Actualizar el estado global
            self.update_state()
    
    def save_team(self):
        current_item = self.team_list.currentItem()
        if not current_item:
            QMessageBox.warning(self, "Advertencia", "Por favor, selecciona un equipo primero.")
            return
            
        team_id = current_item.data(Qt.ItemDataRole.UserRole)
        team = self.teams[team_id]
        
        # Actualizar datos del equipo
        team["name"] = self.team_name.text()
        team["description"] = self.team_description.toPlainText()
        team["type"] = self.team_type.currentText()
        team["verbose"] = self.verbose_checkbox.isChecked()
        team["objective"] = self.objective_text.toPlainText()
        
        # Actualizar el nombre en la lista si ha cambiado
        if current_item.text() != team["name"]:
            current_item.setText(team["name"])
        
        # Actualizar el estado global
        self.update_state()
        
        QMessageBox.information(self, "Éxito", f"Equipo '{team['name']}' guardado correctamente")
    
    def clear_form(self):
        """Limpia el formulario de equipo"""
        self.team_name.clear()
        self.team_description.clear()
        self.agents_label.setText("No hay agentes seleccionados")
        self.team_type.setCurrentIndex(0)
        self.verbose_checkbox.setChecked(True)
        self.objective_text.clear()
        self.results_text.clear()
    
    def run_team(self):
        """Ejecuta el equipo seleccionado usando LangChain"""
        current_item = self.team_list.currentItem()
        if not current_item:
            QMessageBox.warning(self, "Advertencia", "Por favor, selecciona un equipo primero.")
            return
        
        team_id = current_item.data(Qt.ItemDataRole.UserRole)
        team = self.teams[team_id]
        
        # Verificar que el equipo tenga agentes
        if not team["agents"]:
            QMessageBox.warning(self, "Advertencia", "El equipo debe tener al menos un agente.")
            return
        
        # Verificar que el equipo tenga un objetivo
        if not team["objective"]:
            QMessageBox.warning(self, "Advertencia", "Por favor, define un objetivo para el equipo.")
            return
        
        try:
            # Mostrar mensaje de ejecución
            QMessageBox.information(self, "Ejecución iniciada", 
                                   f"El equipo '{team['name']}' ha comenzado a trabajar en el objetivo.")
            
            # Crear agentes LangChain desde los IDs de agentes
            langchain_agents = []
            agents_state = self.state_manager.get_state("agents", {})
            
            for agent_id in team["agents"]:
                if agent_id in agents_state:
                    agent_data = agents_state[agent_id]
                    langchain_agent = self.agent_factory.create_agent(
                        name=agent_data.get("name", ""),
                        role=agent_data.get("role", ""),
                        model=agent_data.get("model", "gpt-3.5-turbo"),
                        tools=agent_data.get("tools", []),
                        temperature=agent_data.get("temperature", 0.7)
                    )
                    langchain_agents.append(langchain_agent)
            
            # Ejecutar el equipo con LangChain
            team_type = team["type"].lower()
            verbose = team["verbose"]
            objective = team["objective"]
            
            # Ejecutar según el tipo de equipo
            if team_type == "secuencial":
                result = self.team_manager.run_sequential_team(
                    agents=langchain_agents,
                    objective=objective,
                    verbose=verbose
                )
            elif team_type == "jerárquico":
                result = self.team_manager.run_hierarchical_team(
                    agents=langchain_agents,
                    objective=objective,
                    verbose=verbose
                )
            elif team_type == "colaborativo":
                result = self.team_manager.run_collaborative_team(
                    agents=langchain_agents,
                    objective=objective,
                    verbose=verbose
                )
            
            # Guardar resultados
            team["results"] = result
            self.results_text.setText(result)
            
            # Actualizar el estado global
            self.update_state()
            
            # Emitir señal de ejecución completada
            self.team_executed.emit(team_id, {"result": result})
            
            QMessageBox.information(self, "Ejecución completada", 
                                   f"El equipo '{team['name']}' ha completado el objetivo.")
            
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Error al ejecutar el equipo: {str(e)}")
            error_message = f"Error durante la ejecución: {str(e)}"
            team["results"] = error_message
            self.results_text.setText(error_message)
    
    def update_state(self):
        """Actualiza el estado global con los equipos actuales"""
        self.state_manager.update_state("teams", self.teams)
    
    def load_teams(self):
        """Carga los equipos desde el estado global"""
        teams_state = self.state_manager.get_state("teams", {})
        if teams_state:
            self.teams = teams_state
            self.team_list.clear()
            
            for team_id, team_data in self.teams.items():
                item = QListWidgetItem(team_data["name"])
                item.setData(Qt.ItemDataRole.UserRole, team_id)
                self.team_list.addItem(item)
    
    def update_from_state(self, teams_state):
        """Actualiza el panel desde el estado global"""
        if teams_state:
            self.teams = teams_state
            self.team_list.clear()
            
            for team_id, team_data in self.teams.items():
                item = QListWidgetItem(team_data["name"])
                item.setData(Qt.ItemDataRole.UserRole, team_id)
                self.team_list.addItem(item)