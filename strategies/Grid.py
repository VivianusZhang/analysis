from datetime import datetime

import matplotlib as plt
import matplotlib.dates as mdates
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

from indicator.Intraday import vwap
from strategies.order.MakeOrder import MakeOrder
from strategies.order.OrderStatus import OrderStatus
from utils.MongoUtils import find_by_code_between, get_today_min


class Grid():
    def __init__(self, stock_in_hand=[], asset=1000000):

        self.stock_in_hand = stock_in_hand
        self.asset = asset
        self.make_order = MakeOrder()

    def grid(self, data, base_price, step, no_of_step, lower_bound, upper_bound, quantity):

        initial_asset = self.asset
        lowest_price = min(lower_bound, base_price - step * no_of_step)
        highest_price = max(upper_bound, base_price + step * no_of_step)

        for index, row in data.iterrows():
            # check whether close is between range, and whether the grid is triggered
            if abs(abs(row.close - base_price) - step) < 0.00000001:
                if lowest_price <= row.close <= highest_price:
                    if row.close > base_price:

                        status, self.asset, self.stock_in_hand = self.make_order.order_buy(
                            row, quantity, self.asset, self.stock_in_hand)
                        if status == OrderStatus.SUCCESS:
                            base_price = row.close
                    else:
                        status, self.asset, self.stock_in_hand = self.make_order.order_sell(
                            row, quantity, self.asset, self.stock_in_hand)
                        if status == OrderStatus.SUCCESS:
                            base_price = row.close
                else:
                    print('[%s]price reach grid at: %.2f, '
                          'no trigger action, '
                          'current total asset: %.2f, '
                          'exceed stop buy or stop sell' % (row.datetime, row.close, self.asset))

        print ('total remaining_asset at day end: %f, profit: %f' % (
            self.asset, (self.asset - initial_asset) / initial_asset))

    @staticmethod
    def plot(data, base_price, step, lower_bound, upper_bound):
        fig, ax = plt.subplots(figsize=(14, 7))
        df = pd.DataFrame(data)

        quotes = []
        for index, (date, close) in enumerate(zip(df.datetime, df.close)):
            val = (mdates.date2num(date), close)
            quotes.append(val)
        daily_quotes = [tuple([i] + list(quote[1:])) for i, quote in enumerate(quotes)]

        ax.set_xticks(range(0, len(daily_quotes), 30))
        ax.set_xticklabels([mdates.num2date(quotes[index][0]).strftime('%b-%d-%H:%M') for index in ax.get_xticks()])

        ax.plot(np.array([i[0] for i in daily_quotes]), np.array([i[1] for i in daily_quotes]))

        plt.axhline(lower_bound, color='r', linestyle='-')
        plt.axhline(upper_bound, color='r', linestyle='-')
        plt.axhline(base_price, color='g', linestyle='-')

        y_ticks = np.arange(lower_bound, upper_bound, step)
        y_bounder = np.arange(np.amin(df.close), np.amax(df.close), 0.2)

        ax.set_yticks(y_ticks)
        ax.set_yticks(y_bounder, minor=True)

        ax.grid(which='both')
        ax.grid(which='minor', alpha=0.2)
        ax.grid(which='major', alpha=0.5)

        plt.show(block=False)


if __name__ == "__main__":
    grid = Grid()

    code = '002230'
    start_date = datetime.strptime('2017/08/01', '%Y/%m/%d')
    end_date = datetime.strptime('2017/10/31', '%Y/%m/%d')
    daily_data = find_by_code_between(code, start_date, end_date)

    for i in range(len(daily_data)):
        if i < 5:
            continue
        if i - 1 == len(daily_data):
            continue

        today = daily_data[i]['datetime'].strftime('%Y/%m/%d')
        next_day = daily_data[i + 1]['datetime'].strftime('%Y/%m/%d')
        step = (daily_data[i]['close'] - daily_data[i]['open']) / 10

        grid.grid(get_today_min(code, next_day), vwap(get_today_min(code, today)), step, 10,
                  min(daily_data[i - 4, i]['close'],
                      max(daily_data[i - 4, i]['close'], 1000)))
