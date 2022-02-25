from simulation import Simulation
import numpy as np
import os
import shutil

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
for eps in [0.01, 0.1, 0.25, 0.5]:

    # eliminate previous results
    folder = 'results/eps' + str(eps)
    try:
        shutil.rmtree(folder)
    except:
        pass

    # create a new folder
    os.mkdir(folder)

    print('-------------------------------------')
    print('------------Epsilon %.2f ------------' % eps)
    print('-------------------------------------')

    for demand in ['baseline', 'low', 'high']:

        ####################################################
        #  Main Experiment
        ####################################################

        print('\n')
        print('----- %s demand simulation -----' % demand)

        # Path for results
        name = folder + '/' + demand + '_demand'

        sim = Simulation(demand_scenario=demand, eps=eps, fname=name)  # Initialize
        sim.run()  # Run simulation
        sim.save_summary_stats()  # Save results



"""
Experiment 2

Vary epsilon and observe the privacy-accuracy tradeoff
"""

# for eps in [0.01, 0.25, 0.5]:
#     print('----- Experiments with eps = %f -----' % eps)
#

