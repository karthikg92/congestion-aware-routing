"""
Define and run the simulation environment
"""
import pandas as pd

from network import Network
from dp_network import DPNetwork
from traffic_generator import TrafficGenerator


class Simulation:

    def __init__(self, demand_scenario=None, capacity_scenario=None, eps=0.01):
        self.demand_scenario = demand_scenario
        self.capacity_scenario = capacity_scenario
        self.max_time = 720  # maximum number of time steps for the simulation
        self.delta_t = 10  # time in seconds per simulation step
        self.t = 0  # current time index of simulation
        self.counts_update_time = 120  # time intervals at which counts are updated
        self.network = Network(capacity_scenario=capacity_scenario)  # road network with users
        self.dp_network = DPNetwork(eps=eps, capacity_scenario=capacity_scenario)  # road network with DP routing
        self.traffic_generator = TrafficGenerator(delta_t=self.delta_t, demand_scenario=demand_scenario)
        self.cars = []  # list of current cars in the network
        self.dp_cars = []  # list of current cars routed with DP
        self.completed_trips = []  # list of cars whose trips are completed
        self.dp_completed_trips = []  # list of cars with DP routing whose trips are completed

    def run(self):

        # Looping through every time step for the simulation
        for t in range(self.max_time):

            print(t)

            if t % int(self.counts_update_time / self.delta_t) == 0:
                self.network.update_latency(self.cars)  # update latency as a function of active cars
                self.dp_network.update_latency(self.dp_cars)  # update latency for DP network

            # generate demand that can be sent to the DP and non-DP network
            new_demand = self.traffic_generator.new_demand()

            """
            Routing for the non-DP network
            """
            new_cars = self.traffic_generator.new_cars(start_time=t, network=self.network, new_traffic=new_demand)
            self.cars.extend(new_cars)  # draw new demand for this time step

            # print((new_demand))
            # print((new_cars))
            assert sum(new_demand) == len(new_cars)

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
            # print(t)
            # if t % 600 == 0:
                # print('--------------------')
                # print('[SimStatus] T = ', t)
                # print('--------------------')
                # self._print_intermediate_stats()
        self._print_intermediate_stats()
        return None

    def _print_intermediate_stats(self):
        print('No privacy:')
        print('Cars in transit = ', len(self.cars))
        print('Cars that completed trips = ', len(self.completed_trips))
        print('Total = ', self.traffic_generator.cars_generated)

        print('With privacy:')
        print('Cars in transit = ', len(self.dp_cars))
        print('Cars that completed trips = ', len(self.dp_completed_trips))
        print('Total = ', self.traffic_generator.dp_cars_generated)
        return None

    def save_summary_stats(self, fname=None):
        """
        Metrics:
            For a car, difference in trip time between private and non-private version
            Total trip time
            When are cars assigned the ''same'' route? (at most 10% of edges are different?)
        """

        """
        Efficiently store information in a dictionary with id = car.id
        """

        stat = {}

        completed_car_id = {car.id for car in self.completed_trips}
        dp_completed_car_id = {car.id for car in self.dp_completed_trips}

        common_id = completed_car_id.intersection(dp_completed_car_id)

        # print('Computed common id')

        for car in self.completed_trips:
            if car.id in common_id:
                stat[car.id] = {'path': car.path,
                                'tt': (car.finish_time - car.start_time) * self.delta_t,
                                'est_tt': car.estimated_trip_time}

        # print('ckpt 1')

        for car in self.dp_completed_trips:
            if car.id in common_id:
                stat[car.id]['dp_path'] = car.path
                stat[car.id]['dp_tt'] = (car.finish_time - car.start_time) * self.delta_t
                stat[car.id]['dp_est_tt'] = car.estimated_trip_time

        # print('ckpt 2')

        # Compute performance metrics
        stat_df = pd.DataFrame(stat.values())
        stat_df['dp_induced_excess_tt'] = stat_df['dp_tt'] - stat_df['tt']
        stat_df['path_similarity'] = stat_df.apply(
            lambda x: len(set(x.path).intersection(x.dp_path)) * 2 / (len(x.path) + len(x.dp_path)), axis=1)
        stat_df['tt_est_error'] = stat_df['tt'] - stat_df['est_tt']
        stat_df['dp_tt_est_error'] = stat_df['dp_tt'] - stat_df['dp_est_tt']

        # print('ckpt 3')

        # retaining only relevant columns and saving the results
        stat_df.drop(columns=['path', 'dp_path'], inplace=True)
        stat_df.to_csv(fname + '.csv', index=False, sep=',')

        """
        Extract other edge params
        """

        lambda_path = fname.split('/')[0] + '/lambda_'
        if self.demand_scenario is None or self.demand_scenario == 'baseline':
            lambda_path = lambda_path + 'baseline.csv'
        if self.demand_scenario == 'low':
            lambda_path = lambda_path + 'low.csv'
        if self.demand_scenario == 'high':
            lambda_path = lambda_path + 'high.csv'

        lambda_df = pd.DataFrame({'lambda': self.traffic_generator.poisson_parameters()})
        lambda_df.to_csv(lambda_path, index=False, sep=',')

        capacity_path = fname.split('/')[0] + '/capacity_'
        if self.capacity_scenario is None or self.capacity_scenario == 'baseline':
            capacity_path = capacity_path + 'baseline.csv'
        if self.capacity_scenario == 'low':
            capacity_path = capacity_path + 'low.csv'
        if self.capacity_scenario == 'high':
            capacity_path = capacity_path + 'high.csv'

        capacity_df = pd.DataFrame({'capacity': self.network.edge_capacity_list()})
        capacity_df.to_csv(capacity_path, index=False, sep=',')

        return None
