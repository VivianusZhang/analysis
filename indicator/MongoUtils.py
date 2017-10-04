import functools

import numpy as np
import pymongo
from  pymongo import MongoClient

client = MongoClient('localhost', 27017)
db = client['stock']


class MongoUtils:
    @staticmethod
    def find_data_on_or_before(code, date, period):
        data = list(db.instrumentDailyData.find(
            {'code': code, 'date': {'$lte': date}}).sort('date', pymongo.DESCENDING).limit(period))

        feed = functools.reduce(lambda x, y: {key: np.append(x[key], [y[key]]) for key in x}, data,
                                {'close': np.array([]), 'high': np.array([]), 'low': np.array([]), 'open': np.array([]),
                                 'volume': np.array([])})

        return feed

    @staticmethod
    def find_close_on_or_before(self, code, date, period):
        return self.find_data_on_or_before(code, date, period)['close']

    @staticmethod
    def find_instrument_list():
        return list(db.instrument.find({}, {'_id': 0, 'code': 1}))
