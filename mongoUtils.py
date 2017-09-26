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

class mongoUtils:

    def findCloseOnorBofore(self, code, date, number):
        data = list(db.instrumentDailyData.find(
            {'code': code}, {'date': {'$lte': date}}).sort('date',pymongo.ASCENDING)).limit(number)

        return self.__dailyDataToClose(data)



    @staticmethod
    def __dailyDataToClose(self, data):
        feed = functools.reduce(lambda x, y: {key: np.append(x[key], [y[key]]) for key in x}, data,
                         {'close': np.array([]), 'high': np.array([]), 'low': np.array([]), 'open': np.array([]),
                          'volume': np.array([])})

        return feed['close']