from talib.abstract import *
import pandas as pd

def compute_ma_indicator(data):
    sma5 = SMA(data, timeperiod=5)
    sma15 = SMA(data, timeperiod=15)
    sma30 = SMA(data, timeperiod=30)
    sma60 = SMA(data, timeperiod=60)
    sma90 = SMA(data, timeperiod=90)
    sma120 = SMA(data, timeperiod=120)
    ema5 = EMA(data, timeperiod=5)
    ema15 = EMA(data, timeperiod=15)
    ema30 = EMA(data, timeperiod=30)
    dema15 = DEMA(data, timeperiod=15)
    dema30 = DEMA(data, timeperiod=30)
    tema = TEMA(data, timeperiod=22)
    # If the price moves back and forth (range), the TMA won't react as much, thus letting you know the trend hasn't shifted
    tma = TRIMA(data, timeperiod=22)
    return pd.DataFrame({'sma5': sma5, 'sma15':sma15, 'sma30':sma30, 'sma60':sma60,
                  'sma90':sma90, 'sma120': sma120, 'ema5': ema5, 'ema15': ema15,
                  'ema30': ema30, 'dema15': dema15, 'dema30': dema30,'tema': tema, 'tma': tma}).to_dict(orient='records')

# http://www.mesasoftware.com/papers/MAMA.pdf
def compute_mama(data):
    mama, fama = MAMA(data, fastlimit=0.5, slowlimit=0.05)
    return pd.DataFrame({'mama':mama, 'fama': fama}).to_dict(orient='records')

#http://stockcharts.com/school/doku.php?id=chart_school:technical_indicators:kaufman_s_adaptive_moving_average
#https://www.backtrader.com/blog/posts/2016-07-26-talib-integration/talib-integration.html
#TODO: may need to implement by ourself
def compute_kama(data):
    kama = KAMA(data, timeperiod=30)
    return pd.DataFrame({'kama': kama}).to_dict(orient='records')

#TODO: http://www.mesasoftware.com/papers/FRAMA.pdf