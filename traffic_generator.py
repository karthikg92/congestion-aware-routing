import numpy as np
import pandas as pd
from car import Car
from network import Network


class TrafficGenerator:

    def __init__(self, delta_t=None):

        # time interval for computing poisson rate
        self.delta_t = delta_t

        # load data
        self.demand_df = pd.read_csv("Locations/SiouxFalls/od.csv")

        # poisson arrival rate
        self.demand_df['lambda'] = self.demand_df['volume'] / (24*60*60) * delta_t

        # track total cars that have been created
        self.cars_generated = 0

        # TODO: check if needed for final sims
        np.random.seed(1729)

    def new_demand(self):
        #  compute the demand for new OD traffic
        demand = np.random.poisson(self.demand_df['lambda'])
        return demand

    def new_cars(self, start_time=None, network=None, new_traffic=None):

        if new_traffic is None:
            new_traffic = np.random.poisson(self.demand_df['lambda'])  # number of new cars

        new_traffic_df = self.demand_df[new_traffic > 0]  # identifying appropriate OD pairs

        new_cars = []  # create new car list

        # create new cars for each of these OD pairs
        for index in range(new_traffic_df.shape[0]):

            # introducing multiple cars within the same OD pair
            for _ in range(new_traffic[index]):

                origin = int(new_traffic_df.iloc[index]['origin'])
                destination = int(new_traffic_df.iloc[index]['destination'])

                car = Car(car_id=self.cars_generated,
                          origin=origin,
                          destination=destination,
                          edge_path=network.shortest_path(origin, destination),
                          start_time=start_time,
                          estimated_trip_time=network.estimate_travel_time(origin, destination))

                self.cars_generated += 1

                new_cars.append(car)

        return new_cars
