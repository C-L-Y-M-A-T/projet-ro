from PyQt5.QtWidgets import QTableWidget, QTableWidgetItem, QHeaderView
from PyQt5.QtCore import Qt, pyqtSlot


class LocationTable(QTableWidget):
    """Table for displaying and editing location data with numeric validation"""

    def __init__(self, parent=None):
        super(LocationTable, self).__init__(parent)
        self.setColumnCount(3)
        self.setHorizontalHeaderLabels(['X', 'Y', 'Demand'])
        
        # Set column widths
        header = self.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.Stretch)
        header.setSectionResizeMode(1, QHeaderView.Stretch)
        header.setSectionResizeMode(2, QHeaderView.Stretch)
        
        # Set alternating row colors
        self.setAlternatingRowColors(True)
        
        # Set selection behavior
        self.setSelectionBehavior(QTableWidget.SelectRows)
        
        # Set edit triggers
        self.setEditTriggers(QTableWidget.DoubleClicked | QTableWidget.EditKeyPressed)
        
        # Connect to itemChanged signal for validation
        self.itemChanged.connect(self.validate_numeric_input)

    def set_data(self, locations, demands):
        """Set the table data from locations and demands lists"""
        # Temporarily disconnect the itemChanged signal to avoid validation during bulk updates
        self.itemChanged.disconnect(self.validate_numeric_input)
        
        self.setRowCount(len(locations))

        for i, ((x, y), demand) in enumerate(zip(locations, demands)):
            x_item = QTableWidgetItem(f"{x:.2f}")
            y_item = QTableWidgetItem(f"{y:.2f}")
            demand_item = QTableWidgetItem(f"{demand:.1f}")
            
            # Set text alignment
            x_item.setTextAlignment(Qt.AlignCenter)
            y_item.setTextAlignment(Qt.AlignCenter)
            demand_item.setTextAlignment(Qt.AlignCenter)
            
            self.setItem(i, 0, x_item)
            self.setItem(i, 1, y_item)
            self.setItem(i, 2, demand_item)
        
        # Reconnect the itemChanged signal
        self.itemChanged.connect(self.validate_numeric_input)

    def get_data(self):
        """Get locations and demands from the table"""
        rows = self.rowCount()
        locations = []
        demands = []

        for i in range(rows):
            try:
                x = float(self.item(i, 0).text())
                y = float(self.item(i, 1).text())
                demand = float(self.item(i, 2).text())

                locations.append((x, y))
                demands.append(demand)
            except (ValueError, AttributeError):
                # Skip invalid rows
                pass

        return locations, demands
    
    @pyqtSlot(QTableWidgetItem)
    def validate_numeric_input(self, item):
        """Validate that the input is numeric for all columns"""
        try:
            # Try to convert to float
            value = float(item.text())
            
            # Format to appropriate decimal places
            if item.column() == 2:  # Demand column
                item.setText(f"{value:.1f}")
            else:  # X and Y columns
                item.setText(f"{value:.2f}")
                
        except ValueError:
            # If not a valid number, reset to 0
            if item.column() == 2:  # Demand column
                item.setText("0.0")
            else:  # X and Y columns
                item.setText("0.00")
