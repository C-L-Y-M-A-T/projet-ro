import sys
import math
import os
import numpy as np
from PyQt5.QtGui import QIcon, QFont, QColor, QPalette, QPixmap, QCursor, QFontDatabase
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
                             QLabel, QLineEdit, QPushButton, QTableWidget, QTableWidgetItem,
                             QMessageBox, QTabWidget, QFormLayout, QSpinBox, QDoubleSpinBox,
                             QFileDialog, QComboBox, QGroupBox, QProgressBar, QSplitter,
                             QFrame, QScrollArea, QSizePolicy, QGraphicsDropShadowEffect,
                             QToolButton, QSlider, QCheckBox)
from PyQt5.QtCore import Qt, QSize, QProcess, pyqtSignal, QPropertyAnimation, QEasingCurve, QTimer

import gurobipy as gp
from gurobipy import GRB
import random

from core.VRPSolverThread import VRPSolverThread
from core.solver import VRPSolver
from gui.location_table import LocationTable
from gui.map_canvas import MapCanvas


class StyleHelper:
    """Helper class for styling the application"""
    @staticmethod
    def apply_light_theme(app):
        app.setStyle("Fusion")
        
        # Light palette
        light_palette = QPalette()
        light_palette.setColor(QPalette.Window, QColor(248, 250, 252))
        light_palette.setColor(QPalette.WindowText, QColor(15, 23, 42))
        light_palette.setColor(QPalette.Base, QColor(255, 255, 255))
        light_palette.setColor(QPalette.AlternateBase, QColor(241, 245, 249))
        light_palette.setColor(QPalette.ToolTipBase, QColor(255, 255, 255))
        light_palette.setColor(QPalette.ToolTipText, QColor(15, 23, 42))
        light_palette.setColor(QPalette.Text, QColor(15, 23, 42))
        light_palette.setColor(QPalette.Button, QColor(226, 232, 240))
        light_palette.setColor(QPalette.ButtonText, QColor(15, 23, 42))
        light_palette.setColor(QPalette.BrightText, QColor(59, 130, 246))
        light_palette.setColor(QPalette.Link, QColor(59, 130, 246))
        light_palette.setColor(QPalette.Highlight, QColor(59, 130, 246))
        light_palette.setColor(QPalette.HighlightedText, QColor(255, 255, 255))
        
        app.setPalette(light_palette)
        
    @staticmethod
    def get_accent_color():
        return QColor(59, 130, 246)  # Blue accent color
        
    @staticmethod
    def get_success_color():
        return QColor(34, 197, 94)  # Green
        
    @staticmethod
    def get_warning_color():
        return QColor(234, 179, 8)  # Yellow
        
    @staticmethod
    def get_error_color():
        return QColor(239, 68, 68)  # Red
        
    @staticmethod
    def style_button(button, primary=False):
        if primary:
            button.setStyleSheet("""
                QPushButton {
                    background-color: #3b82f6;
                    color: #ffffff;
                    border: none;
                    padding: 10px 20px;
                    border-radius: 6px;
                    font-weight: bold;
                }
                QPushButton:hover {
                    background-color: #2563eb;
                }
                QPushButton:pressed {
                    background-color: #1d4ed8;
                    padding: 11px 19px 9px 21px;
                }
                QPushButton:disabled {
                    background-color: #cbd5e1;
                    color: #64748b;
                }
            """)
        else:
            button.setStyleSheet("""
                QPushButton {
                    background-color: #e2e8f0;
                    color: #1e293b;
                    border: none;
                    padding: 10px 20px;
                    border-radius: 6px;
                }
                QPushButton:hover {
                    background-color: #cbd5e1;
                }
                QPushButton:pressed {
                    background-color: #94a3b8;
                    padding: 11px 19px 9px 21px;
                }
                QPushButton:disabled {
                    background-color: #f1f5f9;
                    color: #94a3b8;
                }
            """)
            
    @staticmethod
    def style_table(table):
        table.setStyleSheet("""
            QTableWidget {
                background-color: #ffffff;
                color: #1e293b;
                gridline-color: #e2e8f0;
                border: 1px solid #e2e8f0;
                border-radius: 6px;
                selection-background-color: #3b82f6;
                selection-color: #ffffff;
            }
            QHeaderView::section {
                background-color: #f1f5f9;
                color: #1e293b;
                padding: 6px;
                border: none;
                border-right: 1px solid #e2e8f0;
                border-bottom: 1px solid #e2e8f0;
            }
            QTableWidget::item {
                padding: 6px;
                border-bottom: 1px solid #f1f5f9;
            }
            QTableWidget::item:selected {
                background-color: #3b82f6;
                color: #ffffff;
            }
        """)
        
    @staticmethod
    def style_group_box(group_box):
        group_box.setStyleSheet("""
            QGroupBox {
                background-color: #ffffff;
                border: 1px solid #e2e8f0;
                border-radius: 8px;
                margin-top: 20px;
                font-weight: bold;
                color: #1e293b;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                subcontrol-position: top center;
                padding: 0 10px;
                background-color: #3b82f6;
                color: #ffffff;
                border-radius: 4px;
            }
        """)
        
    @staticmethod
    def style_combo_box(combo_box):
        combo_box.setStyleSheet("""
            QComboBox {
                background-color: #f1f5f9;
                color: #1e293b;
                border: 1px solid #e2e8f0;
                border-radius: 6px;
                padding: 6px 12px;
                min-width: 6em;
            }
            QComboBox:hover {
                background-color: #e2e8f0;
            }
            QComboBox::drop-down {
                subcontrol-origin: padding;
                subcontrol-position: top right;
                width: 20px;
                border: none;
            }
            QComboBox QAbstractItemView {
                background-color: #ffffff;
                color: #1e293b;
                border: 1px solid #e2e8f0;
                selection-background-color: #3b82f6;
                selection-color: #ffffff;
                outline: none;
            }
        """)
        
    @staticmethod
    def style_spin_box(spin_box):
        spin_box.setStyleSheet("""
            QDoubleSpinBox, QSpinBox {
                background-color: #f1f5f9;
                color: #1e293b;
                border: 1px solid #e2e8f0;
                border-radius: 6px;
                padding: 6px 12px;
            }
            QDoubleSpinBox:hover, QSpinBox:hover {
                background-color: #e2e8f0;
            }
            QDoubleSpinBox::up-button, QSpinBox::up-button {
                subcontrol-origin: border;
                subcontrol-position: top right;
                width: 20px;
                border: none;
            }
            QDoubleSpinBox::down-button, QSpinBox::down-button {
                subcontrol-origin: border;
                subcontrol-position: bottom right;
                width: 20px;
                border: none;
            }
        """)
        
    @staticmethod
    def style_text_edit(text_edit):
        text_edit.setStyleSheet("""
            QTextEdit {
                background-color: #ffffff;
                color: #1e293b;
                border: 1px solid #e2e8f0;
                border-radius: 6px;
                padding: 6px;
            }
        """)
        
    @staticmethod
    def add_shadow(widget):
        shadow = QGraphicsDropShadowEffect()
        shadow.setBlurRadius(15)
        shadow.setColor(QColor(0, 0, 0, 30))
        shadow.setOffset(0, 5)
        widget.setGraphicsEffect(shadow)


class ModernButton(QPushButton):
    """Custom styled button"""
    def __init__(self, text, icon=None, parent=None, primary=False):
        super().__init__(text, parent)
        self.primary = primary
        
        if icon:
            self.setIcon(QIcon(icon))
            self.setIconSize(QSize(18, 18))
        
        StyleHelper.style_button(self, primary)


class ModernGroupBox(QGroupBox):
    """Custom styled group box"""
    def __init__(self, title, parent=None):
        super().__init__(title, parent)
        StyleHelper.style_group_box(self)
        StyleHelper.add_shadow(self)


class LoadingOverlay(QWidget):
    """Overlay widget for displaying loading state"""
    def __init__(self, parent=None):
        super(LoadingOverlay, self).__init__(parent)
        self.setObjectName("loadingOverlay")
        
        # Make the overlay semi-transparent
        self.setStyleSheet("""
            #loadingOverlay {
                background-color: rgba(0, 0, 0, 0.7);
                border-radius: 10px;
            }
        """)
        
        # Create layout
        layout = QVBoxLayout(self)
        layout.setAlignment(Qt.AlignCenter)
        
        # Create loading animation container
        animation_container = QWidget()
        animation_container.setFixedSize(200, 200)
        animation_container.setStyleSheet("""
            background-color: white;
            border-radius: 10px;
        """)
        
        animation_layout = QVBoxLayout(animation_container)
        animation_layout.setAlignment(Qt.AlignCenter)
        
        # Loading spinner
        self.progress_bar = QProgressBar()
        self.progress_bar.setRange(0, 0)  # Indeterminate mode
        self.progress_bar.setFixedWidth(150)
        self.progress_bar.setFixedHeight(8)
        self.progress_bar.setTextVisible(False)
        self.progress_bar.setStyleSheet("""
            QProgressBar {
                border: none;
                border-radius: 4px;
                background-color: #e5e7eb;
            }
            QProgressBar::chunk {
                background-color: #3b82f6;
                border-radius: 4px;
            }
        """)
        
        # Loading message
        self.message_label = QLabel("Solving VRP Problem...")
        self.message_label.setFont(QFont("Segoe UI", 12, QFont.Bold))
        self.message_label.setStyleSheet("color: #1e293b;")
        self.message_label.setAlignment(Qt.AlignCenter)
        
        # Description
        self.description_label = QLabel("This may take several minutes for large problems.")
        self.description_label.setFont(QFont("Segoe UI", 9))
        self.description_label.setStyleSheet("color: #64748b;")
        self.description_label.setAlignment(Qt.AlignCenter)
        
        # Cancel button
        self.cancel_button = ModernButton("Cancel", primary=True)
        self.cancel_button.setFixedWidth(120)
        
        # Add widgets to animation layout
        animation_layout.addStretch()
        animation_layout.addWidget(self.message_label, 0, Qt.AlignCenter)
        animation_layout.addSpacing(10)
        animation_layout.addWidget(self.progress_bar, 0, Qt.AlignCenter)
        animation_layout.addSpacing(15)
        animation_layout.addWidget(self.description_label, 0, Qt.AlignCenter)
        animation_layout.addSpacing(20)
        animation_layout.addWidget(self.cancel_button, 0, Qt.AlignCenter)
        animation_layout.addStretch()
        
        # Add animation container to main layout
        layout.addWidget(animation_container, 0, Qt.AlignCenter)
        
        # Hide by default
        self.hide()
    
    def set_message(self, message):
        """Update the loading message"""
        self.message_label.setText(message)


class VRPApp(QMainWindow):
    """Main application window for VRP Solver"""

    def __init__(self):
        super(VRPApp, self).__init__()
        
        # Set window properties
        self.setWindowTitle('Vehicle Routing Problem Solver')
        self.setGeometry(100, 100, 1280, 800)
        self.setMinimumSize(1000, 700)
        
        # Initialize UI components
        self.initUI()
        
        # Initialize loading overlay
        self.loading_overlay = LoadingOverlay(self)
        self.loading_overlay.cancel_button.clicked.connect(self.cancel_solving)
        
        # Initialize with example data
        self.generate_example_data()
        
        # Check if we should show the launcher return button
        self.from_launcher = "--from-launcher" in sys.argv
        if self.from_launcher:
            self.return_button.show()
        else:
            self.return_button.hide()

    def initUI(self):
        """Initialize the UI components"""
        # Create central widget and main layout
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout(central_widget)
        main_layout.setContentsMargins(20, 20, 20, 20)
        main_layout.setSpacing(15)
        
        # Create header
        header_widget = QWidget()
        header_widget.setObjectName("headerWidget")
        header_widget.setStyleSheet("""
            #headerWidget {
                background-color: #ffffff;
                border-radius: 10px;
            }
        """)
        
        # Add shadow to header
        StyleHelper.add_shadow(header_widget)
        
        header_layout = QHBoxLayout(header_widget)
        header_layout.setContentsMargins(20, 15, 20, 15)
        
        # App title and logo
        title_layout = QHBoxLayout()
        
        logo_label = QLabel()
        logo_label.setFixedSize(32, 32)
        logo_label.setStyleSheet("""
            background-color: #3b82f6;
            border-radius: 8px;
            color: white;
            font-size: 18px;
            font-weight: bold;
        """)
        logo_label.setAlignment(Qt.AlignCenter)
        logo_label.setText("VRP")
        title_layout.addWidget(logo_label)
        
        title_label = QLabel("Vehicle Routing Problem Solver")
        title_label.setFont(QFont("Segoe UI", 16, QFont.Bold))
        title_label.setStyleSheet("color: #3b82f6;")
        title_layout.addWidget(title_label)
        
        header_layout.addLayout(title_layout)
        
        # Add spacer
        header_layout.addStretch()
        
        # Return to launcher button (hidden by default)
        self.return_button = ModernButton("Return to Launcher", icon="/icons/home.png")
        self.return_button.clicked.connect(self.return_to_launcher)
        header_layout.addWidget(self.return_button)
        
        # Add header to main layout
        main_layout.addWidget(header_widget)
        
        # Create tab widget
        self.tab_widget = QTabWidget()
        self.tab_widget.setStyleSheet("""
            QTabWidget::pane {
                border: 1px solid #e2e8f0;
                border-radius: 8px;
                background-color: #ffffff;
                top: -1px;
            }
            QTabBar::tab {
                background-color: #f1f5f9;
                color: #1e293b;
                border: 1px solid #e2e8f0;
                border-bottom: none;
                border-top-left-radius: 8px;
                border-top-right-radius: 8px;
                padding: 8px 16px;
                margin-right: 4px;
            }
            QTabBar::tab:selected {
                background-color: #ffffff;
                color: #3b82f6;
                border-bottom-color: #ffffff;
                font-weight: bold;
            }
            QTabBar::tab:!selected {
                margin-top: 2px;
            }
        """)
        StyleHelper.add_shadow(self.tab_widget)
        
        # Create tabs
        input_tab = QWidget()
        solution_tab = QWidget()
        
        self.tab_widget.addTab(input_tab, "Input Data")
        self.tab_widget.addTab(solution_tab, "Solution")
        
        # Set up input tab
        input_layout = QHBoxLayout(input_tab)
        input_layout.setContentsMargins(15, 15, 15, 15)
        input_layout.setSpacing(15)
        
        # Create a splitter for resizable panels
        input_splitter = QSplitter(Qt.Horizontal)
        input_splitter.setHandleWidth(1)
        input_splitter.setStyleSheet("""
            QSplitter::handle {
                background-color: #e2e8f0;
            }
        """)
        
        # Left panel: Parameters
        param_widget = QWidget()
        param_layout = QVBoxLayout(param_widget)
        param_layout.setContentsMargins(0, 0, 0, 0)
        param_layout.setSpacing(15)
        
        # Parameters group
        params_group = ModernGroupBox("Problem Parameters")
        params_form_layout = QFormLayout(params_group)
        params_form_layout.setContentsMargins(15, 25, 15, 15)
        params_form_layout.setSpacing(15)
        params_form_layout.setLabelAlignment(Qt.AlignLeft)
        params_form_layout.setFieldGrowthPolicy(QFormLayout.AllNonFixedFieldsGrow)
        
        # Style for form labels
        label_style = """
            QLabel {
                color: #1e293b;
                font-weight: 500;
            }
        """
        
        # Number of vehicles
        vehicles_label = QLabel("Number of Vehicles:")
        vehicles_label.setStyleSheet(label_style)
        self.num_vehicles_input = QSpinBox()
        self.num_vehicles_input.setRange(1, 100)
        self.num_vehicles_input.setValue(3)
        self.num_vehicles_input.setFixedHeight(36)
        StyleHelper.style_spin_box(self.num_vehicles_input)
        params_form_layout.addRow(vehicles_label, self.num_vehicles_input)
        
        # Depot index
        depot_label = QLabel("Depot Location Index:")
        depot_label.setStyleSheet(label_style)
        self.depot_idx_input = QSpinBox()
        self.depot_idx_input.setRange(0, 999)
        self.depot_idx_input.setValue(0)
        self.depot_idx_input.setFixedHeight(36)
        StyleHelper.style_spin_box(self.depot_idx_input)
        params_form_layout.addRow(depot_label, self.depot_idx_input)
        
        # Vehicle capacity
        capacity_label = QLabel("Vehicle Capacity:")
        capacity_label.setStyleSheet(label_style)
        self.capacity_input = QDoubleSpinBox()
        self.capacity_input.setRange(1, 10000)
        self.capacity_input.setValue(100)
        self.capacity_input.setDecimals(1)
        self.capacity_input.setFixedHeight(36)
        StyleHelper.style_spin_box(self.capacity_input)
        params_form_layout.addRow(capacity_label, self.capacity_input)
        
        param_layout.addWidget(params_group)
        
        # Data management group
        data_group = ModernGroupBox("Data Management")
        data_layout = QVBoxLayout(data_group)
        data_layout.setContentsMargins(15, 25, 15, 15)
        data_layout.setSpacing(10)
        
        # Buttons for generating and loading data
        button_grid = QHBoxLayout()
        button_grid.setSpacing(10)
        
        self.generate_btn = ModernButton("Generate Example", icon="/icons/refresh.png")
        self.generate_btn.clicked.connect(lambda: self.generate_example_data(15))
        button_grid.addWidget(self.generate_btn)
        
        self.load_btn = ModernButton("Load Data", icon="/icons/upload.png")
        self.load_btn.clicked.connect(self.load_data)
        button_grid.addWidget(self.load_btn)
        
        self.save_btn = ModernButton("Save Data", icon="/icons/save.png")
        self.save_btn.clicked.connect(self.save_data)
        button_grid.addWidget(self.save_btn)
        
        data_layout.addLayout(button_grid)
        
        # Location table
        table_label = QLabel("Locations and Demands:")
        table_label.setFont(QFont("Segoe UI", 10, QFont.Bold))
        table_label.setStyleSheet("color: #1e293b;")
        data_layout.addWidget(table_label)
        
        self.location_table = LocationTable()
        StyleHelper.style_table(self.location_table)
        data_layout.addWidget(self.location_table)
        
        # Add/Remove location buttons
        loc_button_layout = QHBoxLayout()
        loc_button_layout.setSpacing(10)
        
        self.add_loc_btn = ModernButton("Add Location", icon="/icons/plus.png")
        self.add_loc_btn.clicked.connect(self.add_location)
        loc_button_layout.addWidget(self.add_loc_btn)
        
        self.remove_loc_btn = ModernButton("Remove Selected", icon="/icons/trash.png")
        self.remove_loc_btn.clicked.connect(self.remove_location)
        loc_button_layout.addWidget(self.remove_loc_btn)
        
        data_layout.addLayout(loc_button_layout)
        
        param_layout.addWidget(data_group)
        
        # Solve button
        self.solve_btn = ModernButton("Solve VRP Problem", icon="/icons/play.png", primary=True)
        self.solve_btn.setFixedHeight(50)
        self.solve_btn.setFont(QFont("Segoe UI", 11, QFont.Bold))
        self.solve_btn.clicked.connect(self.solve_vrp)
        param_layout.addWidget(self.solve_btn)
        
        # Add stretch to push everything to the top
        param_layout.addStretch()
        
        # Right panel: Map visualization
        map_group = ModernGroupBox("Map Visualization")
        map_layout = QVBoxLayout(map_group)
        map_layout.setContentsMargins(15, 25, 15, 15)
        map_layout.setSpacing(10)
        
        self.map_canvas = MapCanvas(map_group)
        map_layout.addWidget(self.map_canvas)
        
        # Add panels to splitter
        input_splitter.addWidget(param_widget)
        input_splitter.addWidget(map_group)
        
        # Set initial sizes (30% for params, 70% for map)
        input_splitter.setSizes([300, 700])
        
        input_layout.addWidget(input_splitter)
        
        # Set up solution tab
        solution_layout = QVBoxLayout(solution_tab)
        solution_layout.setContentsMargins(15, 15, 15, 15)
        solution_layout.setSpacing(15)
        
        # Create a splitter for solution tab
        solution_splitter = QSplitter(Qt.Vertical)
        solution_splitter.setHandleWidth(1)
        solution_splitter.setStyleSheet("""
            QSplitter::handle {
                background-color: #e2e8f0;
            }
        """)
        
        # Solution map
        solution_map_group = ModernGroupBox("Solution Map")
        solution_map_layout = QVBoxLayout(solution_map_group)
        solution_map_layout.setContentsMargins(15, 25, 15, 15)
        
        self.solution_canvas = MapCanvas()
        solution_map_layout.addWidget(self.solution_canvas)
        
        # Solution details
        solution_details_group = ModernGroupBox("Solution Details")
        solution_details_layout = QVBoxLayout(solution_details_group)
        solution_details_layout.setContentsMargins(15, 25, 15, 15)
        
        # Create a scroll area for solution details
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setFrameShape(QFrame.NoFrame)
        scroll_area.setStyleSheet("""
            QScrollArea {
                background-color: transparent;
                border: none;
            }
        """)
        
        scroll_content = QWidget()
        scroll_layout = QVBoxLayout(scroll_content)
        
        self.solution_details = QLabel("No solution yet. Solve the problem first.")
        self.solution_details.setFont(QFont("Segoe UI", 10))
        self.solution_details.setStyleSheet("color: #64748b;")
        self.solution_details.setWordWrap(True)
        self.solution_details.setTextFormat(Qt.RichText)
        self.solution_details.setAlignment(Qt.AlignTop | Qt.AlignLeft)
        scroll_layout.addWidget(self.solution_details)
        scroll_layout.addStretch()
        
        scroll_area.setWidget(scroll_content)
        solution_details_layout.addWidget(scroll_area)
        
        # Add widgets to splitter
        solution_splitter.addWidget(solution_map_group)
        solution_splitter.addWidget(solution_details_group)
        
        # Set initial sizes (60% for map, 40% for details)
        solution_splitter.setSizes([500, 300])
        
        solution_layout.addWidget(solution_splitter)
        
        # Add tab widget to main layout
        main_layout.addWidget(self.tab_widget)
        
        # Status bar
        self.statusBar().showMessage("Ready")
        self.statusBar().setStyleSheet("""
            QStatusBar {
                background-color: #ffffff;
                color: #64748b;
                border-top: 1px solid #e2e8f0;
            }
        """)

    def generate_example_data(self, num_customers=15):
        """Generate example data for the VRP"""
        # Generate random customer locations
        
        # Create a depot at a central position
        depot = (50, 50)
        locations = [depot]
        
        # Generate customer locations in a distribution around the depot
        for _ in range(num_customers):
            x = np.random.uniform(0, 100)
            y = np.random.uniform(0, 100)
            locations.append((x, y))
        
        # Generate demands (depot has 0 demand)
        demands = [0]  # Depot
        for _ in range(num_customers):
            demand = np.random.randint(1, 20)
            demands.append(demand)
        
        # Update UI
        self.location_table.set_data(locations, demands)
        self.depot_idx_input.setValue(0)
        self.map_canvas.plot_locations(locations, 0)
        
        # Show success message in status bar
        self.statusBar().showMessage(f"Generated example data with {num_customers} customers", 3000)

    def add_location(self):
        """Add a new location to the table"""
        current_row = self.location_table.rowCount()
        self.location_table.insertRow(current_row)
        
        # Add default values
        self.location_table.setItem(current_row, 0, QTableWidgetItem("0.00"))
        self.location_table.setItem(current_row, 1, QTableWidgetItem("0.00"))
        self.location_table.setItem(current_row, 2, QTableWidgetItem("0.0"))
        
        # Update map
        self.update_map()

    def remove_location(self):
        """Remove selected location from the table"""
        selected_rows = set(index.row() for index in self.location_table.selectedIndexes())
        
        if not selected_rows:
            QMessageBox.information(self, "Selection Required", "Please select at least one row to remove.")
            return
        
        # Remove rows in reverse order to maintain correct indices
        for row in sorted(selected_rows, reverse=True):
            self.location_table.removeRow(row)
        
        # Update map
        self.update_map()
        
        # Show success message in status bar
        self.statusBar().showMessage(f"Removed {len(selected_rows)} location(s)", 3000)

    def update_map(self):
        """Update the map with current locations"""
        locations, _ = self.location_table.get_data()
        depot_idx = self.depot_idx_input.value()
        
        if locations and 0 <= depot_idx < len(locations):
            self.map_canvas.plot_locations(locations, depot_idx)

    def load_data(self):
        """Load VRP data from a file"""
        try:
            file_name, _ = QFileDialog.getOpenFileName(
                self, "Load VRP Data", "", "CSV Files (*.csv);;All Files (*)"
            )
            
            if file_name:
                data = np.loadtxt(file_name, delimiter=',')
                
                # Format: x, y, demand for each row
                locations = [(row[0], row[1]) for row in data]
                demands = [row[2] for row in data]
                
                self.location_table.set_data(locations, demands)
                self.depot_idx_input.setValue(0)
                self.map_canvas.plot_locations(locations, 0)
                
                # Show success message in status bar
                self.statusBar().showMessage(f"Loaded data from {file_name}", 3000)
        
        except Exception as e:
            QMessageBox.critical(self, "Error Loading Data", f"Failed to load data: {str(e)}")

    def save_data(self):
        """Save VRP data to a file"""
        try:
            file_name, _ = QFileDialog.getSaveFileName(
                self, "Save VRP Data", "", "CSV Files (*.csv);;All Files (*)"
            )
            
            if file_name:
                locations, demands = self.location_table.get_data()
                
                # Combine location and demand data
                data = np.zeros((len(locations), 3))
                for i, ((x, y), demand) in enumerate(zip(locations, demands)):
                    data[i, 0] = x
                    data[i, 1] = y
                    data[i, 2] = demand
                
                np.savetxt(file_name, data, delimiter=',', fmt='%.2f')
                
                # Show success message in status bar
                self.statusBar().showMessage(f"Data saved to {file_name}", 3000)
        
        except Exception as e:
            QMessageBox.critical(self, "Error Saving Data", f"Failed to save data: {str(e)}")

    def validate_inputs(self):
        """Validate user inputs before solving"""
        locations, demands = self.location_table.get_data()
        num_locations = len(locations)
        depot_idx = self.depot_idx_input.value()
        num_vehicles = self.num_vehicles_input.value()
        capacity = self.capacity_input.value()
        
        if num_locations < 2:
            QMessageBox.warning(self, "Invalid Input", "At least 2 locations (depot + 1 customer) are required.")
            return False
        
        if not (0 <= depot_idx < num_locations):
            QMessageBox.warning(self, "Invalid Input", f"Depot index must be between 0 and {num_locations - 1}.")
            return False
        
        if num_vehicles < 1:
            QMessageBox.warning(self, "Invalid Input", "Number of vehicles must be at least 1.")
            return False
        
        if capacity <= 0:
            QMessageBox.warning(self, "Invalid Input", "Vehicle capacity must be positive.")
            return False
        
        for i, demand in enumerate(demands):
            if demand < 0:
                QMessageBox.warning(self, "Invalid Input", f"Demand for location {i} cannot be negative.")
                return False
        
        if demands[depot_idx] != 0:
            # Ask if depot demand should be set to 0
            reply = QMessageBox.question(self, "Depot Demand",
                                         "Depot should have 0 demand. Set it to 0?",
                                         QMessageBox.Yes | QMessageBox.No)
            
            if reply == QMessageBox.Yes:
                demands[depot_idx] = 0
                self.location_table.item(depot_idx, 2).setText("0.0")
            else:
                return False
        
        total_demand = sum(demands) - demands[depot_idx]
        if total_demand > num_vehicles * capacity:
            QMessageBox.warning(self, "Invalid Input",
                                f"Total demand ({total_demand}) exceeds total capacity ({num_vehicles * capacity}).")
            return False
        
        return True

    def resizeEvent(self, event):
        """Ensure loading overlay covers entire window when resized"""
        super().resizeEvent(event)
        if hasattr(self, 'loading_overlay'):
            self.loading_overlay.setGeometry(0, 0, self.width(), self.height())

    def show_loading(self, show, message=None):
        """Show/hide loading overlay with message"""
        if message and hasattr(self, 'loading_overlay'):
            self.loading_overlay.set_message(message)
        
        self.loading_overlay.setGeometry(0, 0, self.width(), self.height())
        self.loading_overlay.setVisible(show)
        QApplication.processEvents()  # Force UI update

    def cancel_solving(self):
        """Cancel the ongoing solving process"""
        if hasattr(self, 'solver_thread') and self.solver_thread.isRunning():
            self.solver_thread.terminate()  # Force stop the thread
            self.solver_thread.wait()  # Wait for thread to finish
            self.show_loading(False)
            self.statusBar().showMessage("Optimization cancelled", 3000)

    def solve_vrp(self):
        """Solve the VRP with current inputs"""
        if not self.validate_inputs():
            return
        
        # Get input data
        locations, demands = self.location_table.get_data()
        num_vehicles = self.num_vehicles_input.value()
        depot_idx = self.depot_idx_input.value()
        capacity = self.capacity_input.value()
        
        # Show loading indicator
        self.show_loading(True, "Solving VRP Problem...")
        
        # Create and start worker thread
        self.solver_thread = VRPSolverThread(
            num_vehicles, depot_idx, locations, demands, capacity
        )
        self.solver_thread.finished.connect(self.on_solving_complete)
        self.solver_thread.error.connect(self.on_solving_error)
        self.solver_thread.start()
        
        # Update status bar
        self.statusBar().showMessage("Optimization in progress...")

    def on_solving_complete(self, solution):
        """Handle completion of VRP solving"""
        self.show_loading(False)
        
        if solution['status'] == 'Optimal':
            # Display the solution
            locations, demands = self.location_table.get_data()
            depot_idx = self.depot_idx_input.value()
            capacity = self.capacity_input.value()
            
            # Display the solution on the map
            self.solution_canvas.plot_solution(locations, depot_idx, solution['routes'])
            
            # Prepare solution details with rich formatting
            details = f"""
            <div style='font-family: Segoe UI; padding: 10px;'>
                <div style='font-size: 16px; font-weight: bold; color: #3b82f6; margin-bottom: 15px;'>
                    Solution Summary
                </div>
                
                <div style='background-color: #f1f5f9; padding: 15px; border-radius: 8px; margin-bottom: 20px;'>
                    <div style='font-weight: bold; color: #1e293b;'>Total Distance: 
                        <span style='color: #3b82f6;'>{solution['total_distance']:.2f}</span>
                    </div>
                    <div style='font-weight: bold; color: #1e293b;'>Number of Vehicles Used: 
                        <span style='color: #3b82f6;'>{len(solution['routes'])}</span>
                    </div>
                </div>
                
                <div style='font-size: 14px; font-weight: bold; color: #1e293b; margin-bottom: 10px;'>
                    Route Details:
                </div>
            """
            
            for i, route in enumerate(solution['routes']):
                route_demand = sum(demands[loc] for loc in route if loc != depot_idx)
                route_distance = 0
                for j in range(len(route) - 1):
                    x1, y1 = locations[route[j]]
                    x2, y2 = locations[route[j + 1]]
                    route_distance += math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)
                
                # Calculate load percentage
                load_color = "#10b981"  # Green for low utilization
                if load_percentage > 90:
                    load_color = "#ef4444"  # Red for high utilization
                elif load_percentage > 70:
                    load_color = "#f59e0b"  # Yellow for medium utilization
                
                details += f"""
                <div style='background-color: white; border: 1px solid #e2e8f0; border-radius: 8px; padding: 15px; margin-bottom: 15px;'>
                    <div style='font-weight: bold; color: #3b82f6; margin-bottom: 10px;'>
                        Vehicle {i + 1}
                    </div>
                    
                    <div style='margin-bottom: 10px;'>
                        <span style='font-weight: bold; color: #64748b;'>Route: </span>
                        <span style='color: #1e293b;'>{' → '.join(map(str, route))}</span>
                    </div>
                    
                    <div style='margin-bottom: 10px;'>
                        <span style='font-weight: bold; color: #64748b;'>Distance: </span>
                        <span style='color: #1e293b;'>{route_distance:.2f}</span>
                    </div>
                    
                    <div style='margin-bottom: 10px;'>
                        <span style='font-weight: bold; color: #64748b;'>Load: </span>
                        <span style='color: {load_color};'>{route_demand:.1f} / {capacity:.1f} ({load_percentage:.1f}%)</span>
                    </div>
                </div>
                """
            
            details += "</div>"
            
            self.solution_details.setText(details)
            
            # Switch to solution tab
            self.tab_widget.setCurrentIndex(1)
            
            # Update status bar
            self.statusBar().showMessage(f"Optimization completed successfully. Total distance: {solution['total_distance']:.2f}")
        
        else:
            QMessageBox.warning(self, "No Solution",
                                f"Could not find a solution: {solution['status']}")
            self.statusBar().showMessage(f"Optimization failed: {solution['status']}")

    def on_solving_error(self, error_msg):
        """Handle solving errors"""
        self.show_loading(False)
        QMessageBox.critical(self, "Error", f"An error occurred: {error_msg}")
        self.statusBar().showMessage(f"Optimization error: {error_msg}")
    
    def return_to_launcher(self):
        """Return to the application launcher"""
        self.close()
        # Try to bring the launcher window back to the foreground
        try:
            # This is a simple approach - in a real app, you might want to use
            # inter-process communication to signal the launcher
            if os.name == 'nt':  # Windows
                os.system('python app_launcher.py &')
            else:  # Linux/Mac
                os.system('python3 app_launcher.py &')
        except Exception as e:
            print(f"Error returning to launcher: {e}")


def main():
    app = QApplication(sys.argv)
    
    # Apply light theme
    StyleHelper.apply_light_theme(app)
    
    # Create and show the main window
    window = VRPApp()
    window.show()
    
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
