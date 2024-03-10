import pandas as pd
import pandas_ta as ta


def add_atr_strategy(df_in: pd.DataFrame, **params):
    df = df_in.copy()
    df["trade_opening_price"] = df["Open"]

    df["atr"] = df_in["stat_ATR_1d"]
    df["close_above_1_atr"] = df["Close"] + df["atr"]
    df["close_above_1_atr"] = df["close_above_1_atr"].shift()
    df["close_below_1_atr"] = df["Close"] - df["atr"]
    df["close_below_1_atr"] = df["close_below_1_atr"].shift()

    df["signal"] = 0
    long_mask = df["Close"] > df["close_above_1_atr"]
    short_mask = df["Close"] < df["close_below_1_atr"]

    df.loc[long_mask, "signal"] = 1
    df.loc[short_mask, "signal"] = -1

    df["signal"] = df["signal"].shift()

    return df
