"""
Network class with added functionalities for DP
"""

from network import Network
import numpy as np


class DPNetwork(Network):

    def __init__(self, eps=None, capacity_scenario=None):

        Network.__init__(self, capacity_scenario=capacity_scenario)

        self.epsilon = eps

        self.dp_traffic_counts = None
        self.dp_latency = None
        self.dp_predecessor_matrix = None
        self.dp_min_distance_matrix = None

    def update_latency(self, cars):
        """
        Main addition is computing noisy traffic counts and updating noisy latency
        """

        # get new self.traffic counts
        self.traffic_count = np.zeros(self.num_edges)
        for car in cars:
            current_edge = car.current_edge
            self.traffic_count[current_edge] += 1

        # compute noisy traffic counts
        noisy_counts = [counts + np.random.laplace(scale=1/self.epsilon) for counts in self.traffic_count]
        self.dp_traffic_counts = [max(c, 0) for c in noisy_counts]

        # call the counts to latency function
        self.latency = self._counts_to_latency(self.traffic_count)
        self.dp_latency = self._counts_to_latency(self.dp_traffic_counts)

        # update predecessor matrix that stores the shortest paths
        self.min_distance_matrix, self.predecessor_matrix = self._update_predecessor_matrix(self.latency)  # TODO:
        # Dont need to compute this!
        self.dp_min_distance_matrix, self.dp_predecessor_matrix = self._update_predecessor_matrix(self.dp_latency)

        return None

    def shortest_path(self, origin, destination):
        """
        Need to return the shortest path based on a noisy estimate of the travel counts
        """

        # Cautionary check if DP predecessor matrix is not initialized
        if self.dp_predecessor_matrix is None:
            self.dp_min_distance_matrix, self.dp_predecessor_matrix = self._update_predecessor_matrix(self.dp_latency)

        edge_path = self._path_from_predecessor(origin, destination, self.dp_predecessor_matrix)

        return edge_path

    def estimate_travel_time(self, origin, destination):
        """
        Need to override and estimate travel time based on noisy counts measurement
        """
        path = self.shortest_path(origin, destination)
        tt = 0
        for edge_index in path:
            tt = self.dp_latency[edge_index]
        return tt
