from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
    QPushButton, QListWidget, QTextEdit, QMessageBox,
    QDialog, QGroupBox, QScrollArea
)
from PyQt6.QtCore import Qt, pyqtSignal
from models.template_model import TemplateModel

class TemplateDetailsDialog(QDialog):
    """Diálogo que muestra los detalles de una plantilla"""
    
    def __init__(self, template, parent=None):
        super().__init__(parent)
        self.template = template
        self.setWindowTitle(f"Plantilla: {template.name}")
        self.setMinimumSize(600, 500)
        self.init_ui()
        
    def init_ui(self):
        layout = QVBoxLayout(self)
        
        # Título y descripción
        title_label = QLabel(self.template.name)
        title_label.setStyleSheet("font-size: 18px; font-weight: bold;")
        
        desc_label = QLabel(self.template.description)
        desc_label.setWordWrap(True)
        
        # Scroll area para el contenido
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_content = QWidget()
        scroll_layout = QVBoxLayout(scroll_content)
        
        # Especialistas
        specialists_group = QGroupBox("Especialistas")
        specialists_layout = QVBoxLayout(specialists_group)
        
        for agent_id, agent_data in self.template.specialists.items():
            agent_widget = QWidget()
            agent_layout = QVBoxLayout(agent_widget)
            
            name_label = QLabel(agent_data.get("name", ""))
            name_label.setStyleSheet("font-weight: bold;")
            
            role_label = QLabel(agent_data.get("role", ""))
            role_label.setWordWrap(True)
            
            agent_layout.addWidget(name_label)
            agent_layout.addWidget(role_label)
            
            specialists_layout.addWidget(agent_widget)
        
        # Objetivos
        objectives_group = QGroupBox("Objetivos")
        objectives_layout = QVBoxLayout(objectives_group)
        
        for task_id, task_data in self.template.objectives.items():
            task_widget = QWidget()
            task_layout = QVBoxLayout(task_widget)
            
            name_label = QLabel(task_data.get("name", ""))
            name_label.setStyleSheet("font-weight: bold;")
            
            desc_label = QLabel(task_data.get("description", ""))
            desc_label.setWordWrap(True)
            
            task_layout.addWidget(name_label)
            task_layout.addWidget(desc_label)
            
            objectives_layout.addWidget(task_widget)
        
        # Instrucciones
        instructions_group = QGroupBox("Instrucciones de Uso")
        instructions_layout = QVBoxLayout(instructions_group)
        
        instructions_text = QTextEdit()
        instructions_text.setPlainText(self.template.instructions)
        instructions_text.setReadOnly(True)
        
        instructions_layout.addWidget(instructions_text)
        
        # Añadir grupos al layout del scroll
        scroll_layout.addWidget(specialists_group)
        scroll_layout.addWidget(objectives_group)
        scroll_layout.addWidget(instructions_group)
        
        scroll_area.setWidget(scroll_content)
        
        # Botones
        button_layout = QHBoxLayout()
        apply_button = QPushButton("Aplicar Plantilla")
        apply_button.setObjectName("primaryButton")
        apply_button.clicked.connect(self.accept)
        
        cancel_button = QPushButton("Cancelar")
        cancel_button.clicked.connect(self.reject)
        
        button_layout.addWidget(cancel_button)
        button_layout.addWidget(apply_button)
        
        # Añadir todo al layout principal
        layout.addWidget(title_label)
        layout.addWidget(desc_label)
        layout.addWidget(scroll_area, 1)  # 1 = stretch factor
        layout.addLayout(button_layout)


class TemplatePanel(QWidget):
    """Panel para gestionar y aplicar plantillas predefinidas"""
    
    template_applied = pyqtSignal(object)  # Señal emitida cuando se aplica una plantilla
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.templates = {}
        self.init_ui()
        self.load_templates()
        
    def init_ui(self):
        layout = QVBoxLayout(self)
        
        # Título
        title_label = QLabel("PLANTILLAS PREMIUM")
        title_label.setStyleSheet("font-size: 16px; font-weight: bold;")
        
        # Lista de plantillas
        self.template_list = QListWidget()
        self.template_list.itemDoubleClicked.connect(self.show_template_details)
        
        # Descripción de la plantilla seleccionada
        self.description_label = QLabel("Selecciona una plantilla para ver su descripción")
        self.description_label.setWordWrap(True)
        self.description_label.setStyleSheet("color: #a9b7c6; font-style: italic;")
        
        # Botones
        button_layout = QHBoxLayout()
        
        self.details_button = QPushButton("Ver Detalles")
        self.details_button.clicked.connect(self.show_template_details)
        
        self.apply_button = QPushButton("Aplicar Plantilla")
        self.apply_button.setObjectName("primaryButton")
        self.apply_button.clicked.connect(self.apply_selected_template)
        
        button_layout.addWidget(self.details_button)
        button_layout.addWidget(self.apply_button)
        
        # Añadir widgets al layout
        layout.addWidget(title_label)
        layout.addWidget(self.template_list, 1)  # 1 = stretch factor
        layout.addWidget(self.description_label)
        layout.addLayout(button_layout)
        
    def load_templates(self):
        """Carga las plantillas disponibles"""
        self.templates = TemplateModel.load_templates()
        self.template_list.clear()
        
        for template_id, template in self.templates.items():
            self.template_list.addItem(template.name)
            
        # Seleccionar la primera plantilla si hay alguna
        if self.template_list.count() > 0:
            self.template_list.setCurrentRow(0)
            self.update_description()
            
    def update_description(self):
        """Actualiza la descripción basada en la plantilla seleccionada"""
        current_item = self.template_list.currentItem()
        if current_item:
            template_name = current_item.text()
            for template in self.templates.values():
                if template.name == template_name:
                    self.description_label.setText(template.description)
                    return
        
        self.description_label.setText("Selecciona una plantilla para ver su descripción")
        
    def get_selected_template(self):
        """Obtiene la plantilla seleccionada"""
        current_item = self.template_list.currentItem()
        if current_item:
            template_name = current_item.text()
            for template in self.templates.values():
                if template.name == template_name:
                    return template
        
        return None
        
    def show_template_details(self):
        """Muestra los detalles de la plantilla seleccionada"""
        template = self.get_selected_template()
        if template:
            dialog = TemplateDetailsDialog(template, self)
            result = dialog.exec()
            
            if result == QDialog.DialogCode.Accepted:
                self.template_applied.emit(template)
        
    def apply_selected_template(self):
        """Aplica la plantilla seleccionada"""
        template = self.get_selected_template()
        if template:
            confirm = QMessageBox.question(
                self, "Confirmar Aplicación", 
                f"¿Estás seguro de que deseas aplicar la plantilla '{template.name}'?\n\n"
                "Esto reemplazará cualquier configuración existente.",
                QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
            )
            
            if confirm == QMessageBox.StandardButton.Yes:
                self.template_applied.emit(template)
