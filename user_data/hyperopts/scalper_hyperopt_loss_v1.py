from math import exp
from typing import Dict

from pandas import DataFrame

from freqtrade.optimize.hyperopt import IHyperOptLoss
from datetime import datetime


# constants:
TARGET_TRADES = 600
TARGET_RATIO = 6

class ScalperHyperOptLossV1(IHyperOptLoss):

    @staticmethod
    def hyperopt_loss_function(results: DataFrame, trade_count: int,
                               min_date: datetime, max_date: datetime,
                               config: Dict, processed: Dict[str, DataFrame],
                               *args, **kwargs) -> float:
        """
        Objective function, returns smaller number for better results
        results {
            pair                                      BTCUP/USDT
            stake_amount                                    2000
            amount                                     34.870543
            open_date                  2021-06-18 12:29:00+00:00
            close_date                 2021-06-18 13:01:00+00:00
            open_rate                                     57.355
            close_rate                                 57.469825
            fee_open                                       0.001
            fee_close                                      0.001
            trade_duration                                    32
            profit_ratio                                     0.0
            profit_abs                                       0.0
            sell_reason                                      roi
            :param sell_reason: Sell reason.
            Can be any of ['roi', 'stop_loss', 'stoploss_on_exchange', 'trailing_stop_loss',
                           'sell_signal', 'force_sell', 'emergency_sell']
            initial_stop_loss_abs                      52.656495
            initial_stop_loss_ratio                     -0.08192
            stop_loss_abs                              52.656495
            stop_loss_ratio                             -0.08192
            min_rate                                        57.1
            max_rate                                      57.637
            is_open                                        False
            open_timestamp                       1624019340000.0
            close_timestamp                      1624021260000.0
        }
        """
        # Win/Loss
        wins = len(results[results['profit_abs'] > 0])
        drawss = len(results[results['profit_abs'] == 0])
        losses = len(results[results['profit_abs'] < 0])

        if losses == 0 and wins > 0:
            losses = 1
            wins += 1

        if wins == 0 and losses > 0:
            wins = 1
            losses += 1

        if wins == 0 and losses == 0:
            wins = 1
            losses = 1

        winrate = wins / losses
        win_result = 1 - 0.5 * winrate / TARGET_RATIO


        # Trade Count
        trade_loss_result = 1 - 0.5 * exp(-(trade_count - TARGET_TRADES) ** 2 / 10 ** 5.8)

        result = 0
        result += win_result
        result += trade_loss_result

        return result
