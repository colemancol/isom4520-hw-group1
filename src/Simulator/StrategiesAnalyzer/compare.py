import os
import pandas as pd
import statsmodels.api as sm
import numpy as np

from .utils import calculate_portoflio_returns, calculate_portoflio_volatility
from ._optimize_weightings import optimize_weightings


def compare(**params):
    base_dir = os.path.join("reports", params["market"])

    # for finding correlation
    strategies_to_compare = params["strategy_names_to_compare"]
    if len(strategies_to_compare) > 2:
        raise NotImplementedError("Currently only supports comparing 2 strategies")
    df_strategy_portfolio_value = pd.DataFrame(columns=strategies_to_compare)

    # for finding best weights
    metrics_data = list[dict]()
    for strategy in strategies_to_compare:
        strategy_daily_budget_path = os.path.join(
            base_dir, strategy, "DailyBudget.csv"  # "ExecutedTrades.csv"
        )
        strategy_summary_path = os.path.join(
            base_dir, strategy, f"Summary_{strategy}.csv"
        )
        print(f"Reading {strategy} strategy at: {strategy_daily_budget_path}")

        try:
            df_corr = pd.read_csv(
                strategy_daily_budget_path,
                usecols=["Date", "PortfolioValue"],
            )
            df_strategy_portfolio_value[strategy] = df_corr["PortfolioValue"]
            df_strategy_summary = pd.read_csv(strategy_summary_path, index_col=0).iloc[
                0
            ]
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
                f"File not found: {strategy_daily_budget_path}. Please run simulation for strategy:{strategy} first"
            )
            continue

        # """ Monthly ROI approach """
        # # since timing of trades in each strategy is different, group them by month of closing time first
        # df_corr["closing_time"] = pd.to_datetime(df_corr["closing_time"], utc=True)
        # df_corr = df_corr.groupby(pd.Grouper(key="closing_time", freq="M")).sum()
        # df_corr["monthly_roi"] = (
        #     df_corr["gain"] / df_corr["invested_budget"]
        # )  # calculate monthly roi, note gain can be negative (i.e including loss)
        # df_strategy_roi[strategy] = df_corr["monthly_roi"]

    # find correlation between monthly roi of the strategies
    correlation_matrix = df_strategy_portfolio_value.corr()
    print("\n----- Correlation Matrix ----")
    print(correlation_matrix)
    print("----------", end="\n\n")

    # find best weights to maximize sharpe ratio
    df_metrics = pd.DataFrame.from_dict(metrics_data)  # type: ignore
    df_metrics.set_index("strategy", inplace=True)
    returns = np.array(df_metrics["annual_return"], dtype=np.float32) / 100
    volatilities = np.array(df_metrics["annual_volatility"], dtype=np.float32)
    print(f"Returns: {returns}")
    print(f"Volatilities: {volatilities}")

    # initialize equal weights
    weights = np.ones(len(strategies_to_compare)) / len(strategies_to_compare)

    print("\n===== Before optimising weights (equal weights) =====")
    portfolio_return = calculate_portoflio_returns(returns, weights)
    portfolio_volatility = calculate_portoflio_volatility(
        volatilities, weights, correlation_matrix
    )
    print(f"\u27a4 Portfolio return: {portfolio_return}")
    print(f"\u27a4 Portfolio volatility: {portfolio_volatility}")
    print(f"\u27a4 Sharpe ratio: {portfolio_return / portfolio_volatility}")
    print("==========")
    print()
    print("===== After optimising weights =====")
    best_sharpe, best_weights = optimize_weightings(
        returns, volatilities, correlation_matrix
    )
    best_portfolio_return = calculate_portoflio_returns(returns, best_weights)
    best_portfolio_volatility = calculate_portoflio_volatility(
        volatilities, best_weights, correlation_matrix
    )
    print(f"\u27a4 Best weights: {best_weights}")
    print(f"\u27a4 Portfolio return: {best_portfolio_return}")
    print(f"\u27a4 Portfolio volatility: {best_portfolio_volatility}")
    print(f"\u27a4 Sharpe ratio: {best_sharpe}")
    print("==========")
