from datetime import datetime
from sys import maxint

import numpy as np
import pandas as pd

from strategies.GridEngine import GridEngine
from utils.MongoUtils import find_by_code_on_and_before, get_today_min


def backtest_grid_on_one_day(code, date, base_price, lower_step, upper_step, usable_asset, quantity=1000, lower_bound=0, upper_bound=maxint):
    """
         sample 2:run with pre set quantity
    """
    target_day = datetime.strptime(date, '%Y/%m/%d')

    target_day_min = get_today_min(code, target_day)
    base = round(target_day_min.open[0], 2)
    initial_asset = quantity * base + usable_asset
    # step = max(round(abs((previous_data.high[0] - previous_data.low[0]) / 10), 2), 0.1)
    print ('-----------------------------------------------------------------')
    print ('[%s]base price: %.2f, lower step: %.2f, upper step:%.2f lower bound: %.2f, upper_bound: %.2f' % (
        target_day, base_price, lower_step, upper_step, lower_bound, upper_bound))

    # set current quantity and price on hand
    previous_date = find_by_code_on_and_before(code, target_day, 2).datetime.tolist()[-1]
    stock_in_hand = [{'price': base, 'quantity': quantity, 'datetime': previous_date}]
    grid = GridEngine(stock_in_hand, initial_asset)

    return grid.grid(target_day_min, base_price, lower_step, upper_step, lower_bound, upper_bound, quantity/20)

def find_grid_best_step(code, date, max_total_asset=True):
    if max_total_asset:
        benchmark = -maxint - 1
    else:
        benchmark = maxint

    best_step = 0
    date = datetime.strptime(date, '%Y/%m/%d')
    data = get_today_min(code, date)
    base = round(data.open[0], 2)
    previous_date = find_by_code_on_and_before(code, date, 2).datetime.tolist()[-1]
    base_price = round(data.open[0], 2)

    for i in list(np.arange(0.02, (pd.Series.max(data.close) - pd.Series.min(data.close)) / 2, 0.01)):
        print ('--------------------run gird at : %.2f----------------------' % i)
        grid = GridEngine([{'price': base, 'quantity': 10000, 'datetime': previous_date}])
        result, day_end_result = grid.grid(data, base_price, i, -maxint - 1, maxint, 1000)

        if max_total_asset:
            if benchmark < day_end_result['day end asset']:
                benchmark = day_end_result['day end asset']
                best_step = i
        else:
            if benchmark > day_end_result['average stock price']:
                benchmark = day_end_result['average stock price']
                best_step = i

    print ('best step: %.2f' % best_step)

if __name__ == '__main__':
    print backtest_grid_on_one_day('002230', '2017/09/29', 54, 0.02,0.03, 1000000, 50000, 51, 55)