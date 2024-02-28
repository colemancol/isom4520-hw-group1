from typing import Optional

from src.Simulator.Signals.SignalFunctions import UniversalSignalFunction


from ._add_bet_against_beta_signal import add_bet_against_beta_signal


def get_universe_signal_func(**params) -> Optional[UniversalSignalFunction]:

    strategy_name = params["strategy_name"]

    strategy_signal_func_dict = {
        "random": None,
        "bet_against_beta": add_bet_against_beta_signal,
    }

    signal_func = strategy_signal_func_dict.get(strategy_name)

    return signal_func
