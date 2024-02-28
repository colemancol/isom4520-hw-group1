from typing import Protocol, Optional

from src.Simulator.DataProviders.AllStocksPrices import AllStocksPrices

from ._add_bet_against_beta_signal import add_bet_against_beta_signal


class SignalFunction(Protocol):
    def __call__(self, stock_histories: AllStocksPrices, **params) -> None: ...


def get_universe_signal_func(**params) -> Optional[SignalFunction]:

    strategy_name = params["strategy_name"]

    strategy_signal_func_dict = {
        "random": None,
        "bet_against_beta": add_bet_against_beta_signal,
    }

    signal_func = strategy_signal_func_dict.get(strategy_name)
    if signal_func is None:
        raise ValueError(
            f"No signal function found for strategy: {strategy_name}. Please double check strategy_signal_func_dict in _get_universal_signal_func.py."
        )

    return signal_func
