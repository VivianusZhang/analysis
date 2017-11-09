from datetime import datetime

from pymongo import MongoClient

from strategies.order.MakeOrder import MakeOrder
from strategies.order.OrderStatus import OrderStatus
from utils.MongoUtils import find_by_code_between, get_today_min
import pandas as pd

class Grid():
    def __init__(self, stock_in_hand=[], asset=1000000):

        self.stock_in_hand = stock_in_hand
        self.asset = asset
        self.make_order = MakeOrder()
        self.trading_profit = 0

    def grid(self, data, base_price, step, no_of_step, lower_bound, upper_bound, quantity):

        initial_asset = self.asset
        lowest_price = min(lower_bound, base_price - step * no_of_step)
        highest_price = max(upper_bound, base_price + step * no_of_step)
        close = data.close.tolist()[-1]

        for index, row in data.iterrows():
            # check whether close is between range, and whether the grid is triggered
            if abs(abs(row.close - base_price) - step) < 0.00000001:
                if lowest_price <= row.close <= highest_price:
                    if row.close < base_price:
                        status, self.asset, self.stock_in_hand = self.make_order.order_buy(
                            row, quantity, self.asset, self.stock_in_hand)
                        if status == OrderStatus.SUCCESS:
                            base_price = row.close
                    else:
                        status, self.asset, self.stock_in_hand , profit= self.make_order.order_sell(
                            row, quantity, self.asset, self.stock_in_hand)
                        self.trading_profit = self.trading_profit + profit
                        if status == OrderStatus.SUCCESS:
                            base_price = row.close
                else:
                    print('[%s]price reach grid at: %.2f, '
                          'no trigger action, '
                          'current total asset: %.2f, '
                          'exceed stop buy or stop sell' % (row.datetime, row.close, self.asset))

        print ('[%s]total remaining_asset at day end: %.2f' % (data.datetime[0], self.asset))
        print ('[%s]trading profit: %f'%(data.datetime[0], self.trading_profit/initial_asset))
        print ('[%s]day end profit: %f'% (data.datetime[0], (self.compute_day_end_profit(close) - initial_asset)/initial_asset))
        print ('[%s]average stock price: %f'% (data.datetime[0],self.compute_average_price()))


    def compute_day_end_profit(self, close):
        remaining = MakeOrder.compute_usable_asset(self.asset, self.stock_in_hand)
        return sum([stock['quantity'] for stock in self.stock_in_hand]) * close + remaining

    def compute_average_price(self):
        quantity = 0
        asset = 0
        for stock in self.stock_in_hand:
            asset = asset + stock['quantity'] * stock['price']
            quantity = quantity + stock['quantity']

        if quantity == 0:
            return 0
        else:
            return asset/quantity




