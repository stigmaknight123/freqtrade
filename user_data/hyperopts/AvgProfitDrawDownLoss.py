__author__ = "PoCk3T"
__copyright__ = "The GNU General Public License v3.0"

from datetime import datetime
from typing import Dict

from pandas import DataFrame

from freqtrade.optimize.hyperopt import IHyperOptLoss
from freqtrade.data.btanalysis import calculate_max_drawdown

# higher numbers penalize drawdowns more severely
DRAWDOWN_MULT = 2
AVG_MULT = 3
TOTAL_DIV = 2

class AvgProfitDrawDownLoss(IHyperOptLoss):

    @staticmethod
    def hyperopt_loss_function(results: DataFrame, trade_count: int,
                               min_date: datetime, max_date: datetime,
                               config: Dict, processed: Dict[str, DataFrame],
                               *args, **kwargs) -> float:
        """
        Custom objective function, returns smaller number for better results
        
        This function optimizes for both: best profit AND stability
        
        On stability, the final score has an incentive, through 'win_ratio', 
        to make more winning deals out of all deals done
        
        This might prove to be more reliable for dry and live runs of FreqTrade
        and prevent over-fitting on best profit only
        """

        try:
            max_drawdown_per, _, _, _, _ = calculate_max_drawdown(results, value_col='profit_ratio')
        except ValueError:
            max_drawdown_per = 0

        avg_profit = results['profit_ratio'].sum()

        if ((max_drawdown_per * DRAWDOWN_MULT) > 1) and (avg_profit < 0):
            avg_profit = avg_profit * -1

        return -1 * (avg_profit * AVG_MULT * (1 - max_drawdown_per * DRAWDOWN_MULT))
        # return -1 * (avg_profit * AVG_MULT / (max_drawdown_per * DRAWDOWN_MULT))
