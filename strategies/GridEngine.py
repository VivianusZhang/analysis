from strategies.order.MakeOrder import MakeOrder
from strategies.order.OrderStatus import OrderStatus


class GridEngine():
    def __init__(self, stock_in_hand=[], asset=1000000):

        self.stock_in_hand = stock_in_hand
        self.asset = asset
        self.make_order = MakeOrder()
        self.trading_profit = 0

    def grid(self, data, base_price, step, lower_bound, upper_bound, quantity):

        initial_asset = self.asset
        initial_quantity = sum([stock['quantity'] for stock in self.stock_in_hand])
        initial_usable_asset = MakeOrder.compute_usable_asset(self.asset, self.stock_in_hand)
        lowest_price = lower_bound
        highest_price = upper_bound
        close = data.close.tolist()[-1]
        buy_count = 0
        sell_count = 0

        for index, row in data.iterrows():
            # check whether close is between range, and whether the grid is triggered
            if abs(row.close - base_price) - step >= 0:
                if lowest_price <= row.close <= highest_price:
                    if row.close < base_price:
                        execution_price = round(base_price - step, 2)
                        status, self.asset, self.stock_in_hand = self.make_order.order_buy(
                            row, execution_price, quantity, self.asset, self.stock_in_hand)
                        if status == OrderStatus.SUCCESS:
                            base_price = execution_price
                            buy_count = buy_count + 1
                    else:
                        execution_price = round(base_price + step, 2)
                        status, self.asset, self.stock_in_hand, profit = self.make_order.order_sell(
                            row, execution_price, quantity, self.asset, self.stock_in_hand)
                        self.trading_profit = self.trading_profit + profit
                        if status == OrderStatus.SUCCESS:
                            base_price = execution_price
                            sell_count = sell_count + 1
                else:
                    print('[%s]price reach grid at: %.2f, '
                          'no trigger action, '
                          'current total asset: %.2f, '
                          'exceed stop buy or stop sell' % (row.datetime, row.close, self.asset))

        # print ('[%s]total remaining_asset at day end: %.2f' % (data.datetime[0], self.asset))
        # print ('[%s]trading profit: %f' % (data.datetime[0], self.trading_profit / initial_asset))
        day_end_asset = self.compute_day_end_asset(close)
        average_price = self.compute_average_price()
        print ('[%s]day end asset: %f, profit: %f' % (data.datetime[0], day_end_asset
                                                      , (day_end_asset - initial_asset) / initial_asset))
        print ('[%s]day benchmark: %f' % (data.datetime[0], initial_quantity * close + initial_usable_asset))
        print ('[%s]average stock price: %f' % (data.datetime[0], average_price))
        print ('[%s]today pair trading: %d' % (data.datetime[0], min(buy_count, sell_count)))

        return day_end_asset, average_price

    def compute_day_end_asset(self, close):
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
            return asset / quantity
