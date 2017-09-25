import functools

import numpy as np
import pandas as pd
import pymongo
import talib
from  pymongo import MongoClient

from importdata.indicator import label
from importdata.indicator import momentum
from importdata.indicator import overlap

client = MongoClient('localhost', 27017)
db = client['stock']


def compute_indicators():
    for value in db.instrumentDailyData.distinct('code'):

        data = list(db.instrumentDailyData.find({'code': value}, {'_id': 0, 'amount': 0, 'label': 0}).sort('date',
                                                                                                           pymongo.ASCENDING))
        #ignore IPO
        if len(data) < 50:
            continue

        if db.ratio.find({'code': value}).count() > 0:
            continue

        print('------starting-----------' + value)

        feed = functools.reduce(lambda x, y: {key: np.append(x[key], [y[key]]) for key in x}, data,
                                {'close': np.array([]), 'high': np.array([]), 'low': np.array([]), 'open': np.array([]),
                                 'volume': np.array([])})

        for value in data:
            value['ratio_open'] = value['close'] - value['open']
            value['ratio_high'] = value['close'] - value['high']
            value['ratio_low'] = value['close'] - value['low']

        ret = pd.DataFrame(data)

        close_ma = overlap.compute_ma_indicator(feed['close'], False)
        close_ma.rename(columns=dict(zip(close_ma.columns, map(lambda x: 'close_' + x, close_ma.columns))),
                        inplace=True)

        bb = overlap.compute_bb(feed['close'], False)
        performance = momentum.compute_performance(feed['close'], False)
        rsi = momentum.compute_rsi(feed['close'], False)
        di = momentum.compute_di(feed['high'], feed['low'], feed['close'], feed['volume'])
        ret['obv'] = talib.OBV(feed['close'], feed['volume'])
        ret[bb.columns.values] = bb
        ret[close_ma.columns.values] = close_ma
        ret[performance.columns.values] = performance
        ret[rsi.columns.values] = rsi
        ret[di.columns.values] = di
        ret['cycle'] = talib.HT_DCPERIOD(feed['close'])
        ret['label'] = label.compute_label(data)

        if db.ratio.find({'code': value}).count() == 0:
            db.ratio.insert_many(ret.to_dict('records'))

if __name__ == '__main__':
    compute_indicators()