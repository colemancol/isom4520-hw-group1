import os
import statsmodels.api as sm
import numpy as np
import pandas_ta as ta 

def add_ema_strategy(df_in, **params):
    df = df_in.copy()
    slippage_rate = params['slippage_rate']

    df['ema'] = ta.ema(df['Close'], length=12)
    #df['ema'] = df['ema'].shift()  Shift one period back to avoid using future data

    df ['trade_opening_price'] = df['Open']

    df['signal'] = 0
    long_mask = df['Close'] > df['ema']
    short_mask = df['Close'] < df['ema']

    df.loc[long_mask, 'signal'] = 1
    df.loc[short_mask, 'signal'] = -1

    df['signal'] = df['signal'].shift(1)

    return df