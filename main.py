from simulation import Simulation

"""
Scenarios:
    Low demand
    Baseline demand <- currently using
    High demand 
    
    Low capacity
    Baseline capacity <- currently being used
    High capacity
            
"""

for demand in ['low', 'baseline', 'high']:
    for capacity in ['low', 'baseline', 'high']:

        print('----- %s demand and %s capacity simulation -----' % (demand, capacity))

        sim = Simulation(demand_scenario=demand, capacity_scenario=capacity)
        sim.run()
        name = 'results/' + demand + '_demand_' + capacity + '_capacity'
        sim.save_summary_stats(fname=name)

"""
Vary epsilon and observe the privacy-accuracy tradeoff
"""
# TODO
# for eps in [0.01, 0.25, 0.5]:
#     print('----- Experiments with eps = %f -----' % eps)
#

