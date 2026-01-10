# ui/main_window.py
from PySide6.QtWidgets import QMainWindow, QLabel, QVBoxLayout, QWidget


class MainWindow(QMainWindow):
    """Main application window."""
    
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Supreme Guacamole - Art Management")
        self.setGeometry(100, 100, 800, 600)
        
        # Create central widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # Create layout
        layout = QVBoxLayout()
        central_widget.setLayout(layout)
        
        # Add welcome label
        welcome_label = QLabel("Welcome to Art Management System")
        welcome_label.setStyleSheet("font-size: 24px; padding: 20px;")
        layout.addWidget(welcome_label)
