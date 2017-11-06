import pandas as pd
import pymongo
from datetime import datetime
from  pymongo import MongoClient

client = MongoClient('localhost', 27017)
db = client['stock']


def find_by_code_on_or_before(code, date, period=1):
    data = list(db.instrumentDailyData.find(
        {'code': code, 'date': {'$lte': date}}).sort('date', pymongo.DESCENDING).limit(period))

    return pd.DataFrame(data)


def find_all_on_or_before(date, period):
    data = list(db.instrumentDailyData.find(
        {'date': {'$lte': date}}).sort('date', pymongo.DESCENDING).limit(period))

    return pd.DataFrame(data)


def get_instruments():
    return pd.DataFrame(list(db.instrument.find({})))


def find_close_on_or_before(self, code, date, period):
    return self.find_data_on_or_before(code, date, period)['close']


def find_by_code_between(code, start_date, end_date):
    data = list(db.instrumentDailyData.find(
        {'code': code, 'datetime': {'gte': start_date, '$lte': end_date}}).sort('datetime', pymongo.DESCENDING))

    return data


def get_today_min(code, date):
    start_time = datetime.strptime(date, '%Y/%m/%d')
    end_time = datetime.strptime(date, '%Y/%m/%d').replace(hour=23)

    return list(db.instrumentHourData.find(
        {'code': code}, {'_id': 0}, {'datetime': {'$gte': start_time, '$lte': end_time}}).sort('datetime',
                                                                                               pymongo.ASCENDING))
