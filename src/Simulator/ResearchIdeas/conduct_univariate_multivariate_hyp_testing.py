import os
import numpy as np
import pandas as pd
import pprint

import statsmodels.api as sm
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report
from sklearn.model_selection import train_test_split
from joblib import dump

from config import LONG, SHORT

from .reseach_utils import clean_nans
from .reseach_utils import convert_categorical_to_binary

import logging

logger = logging.getLogger("research_logger")

P_VALUE_THRESHOLD = 0.1
TEST_SIZE = 0.4


def conduct_univariate_multivariate_hyp_testing(df, **params):
    """
    ## GUIDE: Step 12

    This is an example of how we can use the univariate
    Hypothesis testing to improve a strategy.
    But the below code is written in the class and can be
    significantly better. This is just a starting point for students.

    Args:
        df: pd.DataFrame
            The dataframe of the potential trades

    Returns:
        None
    """

    # Split into train and test
    df_train, df_test = train_test_split(df, test_size=TEST_SIZE, random_state=42)

    # separate df into long and short trades
    short_trades = df_train[df_train["trade_direction"] == SHORT]
    long_trades = df_train[df_train["trade_direction"] == LONG]

    # Univariate Hypothesis Testing on the long ones
    long_holder = {}
    for col in long_trades.columns:

        if not col.startswith("stat_"):
            continue

        df_tmp = long_trades[[col, "PnL_ratio"]].copy()
        df_tmp.dropna(inplace=True, axis=0)

        X = df_tmp[col]
        Y = df_tmp["PnL_ratio"]
        X = sm.add_constant(X)

        model = sm.OLS(Y, X).fit()
        p_value = model.pvalues[col]
        long_holder[col] = p_value

    print("Long Trades")
    pprint.pprint(long_holder)

    # Univariate Hypothesis Testing on the short ones
    short_holder = {}
    for col in short_trades.columns:

        if not col.startswith("stat_"):
            continue

        df_tmp = short_trades[[col, "PnL_ratio"]].copy()
        df_tmp.dropna(inplace=True, axis=0)

        X = df_tmp[col]
        Y = df_tmp["PnL_ratio"]
        X = sm.add_constant(X)

        model = sm.OLS(Y, X).fit()
        p_value = model.pvalues[col]
        short_holder[col] = p_value

    print("Short Trades")
    pprint.pprint(short_holder)

    # conduct multivariate hypothesis testing on significant stat measures from univariate hypothesis testing
    # find signicant stat measures first (top 5 smallest p-value since all p-values are > 0.05)
    long_stats = sorted(long_holder, key=lambda x: long_holder.get(x, 1))[:5]
    short_stats = sorted(short_holder, key=lambda x: short_holder.get(x, 1))[:5]

    # multivariate hypothesis testing: long trades
    print(
        f"Multivariate Hypothesis Testing: Long Trades\n\u27a4 Variables used: {long_stats}"
    )
    long_trades_multi_ht = long_trades[[*long_stats, "PnL_ratio"]].dropna(axis=0)
    X = long_trades_multi_ht[long_stats]
    Y = long_trades_multi_ht["PnL_ratio"]
    X = sm.add_constant(X)

    model = sm.OLS(Y, X).fit()
    print(model.summary())

    print("\n-----\n")

    # multivariate hypothesis testing: short trades
    print(
        f"Multivariate Hypothesis Testing: Short Trades\n\t\u27a4 Variables used: {short_stats}"
    )
    short_trades_multi_ht = short_trades[[*short_stats, "PnL_ratio"]].dropna(axis=0)
    X = short_trades_multi_ht[short_stats]
    Y = short_trades_multi_ht["PnL_ratio"]
    X = sm.add_constant(X)

    model = sm.OLS(Y, X).fit()
    print(model.summary())

    return
