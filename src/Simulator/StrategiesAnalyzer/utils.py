import numpy as np


def calculate_portoflio_returns(returns, weights):
    """
    Calculates the portfolio returns based on the weights of the strategies

    Parameters
    ----------
    strategies : list
        List of dictionaries containing the strategies' returns and volatility
        weights : list

    Returns
    -------
    portfolio_returns : float
    """
    return np.dot(returns, weights)


def calculate_portoflio_volatility(volatilities, weights, correlation_matrix):
    # Write docstring here
    """
    Calculates the portfolio volatility based on the weights of the strategies

    Parameters
    ----------
    strategies : list
        List of dictionaries containing the strategies' returns and volatility
        weights : list
        correlation_matrix : list

    Returns
    -------
    portfolio_volatility : float
    """

    portfolio_volatility = np.sqrt(
        np.dot(
            (
                np.dot(
                    weights,
                    np.dot(
                        np.diag(volatilities),
                        np.dot(correlation_matrix, np.diag(volatilities)),
                    ),
                )
            ),
            np.transpose(weights),
        )
    )

    return portfolio_volatility
