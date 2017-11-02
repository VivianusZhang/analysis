import matplotlib as plt
import matplotlib.dates as mdates
import matplotlib.pyplot as plt
import numpy as np
import tushare as ts


class Grid():
    def __init__(self, instrument, date):
        cons = ts.get_apis()
        self.data = ts.bar(instrument, conn=cons, freq='1min', start_date=date, end_date=date)
        self.data['date'] = self.data.index
        self.data = self.data.reindex(index=self.data.index[::-1])
        self.asset = 1000000
        self.position = 10000
        self.tax = 0.001
        self.commission = 0.0025

    def grid(self, base_price, step, no_of_step, lower_bound, upper_bound, no_of_stock, position_price):

        current_base = base_price
        current_position = initial_position = self.position
        remaining_asset = total_asset = self.asset

        lowest_price = min(lower_bound, base_price - step * no_of_step)
        highest_price = max(upper_bound, base_price + step * no_of_step)

        for index, row in self.data.iterrows():
            # check whether close is between range, and whether the grid is triggered
            if abs(row.close - current_base) - step < 0.00000001:
                if lowest_price <= row.close <= highest_price:
                    if row.close > current_base:
                        current_base, current_position, initial_position, remaining_asset, total_asset = self.order_buy(
                            row, current_base, current_position, initial_position, no_of_stock, remaining_asset,
                            total_asset)

                    else:
                        current_base, current_position, initial_position, remaining_asset, total_asset = self.order_sell(
                            row, current_base, current_position, initial_position, no_of_stock, remaining_asset,
                            total_asset,
                            position_price)
                else:
                    print(
                        'price reach grid at: %f, no trigger action, current remaining_asset: %f exceed stop buy or stop sell' % (
                            row.close, remaining_asset))

        print ('total remaining_asset at day end: %f, profit: %f' % (
            total_asset, (total_asset - self.asset) / self.asset))

        self.plot(step, base_price, lower_bound, upper_bound)

    def plot(self, step, base_price, lower_bound, upper_bound):
        fig, ax = plt.subplots(figsize=(14, 7))
        df = self.data
        df['date'] = df.index

        quotes = []
        for index, (date, close) in enumerate(zip(df.date, df.close)):
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

        plt.show()

    def order_buy(self, current_bar, current_base, current_position, initial_position, no_of_stock, remaining_asset,
                  total_asset):
        if remaining_asset < current_bar.close * no_of_stock:

            print(
                'price reach grid at: %f, trigger action: BUY, current asset: %f, no enough asset, do not make order' % (
                    current_bar.close, remaining_asset))

            return current_base, current_position, initial_position, remaining_asset, total_asset
        else:
            return self.execute_buy(current_bar, current_position, initial_position, no_of_stock, remaining_asset,
                                    total_asset)

    def execute_buy(self, current_bar, current_position, initial_position, no_of_stock, remaining_asset, total_asset):
        remaining_asset = remaining_asset - current_bar.close * no_of_stock
        current_position = current_position + no_of_stock
        initial_position = initial_position - no_of_stock

        remaining_asset = remaining_asset - self.charge_commission(current_bar.close, no_of_stock)
        total_asset = total_asset - self.charge_commission(current_bar.close, no_of_stock)

        print('price reach grid at: %f, trigger action: BUY, current asset: %f, make order, time: %s' % (
            current_bar.close, remaining_asset, current_bar.date))

        return current_bar.close, current_position, initial_position, remaining_asset, total_asset

    def order_sell(self, current_bar, current_base, current_position, initial_position, no_of_stock, remaining_asset,
                   total_asset,
                   position_price):
        if initial_position < no_of_stock:
            print(
                'price reach grid at: %f, trigger action: SELL, current asset: %f, no enough yesterday position, do not make order' % (
                    current_bar.close, remaining_asset))

            return current_base, current_position, initial_position, remaining_asset, total_asset
        else:
            return self.execute_sell(current_bar, current_position, initial_position, no_of_stock, remaining_asset,
                                     total_asset,position_price)

    def execute_sell(self, current_bar, current_position, initial_position, no_of_stock, remaining_asset, total_asset,
                     position_price):
        remaining_asset = remaining_asset + current_bar.close * no_of_stock
        total_asset = total_asset + current_bar.close * no_of_stock

        if current_bar.close - position_price > 0:
            remaining_asset = remaining_asset - (current_bar.close - position_price) * self.tax
            total_asset = total_asset - (current_bar.close - position_price) * self.tax

        current_position = current_position - no_of_stock

        remaining_asset = remaining_asset - self.charge_commission(current_bar.close, no_of_stock)
        total_asset = total_asset - self.charge_commission(current_bar.close, no_of_stock)

        print('price reach grid at: %f, trigger action: SELL, current asset: %f, make order' % (
            current_bar.close, remaining_asset))

        return current_bar.close, current_position, initial_position, remaining_asset, total_asset

    def charge_commission(self, price, no_of_stock):
        return max(price * no_of_stock * self.commission, 5)


if __name__ == "__main__":
    grid = Grid('002001', '2017/10/31')
    grid.grid(25.1, 0.05, 10, 25, 25.6, 1000, 25.1)
