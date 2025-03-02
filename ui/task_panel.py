from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, 
    QTextEdit, QPushButton, QListWidget, QFormLayout, 
    QComboBox, QMessageBox, QInputDialog
)
import yaml
import os
import sys

# Ensure models module is accessible
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
if parent_dir not in sys.path:
    sys.path.append(parent_dir)

from models.task_model import TaskModel

class TaskPanel(QWidget):
    def __init__(self):
        super().__init__()
        self.tasks = {}
        self.agents = {}
        self.available_agents = []  # Added for state management
        self.init_ui()
        
    def init_ui(self):
        layout = QHBoxLayout(self)
        
        # Left panel - Task list
        left_panel = QWidget()
        left_layout = QVBoxLayout(left_panel)
        
        self.task_list = QListWidget()
        self.task_list.itemClicked.connect(self.load_task)
        
        left_layout.addWidget(QLabel("Tasks:"))
        left_layout.addWidget(self.task_list)
        
        button_layout = QHBoxLayout()
        self.add_button = QPushButton("Add Task")
        self.delete_button = QPushButton("Delete Task")
        self.add_button.clicked.connect(self.add_task)
        self.delete_button.clicked.connect(self.delete_task)
        
        button_layout.addWidget(self.add_button)
        button_layout.addWidget(self.delete_button)
        left_layout.addLayout(button_layout)
        
        # Right panel - Task details
        right_panel = QWidget()
        self.right_layout = QFormLayout(right_panel)
        
        self.task_name = QLineEdit()
        self.task_description = QTextEdit()
        self.task_expected_output = QTextEdit()
        self.task_agent = QComboBox()
        self.task_output_file = QLineEdit()
        
        self.right_layout.addRow("Name:", self.task_name)
        self.right_layout.addRow("Description:", self.task_description)
        self.right_layout.addRow("Expected Output:", self.task_expected_output)
        self.right_layout.addRow("Agent:", self.task_agent)
        self.right_layout.addRow("Output File:", self.task_output_file)
        
        # Save button
        self.save_task_button = QPushButton("Save Task")
        self.save_task_button.clicked.connect(self.save_current_task)
        self.right_layout.addRow(self.save_task_button)
        
        # Add panels to main layout
        layout.addWidget(left_panel, 1)
        layout.addWidget(right_panel, 2)
        
        # Load existing tasks
        self.load_tasks()
        
    def add_task(self):
        name, ok = QInputDialog.getText(self, "Add Task", "Task Name:")
        if ok and name:
            if name in self.tasks:
                QMessageBox.warning(self, "Warning", "Task with this name already exists")
                return
                
            self.tasks[name] = TaskModel(name=name)
            self.task_list.addItem(name)
            self.clear_form()
            self.task_name.setText(name)
    
    def delete_task(self):
        current_item = self.task_list.currentItem()
        if current_item:
            name = current_item.text()
            confirm = QMessageBox.question(
                self, "Confirm Deletion", 
                f"Are you sure you want to delete task '{name}'?",
                QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
            )
            
            if confirm == QMessageBox.StandardButton.Yes:
                self.tasks.pop(name, None)
                self.task_list.takeItem(self.task_list.row(current_item))
                self.clear_form()
    
    def load_task(self, item):
        name = item.text()
        if name in self.tasks:
            task = self.tasks[name]
            self.task_name.setText(task.name)
            self.task_description.setText(task.description)
            self.task_expected_output.setText(task.expected_output)
            self.task_output_file.setText(task.output_file)
            
            # Set agent if available
            if task.agent:
                index = self.task_agent.findText(task.agent)
                if index >= 0:
                    self.task_agent.setCurrentIndex(index)
    
    def save_current_task(self):
        name = self.task_name.text()
        if not name:
            QMessageBox.warning(self, "Warning", "Task name cannot be empty")
            return
            
        task = TaskModel(
            name=name,
            description=self.task_description.toPlainText(),
            expected_output=self.task_expected_output.toPlainText(),
            agent=self.task_agent.currentText(),
            output_file=self.task_output_file.text()
        )
        
        # Update or add task
        self.tasks[name] = task
        
        # Update list if it's a new task
        found = False
        for i in range(self.task_list.count()):
            if self.task_list.item(i).text() == name:
                found = True
                break
        
        if not found:
            self.task_list.addItem(name)
            
        QMessageBox.information(self, "Success", f"Task '{name}' saved successfully")
    
    def clear_form(self):
        self.task_name.clear()
        self.task_description.clear()
        self.task_expected_output.clear()
        self.task_agent.setCurrentIndex(0)
        self.task_output_file.clear()
    
    def update_agents(self, agents):
        self.agents = agents
        current_agent = self.task_agent.currentText()
        
        self.task_agent.clear()
        self.task_agent.addItem("")  # Empty option
        
        for agent_name in agents.keys():
            self.task_agent.addItem(agent_name)
        
        # Restore selection if possible
        if current_agent:
            index = self.task_agent.findText(current_agent)
            if index >= 0:
                self.task_agent.setCurrentIndex(index)
    
    def save_tasks(self):
        # Convert tasks to YAML format
        tasks_dict = {}
        for name, task in self.tasks.items():
            tasks_dict[name] = {
                "description": task.description,
                "expected_output": task.expected_output,
                "agent": task.agent,
                "output_file": task.output_file
            }
        
        # Ensure config directory exists
        os.makedirs("config", exist_ok=True)
        
        # Save to YAML file
        with open("config/tasks.yaml", "w") as f:
            yaml.dump(tasks_dict, f)
    
    def load_tasks(self):
        try:
            if os.path.exists("config/tasks.yaml"):
                with open("config/tasks.yaml", "r") as f:
                    tasks_dict = yaml.safe_load(f)
                
                if tasks_dict:
                    self.tasks = {}
                    self.task_list.clear()
                    
                    for name, data in tasks_dict.items():
                        task = TaskModel(
                            name=name,
                            description=data.get("description", ""),
                            expected_output=data.get("expected_output", ""),
                            agent=data.get("agent", ""),
                            output_file=data.get("output_file", "")
                        )
                        
                        self.tasks[name] = task
                        self.task_list.addItem(name)
        except Exception as e:
            QMessageBox.warning(self, "Warning", f"Failed to load tasks: {str(e)}")

    def update_agents_from_state(self, agents_state):
        """
        Actualiza la lista de agentes disponibles desde el estado global.
        
        Args:
            agents_state (dict): Estado de los agentes desde el gestor de estado
        """
        if not agents_state:
            return
            
        # Limpiar la lista actual de agentes
        self.available_agents = []
        
        # Añadir agentes desde el estado
        for agent_id, agent_data in agents_state.items():
            agent = {
                "id": agent_id,
                "name": agent_data.get("name", "Sin nombre"),
                "role": agent_data.get("role", "Sin rol")
            }
            self.available_agents.append(agent)
        
        # Actualizar los selectores de agentes en las tareas existentes
        self.update_agent_selectors()

    def update_agent_selectors(self):
        """
        Actualiza los selectores de agentes con la lista actual de agentes disponibles.
        """
        current_agent = self.task_agent.currentText()
        
        self.task_agent.clear()
        self.task_agent.addItem("")  # Empty option
        
        for agent in self.available_agents:
            self.task_agent.addItem(agent["name"])
        
        # Restore selection if possible
        if current_agent:
            index = self.task_agent.findText(current_agent)
            if index >= 0:
                self.task_agent.setCurrentIndex(index)

    def update_from_state(self, tasks_state):
        """
        Actualiza el panel de tareas desde el estado global.
        
        Args:
            tasks_state (dict): Estado de las tareas desde el gestor de estado
        """
        if not tasks_state:
            return
            
        # Limpiar la lista actual
        self.tasks = {}
        self.task_list.clear()
        
        # Añadir tareas desde el estado
        for task_id, task_data in tasks_state.items():
            task = TaskModel(
                name=task_data.get("name", "Sin nombre"),
                description=task_data.get("description", ""),
                expected_output=task_data.get("output_format", ""),
                agent=task_data.get("agent_id", ""),
                output_file=task_data.get("output_file", "")
            )
            
            self.tasks[task.name] = task
            self.task_list.addItem(task.name)
        
        # Actualizar la interfaz
        if self.tasks:
            self.task_list.setCurrentRow(0)
            self.load_task(self.task_list.item(0))
        else:
            self.clear_form()

    def display_task(self, index):
        """
        Muestra los detalles de una tarea en el formulario.
        
        Args:
            index (int): Índice de la tarea en la lista
        """
        if 0 <= index < len(self.tasks):
            task_name = self.task_list.item(index).text()
            self.load_task(self.task_list.item(index))
