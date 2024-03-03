import matplotlib.pyplot as plt
import numpy as np
import os

def plot_histogram(df_g, **params):
    enums = params['enums']

    mu = df_g['log_return'].mean() # mean of distribution
    sigma = df_g['log_return'].std() # standard deviation of distribution
    x = df_g['log_return'].values

    num_bins = 100

    n, bins, patches = plt.hist(x, num_bins,
    density = 1,
    color ='blue',
    alpha = 0.7)
    y = ((1 / (np.sqrt(2 * np.pi) * sigma)) * np.exp(-0.5 * (1 / sigma * (bins - mu))**2))

    plt.plot(bins, y, '--', color ='black')
    
    plt.xlabel('log returns')
    plt.ylabel('Frequency')
    plt.title('Histogram of the log return')
    plt.savefig(os.path.join(enums.STAT_FIGURES_DIR, "LogReturnHistogram.png"))
    plt.close()