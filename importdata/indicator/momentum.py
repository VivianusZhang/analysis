import pandas as pd
import talib


def compute_macd(data):
    macd, macdsignal, macdhist = talib.MACD(data, fastperiod=12, slowperiod=26, signalperiod=9)
    return pd.DataFrame({'macd': macd, 'macdsignal': macdsignal, 'macdhist': macdhist})


def compute_rsi(data, signal=True):
    rsi = talib.RSI(data, timeperiod=14)

    if signal:
        signal = []
        # >70: sell, down signal;<30: buy, up signal
        for value in rsi:
            if value > 90:
                signal.append(-2)
            elif value > 70:
                signal.append(-1)
            elif value < 30:
                signal.append(1)
            elif value < 10:
                signal.append(2)
            else:
                signal.append(0)
        return pd.DataFrame({'rsi_signal': signal, 'rsi': rsi})
    else:
        return pd.DataFrame({'rsi': rsi})


def compute_performance(data, signal=True):
    min, max = talib.MINMAX(data, timeperiod=30)
    std = talib.STDDEV(data, timeperiod=5, nbdev=1)
    roc1 = talib.ROCP(data, timeperiod=1)
    roc2 = talib.ROCP(data, timeperiod=2)
    roc3 = talib.ROCP(data, timeperiod=3)
    roc5 = talib.ROCP(data, timeperiod=5)
    roc10 = talib.ROCP(data, timeperiod=10)

    if signal:
        return pd.DataFrame(
            {'min': data / min, 'max': data / max, 'std': std, 'roc1': roc1, 'roc2': roc2, 'roc3': roc3, 'roc5': roc5,
             'roc10': roc10})
    else:
        return pd.DataFrame({'min': min, 'max': max, 'std': std, 'roc1': roc1, 'roc2': roc2, 'roc3': roc3, 'roc5': roc5,
                             'roc10': roc10})


def compute_cmo(data, signal=True):
    cmo = talib.CMO(data, timeperiod=14)
    return pd.DataFrame({'cmo': cmo})


def compute_di(high, low, close, volume, signal=True):
    mfi = talib.MFI(high, low, close, volume, timeperiod=14)
    minus_di = talib.MINUS_DI(high, low, close, timeperiod=14)
    minus_dm = talib.MINUS_DM(high, low, timeperiod=14)
    plus_di = talib.PLUS_DI(high, low, close, timeperiod=14)
    plus_dm = talib.PLUS_DM(high, low, timeperiod=14)
    return pd.DataFrame(
        {'mfi': mfi, 'minus_di': minus_di, 'minus_dm': minus_dm, 'plus_di': plus_di, 'plus_dm': plus_dm})
