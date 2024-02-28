from typing import Protocol
import pandas as pd

from src.Simulator.DataProviders.AllStocksPrices import AllStocksPrices


class UniversalSignalFunction(Protocol):
    def __call__(self, stock_histories: AllStocksPrices, **params) -> None: ...


class AlphaSignalFunction(Protocol):
    def __call__(self, df_in: pd.DataFrame, **params) -> None: ...
