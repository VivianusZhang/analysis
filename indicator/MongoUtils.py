import functools

import numpy as np
import pymongo
from  pymongo import MongoClient
import pandas as pd

client = MongoClient('localhost', 27017)
db = client['stock']


def find_by_code_on_or_before(code, date, period):
    data = list(db.instrumentDailyData.find(
        {'code': code, 'date': {'$lte': date}}).sort('date', pymongo.DESCENDING).limit(period))

    return pd.DataFrame(data)


def find_close_on_or_before(self, code, date, period):
    return self.find_data_on_or_before(code, date, period)['close']


def find_instrument_list():
    return list(db.instrument.find({}, {'_id': 0, 'code': 1}))
