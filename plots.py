import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

"""
Overview of the main results from the experiments:

Result # 1:
Justify the validity of our capacity regimes with realistic data.
Plot the CDF for the low, medium, and high capacity

Result # 2:
Adding privacy leads to minimal impact (across the three different capacity)
    - fractional increase in total travel time is small [can compute this number and just write it/ put in a table]
    - per-car increase (absolute numbers/ fractional increase) in travel time is small
    - Shortest paths do not change for most vehicles

    - Do this for the three capacity scenarios

Result # 3:
Higher the privacy requirement, higher the loss in performance
    - Vary epsilon, and plot the increase in total travel time for the three different capacity profiles

"""

data_path = 'results/'
plot_path = 'plots/'
"""
Result # 1: Capacities on most links are large enough to fall into our analysis regime
"""

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


def print_results(df):
    print('')
    print('Total travel time increase due to DP (sec):', df['dp_tt'].mean() - df['tt'].mean())
    print('Fractional increase in total travel time due to DP: ',
          (df['dp_tt'].mean() - df['tt'].mean()) / df['tt'].mean())

    print('Fraction of cars with no additional travel time: ',
          sum(df['dp_induced_excess_tt'] == 0) / df.shape[0])
    print('Fraction of cars with no change in route :',
          sum(df['path_similarity'] == 1) / df.shape[0])
    print('')
    return None


# print('------ Results for low user demand -------')
# df = pd.read_csv(data_path + 'low_demand_baseline_capacity.csv')
# print_results(df)

#
# plt.hist(df['dp_induced_excess_tt'], bins=100)
# plt.savefig(plot_path + 'excess_time_distribution_low.png')
# plt.close()


print('------ Results for baseline user demand -------')
df = pd.read_csv(data_path + 'baseline_demand_baseline_capacity.csv')
print_results(df)

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
