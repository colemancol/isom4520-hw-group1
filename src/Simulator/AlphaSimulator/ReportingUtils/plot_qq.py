import matplotlib.pyplot as plt
import numpy as np
import os
import statsmodels.api as sm
from sklearn.preprocessing import scale

def plot_qq(df_g, **params):
    enums = params['enums']
    # Standardize the logreturn with scalre() imported from sklearn.preprocessing
    data = scale (df_g['log_return'])
    # Create Q-Q plot with 45-degree line added to plot
    sm.qqplot(data, line = '45')
    plt.xlabel ("Theoretical Quantiles")
    plt.ylabel ("Sample Quantiles")
    plt.title ("Q-Q plot of the log return")
    plt.savefig(os.path.join(enums.STAT_FIGURES_DIR, "QQPlot.png"))
    plt.close()