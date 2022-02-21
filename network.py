import numpy as np
from car import Car
from scipy.sparse.csgraph import shortest_path
import pandas as pd


class Network:

    def __init__(self):

        self.df_edges = pd.read_csv("Locations/SiouxFalls/edges.csv")
        self.df_vertices = pd.read_csv("Locations/SiouxFalls/vertices.csv")

        self.num_edges = self.df_edges.shape[0]
        self.num_vertices = self.df_vertices.shape[0]
        self.edge_capacity = (self.df_edges['capacity'] / 2.4).to_list()  # TODO: fixme
        self.edge_max_speed = self.df_edges['speed'].to_list()
        self.edge_distance = self.df_edges['length'].to_list()

        self.nodes_to_edge = self._compute_nodes_to_edge()
        # self.edge_to_nodes = None
        # self._initialize_network()  # initialize above network parameters

        # Current traffic state of the network
        self.traffic_count = np.zeros(self.num_edges)  # zero cars on all edges

        # Current latency of network
        self.latency = [self.edge_distance[e]/self.edge_max_speed[e] for e in range(self.num_edges)]

        self.predecessor_matrix = None
        self.num_cars_generated = 0

    def _compute_nodes_to_edge(self):
        n2e = {}
        for i in range(self.num_edges):
            orig = int(self.df_edges.iloc[i]['edge_tail'])
            dest = int(self.df_edges.iloc[i]['edge_head'])
            n2e[(orig, dest)] = i

        return n2e

    def _counts_to_latency(self):
        # TODO: fixme
        """
        Use self.traffic_count data
        Return: latency array
        Formula:    latency[e] = length[e]/max_speed[e] if flow[e] < capacity
                    latency[e] = length[e]/max_speed[e] + alpha * (flow[e]-capacity[e])^4 if flow[e] > capacity
        """
        alpha = 1e-1
        latency = []
        for e in range(self.num_edges):

            min_latency = self.edge_distance[e] / self.edge_max_speed[e]

            if self.traffic_count[e] <= self.edge_capacity[e]:
                latency.append(min_latency)
            else:
                latency.append(min_latency +
                               alpha * (self.traffic_count[e] - self.edge_capacity[e]) ** 4)

        return latency

    def shortest_path(self, origin, destination):

        # Cautionary check if predecessor matrix is not initialized
        if self.predecessor_matrix is None:
            self._update_predecessor_matrix()

        # Extract the shortest path in terns of the vertex sequence
        vertex_path = [destination]
        current = destination
        while current != origin:
            pre = self.predecessor_matrix[origin, current]
            vertex_path.insert(0, pre)
            current = pre

        # Extract edge sequence from vertex sequence
        edge_path = []
        for i in range(len(vertex_path) - 1):
            od = (vertex_path[i], vertex_path[i+1])
            edge_path.append(self.nodes_to_edge[od])

        return edge_path

    def update_latency(self, cars):

        # get new self.traffic counts
        self.traffic_count = np.zeros(self.num_edges)
        for car in cars:
            current_edge = car.current_edge
            self.traffic_count[current_edge] += 1

        # call the counts to latency function
        self.latency = self._counts_to_latency()

        # update predecessor matrix that stores the shortest paths
        self._update_predecessor_matrix()

        return None

    def _update_predecessor_matrix(self):
        """
        use the current latency estimates to update the predecessor matrix
        return: none
        """

        # set up adjacency matrix
        adj = np.zeros((self.num_vertices, self.num_vertices))
        for i in range(self.num_edges):
            orig = int(self.df_edges.iloc[i]['edge_tail'])
            dest = int(self.df_edges.iloc[i]['edge_head'])
            adj[orig, dest] = self.latency[i]

        # compute the shortest paths
        _, self.predecessor_matrix = shortest_path(adj, directed=True, return_predecessors=True)

    def edge_length(self, edge_index):
        return self.edge_distance[edge_index]

    def edge_speed(self, edge_index):
        return self.latency[edge_index]
