import numpy as np
from car import Car
from scipy.sparse.csgraph import shortest_path
import pandas as pd


class Network:

    def __init__(self, capacity_scenario=None):

        self.city = 'SiouxFalls'

        self.capacity_scenario = capacity_scenario

        self.df_edges = pd.read_csv("Locations/" + self.city + "/edges.csv")
        self.df_vertices = pd.read_csv("Locations/" + self.city + "/vertices.csv")

        self.num_edges = self.df_edges.shape[0]
        self.num_vertices = self.df_vertices.shape[0]

        # max speed is in km/hr in the dataset. Converting to m/s
        self.edge_max_speed = (self.df_edges['speed'] * 1000 / 3600).to_list()
        self.edge_distance = self.df_edges['length'].to_list()

        """
        The edge flow capacity presented in the dataset is 0.1 the flow capacity of the whole day
        Thus, the 2.4 division is edge flow capacity for a day
        The subsequent division by 3600 is edge flow capacity per second
        """
        self.edge_flow_capacity = (self.df_edges['capacity'] / 2.4 / 3600).to_list()

        self.critical_counts = [self.edge_flow_capacity[i] * self.edge_distance[i] / self.edge_max_speed[i]
                                for i in range(self.num_edges)]

        # load mapping from counts to flow # TODO: better variable name
        _, self.x_star = np.load('counts2flow_LUT_ymax200.npy')

        # Dictionary with key (origin, destination) and value as edge index
        self.nodes_to_edge = self._compute_nodes_to_edge()

        # Current traffic state of the network
        self.traffic_count = np.zeros(self.num_edges)  # zero cars on all edges

        # Latency of network. Current value will be updated
        self.latency = [self.edge_distance[e]/self.edge_max_speed[e] for e in range(self.num_edges)]

        # track link utilization
        self.edge_utilization = np.zeros((1, self.num_edges))

        # shortest path routing attributes
        self.predecessor_matrix = None
        self.min_distance_matrix = None

    # """
    # Computes the edge capacity for different scenarios
    # Not currently used as we decided to stick to the baseline capacity
    # """
    # def _compute_c(self):
    #     flow = (self.df_edges['capacity'] / 2.4 / 3600).to_list()
    #     c = [flow[i] * self.edge_distance[i] / self.edge_max_speed[i] for i in range(len(flow))]
    #
    #     if self.capacity_scenario == 'low':
    #         c = [0.5 * capacity for capacity in c]
    #     if self.capacity_scenario == 'high':
    #         c = [1.5 * capacity for capacity in c]
    #
    #     return c

    def _compute_nodes_to_edge(self):
        n2e = {}
        for i in range(self.num_edges):
            orig = int(self.df_edges.iloc[i]['edge_tail'])
            dest = int(self.df_edges.iloc[i]['edge_head'])
            n2e[(orig, dest)] = i

        return n2e

    def _counts_to_latency(self, traffic_count):
        """
        Input: Traffic count on each link
        Return: latency array
        Formula: Refer to slack notes # TODO: Write the formula
        """
        b = 0.15
        latency = []

        for e in range(self.num_edges):

            y_hat = traffic_count[e] / (self.edge_flow_capacity[e] * self.edge_distance[e] / self.edge_max_speed[e])
            j = int(y_hat * 1e3)
            a = self.edge_distance[e] / self.edge_max_speed[e]
            latency.append(a * (1 + b * (self.x_star[j]) ** 4))

        return latency

    def _path_from_predecessor(self, origin, destination, predecessor_matrix):

        # Extract the shortest path in terns of the vertex sequence
        vertex_path = [destination]
        current = destination
        while current != origin:
            pre = predecessor_matrix[origin, current]
            vertex_path.insert(0, pre)
            current = pre

        # Extract edge sequence from vertex sequence
        edge_path = []
        for i in range(len(vertex_path) - 1):
            od = (vertex_path[i], vertex_path[i + 1])
            edge_path.append(self.nodes_to_edge[od])

        return edge_path

    def shortest_path(self, origin, destination):

        # Cautionary check if predecessor matrix is not initialized
        if self.predecessor_matrix is None:
            self.min_distance_matrix, self.predecessor_matrix = self._update_predecessor_matrix(self.latency)

        edge_path = self._path_from_predecessor(origin, destination, self.predecessor_matrix)

        return edge_path

    def update_latency(self, cars):

        # get new self.traffic counts
        self.traffic_count = np.zeros(self.num_edges)
        for car in cars:
            current_edge = car.current_edge
            self.traffic_count[current_edge] += 1

        # call the counts to latency function
        self.latency = self._counts_to_latency(self.traffic_count)

        # update predecessor matrix that stores the shortest paths
        self.min_distance_matrix, self.predecessor_matrix = self._update_predecessor_matrix(self.latency)

        # update link utilization
        self.edge_utilization = self._compute_edge_utilization(self.traffic_count)

        return None

    def _update_predecessor_matrix(self, latency):
        """
        use the current latency estimates to update the predecessor matrix
        return: none
        """

        # set up adjacency matrix
        adj = np.zeros((self.num_vertices, self.num_vertices))
        for i in range(self.num_edges):
            orig = int(self.df_edges.iloc[i]['edge_tail'])
            dest = int(self.df_edges.iloc[i]['edge_head'])
            adj[orig, dest] = latency[i]

        # compute the shortest paths
        dist, pre = shortest_path(adj, directed=True, return_predecessors=True)

        return dist, pre

    def _compute_edge_utilization(self, traffic):
        edge_utilization = np.zeros((1, self.num_edges))
        for e in range(self.num_edges):
            y_hat = traffic[e] / (self.edge_flow_capacity[e] * self.edge_distance[e] / self.edge_max_speed[e])
            j = int(y_hat * 1e3)  # Update if the counts to flow datafile changes
            edge_utilization[0, e] = self.x_star[j]
        return edge_utilization

    def edge_length(self, edge_index):
        return self.edge_distance[edge_index]

    def edge_speed(self, edge_index):
        return self.edge_distance[edge_index] / self.latency[edge_index]

    def estimate_travel_time(self, origin, destination):
        path = self.shortest_path(origin, destination)
        tt = 0
        for edge_index in path:
            tt += self.latency[edge_index]
        return tt

    def edge_capacity_list(self):
        return self.edge_flow_capacity

    def critical_counts_list(self):
        return self.critical_counts

