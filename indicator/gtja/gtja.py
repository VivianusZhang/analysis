import talib

from indicator.MongoUtils import *


def gtja_110(code, date):
    """UM(MAX(0,HIGH-DELAY(CLOSE,1)),20)/SUM(MAX(0,DELAY(CLOSE,1)-LOW),20)*100"""
    data = MongoUtils.find_data_on_or_before(code, date, 21)
    sum1 = sum2 = 0

    for i in range(19):
        sum1 = sum1 + max(0, data['high'][i] - data['close'][i + 1])

    for i in range(19):
        sum2 = sum2 + max(0, data['close'][i + 1] - data['low'][i])

    return sum1 / sum2 * 100


def gtja_9(code, date):
    """SMA(((HIGH+LOW)/2-(DELAY(HIGH,1)+DELAY(LOW,1))/2)*(HIGH-LOW)/VOLUME,7,2)"""
    feed = []
    data = MongoUtils.find_data_on_or_before(code, date, 8)

    for i in range(6):
        feed.append(
            ((data['high'][i] + data['low'][i]) / 2 - (data['high'][i + 1] + data['low'][i + 1]) / 2) *
            (data['high'][i] - data['low'][i]) / data['volume'][i])

    return talib.EMA(feed)


def gtja_2(code, date):
    """(-1 * DELTA((((CLOSE - LOW) - (HIGH - CLOSE)) / (HIGH - LOW)), 1))"""
    data = MongoUtils.find_data_on_or_before(code, date, 2)

    i = 1
    ret = ((data['close'][i] - data['low'][i]) - (data['high'][i] - data['close'][i])) / (
        data['high'][i] - data['low'][i])

    i = 0
    ret = ret - ((data['close'][i] - data['low'][i]) - (data['high'][i] - data['close'][i])) / (
        data['high'][i] - data['low'][i])

    return ret


def gtja_97(code, date):
    """STD(VOLUME,10)"""
    data = MongoUtils.find_data_on_or_before(code, date, 10)
    return np.std(data['volume'])
