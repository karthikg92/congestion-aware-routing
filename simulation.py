"""
Define and run the simulation environment
"""
from network import Network
from dp_network import DPNetwork
from traffic_generator import TrafficGenerator


class Simulation:

    def __init__(self):
        self.max_time = 1000  # maximum number of time steps for the simulation
        self.delta_t = 10  # time in seconds per simulation step
        self.t = 0  # current time index of simulation
        self.network = Network()  # road network with users
        self.dp_network = DPNetwork(eps=0.01)  # road network with DP routing
        self.traffic_generator = TrafficGenerator(delta_t=self.delta_t)
        self.cars = []  # list of current cars in the network
        self.dp_cars = []  # list of current cars routed with DP
        self.completed_trips = []  # list of cars whose trips are completed
        self.dp_completed_trips = []  # list of cars with DP routing whose trips are completed

    def run(self):

        # Looping through every time step for the simulation
        for t in range(self.max_time):

            self.network.update_latency(self.cars)  # update latency as a function of active cars
            self.dp_network.update_latency(self.dp_cars)  # update latency for DP network

            # generate demand that can be sent to the DP and non-DP network
            new_demand = self.traffic_generator.new_demand()

            """
            Routing for the non-DP network
            """
            new_cars = self.traffic_generator.new_cars(start_time=t, network=self.network, new_traffic=new_demand)
            self.cars.extend(new_cars)  # draw new demand for this time step

            # update location for each car depending on current network state
            for car in self.cars:
                car.update_location(network=self.network, delta_t=self.delta_t)

            # remove completed trips from active car list
            just_completed = [car for car in self.cars if car.completed_trip is True]
            self.cars = [car for car in self.cars if car.completed_trip is False]
            self.completed_trips.extend(just_completed)

            """
            Routing in the DP network
            """
            new_cars = self.traffic_generator.new_cars(start_time=t, network=self.dp_network, new_traffic=new_demand)
            self.dp_cars.extend(new_cars)  # draw new demand for this time step

            # update location for each car depending on current network state
            for car in self.dp_cars:
                car.update_location(network=self.dp_network, delta_t=self.delta_t)

            # remove completed trips from active car list
            just_completed = [car for car in self.dp_cars if car.completed_trip is True]
            self.dp_cars = [car for car in self.dp_cars if car.completed_trip is False]
            self.dp_completed_trips.extend(just_completed)

            """
            Log and print status
            """
            if t % 600 == 0:
                print('--------------------')
                print('[SimStatus] T = ', t)
                print('--------------------')
                self.print_intermediate_stats()

        return None

    def print_intermediate_stats(self):
        print('No privacy:')
        print('Cars in transit = ', len(self.cars))
        print('Cars that completed trips = ', len(self.completed_trips))
        print('Total = ', self.traffic_generator.cars_generated)

        print('With privacy:')
        print('Cars in transit = ', len(self.dp_cars))
        print('Cars that completed trips = ', len(self.dp_completed_trips))
        print('Total = ', self.traffic_generator.cars_generated)
        return None

    def print_summary_stats(self):
        # TODO: identify appropriate stats to print
        """
        Examples of statistics that might be relevant?
        Error in travel time prediction for each car
        """
        return None
