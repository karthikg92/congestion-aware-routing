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


print('----- Baseline simulation -----')

sim = Simulation()
sim.run()
sim.save_summary_stats(fname='results/baseline')

print('----- Low demand and high capacity simulation -----')

sim = Simulation(demand_scenario='low', capacity_scenario='high')
sim.run()
sim.save_summary_stats(fname='results/low_demand_high_capacity')

print('----- Low demand and low capacity simulation -----')

sim = Simulation(demand_scenario='low', capacity_scenario='low')
sim.run()
sim.save_summary_stats(fname='results/low_demand_low_capacity')

print('----- High demand and low capacity simulation -----')

sim = Simulation(demand_scenario='high', capacity_scenario='low')
sim.run()
sim.save_summary_stats(fname='results/high_demand_low_capacity')

print('----- High demand and high capacity simulation -----')

sim = Simulation(demand_scenario='high', capacity_scenario='high')
sim.run()
sim.save_summary_stats(fname='results/high_demand_high_capacity')
