import pandas as pd


def add_macd_strategy(df_in: pd.DataFrame, **params):
    df = df_in.copy()
    df["trade_opening_price"] = df["Open"]
    df["macd_histogram"] = df_in["stat_MACDh_12_26_9"]

    df["bullish_crossover"] = (
        df["macd_histogram"].rolling(2).apply(lambda x: x.iloc[0] < 0 and x.iloc[1] > 0)
    )
    df["bearish_crossover"] = (
        df["macd_histogram"].rolling(2).apply(lambda x: x.iloc[0] > 0 and x.iloc[1] < 0)
    )

    df["signal"] = 0
    long_mask = df["bullish_crossover"] == True
    short_mask = df["bearish_crossover"] == True

    df.loc[long_mask, "signal"] = 1
    df.loc[short_mask, "signal"] = -1

    df["signal"] = df["signal"].shift()

    return df
