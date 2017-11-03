from __future__ import print_function

from strategies.order.OrderStatus import OrderStatus


class MakeOrder:
    def __init__(self, tax=0.001, commission=0.0025):
        self.tax = tax
        self.commission = commission

    def order_buy(self, current_bar, quantity, asset, stock_in_hand):
        usable_asset = self.compute_usable_asset(asset, stock_in_hand)

        if usable_asset < current_bar.close * quantity:
            print('[%s]price reach at: %.2f, '
                  'trigger action: BUY , '
                  'current total asset: %.2f, '
                  'current usable asset: %.2f, '
                  'no enough asset, do not make order' % (current_bar.time, current_bar.close, asset, usable_asset))

            return OrderStatus.FAIL, asset, stock_in_hand
        else:
            return self.execute_buy(current_bar, quantity, asset, stock_in_hand)

    def order_sell(self, current_bar, quantity, asset, stock_in_hand):
        history_stock = [stock for stock in stock_in_hand if stock['time'] < current_bar.time.replace(hour=0)]
        total_quantity = sum([stock['quantity'] for stock in history_stock])

        if total_quantity < quantity:
            print('[%s]price reach grid at: %.2f, '
                  'trigger action: SELL, '
                  'current total asset: %.2f, '
                  'current total quantity: %.2f'
                  'no enough yesterday position, do not make order' % (
                      current_bar.time, current_bar.close, asset, total_quantity))

            return OrderStatus.FAIL, asset, stock_in_hand
        else:
            return self.execute_sell(current_bar, quantity, asset, stock_in_hand)

    def execute_buy(self, current_bar, no_of_stock, asset, stock_in_hand):
        asset = asset - self.charge_commission(current_bar.close, no_of_stock)

        stock_in_hand.append({'price': current_bar.close, 'quantity': no_of_stock, 'time': current_bar.time})

        print('[%s]price reach at: %.2f, '
              'trigger action: BUY , '
              'current total asset: %.2f, '
              'make order' % (current_bar.time, current_bar.close, asset))

        print(*stock_in_hand, sep='\n')

        return OrderStatus.SUCCESS, asset, stock_in_hand

    def execute_sell(self, current_bar, quantity, asset, stock_in_hand):
        asset = asset - self.charge_commission(current_bar.close, quantity)

        profit = 0
        index = 0
        for i in range(len(stock_in_hand)):
            if quantity - stock_in_hand[i]['quantity'] >= 0:
                profit = profit + (current_bar.close - stock_in_hand[i]['price']) * stock_in_hand[i]['quantity']
                quantity = quantity - stock_in_hand[i]['quantity']
                index = i + 1
                if quantity == 0:
                    break
            else:
                profit = profit + (current_bar.close - stock_in_hand[i]['price']) * quantity
                stock_in_hand[i]['quantity'] = stock_in_hand[i]['quantity'] - quantity
                break

        stock_in_hand = stock_in_hand[index:]

        if profit > 0:
            asset = asset + profit * (1 + self.tax)
        else:
            asset = asset + profit

        print('[%s]price reach at: %.2f, '
              'trigger action: SELL, '
              'current total asset: %.2f, '
              'make order' % (current_bar.time, current_bar.close, asset))

        print(*stock_in_hand, sep='\n')

        return OrderStatus.SUCCESS, asset, stock_in_hand

    def charge_commission(self, price, quantity):
        return max(price * quantity * self.commission, 5)

    @staticmethod
    def compute_usable_asset(asset, stock_in_hand):
        sum = 0
        for stock in stock_in_hand:
            sum = sum + stock['quantity'] * stock['price']
        return asset - sum
