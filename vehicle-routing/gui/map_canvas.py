import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import numpy as np


class MapCanvas(FigureCanvas):
    """Canvas for displaying the map and routes"""

    def __init__(self, parent=None, width=8, height=6, dpi=100):
        # Set style before creating figure
        plt.style.use('default')
        
        # Create figure with white background
        self.fig = Figure(figsize=(width, height), dpi=dpi, facecolor='#ffffff')
        self.axes = self.fig.add_subplot(111, facecolor='#f8f9fa')
        
        # Customize axes appearance
        self.axes.spines['top'].set_visible(False)
        self.axes.spines['right'].set_visible(False)
        self.axes.spines['left'].set_color('#cbd5e1')
        self.axes.spines['bottom'].set_color('#cbd5e1')
        self.axes.tick_params(colors='#64748b')
        self.axes.grid(color='#e2e8f0', linestyle='-', linewidth=0.5, alpha=0.7)
        
        super(MapCanvas, self).__init__(self.fig)
        self.setParent(parent)
        
        # Set minimum size
        self.setMinimumSize(400, 300)
        
        # Initialize plot elements
        self.depot_marker = None
        self.customer_markers = None
        self.route_lines = []
        
        # Set tight layout
        self.fig.tight_layout(pad=3.0)

    def clear_plot(self):
        """Clear the plot"""
        self.axes.clear()
        self.route_lines = []
        
        # Reset axes appearance
        self.axes.spines['top'].set_visible(False)
        self.axes.spines['right'].set_visible(False)
        self.axes.spines['left'].set_color('#cbd5e1')
        self.axes.spines['bottom'].set_color('#cbd5e1')
        self.axes.tick_params(colors='#64748b')
        self.axes.grid(color='#e2e8f0', linestyle='-', linewidth=0.5, alpha=0.7)
        
        self.fig.canvas.draw()

    def plot_locations(self, locations, depot_idx):
        """Plot all locations on the map"""
        self.clear_plot()
        
        if not locations:
            self.axes.set_title('No locations to display', color='#64748b')
            self.fig.canvas.draw()
            return
        
        x_coords = [loc[0] for loc in locations]
        y_coords = [loc[1] for loc in locations]
        
        # Plot all locations
        self.axes.scatter(x_coords, y_coords, color='#3b82f6', s=80, alpha=0.7, 
                          edgecolor='white', linewidth=1.5, zorder=2)
        
        # Highlight the depot
        if 0 <= depot_idx < len(locations):
            self.axes.scatter(locations[depot_idx][0], locations[depot_idx][1],
                              color='#ef4444', s=150, marker='*', 
                              edgecolor='white', linewidth=1.5, zorder=3)
        
        # Add location indices
        for i, (x, y) in enumerate(locations):
            if i == depot_idx:
                # Depot label
                self.axes.annotate(str(i), (x, y), xytext=(0, 0),
                                   textcoords='offset points', ha='center', va='center',
                                   color='white', fontweight='bold', fontsize=9, zorder=4)
            else:
                # Customer label
                self.axes.annotate(str(i), (x, y), xytext=(0, 0),
                                   textcoords='offset points', ha='center', va='center',
                                   color='white', fontweight='bold', fontsize=9, zorder=4)
        
        # Set axis labels and title
        self.axes.set_xlabel('X Coordinate', fontsize=10, color='#1e293b')
        self.axes.set_ylabel('Y Coordinate', fontsize=10, color='#1e293b')
        self.axes.set_title('VRP Locations', fontsize=12, fontweight='bold', color='#1e293b')
        
        # Add a legend
        self.axes.scatter([], [], color='#3b82f6', s=80, edgecolor='white', linewidth=1.5, label='Customer')
        self.axes.scatter([], [], color='#ef4444', s=150, marker='*', edgecolor='white', linewidth=1.5, label='Depot')
        self.axes.legend(loc='upper right', frameon=True, framealpha=0.9, 
                         facecolor='white', edgecolor='#cbd5e1')
        
        # Set axis limits with some padding
        x_min, x_max = min(x_coords), max(x_coords)
        y_min, y_max = min(y_coords), max(y_coords)
        x_padding = (x_max - x_min) * 0.1 if x_max > x_min else 10
        y_padding = (y_max - y_min) * 0.1 if y_max > y_min else 10
        self.axes.set_xlim(x_min - x_padding, x_max + x_padding)
        self.axes.set_ylim(y_min - y_padding, y_max + y_padding)
        
        # Update the figure
        self.fig.tight_layout(pad=3.0)
        self.fig.canvas.draw()

    def plot_solution(self, locations, depot_idx, routes):
        """Plot the solution routes on the map"""
        self.clear_plot()
        
        if not locations or not routes:
            self.axes.set_title('No solution to display', color='#64748b')
            self.fig.canvas.draw()
            return
        
        # Plot all locations
        x_coords = [loc[0] for loc in locations]
        y_coords = [loc[1] for loc in locations]
        
        # Plot all locations (customers)
        self.axes.scatter(x_coords, y_coords, color='#3b82f6', s=80, alpha=0.7, 
                          edgecolor='white', linewidth=1.5, zorder=2)
        
        # Highlight the depot
        if 0 <= depot_idx < len(locations):
            self.axes.scatter(locations[depot_idx][0], locations[depot_idx][1],
                              color='#ef4444', s=150, marker='*', 
                              edgecolor='white', linewidth=1.5, zorder=3)
        
        # Add location indices
        for i, (x, y) in enumerate(locations):
            if i == depot_idx:
                # Depot label
                self.axes.annotate(str(i), (x, y), xytext=(0, 0),
                                   textcoords='offset points', ha='center', va='center',
                                   color='white', fontweight='bold', fontsize=9, zorder=4)
            else:
                # Customer label
                self.axes.annotate(str(i), (x, y), xytext=(0, 0),
                                   textcoords='offset points', ha='center', va='center',
                                   color='white', fontweight='bold', fontsize=9, zorder=4)
        
        # Plot routes with different colors
        # Use a modern color palette that matches the Production Problem app
        colors = ['#3b82f6', '#8b5cf6', '#10b981', '#f59e0b', '#ef4444', 
                  '#06b6d4', '#84cc16', '#ec4899', '#f97316', '#6366f1']
        
        for i, route in enumerate(routes):
            color = colors[i % len(colors)]
            
            # Plot route lines
            route_x = [locations[j][0] for j in route]
            route_y = [locations[j][1] for j in route]
            self.axes.plot(route_x, route_y, '-', color=color, linewidth=2.5, 
                           alpha=0.7, label=f'Vehicle {i + 1}', zorder=1)
            
            # Add arrows to show direction
            for j in range(len(route) - 1):
                x1, y1 = locations[route[j]]
                x2, y2 = locations[route[j + 1]]
                dx = x2 - x1
                dy = y2 - y1
                
                # Calculate the position for the arrow (80% along the path)
                arrow_x = x1 + dx * 0.6
                arrow_y = y1 + dy * 0.6
                
                # Calculate the direction vector
                length = np.sqrt(dx**2 + dy**2)
                if length > 0:
                    dx = dx / length
                    dy = dy / length
                
                # Draw the arrow
                self.axes.arrow(arrow_x, arrow_y, dx * 3, dy * 3, 
                                head_width=2, head_length=3, fc=color, ec=color, 
                                alpha=0.9, zorder=5)
        
        # Set axis labels and title
        self.axes.set_xlabel('X Coordinate', fontsize=10, color='#1e293b')
        self.axes.set_ylabel('Y Coordinate', fontsize=10, color='#1e293b')
        self.axes.set_title('VRP Solution', fontsize=12, fontweight='bold', color='#1e293b')
        
        # Add a legend
        self.axes.legend(loc='upper right', frameon=True, framealpha=0.9, 
                         facecolor='white', edgecolor='#cbd5e1')
        
        # Set axis limits with some padding
        x_min, x_max = min(x_coords), max(x_coords)
        y_min, y_max = min(y_coords), max(y_coords)
        x_padding = (x_max - x_min) * 0.1 if x_max > x_min else 10
        y_padding = (y_max - y_min) * 0.1 if y_max > y_min else 10
        self.axes.set_xlim(x_min - x_padding, x_max + x_padding)
        self.axes.set_ylim(y_min - y_padding, y_max + y_padding)
        
        # Update the figure
        self.fig.tight_layout(pad=3.0)
        self.fig.canvas.draw()
