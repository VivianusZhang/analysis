import matplotlib as plt
import matplotlib.dates as mdates
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from datetime import datetime

from strategies.Grid import backtest_grid_on_one_day
from strategies.order.OrderStatus import OrderStatus

from utils.MongoUtils import get_today_min


def plot_grid(transaction, data, base_price, step, lower_bound, upper_bound):
    fig, ax = plt.subplots(figsize=(13, 8))
    df = pd.DataFrame(data)

    quotes = []
    buy_marker = []
    sell_marker = []
    i = 0
    for index, (date, close) in enumerate(zip(df.datetime, df.close)):
        val = (mdates.date2num(date), close)
        quotes.append(val)
        if i < len(transaction) and transaction[i]['datetime'] == date:
            if transaction[i]['action'] == 'BUY':
                buy_marker.append(mdates.date2num(date))
            else:
                sell_marker.append(mdates.date2num(date))
            i = i +1

    daily_quotes = []
    daily_buy_marker = []
    daily_sell_marker = []
    for i, quote in enumerate(quotes):
        daily_quotes.append(tuple([i] + list(quote[1:])))
        if quote[0] in buy_marker:
            daily_buy_marker.append(tuple([i] + list(quote[1:])))
        elif quote[0] in sell_marker:
            daily_sell_marker.append(tuple([i] + list(quote[1:])))

    #daily_quotes = [tuple([i] + list(quote[1:])) for i, quote in enumerate(quotes)]

    ax.set_xticks(range(0, len(daily_quotes), 15))
    ax.set_xticklabels([mdates.num2date(quotes[index][0]).strftime('%b-%d-%H:%M') for index in ax.get_xticks()],rotation=30)
    ax.plot(np.array([i[0] for i in daily_quotes]), np.array([i[1] for i in daily_quotes]))

    plt.axhline(lower_bound, color='r', linestyle='-.')
    plt.axhline(upper_bound, color='r', linestyle='-.')
    plt.axhline(base_price, color='k', linestyle='-.')

    n_upper = 0
    highest_price = max(upper_bound, pd.Series.max(data.close))
    lowest_price = min(lower_bound, pd.Series.min(data.close))
    while base_price + n_upper*step < highest_price:
        n_upper = n_upper + 1
    n_lower = 0
    while base_price - n_lower*step > lowest_price:
        n_lower = n_lower + 1

    y_ticks = np.arange(base_price - n_lower*step, base_price + n_upper*step, step)
    y_bounder = np.arange(np.amin(df.close), np.amax(df.close), 0.2)

    ax.set_yticks(y_ticks)
    ax.set_yticks(y_bounder, minor=True)

    ax.grid(which='both')
    ax.grid(which='minor', alpha=0.2)
    ax.grid(which='major', alpha=0.5)
    ax.autoscale_view()


    plt.ylabel('Price')

    #plt.show(block=False)
    plt.plot(np.array([i[0] for i in daily_buy_marker]), np.array([i[1] for i in daily_buy_marker]), 'r^')
    plt.plot(np.array([i[0] for i in daily_sell_marker]), np.array([i[1] for i in daily_sell_marker]), 'gv')
    plt.show()


if __name__ == '__main__':
    target_day = datetime.strptime('2017/10/16', '%Y/%m/%d')
    target_day_min = get_today_min('300094', target_day)

    result, day_end_result = backtest_grid_on_one_day('300094', '2017/10/16', 6.85, 0.02, 100000, 10000, 6.5, 7.8)
    transactions = []

    for i in range(len(result['order_status'])):
        if result['order_status'][i] == OrderStatus.SUCCESS:
            transactions.append({'action': result['action'][i], 'datetime': result['action_datetime'][i]})

    plot_grid(transactions, target_day_min, 6.85, 0.02, 6.8, 7.03)

