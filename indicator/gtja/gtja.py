import numpy as np
import pandas as pd
import talib

from utils.MongoUtils import get_instruments, find_by_code_on_and_before


def gtja_110(code, date):
    """UM(MAX(0,HIGH-DELAY(CLOSE,1)),20)/SUM(MAX(0,DELAY(CLOSE,1)-LOW),20)*100"""
    data = find_by_code_on_and_before(code, date, 21)
    sum1 = sum2 = 0

    for i in range(19):
        sum1 = sum1 + max(0, data.high[i] - data.close[i + 1])

    for i in range(19):
        sum2 = sum2 + max(0, data.close[i + 1] - data.low[i])

    return sum1 / sum2 * 100


def gtja_9(code, date):
    """SMA(((HIGH+LOW)/2-(DELAY(HIGH,1)+DELAY(LOW,1))/2)*(HIGH-LOW)/VOLUME,7,2)"""
    feed = []
    data = find_by_code_on_and_before(code, date, 8)

    for i in range(7):
        feed.append(
            ((data.high[i] + data.low[i]) / 2 - (data.high[i + 1] + data.low[i + 1]) / 2) *
            (data.high[i] - data.low[i]) / data.volume[i])

    return talib.EMA(np.array(feed), timeperiod=7)[-1]


def gtja_2(code, date):
    """(-1 * DELTA((((CLOSE - LOW) - (HIGH - CLOSE)) / (HIGH - LOW)), 1))"""
    data = find_by_code_on_and_before(code, date, 2)

    i = 1
    ret = ((data.close[i] - data.low[i]) - (data.high[i] - data.close[i])) / (
        data.high[i] - data.low[i])

    i = 0
    ret = ret - ((data.close[i] - data.low[i]) - (data.high[i] - data.close[i])) / (
        data.high[i] - data.low[i])

    return ret


def gtja_97(code, date):
    """STD(VOLUME,10)"""
    data = find_by_code_on_and_before(code, date, 10)
    return np.std(data['volume'])


def gtja_68(code, date):
    """SMA(((HIGH+LOW)/2-(DELAY(HIGH,1)+DELAY(LOW,1))/2)*(HIGH-LOW)/VOLUME,15,2)"""
    data = find_by_code_on_and_before(code, date, 16)

    feed = []
    for i in range(15):
        feed.append(
            ((data.high[i] + data.low[i]) / 2 - (data.high[i + 1] + data.low[i + 1]) / 2) * (
                data.high[i] - data.low[i]) /
            data.volume[i]
        )

    return talib.EMA(np.array(feed), timeperiod=15)[-1]


def gtja_31(code, date):
    """(CLOSE-MEAN(CLOSE,12))/MEAN(CLOSE,12)*100"""
    data = find_by_code_on_and_before(code, date, 12)
    close_mean = np.mean(np.array(data.close))
    return (data.close[0] - close_mean) / close_mean


def gtja_29(code, date):
    """(CLOSE-DELAY(CLOSE,6))/DELAY(CLOSE,6)*VOLUME"""
    data = find_by_code_on_and_before(code, date, 6)
    return (data.close[0] - data.close[5]) / data.close[5] * data.volume[0]


def gtja_80(code, date):
    """(VOLUME-DELAY(VOLUME,5))/DELAY(VOLUME,5)*100"""
    data = find_by_code_on_and_before(code, date, 5)
    return (data.close[0] - data.close[4]) / data.close[4] * data.volume[0]


def gtja_60(code, date):
    """SUM(((CLOSE-LOW)-(HIGH-CLOSE))/(HIGH-LOW)*VOLUME,20)"""
    data = find_by_code_on_and_before(code, date, 20)
    sum = 0
    for i in range(20):
        sum = sum + ((data.close[i] - data.low[i]) - (data.high[i] - data.close[i])) / (
            (data.high[i] - data.low[i]) * data.volume[i])

    return sum


def gtja_71(code, date):
    """(CLOSE-MEAN(CLOSE,24))/MEAN(CLOSE,24)*100"""
    data = find_by_code_on_and_before(code, date, 24)
    close_mean = np.mean(np.array(data.close))
    return (data.close[0] - close_mean) / close_mean


# TODO:
def gtja_26(code, date):
    """((((SUM(CLOSE, 7) / 7) - CLOSE)) + ((CORR(VWAP, DELAY(CLOSE, 5), 230))))"""
    data = find_by_code_on_and_before(code, date, 230)


def gtja_34(code, date):
    """MEAN(CLOSE,12)/CLOSE"""
    data = find_by_code_on_and_before(code, date, 12)
    return np.mean(np.array(data.close)) / data.close[0]


def gtja_57(code, date):
    """SMA((CLOSE-TSMIN(LOW,9))/(TSMAX(HIGH,9)-TSMIN(LOW,9))*100,3,1)"""
    data = find_by_code_on_and_before(code, date, 11)

    feed = []
    for i in range(3):
        feed.append(
            (data.close[0] - pd.Series.min(data.low[i:i + 9])) / (
                pd.Series.max(data.high[i:i + 9]) - pd.Series.min(data.low[i:i + 9]))
        )

    return talib.SMA(np.array(feed), timeperiod=3)[-1]


def gtja_88(code, date):
    """(CLOSE-DELAY(CLOSE,20))/DELAY(CLOSE,20)*100"""
    data = find_by_code_on_and_before(code, date, 20)
    return (data.close[0] - data.close.iloc[-1]) / data.close.iloc[-1] * 100


def gtja_14(code, date):
    """CLOSE-DELAY(CLOSE,5)"""
    data = find_by_code_on_and_before(code, date, 5)
    return (data.close[0] - data.close.iloc[-1]) / data.close.iloc[-1] * 100


def gtja_81(code, date):
    """SMA(VOLUME,21,2)"""
    data = find_by_code_on_and_before(code, date, 21)
    return talib.EMA(np.array(data.volume), timeperiod=21)[-1]


def gtja_18(code, date):
    """CLOSE/DELAY(CLOSE,5)"""
    data = find_by_code_on_and_before(code, date, 5)
    return data.close[0] / data.close.iloc[-1]


def gtja_95(code, date):
    """STD(AMOUNT,20)"""
    data = find_by_code_on_and_before(code, date, 20)
    return pd.Series.std(data.amount)


def gtja_11(code, date):
    """SUM(((CLOSE-LOW)-(HIGH-CLOSE))/(HIGH-LOW)*VOLUME,6)"""
    data = find_by_code_on_and_before(code, date, 6)
    ret = 0
    for i in range(6):
        ret = ret + ((data.close[i] - data.low[i]) - (data.high[i] - data.close[i])) / (
            (data.high[i] - data.low[i]) * data.volume[i])

    return ret


def gtja_78(code, date):
    """((HIGH+LOW+CLOSE)/3-MA((HIGH+LOW+CLOSE)/3,12))/(0.015*MEAN(ABS(CLOSE-MEAN((HIGH+LOW+CLOSE)/3,12)),12))"""

    def _helper_get_average(data_average):
        return (data_average.high + data_average.low + data_average.close) / 3

    def _helper_get_array(data_array):
        ret_array = []

        for helper_i in range(12):
            _helper_get_average(data.iloc[helper_i])
            ret_array.append(
                (data_array.high.iloc[helper_i] + data_array.low.iloc[helper_i] + data_array.close.iloc[helper_i]) / 3)

        return np.array(ret_array)

    data = find_by_code_on_and_before(code, date, 24)
    feed = []
    for i in range(12):
        data_array_input = data[i:i + 12]
        feed.append(abs(data_array_input.close.iloc[0] - np.mean(_helper_get_array(data_array_input))))

    return (_helper_get_average(data.iloc[0]) - talib.SMA(_helper_get_array(data[0:12]), timeperiod=12)[-1]) / (
        0.015 * np.mean(np.array(feed)))


def gtja_70(code, date):
    """STD(AMOUNT,6)"""
    data = find_by_code_on_and_before(code, date, 6)
    return pd.Series.std(data.amount)


def gtja_82(code, date):
    """SMA((TSMAX(HIGH,6)-CLOSE)/(TSMAX(HIGH,6)-TSMIN(LOW,6))*100,20,1)"""
    data = find_by_code_on_and_before(code, date, 26)

    feed = []
    for i in range(20):
        feed.append((pd.Series.min(data.high[i:i + 6]) - data.close.iloc[i]) / (
            pd.Series.max(data.high[i:i + 6]) - pd.Series.min(data.low[i:i + 6])) * 100)

    return talib.SMA(np.array(feed), timeperiod=20)[-1]


def gtja_96(code, date):
    """SMA(SMA((CLOSE-TSMIN(LOW,9))/(TSMAX(HIGH,9)-TSMIN(LOW,9))*100,3,1),3,1)"""

    def _helper(helper_data):
        helper_feed = []
        for helper_i in range(3):
            _ = helper_data[helper_i:helper_i + 9]
            helper_feed.append(
                ((_.close.iloc[0] - pd.Series.min(_.low)) / (pd.Series.max(_.high) - pd.Series.min(_.low))) * 100)
        return helper_feed

    data = find_by_code_on_and_before(code, date, 14)

    feed = []
    for i in range(3):
        feed.append(talib.SMA(np.array(_helper(data[i:i + 3])), timeperiod=3)[-1])

    return talib.SMA(np.array(feed), timeperiod=3)[-1]


def gtja_20(code, date):
    """(CLOSE-DELAY(CLOSE,6))/DELAY(CLOSE,6)*100"""
    data = find_by_code_on_and_before(code, date, 6)
    return (data.close[0] - data.close.iloc[-1]) / data.close.iloc[-1] * 100


# TODO:
def gtja_13(code, date):
    """(((HIGH * LOW)^0.5) - VWAP)"""


def gtja_46(code, date):
    """(MEAN(CLOSE,3)+MEAN(CLOSE,6)+MEAN(CLOSE,12)+MEAN(CLOSE,24))/(4*CLOSE)"""
    data = find_by_code_on_and_before(code, date, 24)
    return (pd.Series.mean(data.close[0:3])
            + pd.Series.mean(data.close[0:6])
            + pd.Series.mean(data.close[0:12])
            + pd.Series.mean(data.close[0:24])) / (4 * data.close.iloc[0])


def gtja_24(code, date):
    """SMA(CLOSE-DELAY(CLOSE,5),5,1)"""
    data = find_by_code_on_and_before(code, date, 10)
    feed = []
    for i in range(5):
        feed.append(data.close[i] - data.close[i + 5])

    return talib.SMA(np.array(feed), timeperiod=5)[-1]


def gtja_109(code, date):
    """SMA(HIGH-LOW,10,2)/SMA(SMA(HIGH-LOW,10,2),10,2)"""

    def helper(helper_data):
        helper_feed = []
        for helper_i in range(10):
            helper_feed.append(helper_data.high.iloc[helper_i] - helper_data.low.iloc[helper_i])
        return talib.EMA(np.array(helper_feed), timeperiod=10)[-1]

    data = find_by_code_on_and_before(code, date, 20)
    feed = []
    for i in range(10):
        feed.append(helper(data[i:i + 10]))
    return helper(data[0:10]) / talib.EMA(np.array(feed), timeperiod=10)[-1]


def gtja_158(code, date):
    """((HIGH-SMA(CLOSE,15,2))-(LOW-SMA(CLOSE,15,2)))/CLOSE"""
    data = find_by_code_on_and_before(code, date, 15)
    ema = talib.EMA(np.array(data.close), timeperiod=15)[-1]
    return ((data.high[0] - ema) - (data.low[0] - ema)) / data.close[0]


def gtja_126(code, date):
    """(CLOSE+HIGH+LOW)/3"""
    data = find_by_code_on_and_before(code, date, 1)
    return (data.close[0] + data.high[0] + data.low[0]) / 3


def gtja_100(code, date):
    """STD(VOLUME,20)"""
    data = find_by_code_on_and_before(code, date, 20)
    return pd.Series.std(data.volume)


# TODO:
def gtja_146(code, date):
    """MEAN((CLOSE-DELAY(CLOSE,1))/DELAY(CLOSE,1)-SMA((CLOSE-DELAY(CLOSE,1))/DELAY(CLOSE,1),61,2),20)*((
    CLOSE-DELAY(CLOSE,1))/DELAY(CLOSE,1)-SMA((CLOSE-DELAY(CLOSE,1))/DELAY(CLOSE,1),61,2))/SMA(((CLOS
    E-DELAY(CLOSE,1))/DELAY(CLOSE,1)-((CLOSE-DELAY(CLOSE,1))/DELAY(CLOSE,1)-SMA((CLOSE-DELAY(CLOSE,
    1))/DELAY(CLOSE,1),61,2)))^2,60)"""


def gtja_153(code, date):
    """(MEAN(CLOSE,3)+MEAN(CLOSE,6)+MEAN(CLOSE,12)+MEAN(CLOSE,24))/4"""
    data = find_by_code_on_and_before(code, date, 24)
    return (pd.Series.mean(data.close[0:3])
            + pd.Series.mean(data.close[0:6])
            + pd.Series.mean(data.close[0:12])
            + pd.Series.mean(data.close[0:24])) / 4


# TODO:
def gtja_8(code, date):
    """RANK(DELTA(((((HIGH + LOW) / 2) * 0.2) + (VWAP * 0.8)), 4) * -1)"""


# TODO:
def gtja_6(code, date):
    """(RANK(SIGN(DELTA((((OPEN * 0.85) + (HIGH * 0.15))), 4)))* -1)"""
    instruments = get_instruments()
    for row in instruments.iterrows():
        data = find_by_code_on_and_before(row.code, date, 4)
        delta = (data.open[0] * 0.85 + data.high[0] * 0.15) - (data.open[-1] * 0.85 + data.high[-1] * 0.15)


def gtja_139(code, date):
    """(-1 * CORR(OPEN, VOLUME, 10))"""
    data = find_by_code_on_and_before(code, date, 10)
    return -1 * data.open.corr(data.volume)


def gtja_106(code, date):
    """CLOSE-DELAY(CLOSE,20)"""
    data = find_by_code_on_and_before(code, date, 10)
    return data.close[0] - data.close.iloc[-1]


def gtja_178(code, date):
    """(CLOSE-DELAY(CLOSE,1))/DELAY(CLOSE,1)*VOLUME"""
    data = find_by_code_on_and_before(code, date, 2)
    return (data.close[0] - data.close.iloc[-1]) / data.close.iloc[-1] * data.volume[0]


def gtja_134(code, date):
    """(CLOSE-DELAY(CLOSE,12))/DELAY(CLOSE,12)*VOLUME"""
    data = find_by_code_on_and_before(code, date, 12)
    return (data.close[0] - data.close.iloc[-1]) / data.close.iloc[-1] * data.volume[0]


def gtja_188(code, date):
    """(HIGH-LOW-SMA(HIGH-LOW,11,2))/SMA(HIGH-LOW,11,2)*100"""
    data = find_by_code_on_and_before(code, date, 11)
    feed = []
    for i in range(11):
        feed.append(data.high[i] - data.low[i])
    ema = talib.EMA(np.array(feed), timeperiod=11)[-1]
    return (data.high[0] - data.low[0] - ema) / ema * 100


def gtja_189(code, date):
    """MEAN(ABS(CLOSE-MEAN(CLOSE,6)),6)"""
    data = find_by_code_on_and_before(code, date, 12)
    feed = []
    for i in range(6):
        feed.append(abs(data.close[0] - pd.Series.mean(data.close)))
    return np.mean(np.array(feed))


def gtja_171(code, date):
    """((-1 * ((LOW - CLOSE) * (OPEN^5))) / ((CLOSE - HIGH) * (CLOSE^5)))"""
    data = find_by_code_on_and_before(code, date)
    return ((data.low[0] - data.close[0]) * pow(data.open[0], 5)) / (
        (data.close[0] - data.high[0]) * pow(data.close[0], 5))


def gtja_132(code, date):
    """MEAN(AMOUNT,20)"""
    data = find_by_code_on_and_before(code, date, 20)
    return pd.Series.mean(data.amount)
