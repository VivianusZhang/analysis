from datetime import datetime

import pandas as pd

from strategies.Grid import Grid
from utils.MatplotlibUtils import plot_grid
from utils.MongoUtils import find_by_code_between, get_today_min, find_by_code_on_and_before


def sample1():
    """
        sample 1:run with no pre condition
    """

    grid = Grid()

    code = '002001'
    start_date = datetime.strptime('2017/06/15', '%Y/%m/%d')
    end_date = datetime.strptime('2017/08/30', '%Y/%m/%d')
    daily_data = find_by_code_between(code, start_date, end_date)

    for i, row in daily_data.iterrows():
        if i < 5:
            continue
        if i == daily_data.datetime.size - 1:
            continue

        next_day = daily_data.loc[i + 1]

        step = max(round(abs((row.high - row.low) / 10), 2), 0.1)

        next_day_min = get_today_min(code, next_day.datetime)
        base = next_day.open
        lower_bound = pd.Series.min(daily_data[i - 4:i].low)
        upper_bound = pd.Series.max(daily_data[i - 4:i].high)
        print ('-----------------------------------------------------------------')
        print ('[%s]base price: %.2f, step: %.2f, lower bound: %.2f, upper_bound: %.2f' % (
            next_day.datetime, base, step, lower_bound, upper_bound))

        grid.grid(next_day_min, base, step, 10, lower_bound, upper_bound, 2000)


def sample2():
    """
         sample 2:run with pre set quantity
    """
    code = '002001'
    target_day = datetime.strptime('2017/10/31', '%Y/%m/%d')
    previous_day = datetime.strptime('2017/10/30', '%Y/%m/%d')

    previous_data = find_by_code_on_and_before(code, previous_day)

    next_day_min = get_today_min(code, target_day)
    base = next_day_min.open[0]
    #step = max(round(abs((previous_data.high[0] - previous_data.low[0]) / 10), 2), 0.1)
    step = 0.08
    lower_bound = previous_data.low[0]
    upper_bound = previous_data.high[0]
    print ('-----------------------------------------------------------------')
    print ('[%s]base price: %.2f, step: %.2f, lower bound: %.2f, upper_bound: %.2f' % (
        target_day, base, step, lower_bound, upper_bound))

    # set current quantity and price on hand
    stock_in_hand = [{'price': base, 'datetime': previous_day, 'quantity': 10000}]
    grid = Grid(stock_in_hand)
    grid.grid(next_day_min, base, step, 10, lower_bound, upper_bound, 2000)

    plot_grid(next_day_min, base, step, lower_bound, upper_bound)


if __name__ == '__main__':
    sample2()