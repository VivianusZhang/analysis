import matplotlib as plt
import matplotlib.dates as mdates
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd


def plot_grid(data, base_price, step, lower_bound, upper_bound):
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

    #plt.show(block=False)
    plt.show()
