# pragma pylint: disable=missing-docstring, invalid-name, pointless-string-statement

# --- Do not remove these libs ---
from functools import reduce
from typing import Any, Callable, Dict, List
import numpy as np  # noqa
import pandas as pd  # noqa
from pandas import DataFrame
from freqtrade.optimize.space import Categorical, Dimension, Integer, SKDecimal, Real  # noqa
from freqtrade.optimize.hyperopt_interface import IHyperOpt
import talib.abstract as ta  # noqa
import freqtrade.vendor.qtpylib.indicators as qtpylib


class ichiV1Hyperopt(IHyperOpt):

    @staticmethod
    def indicator_space() -> List[Dimension]:
        return [
            Integer(1, 8, name='buy_trend_above_senkou_level'),
            Integer(1, 8, name='buy_trend_bullish_level'),
            Integer(1, 10, name='buy_fan_magnitude_shift_value'),
            SKDecimal(1.00, 1.01, name='buy_min_fan_magnitude_gain')
        ]

    @staticmethod
    def buy_strategy_generator(params: Dict[str, Any]) -> Callable:

        def populate_buy_trend(dataframe: DataFrame, metadata: dict) -> DataFrame:

            conditions = []

            # Trending market
            if params['buy_trend_above_senkou_level'] >= 1:
                conditions.append(dataframe['trend_close_5m'] > dataframe['senkou_a'])
                conditions.append(dataframe['trend_close_5m'] > dataframe['senkou_b'])

            if params['buy_trend_above_senkou_level'] >= 2:
                conditions.append(dataframe['trend_close_15m'] > dataframe['senkou_a'])
                conditions.append(dataframe['trend_close_15m'] > dataframe['senkou_b'])

            if params['buy_trend_above_senkou_level'] >= 3:
                conditions.append(dataframe['trend_close_30m'] > dataframe['senkou_a'])
                conditions.append(dataframe['trend_close_30m'] > dataframe['senkou_b'])

            if params['buy_trend_above_senkou_level'] >= 4:
                conditions.append(dataframe['trend_close_1h'] > dataframe['senkou_a'])
                conditions.append(dataframe['trend_close_1h'] > dataframe['senkou_b'])

            if params['buy_trend_above_senkou_level'] >= 5:
                conditions.append(dataframe['trend_close_2h'] > dataframe['senkou_a'])
                conditions.append(dataframe['trend_close_2h'] > dataframe['senkou_b'])

            if params['buy_trend_above_senkou_level'] >= 6:
                conditions.append(dataframe['trend_close_4h'] > dataframe['senkou_a'])
                conditions.append(dataframe['trend_close_4h'] > dataframe['senkou_b'])

            if params['buy_trend_above_senkou_level'] >= 7:
                conditions.append(dataframe['trend_close_6h'] > dataframe['senkou_a'])
                conditions.append(dataframe['trend_close_6h'] > dataframe['senkou_b'])

            if params['buy_trend_above_senkou_level'] >= 8:
                conditions.append(dataframe['trend_close_8h'] > dataframe['senkou_a'])
                conditions.append(dataframe['trend_close_8h'] > dataframe['senkou_b'])

            # Trends bullish
            if params['buy_trend_bullish_level'] >= 1:
                conditions.append(dataframe['trend_close_5m'] > dataframe['trend_open_5m'])

            if params['buy_trend_bullish_level'] >= 2:
                conditions.append(dataframe['trend_close_15m'] > dataframe['trend_open_15m'])

            if params['buy_trend_bullish_level'] >= 3:
                conditions.append(dataframe['trend_close_30m'] > dataframe['trend_open_30m'])

            if params['buy_trend_bullish_level'] >= 4:
                conditions.append(dataframe['trend_close_1h'] > dataframe['trend_open_1h'])

            if params['buy_trend_bullish_level'] >= 5:
                conditions.append(dataframe['trend_close_2h'] > dataframe['trend_open_2h'])

            if params['buy_trend_bullish_level'] >= 6:
                conditions.append(dataframe['trend_close_4h'] > dataframe['trend_open_4h'])

            if params['buy_trend_bullish_level'] >= 7:
                conditions.append(dataframe['trend_close_6h'] > dataframe['trend_open_6h'])

            if params['buy_trend_bullish_level'] >= 8:
                conditions.append(dataframe['trend_close_8h'] > dataframe['trend_open_8h'])

            # Trends magnitude
            conditions.append(dataframe['fan_magnitude_gain'] >= params['buy_min_fan_magnitude_gain'])
            conditions.append(dataframe['fan_magnitude'] > 1)

            for x in range(params['buy_fan_magnitude_shift_value']):
                conditions.append(dataframe['fan_magnitude'].shift(x+1) < dataframe['fan_magnitude'])

            if conditions:
                dataframe.loc[
                    reduce(lambda x, y: x & y, conditions),
                    'buy'] = 1

            return dataframe

        return populate_buy_trend

    @staticmethod
    def sell_indicator_space() -> List[Dimension]:
        return [
            Categorical([
                'trend_close_15m',
                'trend_close_30m',
                'trend_close_1h',
                'trend_close_2h',
                'trend_close_4h',
                'trend_close_6h',
                'trend_close_8h'
            ], name='sell_trend_indicator')
        ]

    @staticmethod
    def sell_strategy_generator(params: Dict[str, Any]) -> Callable:

        def populate_sell_trend(dataframe: DataFrame, metadata: dict) -> DataFrame:

            conditions = []

            conditions.append(qtpylib.crossed_below(dataframe['trend_close_5m'], dataframe[params['sell_trend_indicator']]))

            if conditions:
                dataframe.loc[
                    reduce(lambda x, y: x & y, conditions),
                    'sell'] = 1

            return dataframe

        return populate_sell_trend
