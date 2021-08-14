# pragma pylint: disable=missing-docstring, invalid-name, pointless-string-statement
# flake8: noqa: F401
# isort: skip_file
# --- Do not remove these libs ---
import numpy as np  # noqa
import pandas as pd  # noqa
import math
from pandas import DataFrame

from freqtrade.strategy import IStrategy
from freqtrade.strategy import CategoricalParameter, DecimalParameter, IntParameter

# --------------------------------
# Add your lib to import here
import talib.abstract as ta
import freqtrade.vendor.qtpylib.indicators as qtpylib


def highpass(Data, n=30):
    a = (0.707 * 2 * math.pi) / n

    alpha1 = (math.cos(a) + math.sin(a) - 1) / math.cos(a)
    b = 1 - alpha1 / 2
    c = 1 - alpha1

    ret = [0] * len(Data)
    for i in range(2, len(Data)):
        ret[i] = (
            b * b * (Data.iloc[i] - 2 * Data[i - 1] + Data.iloc[i - 2])
            + 2 * c * ret[i - 1]
            - c * c * ret[i - 2]
        )

    return pd.Series(ret, index=Data.index)


def fisherN(dataframe, period):
    """Fisher transformation of normalized data"""
    data = dataframe.copy()
    min_value = data.rolling(period).min()
    max_value = data.rolling(period).max()
    norm = (2 * (data - min_value) / (max_value - min_value)) - 1
    norm.replace(to_replace=1, value=0.999, inplace=True)
    norm.replace(to_replace=-1, value=-0.999, inplace=True)

    frac = (1 + norm) / (1 - norm)
    fisher = frac.apply(lambda value: 0.5 * math.log(value))
    return fisher


def EWO(dataframe, ema_length=5, ema2_length=35):
    df = dataframe.copy()
    ema1 = ta.EMA(df, timeperiod=ema_length)
    ema2 = ta.EMA(df, timeperiod=ema2_length)
    emadif = (ema1 - ema2) / df["close"] * 100
    return emadif


# This class is a sample. Feel free to customize it.
class MrMeanV1(IStrategy):
    # Strategy interface version - allow new iterations of the strategy interface.
    # Check the documentation or the Sample strategy to get the latest version.
    INTERFACE_VERSION = 2

    buy_params = {
        "highpass_threshold": 40,
        "buy_signal_threshold": -3.8,
        "fisher_lookback": 175,
        "ewo_high": 4,
        "fast_ewo": 50,
        "slow_ewo": 200,
    }

    sell_params = {"sell_signal_threshold": 3.8}

    # Minimal ROI designed for the strategy.
    # This attribute will be overridden if the config file contains "minimal_roi".
    minimal_roi = {"0": 0.075, "20": 0.045, "60": 0.03, "150": 0.04}

    # Optimal stoploss designed for the strategy.
    # This attribute will be overridden if the config file contains "stoploss".
    stoploss = -0.10

    # Trailing stoploss
    trailing_stop = False
    # trailing_only_offset_is_reached = False
    # trailing_stop_positive = 0.01
    # trailing_stop_positive_offset = 0.0  # Disabled / not configured

    # Hyperoptable parameters
    highpass_threshold = IntParameter(
        low=10,
        high=50,
        default=buy_params["highpass_threshold"],
        space="buy",
        optimize=True,
        load=True,
    )
    fisher_lookback = IntParameter(
        low=50,
        high=500,
        default=buy_params["fisher_lookback"],
        space="buy",
        optimize=True,
        load=True,
    )
    buy_signal_threshold = DecimalParameter(
        low=-4, high=-1, default=-3.8, space="buy", optimize=True, load=True
    )
    sell_signal_threshold = DecimalParameter(
        low=1, high=4, default=3.8, space="sell", optimize=True, load=True
    )

    # Protections
    ewo_high = DecimalParameter(
        2.0, 12.0, default=buy_params["ewo_high"], space="buy", optimize=True
    )
    fast_ewo = IntParameter(
        10, 50, default=buy_params["fast_ewo"], space="buy", optimize=False
    )
    slow_ewo = IntParameter(
        100, 200, default=buy_params["slow_ewo"], space="buy", optimize=False
    )

    # Optimal timeframe for the strategy.
    timeframe = "5m"

    # Run "populate_indicators()" only for new candle.
    process_only_new_candles = True

    # These values can be overridden in the "ask_strategy" section in the config.
    use_sell_signal = True
    sell_profit_only = False
    ignore_roi_if_buy_signal = False

    # Number of candles the strategy requires before producing valid signals
    startup_candle_count: int = 200

    # Optional order type mapping.
    order_types = {
        "buy": "limit",
        "sell": "limit",
        "stoploss": "market",
        "stoploss_on_exchange": False,
    }

    # Optional order time in force.
    order_time_in_force = {"buy": "gtc", "sell": "gtc"}

    def populate_indicators(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
        dataframe["highpass"] = highpass(
            dataframe["close"], self.highpass_threshold.value
        )
        dataframe["fisherN"] = fisherN(
            dataframe["highpass"], self.fisher_lookback.value
        )
        dataframe["EWO"] = EWO(dataframe, self.fast_ewo.value, self.slow_ewo.value)

        return dataframe

    def populate_buy_trend(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
        """
        Based on TA indicators, populates the buy signal for the given dataframe
        :param dataframe: DataFrame populated with indicators
        :param metadata: Additional information, like the currently traded pair
        :return: DataFrame with buy column
        """
        dataframe.loc[
            (
                # Signal: RSI crosses above 30
                (
                    qtpylib.crossed_below(
                        dataframe["fisherN"], self.buy_signal_threshold.value
                    )
                )
                & (dataframe["EWO"] >= self.ewo_high.value)
                & (dataframe["volume"] > 0)  # Make sure Volume is not 0
            ),
            "buy",
        ] = 1

        return dataframe

    def populate_sell_trend(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
        """
        Based on TA indicators, populates the sell signal for the given dataframe
        :param dataframe: DataFrame populated with indicators
        :param metadata: Additional information, like the currently traded pair
        :return: DataFrame with sell column
        """
        dataframe.loc[
            (
                # Signal: RSI crosses above 70
                (
                    qtpylib.crossed_above(
                        dataframe["fisherN"], self.sell_signal_threshold.value
                    )
                )
                & (dataframe["volume"] > 0)  # Make sure Volume is not 0
            ),
            "sell",
        ] = 1
        return dataframe
