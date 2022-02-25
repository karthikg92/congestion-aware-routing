"""
Define and run the simulation environment
"""
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from alive_progress import alive_bar


from network import Network
from dp_network import DPNetwork
from traffic_generator import TrafficGenerator


class Simulation:

    def __init__(self, demand_scenario=None, capacity_scenario=None, eps=0.01, fname=None):
        self.demand_scenario = demand_scenario
        self.capacity_scenario = capacity_scenario
        self.max_time = 10  # maximum number of time steps for the simulation
        self.delta_t = 10  # time in seconds per simulation step
        self.t = 0  # current time index of simulation
        self.counts_update_time = 120  # time intervals at which counts are updated
        self.network = Network(capacity_scenario=capacity_scenario)  # road network with users
        self.dp_network = DPNetwork(eps=eps, capacity_scenario=capacity_scenario)  # road network with DP routing
        self.traffic_generator = TrafficGenerator(delta_t=self.delta_t, demand_scenario=demand_scenario)
        self.new_cars = None  # new cars generated for a time instant
        self.cars = []  # list of current cars in the network
        self.dp_cars = []  # list of current cars routed with DP
        self.completed_trips = []  # list of cars whose trips are completed
        self.dp_completed_trips = []  # list of cars with DP routing whose trips are completed
        self.run_log = []  # log runtime results
        self.fname = fname  # path for storing results and runtime progress

    def run(self):

        # Initializing run__log
        self.run_log = []

        # Looping through every time step for the simulation
        t = 0

        # Initializing progress bar
        with alive_bar(self.max_time) as bar:

            # Run simulation for max_time and then wait till all cars reach destination
            while t < self.max_time or len(self.cars) > 0 or len(self.dp_cars) > 0:

                # Progress update of the simulation
                if t < self.max_time:
                    bar()
                elif t == self.max_time:
                    print('[Simulation] Cool off period begins')

                if t % int(self.counts_update_time / self.delta_t) == 0:
                    self.network.update_latency(self.cars)  # update latency as a function of active cars
                    self.dp_network.update_latency(self.dp_cars)  # update latency for DP network

                # generate demand that can be sent to the DP and non-DP network
                if t < self.max_time:
                    # only generate demand for max_time
                    new_demand = self.traffic_generator.new_demand()
                else:
                    # after max_time, new demand = 0
                    new_demand = 0 * self.traffic_generator.new_demand()

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

                # Log and update status
                log_t = {'t': t,
                         'new_cars_added': len(new_cars),
                         'cars_in_transit': len(self.cars),
                         'completed_trips': len(just_completed),
                         'edge_utilization': self.network.edge_utilization}

                self._update_run_log(log_t)

                """
                Routing in the DP network
                """
                new_cars = self.traffic_generator.new_cars(start_time=t,
                                                           network=self.dp_network,
                                                           new_traffic=new_demand)
                self.dp_cars.extend(new_cars)  # draw new demand for this time step

                # update location for each car depending on current network state
                for car in self.dp_cars:
                    car.update_location(network=self.dp_network, delta_t=self.delta_t)

                # remove completed trips from active car list
                just_completed = [car for car in self.dp_cars if car.completed_trip is True]
                self.dp_cars = [car for car in self.dp_cars if car.completed_trip is False]
                self.dp_completed_trips.extend(just_completed)

                # increment time counter
                t += 1

        # self._print_intermediate_stats()
        return None

    def _update_run_log(self, log_t):
        # update master log
        self.run_log.append(log_t)

        # create a dataframe
        log_df = pd.DataFrame(self.run_log)

        # plot progress
        log_df.plot(x='t', y=['new_cars_added', 'cars_in_transit', 'completed_trips'])
        plt.xlabel('time step')
        plt.ylabel('counts')
        plt.savefig(self.fname + '_flow_evolution_log.png')
        plt.close()

        # save edge utilization
        edge_utilization_array = np.vstack(log_df['edge_utilization'].to_list())
        np.savetxt(self.fname + "_array_utilization.csv", edge_utilization_array, delimiter=",")

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

    def _compute_car_stats_df(self):

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

        for car in self.completed_trips:
            if car.id in common_id:
                stat[car.id] = {'path': car.path,
                                'tt': (car.finish_time - car.start_time) * self.delta_t,
                                'est_tt': car.estimated_trip_time}

        for car in self.dp_completed_trips:
            if car.id in common_id:
                stat[car.id]['dp_path'] = car.path
                stat[car.id]['dp_tt'] = (car.finish_time - car.start_time) * self.delta_t
                stat[car.id]['dp_est_tt'] = car.estimated_trip_time

        # Compute performance metrics
        stat_df = pd.DataFrame(stat.values())
        stat_df['dp_induced_excess_tt'] = stat_df['dp_tt'] - stat_df['tt']
        stat_df['path_similarity'] = stat_df.apply(
            lambda x: len(set(x.path).intersection(x.dp_path)) * 2 / (len(x.path) + len(x.dp_path)), axis=1)
        stat_df['tt_est_error'] = stat_df['tt'] - stat_df['est_tt']
        stat_df['dp_tt_est_error'] = stat_df['dp_tt'] - stat_df['dp_est_tt']

        # retaining only relevant columns and saving the results
        stat_df.drop(columns=['path', 'dp_path'], inplace=True)

        return stat_df

    def _save_capacity(self):
        capacity_df = pd.DataFrame({'capacity': self.network.edge_capacity_list()})
        capacity_df.to_csv(self.fname + '_edgeflowcapacity.csv', index=False, sep=',')

    def _save_critical_counts(self):
        counts_df = pd.DataFrame({'counts': self.network.critical_counts_list()})
        counts_df.to_csv(self.fname + '_critical_counts.csv', index=False, sep=',')

    def _save_demand(self):
        demand_df = pd.DataFrame({'lambda': self.traffic_generator.poisson_parameters()})
        demand_df.to_csv(self.fname + '_lambda.csv', index=False, sep=',')

    def save_summary_stats(self):

        # car specific stats
        stat_df = self._compute_car_stats_df()
        stat_df.to_csv(self.fname + '.csv', index=False, sep=',')

        self._save_capacity()

        self._save_demand()

        self._save_critical_counts()

        return None
