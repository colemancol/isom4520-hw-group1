import os
import pandas as pd
import statsmodels.api as sm


def compare(**params):
    base_dir = os.path.join("reports", params["market"])
    strategies_to_compare = params["strategy_names_to_compare"]
    df_strategy_roi = pd.DataFrame(columns=strategies_to_compare)
    for strategy in strategies_to_compare:
        strategy_executed_trades_path = os.path.join(
            base_dir, strategy, "ExecutedTrades.csv"
        )
        print(f"Reading {strategy} strategy at: {strategy_executed_trades_path}")
        try:
            df = pd.read_csv(
                strategy_executed_trades_path,
                index_col=0,
                usecols=["symbol", "closing_time", "invested_budget", "gain"],
            )
        except FileNotFoundError as e:
            print(
                f"File not found: {strategy_executed_trades_path}. Please run simulation for strategy:{strategy} first"
            )
            continue

        df["closing_time"] = pd.to_datetime(df["closing_time"], utc=True)

        # since timing of trades in each strategy is different, group them by month of closing time first
        df = df.groupby(pd.Grouper(key="closing_time", freq="M")).sum()
        df["monthly_roi"] = (
            df["gain"] / df["invested_budget"]
        )  # calculate monthly roi, note gain can be negative (i.e including loss)
        df_strategy_roi[strategy] = df["monthly_roi"]

    # find correlation between monthly roi of the strategies
    correlation_matrix = df_strategy_roi.corr()
    print("----- Correlation Matrix ----")
    print(correlation_matrix)
    metrics = ["annual(%)", "sharpe_ratio"]
