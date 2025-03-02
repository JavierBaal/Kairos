from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
    QPushButton, QFrame, QScrollArea, QSizePolicy,
    QGridLayout, QGroupBox, QSpacerItem, QStackedWidget
)
from PyQt6.QtCore import Qt, QSize, pyqtSignal
from PyQt6.QtGui import QIcon, QPixmap, QColor, QPainter, QPen, QBrush

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


class WorkflowPanelSimple(QWidget):
    """Simplified version of the workflow panel"""
    
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
        
        # Create simple content for each step
        for i in range(5):
            step_widget = QWidget()
            step_layout = QVBoxLayout(step_widget)
            
            # Add a label with the step name
            step_label = QLabel(f"Contenido para el paso {i+1}: {steps[i][1]}")
            step_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            step_label.setStyleSheet("font-size: 18px; font-weight: bold; margin: 20px;")
            
            # Add a description
            description = QLabel("Esta es una versión simplificada de la interfaz para solucionar problemas de compatibilidad.")
            description.setAlignment(Qt.AlignmentFlag.AlignCenter)
            description.setWordWrap(True)
            
            # Add a placeholder content
            placeholder = QLabel("Contenido en desarrollo")
            placeholder.setAlignment(Qt.AlignmentFlag.AlignCenter)
            placeholder.setStyleSheet("background-color: #3c3f41; padding: 40px; border-radius: 8px; margin: 20px;")
            
            step_layout.addWidget(step_label)
            step_layout.addWidget(description)
            step_layout.addWidget(placeholder)
            step_layout.addStretch(1)
            
            self.content_stack.addWidget(step_widget)
        
        # Bottom panel - simple configuration
        bottom_panel = QGroupBox("CONFIGURACIÓN")
        bottom_layout = QVBoxLayout(bottom_panel)
        
        # Add a simple button
        button = QPushButton("Continuar")
        button.setObjectName("primaryButton")
        bottom_layout.addWidget(button, 0, Qt.AlignmentFlag.AlignCenter)
        
        # Add all components to main layout
        main_layout.addWidget(steps_widget)
        main_layout.addWidget(self.content_stack, 1)
        main_layout.addWidget(bottom_panel)
        
    def set_current_step(self, step_num):
        """Change the current active step"""
        if 1 <= step_num <= len(self.step_indicators):
            # Update step indicators
            for i, indicator in enumerate(self.step_indicators):
                indicator.set_active(i + 1 == step_num)
            
            self.current_step = step_num
            
            # Update content stack
            self.content_stack.setCurrentIndex(step_num - 1)
