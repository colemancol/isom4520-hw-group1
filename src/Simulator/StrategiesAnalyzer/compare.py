import os
import pandas as pd
import statsmodels.api as sm


def compare(**params):
    base_dir = os.path.join("reports", params["market"])

    # for finding correlation
    strategies_to_compare = params["strategy_names_to_compare"]
    df_strategy_roi = pd.DataFrame(columns=strategies_to_compare)

    # for finding best weights
    metrics = ["annual(%)", "annual_volatility", "sharpe_ratio"]
    metrics_data = list[dict]()
    for strategy in strategies_to_compare:
        strategy_executed_trades_path = os.path.join(
            base_dir, strategy, "ExecutedTrades.csv"
        )
        strategy_summary_path = os.path.join(
            base_dir, strategy, f"Summary_{strategy}.csv"
        )
        print(f"Reading {strategy} strategy at: {strategy_executed_trades_path}")

        df_corr = None
        try:
            df_corr = pd.read_csv(
                strategy_executed_trades_path,
                index_col=0,
                usecols=["symbol", "closing_time", "invested_budget", "gain"],
            )
            df_strategy_summary = pd.read_csv(strategy_summary_path, index_col=0).iloc[
                0
            ]
            print(df_strategy_summary)
            metrics_data.append(
                {
                    "strategy": strategy,
                    "annual_return": df_strategy_summary["annual(%)"],
                    "annual_volatility": df_strategy_summary["annual_volatility"],
                    "sharpe_ratio": df_strategy_summary["sharpe_ratio"],
                }
            )
        except FileNotFoundError as e:
            print(
                f"File not found: {strategy_executed_trades_path}. Please run simulation for strategy:{strategy} first"
            )
            continue

        df_corr["closing_time"] = pd.to_datetime(df_corr["closing_time"], utc=True)

        # since timing of trades in each strategy is different, group them by month of closing time first
        df_corr = df_corr.groupby(pd.Grouper(key="closing_time", freq="M")).sum()
        df_corr["monthly_roi"] = (
            df_corr["gain"] / df_corr["invested_budget"]
        )  # calculate monthly roi, note gain can be negative (i.e including loss)
        df_strategy_roi[strategy] = df_corr["monthly_roi"]

    # find correlation between monthly roi of the strategies
    correlation_matrix = df_strategy_roi.corr()
    print("----- Correlation Matrix ----")
    print(correlation_matrix)
    print("----------")

    # find best weights to maximize sharpe ratio
    df_metrics = pd.DataFrame.from_dict(metrics_data)  # type: ignore
    df_metrics.set_index("strategy", inplace=True)
    print(df_metrics)
