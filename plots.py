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

"""

data_path = 'results/eps0.1/'

"""
Result # 1: Capacities on most links are large enough to fall into our analysis regime
"""
plt.rcParams.update({'font.size': 10})

df_counts = pd.read_csv(data_path + 'baseline_demand_critical_counts.csv')
c = (df_counts['counts']).to_list()
count, bins_count = np.histogram(c, bins=500)

plt.hist(c, bins=50, color='tab:grey')
# pdf = count / sum(count)
# cdf = np.cumsum(pdf)
# plt.plot(bins_count[1:], cdf, color="black")

# reference lines
plt.axvline(x=127, ymin=0.00, ymax=1.00, ls='--', color='tab:red', label='Counts = 127', linewidth=2)

plt.text(170, 12, 'threshold = 127', color='tab:red')
# plt.legend()
plt.xlabel('$\delta$-critical counts')
# plt.ylabel('Cumulative mass function')
plt.ylabel('Number of roads')

fig = plt.gcf()
fig.set_size_inches(3.54, 2.5)

plt.tight_layout()

plt.savefig('results/critical_counts.png', dpi=250)
plt.close()


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

        f.write('Average travel time without privacy (sec), %.4f \n'
                % (df_results['tt'].mean())
                )

        f.write('Average travel time with DP (sec), %.4f \n'
                % (df_results['dp_tt'].mean())
                )

        f.write('Travel time increase due to DP (sec), %.4f \n'
                % (df_results['dp_tt'].mean() - df_results['tt'].mean())
                )

        f.write('Percentage increase in travel time due to DP (percent), %.4f \n'
                % (100 * (df_results['dp_tt'].mean() - df_results['tt'].mean()) / df_results['tt'].mean())
                )

        f.write('Percentage cars with no additional travel time due to DP (percent), %.4f \n'
                % (100 * sum(df_results['dp_induced_excess_tt'] == 0) / df_results.shape[0])
                )

        f.write('Percentage cars with no change in route due to DP (percent), %.4f \n'
                % (100 * sum(df_results['path_similarity'] == 1) / df_results.shape[0])
                )

        f.write('Average number of vehicles joining the network every time step, %.4f \n'
                % (df_lambda['lambda'].sum())
                )

        f.write('Min link utilization, %.4f \n'
                % (min(utilization))
                )

        f.write('Max link utilization, %.4f \n'
                % (max(utilization))
                )

        f.write('Average link utilization, %.4f \n'
                % (np.mean(utilization))
                )

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

