from PyQt5.QtCore import QThread, pyqtSignal

from core.solver import VRPSolver


class VRPSolverThread(QThread):
    finished = pyqtSignal(dict)  # Signal to emit when solving is complete
    error = pyqtSignal(str)     # Signal for errors

    def __init__(self, num_vehicles, depot_idx, locations, demands, capacity):
        super().__init__()
        self.num_vehicles = num_vehicles
        self.depot_idx = depot_idx
        self.locations = locations
        self.demands = demands
        self.capacity = capacity

    def run(self):
        try:
            solver = VRPSolver(
                self.num_vehicles,
                self.depot_idx,
                self.locations,
                self.demands,
                self.capacity
            )
            solution = solver.solve()
            self.finished.emit(solution)
        except Exception as e:
            self.error.emit(str(e))