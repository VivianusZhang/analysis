import talib
import pandas as pd

def compute_ma_indicator(data, signal = True):
    sma5 = talib.SMA(data, timeperiod=5)
    sma15 = talib.SMA(data, timeperiod=15)
    sma30 = talib.SMA(data, timeperiod=30)
    sma60 = talib.SMA(data, timeperiod=60)
    sma90 = talib.SMA(data, timeperiod=90)
    sma120 = talib.SMA(data, timeperiod=120)
    ema5 = talib.EMA(data, timeperiod=5)
    ema15 = talib.EMA(data, timeperiod=15)
    ema30 = talib.EMA(data, timeperiod=30)
    dema15 = talib.DEMA(data, timeperiod=15)
    dema30 = talib.DEMA(data, timeperiod=30)
    tema = talib.TEMA(data, timeperiod=22)
    # If the price moves back and forth (range), the TMA won't react as much, thus letting you know the trend hasn't shifted
    tma = talib.TRIMA(data, timeperiod=22)

    if signal:
        return pd.DataFrame({'sma5': data/sma5, 'sma15':sma5/sma15, 'sma30':sma15/sma30, 'sma60':data/sma60,
                      'sma90':data/sma90, 'sma120': data/sma120, 'ema5': data/ema5, 'ema15': data/ema15,
                      'ema30': data/ema30, 'dema15': data/dema15, 'dema30': dema15/dema30,'tema': data/tema, 'tma': data/tma})
        #return pd.DataFrame({'sma5': data / sma5, 'sma15': data / sma15, 'sma30': data / sma30, 'sma60': data / sma60,
        #                     'sma90': data / sma90, 'sma120': data / sma120, 'ema5': data / ema5, 'ema15': data / ema15,
        #                     'ema30': data / ema30, 'dema15': data / dema15, 'dema30': dema15 / dema30, 'tema': data / tema,
        #                     'tma': data / tma})

    else:
        return pd.DataFrame({'sma5':sma5, 'sma15':sma15, 'sma30':sma30, 'sma60':sma60,
                      'sma90':sma90, 'sma120': sma120, 'ema5': ema5, 'ema15': ema15,
                      'ema30': ema30, 'dema15': dema15, 'dema30': dema30,'tema': tema, 'tma': tma})


# http://www.mesasoftware.com/papers/MAMA.pdf
def compute_mama(data):
    mama, fama = talib.MAMA(data, fastlimit=0.5, slowlimit=0.05)
    return pd.DataFrame({'mama':mama, 'fama': fama}).to_dict(orient='records')

#http://stockcharts.com/school/doku.php?id=chart_school:technical_indicators:kaufman_s_adaptive_moving_average
#https://www.backtrader.com/blog/posts/2016-07-26-talib-integration/talib-integration.html
#TODO: may need to implement by ourself
def compute_kama(data):
    kama = talib.KAMA(data, timeperiod=30)
    return pd.DataFrame({'kama': kama}).to_dict(orient='records')

def compute_bb(data, signal=True):
    upperband, middleband, lowerband = talib.BBANDS(data, timeperiod=22, nbdevup=2, nbdevdn=2, matype=0)
    if signal:
        return pd.DataFrame({'upperband': data/upperband, 'middleband': middleband, 'lowerband': data/lowerband})
    else:
        return pd.DataFrame({'upperband': upperband, 'middleband': middleband, 'lowerband':lowerband})




#TODO: http://www.mesasoftware.com/papers/FRAMA.pdf