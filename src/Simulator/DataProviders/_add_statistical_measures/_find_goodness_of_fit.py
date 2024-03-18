import pandas as pd
import numpy as np

def find_goodness_of_fit(series1, series2):
    # Concat the series and drop nan
    df = pd.concat([series1, series2], axis=1)
    df = df.dropna()

    series1 = df.iloc[:, 0]
    series2 = df.iloc[:, 1]

    corr = np.corrcoef(series1, series2)[0, 1]
    mse = np.mean((series1 - series2) ** 2)
    mape = np.mean(np.abs((series1 - series2) / series1))

    return corr, mse, mape