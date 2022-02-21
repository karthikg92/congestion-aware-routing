"""
Class for each car

State of each car:
ID
Location
Shortest path

Methods:
Update location
Trip stats

Trip stats includes:
Total travel time
Travel time on each link
"""


class Car:

    def __init__(self,
                 car_id=None,
                 origin=None,
                 destination=None,
                 edge_path=None,
                 start_time=None,
                 estimated_trip_time=None):

        self.id = car_id
        self.origin = origin
        self.destination = destination
        self.path = edge_path
        self.current_edge = edge_path[0]
        self.current_edge_progress = 0  # 0 is start of an edge, 1 is completion of edge
        self.start_time = start_time
        self.finish_time = start_time
        self.estimated_trip_time = estimated_trip_time
        self.completed_trip = False

    def update_location(self, network=None, delta_t=None):
        # update edge progress
        distance_covered = delta_t * network.edge_speed(self.current_edge)
        fractional_distance_covered = distance_covered / network.edge_length(self.current_edge)
        self.current_edge_progress += fractional_distance_covered

        # Update status if edge is completely  traversed
        if self.current_edge_progress > 1:
            # reset edge progress
            self.current_edge_progress = 0

            # find next edge
            current_leg = self.path.index(self.current_edge)
            if current_leg < (len(self.path) - 1):
                # edges remaining in path
                self.current_edge = self.path[current_leg + 1]
            else:
                # this was the last edge
                self.completed_trip = True

        self.finish_time += 1
