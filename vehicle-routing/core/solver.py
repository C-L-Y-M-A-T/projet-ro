import math
import numpy as np
import gurobipy as gp
from gurobipy import GRB


class VRPSolver:
    """Vehicle Routing Problem solver using Gurobi"""

    def __init__(self, num_vehicles, depot_idx, locations, demands, capacity):
        """
        Initialize the VRP solver

        Parameters:
        -----------
        num_vehicles : int
            Number of vehicles
        depot_idx : int
            Index of the depot location
        locations : list of tuples
            List of (x, y) coordinates for all locations (including depot)
        demands : list
            Customer demands (demand for depot should be 0)
        capacity : float
            Vehicle capacity
        """
        self.num_vehicles = num_vehicles
        self.depot_idx = depot_idx
        self.locations = locations
        self.demands = demands
        self.capacity = capacity
        self.num_locations = len(locations)
        self.dist_matrix = self._compute_distance_matrix()
        self.solution = None

    def _compute_distance_matrix(self):
        """Compute the distance matrix between all locations"""
        dist_matrix = np.zeros((self.num_locations, self.num_locations))
        for i in range(self.num_locations):
            for j in range(self.num_locations):
                if i != j:
                    x1, y1 = self.locations[i]
                    x2, y2 = self.locations[j]
                    dist_matrix[i, j] = math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)
        return dist_matrix

    def solve(self):
        """Solve the VRP using Gurobi"""
        try:
            # Create a new model
            model = gp.Model("VRP")

            # Create variables
            # x[i,j,k] = 1 if vehicle k travels from location i to location j
            x = model.addVars(self.num_locations, self.num_locations, self.num_vehicles,
                              vtype=GRB.BINARY, name="x")

            # u[i,k] represents the cumulative demand after visiting location i with vehicle k
            u = model.addVars(self.num_locations, self.num_vehicles,
                              vtype=GRB.CONTINUOUS, name="u")

            # Set objective: minimize total distance
            obj = gp.quicksum(self.dist_matrix[i, j] * x[i, j, k]
                              for i in range(self.num_locations)
                              for j in range(self.num_locations) if i != j
                              for k in range(self.num_vehicles))
            model.setObjective(obj, GRB.MINIMIZE)

            # Constraint: each customer must be visited exactly once
            for j in range(self.num_locations):
                if j != self.depot_idx:
                    model.addConstr(gp.quicksum(x[i, j, k]
                                                for i in range(self.num_locations) if i != j
                                                for k in range(self.num_vehicles)) == 1)

            # Constraint: flow conservation - each vehicle that enters a node must exit it
            for k in range(self.num_vehicles):
                for h in range(self.num_locations):
                    model.addConstr(
                        gp.quicksum(x[i, h, k] for i in range(self.num_locations) if i != h) ==
                        gp.quicksum(x[h, j, k] for j in range(self.num_locations) if j != h)
                    )

            # Constraint: all vehicles start and end at the depot
            for k in range(self.num_vehicles):
                model.addConstr(gp.quicksum(x[self.depot_idx, j, k]
                                            for j in range(self.num_locations) if j != self.depot_idx) <= 1)
                model.addConstr(gp.quicksum(x[i, self.depot_idx, k]
                                            for i in range(self.num_locations) if i != self.depot_idx) <= 1)

            # Capacity constraints using MTZ formulation to prevent subtours
            for k in range(self.num_vehicles):
                # Set the starting cumulative demand at depot to 0
                model.addConstr(u[self.depot_idx, k] == 0)

                # Track cumulative demand and prevent subtours
                for i in range(self.num_locations):
                    if i != self.depot_idx:
                        model.addConstr(u[i, k] <= self.capacity)
                        model.addConstr(u[i, k] >= self.demands[i])

                # MTZ subtour elimination
                for i in range(self.num_locations):
                    if i != self.depot_idx:
                        for j in range(self.num_locations):
                            if j != self.depot_idx and i != j:
                                model.addConstr(
                                    u[j, k] >= u[i, k] + self.demands[j] -
                                    self.capacity * (1 - x[i, j, k])
                                )

            # Optimize the model
            model.setParam('OutputFlag', 1)  # Show Gurobi output
            model.optimize()

            # Check if a solution was found
            if model.status == GRB.OPTIMAL:
                # Extract solution
                routes = [[] for _ in range(self.num_vehicles)]

                for k in range(self.num_vehicles):
                    current = self.depot_idx
                    route = [current]

                    while True:
                        next_stop = None
                        for j in range(self.num_locations):
                            if j != current and x[current, j, k].x > 0.5:
                                next_stop = j
                                break

                        if next_stop is None or next_stop == self.depot_idx:
                            if next_stop == self.depot_idx:
                                route.append(self.depot_idx)
                            break

                        route.append(next_stop)
                        current = next_stop

                    if len(route) > 2:  # Only include routes that visit at least one customer
                        routes[k] = route

                # Filter out empty routes
                routes = [r for r in routes if r]

                # Calculate total distance
                total_distance = 0
                for k, route in enumerate(routes):
                    route_distance = 0
                    for i in range(len(route) - 1):
                        route_distance += self.dist_matrix[route[i], route[i + 1]]
                    total_distance += route_distance

                self.solution = {
                    'routes': routes,
                    'total_distance': total_distance,
                    'status': 'Optimal'
                }

                return self.solution
            else:
                self.solution = {
                    'routes': [],
                    'total_distance': 0,
                    'status': 'No solution found'
                }
                return self.solution

        except gp.GurobiError as e:
            print(f"Gurobi error: {e}")
            self.solution = {
                'routes': [],
                'total_distance': 0,
                'status': f'Error: {str(e)}'
            }
            return self.solution