from talib.abstract import *
import pandas as pd

def compute_bb(data):
    upperband, middleband, lowerband = BBANDS(data, timeperiod=22, nbdevup=2, nbdevdn=2, matype=0)
    return pd.DataFrame({'upperband': upperband, 'middleband': middleband, 'lowerband': lowerband}).to_dict(orient='records')


