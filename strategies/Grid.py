import pandas as pd
import tushare as ts

class Grid():

    def __init__(self, instrument, date):
        cons = ts.get_apis()
        self.data = ts.bar(instrument, conn=cons, freq='1min', start_date = date, end_date='')
        self.asset = 1000000
        self.position = 10000
        self.tax = 0.001
        self.commission = 0.0025

    def grid(self, base_price, step, no_of_step, stop_buy, stop_sell, no_of_stock, position_price, asset):

        current_base = base_price
        current_position = initial_position = self.position

        for index, row in self.data.iterrows():
            # check whether close is between range, and whether the grid is triggered
            if stop_buy <= row.close <= stop_sell & abs(row.close - current_base) == step:
                # check whether exceed upper and lower boundary
                if (current_base - base_price)/step <= no_of_step:
                    if row.close > current_base:
                        current_base, current_position, initial_position, asset = self.order_buy(
                            row.close, current_position, initial_position,no_of_stock, asset)

                    else:
                        current_base, current_position, initial_position, asset = self.order_sell(row.close, current_position, initial_position,
                                                                       no_of_stock, asset, position_price)

                else:
                    print('price reach grid at: ' + row.close + 'no trigger action: ' + ' current asset: ' + asset +
                          'exceed stop buy or stop sell')

    def order_buy(self, price, current_position, initial_position, no_of_stock, current_base, asset):
        if asset < price * no_of_stock:
            print('price reach grid at: ' + price + ' trigger action: BUY, current asset: ' + asset +
                  'no enough asset, do not make order')
            return current_base, current_position, initial_position, asset
        else:
            return self.execute_buy(price, current_position, initial_position, no_of_stock, asset)

    def execute_buy(self, price, current_position, initial_position, no_of_stock, asset):
        asset = asset - price * no_of_stock
        current_position = current_position + no_of_stock
        initial_position = initial_position - no_of_stock

        asset = asset - self.charge_commission(price, no_of_stock)

        print('price reach grid at: ' + price + ' trigger action: BUY, current asset' + asset +
              ' make order')

        return price, current_position, initial_position, asset

    def order_sell(self, price, current_position, initial_position, no_of_stock, current_base, asset, position_price):
        if initial_position < no_of_stock:
            print('price reach grid at: ' + price + ' trigger action: SELL, current asset: ' + asset +
                  'no enough yesterday position, do not make order')
            return current_base, current_position, initial_position, asset
        else:
            return self.execute_sell(price, current_position, initial_position, no_of_stock, asset, position_price)

    def execute_sell(self, price, current_position, initial_position, no_of_stock, asset, position_price):
        asset = asset + price * no_of_stock
        asset = asset - price * position_price * self.tax
        current_position = current_position - no_of_stock

        asset = asset - self.charge_commission(price, no_of_stock)

        print('price reach grid at: ' + price + ' trigger action: SELL, current asset: ' + asset +
              ' make order')

        return price, current_position, initial_position, asset

    @staticmethod
    def charge_commission(self, price, no_of_stock):
        return max(price * no_of_stock * self.commission, 5)

