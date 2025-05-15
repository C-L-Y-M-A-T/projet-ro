import sys
import os
import json
import subprocess
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, 
                            QLabel, QPushButton, QScrollArea, QGridLayout, QFrame, 
                            QSizePolicy, QSpacerItem, QGraphicsDropShadowEffect)
from PyQt5.QtCore import Qt, QSize, QProcess, pyqtSignal, QPropertyAnimation, QEasingCurve
from PyQt5.QtGui import QIcon, QFont, QColor, QPalette, QPixmap, QCursor

# Configuration file path
CONFIG_FILE = "launcher_config.json"

class AppCard(QFrame):
    """Custom widget for application cards in the launcher"""
    clicked = pyqtSignal(str)
    
    def __init__(self, app_id, app_name, description, icon_path, app_path, parent=None):
        super().__init__(parent)
        self.app_id = app_id
        self.app_path = app_path
        
        # Set up the card appearance
        self.setObjectName("appCard")
        self.setFixedSize(350, 250)
        self.setCursor(QCursor(Qt.PointingHandCursor))
        
        # Add shadow effect
        shadow = QGraphicsDropShadowEffect()
        shadow.setBlurRadius(15)
        shadow.setColor(QColor(0, 0, 0, 30))
        shadow.setOffset(0, 5)
        self.setGraphicsEffect(shadow)
        
        # Create layout
        layout = QVBoxLayout(self)
        layout.setContentsMargins(15, 15, 15, 15)
        layout.setSpacing(10)
        
        # Add icon
        icon_label = QLabel()
        icon_label.setAlignment(Qt.AlignCenter)
        
        if os.path.exists(icon_path):
            pixmap = QPixmap(icon_path)
            icon_label.setPixmap(pixmap.scaled(64, 64, Qt.KeepAspectRatio, Qt.SmoothTransformation))
        else:
            # Default icon if the specified one doesn't exist
            icon_label.setText("🚀")
            icon_label.setFont(QFont("Segoe UI", 32))
            
        layout.addWidget(icon_label)
        
        # Add app name
        name_label = QLabel(app_name)
        name_label.setAlignment(Qt.AlignCenter)
        name_label.setFont(QFont("Segoe UI", 14, QFont.Bold))
        layout.addWidget(name_label)
        
        # Add description
        desc_label = QLabel(description)
        desc_label.setAlignment(Qt.AlignCenter)
        desc_label.setWordWrap(True)
        desc_label.setFont(QFont("Segoe UI", 10))
        layout.addWidget(desc_label)
        
        # Add launch button
        launch_button = QPushButton("Launch")
        launch_button.setFont(QFont("Segoe UI", 10, QFont.Bold))
        launch_button.setCursor(QCursor(Qt.PointingHandCursor))
        launch_button.setStyleSheet("""
            QPushButton {
                background-color: #3b82f6;
                color: white;
                border: none;
                border-radius: 6px;
                padding: 8px 16px;
            }
            QPushButton:hover {
                background-color: #2563eb;
            }
            QPushButton:pressed {
                background-color: #1d4ed8;
            }
        """)
        launch_button.clicked.connect(self.on_click)
        layout.addWidget(launch_button)
        
        # Set the card style
        self.setStyleSheet("""
            #appCard {
                background-color: white;
                border-radius: 10px;
                border: 1px solid #e2e8f0;
            }
            #appCard:hover {
                border: 1px solid #3b82f6;
                background-color: #f8fafc;
            }
        """)
        
    def on_click(self):
        self.clicked.emit(self.app_id)
        
    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.on_click()
        super().mousePressEvent(event)

class AppLauncher(QMainWindow):
    """Main application launcher window"""
    def __init__(self):
        super().__init__()
        
        # Set window properties
        self.setWindowTitle("Application Launcher")
        self.setMinimumSize(900, 600)
        
        # Initialize UI
        self.init_ui()
        
        # Load applications
        self.load_apps()
        
    def init_ui(self):
        # Set the window style
        self.setStyleSheet("""
            QMainWindow {
                background-color: #f1f5f9;
            }
            QLabel {
                color: #1e293b;
            }
            QScrollArea {
                background-color: #f1f5f9;
                border: none;
            }
        """)
        
        # Create central widget and main layout
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        main_layout = QVBoxLayout(central_widget)
        main_layout.setContentsMargins(30, 30, 30, 30)
        main_layout.setSpacing(20)
        
        # Create header
        header_widget = QWidget()
        header_widget.setStyleSheet("background-color: white; border-radius: 10px;")
        
        # Add shadow to header
        header_shadow = QGraphicsDropShadowEffect()
        header_shadow.setBlurRadius(15)
        header_shadow.setColor(QColor(0, 0, 0, 30))
        header_shadow.setOffset(0, 5)
        header_widget.setGraphicsEffect(header_shadow)
        
        header_layout = QHBoxLayout(header_widget)
        header_layout.setContentsMargins(20, 15, 20, 15)
        
        # App title
        header_label = QLabel("Application Launcher")
        header_label.setFont(QFont("Segoe UI", 22, QFont.Bold))
        header_label.setStyleSheet("color: #3b82f6;")
        header_layout.addWidget(header_label)
        
        # Add spacer
        header_layout.addStretch()
        
        # Add refresh button
        self.refresh_button = QPushButton("Refresh Apps")
        self.refresh_button.setFont(QFont("Segoe UI", 10))
        self.refresh_button.setCursor(QCursor(Qt.PointingHandCursor))
        self.refresh_button.setStyleSheet("""
            QPushButton {
                background-color: #e2e8f0;
                color: #1e293b;
                border: none;
                border-radius: 6px;
                padding: 8px 16px;
            }
            QPushButton:hover {
                background-color: #cbd5e1;
            }
            QPushButton:pressed {
                background-color: #94a3b8;
            }
        """)
        self.refresh_button.clicked.connect(self.load_apps)
        header_layout.addWidget(self.refresh_button)
        
        main_layout.addWidget(header_widget)
        
        # Create scroll area for app cards
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setFrameShape(QFrame.NoFrame)
        
        scroll_content = QWidget()
        self.grid_layout = QGridLayout(scroll_content)
        self.grid_layout.setContentsMargins(10, 10, 10, 10)
        self.grid_layout.setSpacing(20)
        
        scroll_area.setWidget(scroll_content)
        main_layout.addWidget(scroll_area)
        
    def load_apps(self):
        """Load applications from configuration file"""
        # Clear existing app cards
        while self.grid_layout.count():
            item = self.grid_layout.takeAt(0)
            widget = item.widget()
            if widget:
                widget.deleteLater()
        
        # Load app configuration
        apps = self.load_app_config()
        
        # Add app cards to grid
        row, col = 0, 0
        max_cols = 3  # Number of columns in the grid
        
        for app_id, app_info in apps.items():
            app_card = AppCard(
                app_id=app_id,
                app_name=app_info.get("name", "Unknown App"),
                description=app_info.get("description", ""),
                icon_path=app_info.get("icon", ""),
                app_path=app_info.get("path", "")
            )
            app_card.clicked.connect(self.launch_app)
            
            self.grid_layout.addWidget(app_card, row, col)
            
            col += 1
            if col >= max_cols:
                col = 0
                row += 1
        
        # Add spacer at the end
        if apps:
            self.grid_layout.addItem(
                QSpacerItem(20, 20, QSizePolicy.Minimum, QSizePolicy.Expanding), 
                row + 1, 0, 1, max_cols
            )
        
    def load_app_config(self):
        """Load application configuration from JSON file"""
        default_config = {
            "production_optimizer": {
                "name": "Production Optimizer",
                "description": "Optimize production planning with resource constraints",
                "icon": "icons/production.png",
                "path": "main.py"
            }
        }
        
        try:
            if os.path.exists(CONFIG_FILE):
                with open(CONFIG_FILE, 'r') as f:
                    return json.load(f)
            else:
                # Create default config file if it doesn't exist
                with open(CONFIG_FILE, 'w') as f:
                    json.dump(default_config, f, indent=4)
                return default_config
        except Exception as e:
            print(f"Error loading configuration: {e}")
            return default_config
    
    def launch_app(self, app_id):
        """Launch the selected application"""
        apps = self.load_app_config()
        if app_id in apps:
            app_path = apps[app_id].get("path", "")
            if app_path:
                try:
                    # Pass a command line argument to indicate it was launched from the launcher
                    subprocess.Popen([sys.executable, app_path, "--from-launcher"])
                    
                    # Minimize the launcher window
                    self.showMinimized()
                except Exception as e:
                    print(f"Error launching application: {e}")

def main():
    app = QApplication(sys.argv)
    
    # Set application style
    app.setStyle("Fusion")
    
    # Set light palette
    palette = QPalette()
    palette.setColor(QPalette.Window, QColor(241, 245, 249))
    palette.setColor(QPalette.WindowText, QColor(15, 23, 42))
    palette.setColor(QPalette.Base, QColor(255, 255, 255))
    palette.setColor(QPalette.AlternateBase, QColor(248, 250, 252))
    palette.setColor(QPalette.ToolTipBase, QColor(255, 255, 255))
    palette.setColor(QPalette.ToolTipText, QColor(15, 23, 42))
    palette.setColor(QPalette.Text, QColor(15, 23, 42))
    palette.setColor(QPalette.Button, QColor(226, 232, 240))
    palette.setColor(QPalette.ButtonText, QColor(15, 23, 42))
    palette.setColor(QPalette.BrightText, QColor(59, 130, 246))
    palette.setColor(QPalette.Link, QColor(59, 130, 246))
    palette.setColor(QPalette.Highlight, QColor(59, 130, 246))
    palette.setColor(QPalette.HighlightedText, QColor(255, 255, 255))
    app.setPalette(palette)
    
    window = AppLauncher()
    window.show()
    
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
