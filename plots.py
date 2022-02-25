import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import os

"""
Overview of the main results from the experiments:

Result # 1:
Justify the validity of our capacity regimes with realistic data.
Plot the CDF of the flow capacity profile

Result # 2:
Adding privacy leads to minimal impact (across the three different demand profiles)
    - fractional increase in total travel time is small [can compute this number and just write it/ put in a table]
    - per-car increase (absolute numbers/ fractional increase) in travel time is small
    - Shortest paths do not change for most vehicles

Result # 3:
Higher the privacy requirement, higher the loss in performance
    - Vary epsilon, and plot the increase in total travel time for the three different capacity profiles

"""

data_path = 'results/eps0.1/'

"""
Result # 1: Capacities on most links are large enough to fall into our analysis regime
"""

df_counts = pd.read_csv(data_path + 'baseline_demand_critical_counts.csv')
c = df_counts['counts'].to_list()
count, bins_count = np.histogram(c, bins=500)
pdf = count / sum(count)
cdf = np.cumsum(pdf)
plt.plot(bins_count[1:], cdf, color="black")

# reference lines
plt.axvline(x=127, ymin=0.05, ymax=0.95, ls='--', color='tab:blue', label='Counts = 127')

plt.legend()
plt.xlabel('Critical traffic counts')
plt.ylabel('Cumulative mass function')

plt.savefig('results/critical_counts.png', dpi=250)
plt.close()



# n_bins = 500
#
# df_low_capacity = pd.read_csv(data_path + 'capacity_low.csv')
# c = df_low_capacity['capacity'].to_list()
# count, bins_count = np.histogram(c, bins=n_bins)
# pdf = count / sum(count)
# cdf = np.cumsum(pdf)
# plt.plot(bins_count[1:], cdf, color="red", label="low capacity")
#
# df_baseline_capacity = pd.read_csv(data_path + 'capacity_baseline.csv')
# c = df_baseline_capacity['capacity'].to_list()
# count, bins_count = np.histogram(c, bins=n_bins)
# pdf = count / sum(count)
# cdf = np.cumsum(pdf)
# plt.plot(bins_count[1:], cdf, color="blue", label="baseline capacity")
#
# df_high_capacity = pd.read_csv(data_path + 'capacity_high.csv')
# c = df_high_capacity['capacity'].to_list()
# count, bins_count = np.histogram(c, bins=n_bins)
# pdf = count / sum(count)
# cdf = np.cumsum(pdf)
# plt.plot(bins_count[1:], cdf, color="black", label="high capacity")
#
# plt.legend()
# plt.xlabel('Edge capacity')
# plt.ylabel('Cumulative density function')
# plt.savefig(plot_path + 'capacity.png')
# plt.close()

"""
Result # 2:

Adding privacy leads to minimal impact (across the three different capacity)
    - fractional increase in total travel time is small [can compute this number and just write it/ put in a table]
    - spread in per-car travel-time increase 
    - Shortest paths do not change for most vehicles

    - Do this for the three user demand scenarios
    
"""


def summarize_results(path=None, df_results=None, df_lambda=None, utilization_array=None):

    try:
        os.remove(path)
    except:
        pass

    utilization = np.mean(utilization_array, axis=0)

    with open(path, 'a') as f:

        f.write('Average travel time without privacy (sec), %.2f \n'
                % (df_results['tt'].mean())
                )

        f.write('Average travel time with DP (sec), %.2f \n'
                % (df_results['dp_tt'].mean())
                )

        f.write('Travel time increase due to DP (sec), %.2f \n'
                % (df_results['dp_tt'].mean() - df_results['tt'].mean())
                )

        f.write('Percentage increase in travel time due to DP (percent), %.2f \n'
                % (100 * (df_results['dp_tt'].mean() - df_results['tt'].mean()) / df_results['tt'].mean())
                )

        f.write('Percentage cars with no additional travel time due to DP (percent), %.2f \n'
                % (100 * sum(df_results['dp_induced_excess_tt'] == 0) / df_results.shape[0])
                )

        f.write('Percentage cars with no change in route due to DP (percent), %.2f \n'
                % (100 * sum(df_results['path_similarity'] == 1) / df_results.shape[0])
                )

        f.write('Percentage cars with no change in route due to DP (percent), %.2f \n'
                % (100 * sum(df_results['path_similarity'] == 1) / df_results.shape[0])
                )

        f.write('Average number of vehicles joining the network every time step, %.2f \n'
                % (df_lambda['lambda'].sum())
                )

        f.write('Min link utilization, %.2f \n'
                % (min(utilization))
                )

        f.write('Max link utilization, %.2f \n'
                % (max(utilization))
                )

        f.write('Average link utilization, %.2f \n'
                % (np.mean(utilization))
                )
    #
    # print('Fraction of cars with no additional travel time: ',
    #       sum(df['dp_induced_excess_tt'] == 0) / df.shape[0])
    # print('Fraction of cars with no change in route :',
    #       sum(df['path_similarity'] == 1) / df.shape[0])
    # print('')

    # some logging for debug purposes
    # print('Average lambda: ', np.mean(sim.traffic_generator.poisson_parameters()))
    # print('Total lambda: ', np.sum(sim.traffic_generator.poisson_parameters()))
    # print('Average link utilization: ', np.mean(sim.network.edge_utilization))
    # print('Average utilization = ', np.mean(sim.network.hacky_tracker))

    return None


for eps in [0.01, 0.1, 0.25, 0.5]:

    folder = 'results/eps' + str(eps)

    for demand in ['baseline', 'low', 'high']:

        path = folder + '/' + demand + '_demand.csv'
        df_results = pd.read_csv(path)

        path = folder + '/' + demand + '_demand_array_utilization.csv'
        utilization_array = np.loadtxt(path, delimiter=',')

        path = folder + '/' + demand + '_demand_lambda.csv'
        df_lambda = pd.read_csv(path)

        path = folder + '/' + demand + '_demand_summary.csv'
        summarize_results(path, df_results=df_results, utilization_array=utilization_array, df_lambda=df_lambda)





# print('------ Results for low user demand -------')
# df = pd.read_csv(data_path + 'low_demand_baseline_capacity.csv')
# print_results(df)

#
# plt.hist(df['dp_induced_excess_tt'], bins=100)
# plt.savefig(plot_path + 'excess_time_distribution_low.png')
# plt.close()


# print('------ Results for baseline user demand -------')
# df = pd.read_csv(data_path + 'baseline_demand_baseline_capacity.csv')
# print_results(df)

# print('Total travel time increase due to DP (sec):', df['dp_tt'].mean() - df['tt'].mean())
# print('Fractional increase in total travel time due to DP: ', (df['dp_tt'].mean() - df['tt'].mean()) / df['tt'].mean())
# plt.hist(df['dp_induced_excess_tt'], bins=100)
# plt.savefig(plot_path + 'excess_time_distribution_baseline.png')
# plt.close()
# print('Fraction of cars with no additional travel time: ',
#       sum(df['dp_induced_excess_tt'] == 0) / df.shape[0])
# print('Fraction of cars with no change in route :',
#       sum(df['path_similarity'] == 1) / df.shape[0])

# print('------ Results for high user demand -------')
# df = pd.read_csv(data_path + 'high_demand_baseline_capacity.csv')
# print_results(df)

# print('Total travel time increase due to DP (sec):', df['dp_tt'].mean() - df['tt'].mean())
# print('Fractional increase in total travel time due to DP: ', (df['dp_tt'].mean() - df['tt'].mean()) / df['tt'].mean())
# plt.hist(df['dp_induced_excess_tt'], bins=100)
# plt.savefig(plot_path + 'excess_time_distribution_high.png')
# plt.close()
# print('Fraction of cars with no additional travel time: ',
#       sum(df['dp_induced_excess_tt'] == 0) / df.shape[0])
# print('Fraction of cars with no change in route :',
#       sum(df['path_similarity'] == 1) / df.shape[0])

"""
Result # 3:
Higher the privacy requirement, higher the loss in performance
    - Vary epsilon, and plot the increase in total travel time for the three different capacity profiles
"""

