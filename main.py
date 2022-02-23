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

        print('----- %s demand and %s capacity simulation -----' %(demand, capacity))

        sim = Simulation(demand_scenario=demand, capacity_scenario=capacity)
        sim.run()
        name = 'results/' + demand + '_demand_' + capacity + '_capacity'
        sim.save_summary_stats(fname=name)
#
# print('----- Baseline simulation -----')
#
# sim = Simulation()
# sim.run()
# sim.save_summary_stats(fname='results/baseline')
#
# print('----- Low demand and high capacity simulation -----')
#
# sim = Simulation(demand_scenario='low', capacity_scenario='high')
# sim.run()
# sim.save_summary_stats(fname='results/low_demand_high_capacity')
#
# print('----- Low demand and low capacity simulation -----')
#
# sim = Simulation(demand_scenario='low', capacity_scenario='low')
# sim.run()
# sim.save_summary_stats(fname='results/low_demand_low_capacity')
#
# print('----- High demand and low capacity simulation -----')
#
# sim = Simulation(demand_scenario='high', capacity_scenario='low')
# sim.run()
# sim.save_summary_stats(fname='results/high_demand_low_capacity')
#
# print('----- High demand and high capacity simulation -----')
#
# sim = Simulation(demand_scenario='high', capacity_scenario='high')
# sim.run()
# sim.save_summary_stats(fname='results/high_demand_high_capacity')
