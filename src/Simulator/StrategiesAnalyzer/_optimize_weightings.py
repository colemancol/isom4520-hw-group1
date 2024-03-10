import numpy as np
import numpy.typing as npt
import pandas as pd

from .utils import calculate_portoflio_returns, calculate_portoflio_volatility


def optimize_weightings(
    returns: npt.NDArray[np.float32],
    volatilities: npt.NDArray[np.float32],
    correlation_matrix: pd.DataFrame,
) -> tuple[float, tuple[float, float]]:
    sharpe_holder = list[float]()
    return_holder = list[float]()
    x = [i / 100 for i in range(100)]
    for i in x:
        weights = np.array([i, 1 - i])

        portfolio_return = calculate_portoflio_returns(returns, weights)
        portfolio_volatility = calculate_portoflio_volatility(
            volatilities, weights, correlation_matrix
        )
        portfolio_sharpe = portfolio_return / portfolio_volatility

        sharpe_holder.append(portfolio_sharpe)
        return_holder.append(portfolio_return)
    best_sharpe = max(sharpe_holder)
    best_weights = (x[np.argmax(sharpe_holder)], 1 - x[np.argmax(sharpe_holder)])
    return best_sharpe, best_weights
