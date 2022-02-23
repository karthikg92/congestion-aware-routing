from simulation import Simulation
import numpy as np

"""
Scenarios:
    Low demand
    Baseline demand <- currently using
    High demand 
    
    Low capacity
    Baseline capacity <- currently being used
    High capacity
            
"""

for demand in ['baseline']:
    for capacity in ['baseline']:
        print('----- %s demand and %s capacity simulation -----' % (demand, capacity))

        sim = Simulation(demand_scenario=demand, capacity_scenario=capacity, eps=0.01)
        sim.run()

        # some logging for debug purposes
        print('Average lambda: ', np.mean(sim.traffic_generator.poisson_parameters()))
        print('Average link utilization: ', np.mean(sim.network.edge_utilization))

        name = 'results/' + demand + '_demand_' + capacity + '_capacity'
        sim.save_summary_stats(fname=name)

"""
Vary epsilon and observe the privacy-accuracy tradeoff
"""

# for eps in [0.01, 0.25, 0.5]:
#     print('----- Experiments with eps = %f -----' % eps)
#

