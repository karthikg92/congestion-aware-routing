import numpy as np
import pandas as pd
from car import Car
from network import Network


class TrafficGenerator:

    def __init__(self, delta_t=None, demand_scenario=None):

        # time interval for computing poisson rate
        self.delta_t = delta_t

        # demand scaling
        self.demand_scenario = demand_scenario

        # load data
        self.city = 'SiouxFalls'
        self.demand_df = pd.read_csv("Locations/" + self.city + "/od.csv")

        # poisson arrival rate
        self.demand_df['lambda'] = self.demand_df['volume'] / (24*60*60) * delta_t
        if self.demand_scenario == 'low':
            self.demand_df['lambda'] = 0.5 * self.demand_df['lambda']
        if self.demand_scenario == 'high':
            self.demand_df['lambda'] = 1.5 * self.demand_df['lambda']

        # track total cars that have been created
        self.cars_generated = 0
        self.dp_cars_generated = 0

        # TODO: check if needed for final sims
        np.random.seed(1729)

    def new_demand(self):
        #  compute the demand for new OD traffic
        demand = np.random.poisson(self.demand_df['lambda'])
        return demand

    def new_cars(self, start_time=None, network=None, new_traffic=None):

        if type(network) == Network:
            is_dp = False
        else:
            is_dp = True

        if new_traffic is None:
            new_traffic = np.random.poisson(self.demand_df['lambda'])  # number of new cars

        new_traffic_df = self.demand_df[new_traffic > 0]  # identifying appropriate OD pairs

        new_cars = []  # create new car list

        # create new cars for each of these OD pairs
        for index in range(new_traffic_df.shape[0]):

            # introducing multiple cars within the same OD pair
            # TODO: Can potentially platoon these cars into one attribute
            for _ in range(new_traffic[index]):

                origin = int(new_traffic_df.iloc[index]['origin'])
                destination = int(new_traffic_df.iloc[index]['destination'])

                car = Car(car_id=self.dp_cars_generated if is_dp else self.cars_generated,
                          origin=origin,
                          destination=destination,
                          edge_path=network.shortest_path(origin, destination),
                          start_time=start_time,
                          estimated_trip_time=network.estimate_travel_time(origin, destination))

                if is_dp:
                    self.dp_cars_generated += 1
                else:
                    self.cars_generated += 1

                new_cars.append(car)

        return new_cars

    def poisson_parameters(self):
        return self.demand_df['lambda'].to_list()
