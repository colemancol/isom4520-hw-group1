import pandas as pd
import numpy as np

from ._add_arima_forecasting import _add_arima_forecasting
from ._add_garch_forecasting import _add_garch_forecasting


def add_statistical_measures(
    df: pd.DataFrame, macro_and_other_data=None, interval=None, **params
):
    """
    ## GUIDE: Step 3

    Add statistical measures to the data
    This function adds statistical measures to the data.
    Don't forget to shift the data before using it if you are using
    the high, low, or close prices and assume that the trade is opened at open.

    IMPORTANT NOTE: Add "stat_" prefix to the new columns that you add to the data.
    This is important because we use this prefix to get the statistical measures
    from the data in the simulator, signal generator, alpha strategiy, and research.

    Args:
        df: pd.DataFrame
            The data

        macro_and_other_data: dict

            It consists of information provided from the AllStockPrices class.
            It contains the dataframes of the other stocks, the market index.
            It is usually passed for the daily data, so that we can use the daily data of the other indices

        interval: str
            The interval of the data

    Returns:
        df: pd.DataFrame
    """
    # This flag will be used to check if we need to save the data to cache
    is_updated = False
    suffix = "" if interval is None else f"_{interval}"
    initial_length_of_columns = len(df.columns)

    for t in [22]:
        if f"stat_Vola({t}){suffix}" not in df:
            df[f"stat_Vola({t}){suffix}"] = df["Close"].shift().pct_change().rolling(
                window=t
            ).std() * (252**0.5)

    if macro_and_other_data is not None:
        # For adding the data related to the macro and market index

        for k, data in macro_and_other_data.items():
            if k in ["data", "symbol", "cache_dir"]:
                continue

            if f"stat_{k}_change(t_1)_ratio{suffix}" not in df:
                df[f"stat_{k}_change(t_1)_ratio{suffix}"] = (
                    data["Close"].pct_change().shift()
                )

    col = "stat_50d_std_over_50_sma"  # has to start with stat
    if col not in df:
        df[col] = (
            df["Close"].rolling(window=50).std() / df["Close"].rolling(window=50).mean()
        )

    ## TODO: ASSIGNMENT #2: Add Beta and IV here
    col = "stat_Beta"
    if col not in df:
        market_return = df["stat_market_index_change(t_1)_ratio_1d"].rolling(window = 22)
        stock_return = df["Close"].shift(1).pct_change().rolling(window = 22)
        var_market = market_return.var()
        covariance = market_return.cov(stock_return)
        beta = covariance / var_market
        df[col] = beta

    col = "stat_iv"
    if col not in df:
        market_return = df["stat_market_index_change(t_1)_ratio_1d"].rolling(window = 22)
        stock_return = df["Close"].shift(1).pct_change().rolling(window = 22)
        beta = df["stat_Beta"]
        non_systematic_risk = (
            stock_return.var() - beta**2 * market_return.var()
        )  # Overall risk = systematic risk + non-systematic risk (in terms of variance, assuming no correlation between SR & NSR)
        iv = non_systematic_risk**0.5
        df[col] = iv

    if len(df) == 0:
        return df.copy(), False

    df = _add_arima_forecasting(df, interval, **params)
    df = _add_garch_forecasting(df, interval, **params)

    """
    PerformanceWarning: DataFrame is highly fragmented. 
    This is usually the result of calling `frame.insert` many times,
    which has poor performance.  Consider joining all columns at once using
    pd.concat(axis=1) instead. To get a de-fragmented frame,
    use `newframe = frame.copy()`
    """

    new_df_columns = list(df.columns)

    # Check if the any new columns are added
    if len(new_df_columns) > initial_length_of_columns:
        is_updated = True

    return df.copy(), is_updated
