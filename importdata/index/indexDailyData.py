import functools
import time

import numpy as np
import pandas as pd
import pymongo
import tushare as ts
from importdata.indicator import label
from importdata.indicator import momentum
from pymongo import MongoClient

from indicator.talib import overlap

client = MongoClient()
client = MongoClient('localhost', 27017)
db = client['stock']


def import_tushare(code):
    dailyData = ts.get_h_data(code, start='2010-01-01', end=time.strftime("%Y-%m-%d"), index=True)
    dailyData['code'] = code

    x = dailyData.as_matrix(columns=dailyData.columns[0:5])

    dailyData['date'] = dailyData.index

    db.temp.insert_many(dailyData.to_dict('records'))
    dailyData = list(db.temp.find({'code': code}).sort('date', pymongo.ASCENDING))

    data = compute_indicator(dailyData)
    db.index.insert(data.to_dict('records'))


def compute_indicator(data):
    feed = functools.reduce(lambda x, y: {key: np.append(x[key], [y[key]]) for key in x}, data,
                            {'close': np.array([]), 'high': np.array([]), 'low': np.array([]), 'open': np.array([]),
                             'volume': np.array([])})

    close_ma = overlap.compute_ma_indicator(feed['close'], False)
    close_ma.rename(columns=dict(zip(close_ma.columns, map(lambda x: 'close_' + x, close_ma.columns))), inplace=True)
    performance = momentum.compute_performance(feed['close'], False)

    ret = pd.DataFrame(data)

    ret['label'] = label.compute_label(ret)
    ret[close_ma.columns.values] = close_ma
    ret[performance.columns.values] = performance
    return ret


if __name__ == "__main__":
    code = '000001'
    import_tushare(code)
