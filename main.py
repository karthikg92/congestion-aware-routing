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

import os
try:
    os.remove('plots/utilization_log.csv')
except:
    pass

"""
Experiment 1

Compare DP network with non-noisy version
Fixed demand and capacity
"""

for demand in ['baseline']:

    for capacity in ['baseline']:

        ####################################################
        #  Main Experiment
        ####################################################

        print('\n')
        print('----- %s demand and %s capacity simulation -----' % (demand, capacity))

        # Path for results
        name = 'results/' + demand + '_demand_' + capacity + '_capacity'

        sim = Simulation(demand_scenario=demand, capacity_scenario=capacity, eps=0.01, fname=name)  # Initialize
        sim.run()  # Run simulation
        sim.save_summary_stats()  # Save results

        # some logging for debug purposes
        # print('Average lambda: ', np.mean(sim.traffic_generator.poisson_parameters()))
        # print('Total lambda: ', np.sum(sim.traffic_generator.poisson_parameters()))
        # print('Average link utilization: ', np.mean(sim.network.edge_utilization))
        # print('Average utilization = ', np.mean(sim.network.hacky_tracker))


"""
Experiment 2

Vary epsilon and observe the privacy-accuracy tradeoff
"""

# for eps in [0.01, 0.25, 0.5]:
#     print('----- Experiments with eps = %f -----' % eps)
#

