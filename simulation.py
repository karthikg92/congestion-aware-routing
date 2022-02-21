"""
Define and run the simulation environment
"""
from network import Network
from traffic_generator import TrafficGenerator


class Simulation:

    def __init__(self):
        self.max_time = 1000  # maximum number of time steps for the simulation
        self.delta_t = 10  # time in seconds per simulation step
        self.t = 0  # current time index of simulation
        self.network = Network()  # road network with users
        self.traffic_generator = TrafficGenerator(delta_t=self.delta_t)
        self.cars = []  # list of current cars in the network
        self.completed_trips = []  # list of cars whose trips are completed

    def run(self):

        # Looping through every time step for the simulation
        for t in range(self.max_time):
            self.network.update_latency(self.cars)  # update latency as a function of active cars

            new_cars = self.traffic_generator.new_cars(start_time=t, network=self.network)
            self.cars.extend(new_cars)  # draw new demand for this time step

            # update location for each car depending on current network state
            for car in self.cars:
                car.update_location(network=self.network, delta_t=self.delta_t)

            # remove completed trips from active car list
            just_completed = [car for car in self.cars if car.completed_trip is True]
            self.cars = [car for car in self.cars if car.completed_trip is False]
            self.completed_trips.extend(just_completed)

            if t % 600 == 0:
                print('--------------------')
                print('[SimStatus] T = ', t)
                print('--------------------')
                self.print_stats()

        return None

    def print_stats(self):
        # TODO: log parameters and print progress
        print('Cars in transit = ', len(self.cars))
        print('Cars that completed trips = ', len(self.completed_trips))
        print('Total = ', self.traffic_generator.cars_generated)
        return None
