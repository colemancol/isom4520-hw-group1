from ._add_random_signal import add_random_signal
from ._add_MA5_crosses_MA50_signal import add_MA5_crosses_MA50_signal
from ._add_buy_and_hold_signal import add_buy_and_hold_signal
from ._add_ema_strategy import add_ema_strategy
from ._add_atr_strategy import add_atr_strategy
from ._add_macd_strategy import add_macd_strategy


def get_alpha_signal_func(**params):

    strategy_name = params["strategy_name"]

    strategy_signal_func_dict = {
        "random": add_random_signal,
        "MA5_cross_MA50": add_MA5_crosses_MA50_signal,
        "buy_and_hold": add_buy_and_hold_signal,
        "ema": add_ema_strategy,
        "atr": add_atr_strategy,
        "macd": add_macd_strategy,
    }

    signal_func = strategy_signal_func_dict.get(strategy_name)
    if signal_func is None:
        raise NotImplementedError(f"Signal '{strategy_name}' is not implemented yet.")

    return signal_func
