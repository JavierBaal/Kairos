from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
    QPushButton, QFrame, QScrollArea, QSizePolicy,
    QGridLayout, QGroupBox, QSpacerItem, QStackedWidget
)
from PyQt6.QtCore import Qt, QSize, pyqtSignal
from PyQt6.QtGui import QIcon, QPixmap, QColor, QPainter, QPen, QBrush
from ui.template_panel import TemplatePanel

class StepIndicator(QWidget):
    """Widget that displays a step in the workflow with number and label"""
    
    clicked = pyqtSignal(int)  # Signal emitted when step is clicked
    
    def __init__(self, step_number, step_name, is_active=False, is_completed=False, parent=None):
        super().__init__(parent)
        self.step_number = step_number
        self.step_name = step_name
        self.is_active = is_active
        self.is_completed = is_completed
        self.setObjectName("stepIndicator")
        self.init_ui()
        
    def init_ui(self):
        layout = QVBoxLayout(self)
        
        # Step number with circle
        self.number_label = QLabel(str(self.step_number))
        self.number_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.number_label.setFixedSize(36, 36)
        self.number_label.setStyleSheet(f"""
            background-color: {"#4dabf7" if self.is_active else "#3c3f41"};
            color: white;
            border-radius: 18px;
            font-weight: bold;
            font-size: 16px;
        """)
        
        # Step name
        self.name_label = QLabel(self.step_name)
        self.name_label.setObjectName("stepLabelActive" if self.is_active else "stepLabel")
        self.name_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        layout.addWidget(self.number_label, 0, Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.name_label, 0, Qt.AlignmentFlag.AlignCenter)
        
        # Make widget clickable
        self.setCursor(Qt.CursorShape.PointingHandCursor)
        
    def mousePressEvent(self, event):
        self.clicked.emit(self.step_number)
        super().mousePressEvent(event)
        
    def set_active(self, active):
        self.is_active = active
        self.number_label.setStyleSheet(f"""
            background-color: {"#4dabf7" if active else "#3c3f41"};
            color: white;
            border-radius: 18px;
            font-weight: bold;
            font-size: 16px;
        """)
        self.name_label.setObjectName("stepLabelActive" if active else "stepLabel")
        # Force style update
        self.name_label.setStyleSheet("")
        self.name_label.style().unpolish(self.name_label)
        self.name_label.style().polish(self.name_label)
        
    def set_completed(self, completed):
        self.is_completed = completed
        # Update styling for completed state
        # (could add a checkmark or different color)


class SpecialistCard(QFrame):
    """Card widget that displays a specialist with icon, name and description"""
    
    clicked = pyqtSignal(object)  # Signal emitted when card is clicked
    
    def __init__(self, specialist_data, parent=None):
        super().__init__(parent)
        self.specialist_data = specialist_data
        self.setObjectName("specialistCard")
        self.setFixedSize(200, 180)
        self.setCursor(Qt.CursorShape.PointingHandCursor)
        self.init_ui()
        
    def init_ui(self):
        layout = QVBoxLayout(self)
        
        # Specialist icon (placeholder for now)
        icon_label = QLabel()
        icon_label.setFixedSize(48, 48)
        icon_label.setStyleSheet("""
            background-color: #4dabf7;
            border-radius: 24px;
        """)
        
        # Specialist name
        name_label = QLabel(self.specialist_data.name)
        name_label.setObjectName("specialistTitle")
        
        # Specialist description (truncated role)
        role = self.specialist_data.role
        description = role[:80] + "..." if len(role) > 80 else role
        desc_label = QLabel(description)
        desc_label.setObjectName("specialistDescription")
        desc_label.setWordWrap(True)
        
        layout.addWidget(icon_label, 0, Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(name_label, 0, Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(desc_label, 1)
        
    def mousePressEvent(self, event):
        self.clicked.emit(self.specialist_data)
        super().mousePressEvent(event)


class SpecialistLibraryPanel(QWidget):
    """Panel that displays a library of available specialists"""
    
    specialist_selected = pyqtSignal(object)  # Signal emitted when specialist is selected
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.init_ui()
        
    def init_ui(self):
        layout = QVBoxLayout(self)
        
        # Title
        title = QLabel("ESPECIALISTAS")
        title.setStyleSheet("font-weight: bold; font-size: 16px;")
        
        # Scrollable area for specialists
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        
        # Container for specialist cards
        self.specialists_container = QWidget()
        self.specialists_layout = QVBoxLayout(self.specialists_container)
        
        scroll_area.setWidget(self.specialists_container)
        
        layout.addWidget(title)
        layout.addWidget(scroll_area)
        
    def add_specialist(self, specialist_data):
        """Add a specialist card to the library"""
        card = SpecialistCard(specialist_data)
        card.clicked.connect(lambda spec: self.specialist_selected.emit(spec))
        self.specialists_layout.addWidget(card)
        
    def clear(self):
        """Remove all specialists from the library"""
        while self.specialists_layout.count():
            item = self.specialists_layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()


class TeamBuildingPanel(QWidget):
    """Panel where users build their team by adding and connecting specialists"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.specialists = []  # List of specialists in the team
        self.connections = []  # List of connections between specialists
        self.init_ui()
        
    def init_ui(self):
        layout = QVBoxLayout(self)
        
        # Title
        title = QLabel("TU EQUIPO DE INTELIGENCIA")
        title.setStyleSheet("font-weight: bold; font-size: 16px;")
        
        # Team building area
        self.team_area = QWidget()
        self.team_area.setMinimumHeight(300)
        self.team_area.setObjectName("workflowPanel")
        
        # Placeholder message when empty
        self.placeholder = QLabel("Arrastra especialistas aquí para crear tu equipo")
        self.placeholder.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.placeholder.setStyleSheet("color: #a9b7c6; font-style: italic;")
        
        team_layout = QVBoxLayout(self.team_area)
        team_layout.addWidget(self.placeholder, 0, Qt.AlignmentFlag.AlignCenter)
        
        layout.addWidget(title)
        layout.addWidget(self.team_area, 1)  # 1 = stretch factor
        
    def add_specialist(self, specialist_data):
        """Add a specialist to the team"""
        # Implementation for adding specialists to the team area
        # This would involve creating visual representations and handling positioning
        pass
        
    def clear(self):
        """Remove all specialists from the team"""
        self.specialists = []
        self.connections = []
        # Reset the team area UI


class WorkflowConfigPanel(QWidget):
    """Panel for configuring workflow settings"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.init_ui()
        
    def init_ui(self):
        layout = QVBoxLayout(self)
        
        # Create a group box for the configuration
        config_group = QGroupBox("PERSONALIZACIÓN DE FLUJO DE TRABAJO")
        config_layout = QVBoxLayout(config_group)
        
        # Process type selection
        process_layout = QHBoxLayout()
        process_layout.addWidget(QLabel("Tipo de Colaboración:"))
        
        # Radio buttons would go here
        # For simplicity, just adding placeholder labels
        process_layout.addWidget(QLabel("○ Paso a paso"))
        process_layout.addWidget(QLabel("● Estratégica"))
        process_layout.addWidget(QLabel("○ Personalizada"))
        process_layout.addStretch(1)
        
        # Team goal
        goal_layout = QVBoxLayout()
        goal_layout.addWidget(QLabel("Objetivo del Equipo:"))
        goal_label = QLabel("[Descubrir oportunidades de mercado y desarrollar estrategias competitivas]")
        goal_label.setStyleSheet("background-color: #3c3f41; padding: 8px; border-radius: 4px;")
        goal_layout.addWidget(goal_label)
        
        # Action buttons
        button_layout = QHBoxLayout()
        save_button = QPushButton("Guardar Configuración")
        run_button = QPushButton("Activar Equipo de Inteligencia")
        run_button.setObjectName("primaryButton")
        
        button_layout.addWidget(save_button)
        button_layout.addWidget(run_button)
        
        # Add all layouts to the main config layout
        config_layout.addLayout(process_layout)
        config_layout.addLayout(goal_layout)
        config_layout.addLayout(button_layout)
        
        layout.addWidget(config_group)


class WorkflowPanel(QWidget):
    """Main panel that implements the horizontal workflow interface"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.current_step = 1
        self.init_ui()
        
    def init_ui(self):
        main_layout = QVBoxLayout(self)
        
        # Steps indicator
        steps_widget = QWidget()
        steps_layout = QHBoxLayout(steps_widget)
        
        self.step_indicators = []
        steps = [
            (1, "FORMAR"),
            (2, "DEFINIR"),
            (3, "CONECTAR"),
            (4, "ACTIVAR"),
            (5, "RESULTADOS")
        ]
        
        for step_num, step_name in steps:
            indicator = StepIndicator(step_num, step_name, is_active=(step_num == self.current_step))
            indicator.clicked.connect(self.set_current_step)
            steps_layout.addWidget(indicator)
            self.step_indicators.append(indicator)
        
        # Content area - using stacked widget for different steps
        self.content_stack = QStackedWidget()
        
        # Step 1: Templates and Team Formation
        self.step1_widget = QWidget()
        step1_layout = QHBoxLayout(self.step1_widget)
        
        # Template panel
        self.template_panel = TemplatePanel()
        self.template_panel.template_applied.connect(self.apply_template)
        
        # Team building area
        self.team_building = TeamBuildingPanel()
        
        step1_layout.addWidget(self.template_panel, 1)
        step1_layout.addWidget(self.team_building, 2)
        
        # Step 2: Specialist Configuration
        self.step2_widget = QWidget()
        step2_layout = QHBoxLayout(self.step2_widget)
        
        # Left panel - Specialist library
        self.specialist_library = SpecialistLibraryPanel()
        
        # Right panel - Specialist details (placeholder)
        specialist_details = QWidget()
        specialist_details.setStyleSheet("background-color: #2b2d30; border-radius: 6px;")
        
        step2_layout.addWidget(self.specialist_library, 1)
        step2_layout.addWidget(specialist_details, 2)
        
        # Step 3: Connection Configuration
        self.step3_widget = QWidget()
        # Placeholder for step 3 content
        
        # Step 4: Execution
        self.step4_widget = QWidget()
        # Placeholder for step 4 content
        
        # Step 5: Results
        self.step5_widget = QWidget()
        # Placeholder for step 5 content
        
        # Add all steps to the stack
        self.content_stack.addWidget(self.step1_widget)  # Index 0 - Step 1
        self.content_stack.addWidget(self.step2_widget)  # Index 1 - Step 2
        self.content_stack.addWidget(self.step3_widget)  # Index 2 - Step 3
        self.content_stack.addWidget(self.step4_widget)  # Index 3 - Step 4
        self.content_stack.addWidget(self.step5_widget)  # Index 4 - Step 5
        
        # Set current step
        self.content_stack.setCurrentIndex(0)
        
        # Bottom panel - Workflow configuration
        self.workflow_config = WorkflowConfigPanel()
        
        # Add all components to main layout
        main_layout.addWidget(steps_widget)
        main_layout.addWidget(self.content_stack, 1)
        main_layout.addWidget(self.workflow_config)
        
    def set_current_step(self, step_num):
        """Change the current active step"""
        if 1 <= step_num <= len(self.step_indicators):
            # Update step indicators
            for i, indicator in enumerate(self.step_indicators):
                indicator.set_active(i + 1 == step_num)
            
            self.current_step = step_num
            
            # Update content stack
            self.content_stack.setCurrentIndex(step_num - 1)
            
    def populate_specialist_library(self, agents):
        """Populate the specialist library with available agents"""
        self.specialist_library.clear()
        for name, agent in agents.items():
            self.specialist_library.add_specialist(agent)
    
    def apply_template(self, template):
        """Apply a template to the workflow"""
        # This would be connected to the agent_panel, task_panel, and crew_panel
        # in the main window to apply the template
        
        # For now, just show a message in the team building area
        self.team_building.placeholder.setText(f"Plantilla aplicada: {template.name}\n\n{template.description}")
        
        # Move to the next step
        self.set_current_step(2)
