from simulation import Simulation
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
Experiment objective:

Compare DP network with non-noisy version for
- varying privacy requirements (epsilon value)
- varying traffic demand (three demand scenarios)
"""

for eps in [0.01, 0.1, 0.25, 0.5]:

    # plan to overwrite any saved results
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

