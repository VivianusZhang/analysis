from strategies.order.MakeOrder import MakeOrder
from strategies.order.OrderStatus import OrderStatus


class GridEngine():
    def __init__(self, stock_in_hand=[], asset=2000000):

        self.stock_in_hand = stock_in_hand
        self.asset = asset
        self.make_order = MakeOrder()
        self.trading_profit = 0

    def grid(self, data, base_price, lower_step, upper_step, lower_bound, upper_bound, quantity):

        initial_asset = self.asset
        initial_quantity = sum([stock['quantity'] for stock in self.stock_in_hand])
        initial_usable_asset = MakeOrder.compute_usable_asset(self.asset, self.stock_in_hand)
        lowest_price = lower_bound
        highest_price = upper_bound
        close = data.close.tolist()[-1]
        buy_count = 0
        sell_count = 0
        result = self.init_logs()

        for index, row in data.iterrows():
            # check whether close is between range, and whether the grid is triggered
            # -0.0000001 cater for rounding error
            if lowest_price <= row.close <= highest_price:
                if base_price - row.close - lower_step >= -0.0000001:

                    self.log_base_price(result, base_price, upper_step)

                    execution_price = round(base_price - upper_step, 2)
                    status, self.asset, self.stock_in_hand = self.make_order.order_buy(
                        row, execution_price, quantity, self.asset, self.stock_in_hand)
                    if status == OrderStatus.SUCCESS:
                        base_price = execution_price
                        buy_count = buy_count + 1
                    self.log_transactions(result, row, status, 'BUY', execution_price,
                                     initial_asset, quantity, buy_count, sell_count)
                elif row.close - base_price - upper_step >= -0.0000001:
                    execution_price = round(base_price + lower_step, 2)
                    status, self.asset, self.stock_in_hand, profit = self.make_order.order_sell(
                        row, execution_price, quantity, self.asset, self.stock_in_hand)
                    self.trading_profit = self.trading_profit + profit
                    if status == OrderStatus.SUCCESS:
                        base_price = execution_price
                        sell_count = sell_count + 1
                    self.log_transactions(result, row, status, 'SELL', execution_price,
                                          initial_asset, quantity, buy_count, sell_count)

        # print ('[%s]total remaining_asset at day end: %.2f' % (data.datetime[0], self.asset))
        # print ('[%s]trading profit: %f' % (data.datetime[0], self.trading_profit / initial_asset))
        day_end_asset = self.compute_total_asset(close)
        average_price = self.compute_average_price()
        # print ('[%s]day end asset: %f, profit: %f' % (data.datetime[0], day_end_asset
        #                                               , (day_end_asset - initial_asset) / initial_asset))
        # print ('[%s]day benchmark: %f' % (data.datetime[0], initial_quantity * close + initial_usable_asset))
        # print ('[%s]average stock price: %f' % (data.datetime[0], average_price))
        # print ('[%s]today pair trading: %d' % (data.datetime[0], min(buy_count, sell_count)))

        day_end_result = {'datetime': data.datetime[0],
                          'day end asset':day_end_asset,
                          'day end profit':(day_end_asset - initial_asset) / initial_asset,
                          'benchmark':initial_quantity * close + initial_usable_asset,
                          'average stock price': average_price,
                          'pair trading': min(buy_count, sell_count)}

        return result, day_end_result

    def compute_total_asset(self, close):
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

    @staticmethod
    def init_logs():

        return {
            'action_datetime': [],
            'base_price': [],
            'base_price_up': [],
            'base_price_down': [],
            'execution_price': [],
            'action': [],
            'order_status': [],
            'trading_pair': [],
            'buy_count': [],
            'sell_count': [],
            'asset_details': [],
            'cash_details':[],
            'history_quantity': [],
            'stock_quantity':[],
            'profit': []}

    def log_base_price(self, result, base_price, step):
        result['base_price'].append(base_price)
        result['base_price_up'].append(base_price + step)
        result['base_price_down'].append(base_price - step)

    def log_transactions(self, result, row, status, action, execution_price, initial_asset, quantity, buy_count, sell_count):
        history_stock = [stock for stock in self.stock_in_hand if
                         stock['datetime'] < row.datetime.replace(hour=0)]
        result['history_quantity'].append(sum([stock['quantity'] for stock in history_stock]))
        result['asset_details'].append(self.asset)
        result['order_status'].append(status)
        if status == OrderStatus.SUCCESS:
            result['stock_quantity'].append(quantity)
        else:
            result['stock_quantity'].append(0)
        result['buy_count'].append(buy_count)
        result['sell_count'].append(sell_count)
        result['trading_pair'].append(min(buy_count, sell_count))
        result['action'].append(action)
        result['execution_price'].append(execution_price)
        result['action_datetime'].append(row.datetime)
        result['profit'].append((self.compute_total_asset(row.close) - initial_asset) / initial_asset)
        result['cash_details'].append(MakeOrder.compute_usable_asset(self.asset, self.stock_in_hand))