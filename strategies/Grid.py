from datetime import datetime
from sys import maxint

import numpy as np
import pandas as pd

from strategies.GridEngine import GridEngine
from utils.MongoUtils import find_by_code_on_and_before, get_today_min


def backtest_grid_on_one_day(code, date, step, quantity=1000, lower_bound=0, upper_bound=maxint):
    """
         sample 2:run with pre set quantity
    """
    target_day = datetime.strptime(date, '%Y/%m/%d')

    target_day_min = get_today_min(code, target_day)
    base = round(target_day_min.open[0], 2)
    # step = max(round(abs((previous_data.high[0] - previous_data.low[0]) / 10), 2), 0.1)
    print ('-----------------------------------------------------------------')
    print ('[%s]base price: %.2f, step: %.2f, lower bound: %.2f, upper_bound: %.2f' % (
        target_day, base, step, lower_bound, upper_bound))

    # set current quantity and price on hand
    previous_date = find_by_code_on_and_before(code, target_day, 2).datetime.tolist()[-1]
    stock_in_hand = [{'price': base, 'quantity': 10000, 'datetime': previous_date}]
    grid = GridEngine(stock_in_hand)
    grid.grid(target_day_min, base, step, lower_bound, upper_bound, quantity)


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
        grid = GridEngine([{'price': base, 'quantity': 20000, 'datetime': previous_date}])
        asset, stock_price = grid.grid(data, base_price, i, -maxint - 1, maxint, 2000)
        if max_total_asset:
            if benchmark < asset:
                benchmark = asset
                best_step = i
        else:
            if benchmark > stock_price:
                benchmark = stock_price
                best_step = i

    print ('best step: %.2f' % best_step)


if __name__ == '__main__':
    find_grid_best_step('002001', '2017/10/30', False)
