from arch import arch_model
from ._find_goodness_of_fit import find_goodness_of_fit
import matplotlib.pyplot as plt
import os

def _add_garch_forecasting(df, interval, **params):
    """
    Add GARCH forecasting results to the dataframe.
    """

    ##TODO: ASSIGNMENT #4 - Add GARCH forecasting here

    sholud_add_garch = params['should_add_garch']

    if not sholud_add_garch:
        return df

    df = df.copy()
    
    ## TODO: Add GARCH forecasting
    window = 22

    df['daily_return'] = df['Close'].pct_change() * 100
    df['r_star'] = (df['daily_return'] - df['daily_return'].rolling(window=window).mean()) ** 2

    tmp_holder = [None for _ in range(window)]

    for i in range(window, len(df)):
        tmp = df['daily_return'].iloc[i-window:i].dropna()
        model = arch_model(tmp, vol='Garch', p=1, q=1, rescale=False)
        model_fit = model.fit(disp='off')

        # Print the conditional volatility
        vol_forecast = model_fit.forecast(horizon=1)
        tmp_holder.append(vol_forecast.variance.values[-1][0])

    df['garch_vol_t_hat'] = tmp_holder

    # Dropna
    df = df.fillna(0)

    # Find the goodness of fit for all and print as a table
    corr, mse, mape = find_goodness_of_fit(df['garch_vol_t_hat'], df['r_star'])
    print(f"{corr=:.5f}, {mse=:.5f}, {mape=:.5f}")

    print (f"{params['symbol']} - Based on GARCH")
    print(df)

    # Plot the goodness of fit for AAPL using scatter plot
    plt.scatter(df['r_star'], df['garch_vol_t_hat'])
    plt.xlabel('Volatility')
    plt.ylabel('Volatility_hat')
    plt.title('GARCH Volatility')
    
    GARCH_FIGURE_FOLDER = os.path.join(params["enums"].STAT_FIGURES_DIR, "garch")
    if not os.path.exists(GARCH_FIGURE_FOLDER):
        os.makedirs(GARCH_FIGURE_FOLDER)
    plt.savefig(os.path.join(GARCH_FIGURE_FOLDER, f"GarchVolatility_{params['symbol']}.png"))
    plt.show()
    return df