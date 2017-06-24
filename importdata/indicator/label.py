import pandas as pd

#add label; up:1, down:-1
def compute_label(data):
    label = []
    dailyData = pd.DataFrame(data)
    for index in range(len(dailyData.index) - 1):
        if dailyData.iloc[index + 1]['close'] > dailyData.iloc[index]['close']:
            label.append(1)
        else:
            label.append(-1)

    label.append(0)
    return label

def compute_signal(source, indicator):
    signal = [0]
    for i in range(len(source)) - 1:
        if source[i + 1] > indicator[i + 1] & source[i] < indicator[i]:
            signal.append(1)
        elif source[i + 1] < indicator[i + 1] & source[i] > indicator[i]:
            signal.append(-1)
        else:
            signal.append(0)

    return signal