import numpy as np
import pandas as pd


# add label; up:1, down:-1
def compute_label(data):
    label = []
    dailyData = pd.DataFrame(data)
    for index in range(len(dailyData.index) - 5):
        if dailyData.iloc[index + 5]['close'] > dailyData.iloc[index]['close']:
            label.append(1)
        else:
            label.append(0)

    label.append(-1)
    label.append(-1)
    label.append(-1)
    label.append(-1)
    label.append(-1)
    return label


def compute_signal_ma(source, indicator):
    signal = []
    i = 1
    for i in range(len(source)):
        if i == 0:
            signal.append(0)
        else:
            if source[i] > indicator[i] and source[i - 1] < indicator[i - 1]:
                signal.append(1)
            elif source[i] < indicator[i] and source[i - 1] > indicator[i - 1]:
                signal.append(-1)
            else:
                signal.append(0)

    return np.asarray(signal)
