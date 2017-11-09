import pandas as pd
import pymongo
from  pymongo import MongoClient

#client = MongoClient('localhost', 27017)
client = MongoClient('119.23.219.217', 27017)
db = client['stock']


def find_by_code_on_and_before(code, date, period=1):
    data = list(db.instrumentDailyData.find(
        {'code': code, 'datetime': {'$lte': date}}).sort('datetime', pymongo.DESCENDING).limit(period))

    return pd.DataFrame(data)


def find_all_on_and_before(date, period):
    data = list(db.instrumentDailyData.find(
        {'datetime': {'$lte': date}}).sort('datetime', pymongo.DESCENDING).limit(period))

    return pd.DataFrame(data)


def find_by_code_on_and_after(code, date):
    data = list(db.instrumentDailyData.find(
        {'code': code, 'datetime': {'$gte': date}}).sort('datetime', pymongo.ASCENDING))
    return pd.DataFrame(data)


def get_instruments():
    return pd.DataFrame(list(db.instrument.find({})))


def find_instrument_list():
    return list(db.instrument.find({}, {'_id': 0, 'code': 1}))


def find_instument_by_industry(industry):
    return pd.DataFrame(list(db.instrument.find({'industry': industry})))


def find_close_on_or_before(self, code, date, period):
    return self.find_data_on_or_before(code, date, period)['close']


def find_by_code_between(code, start_date, end_date):
    data = list(db.instrumentDailyData.find(
        {'code': code, 'datetime': {'$gte': start_date, '$lte': end_date}}).sort('datetime', pymongo.ASCENDING))

    return pd.DataFrame(data)


def find_by_code_list_between(code_list, start_date, end_date):
    data = list(db.instrumentDailyData.find(
        {'code': {'$in': code_list}, 'datetime': {'$gte': start_date, '$lte': end_date}}).sort('datetime',
                                                                                               pymongo.ASCENDING))

    return pd.DataFrame(data)


def find_raito_by_code_list_between(code_list, start_date, end_date):
    data = list(db.ratio.find(
        {'code': {'$in': code_list}, 'datetime': {'$gte': start_date, '$lte': end_date}}).sort('datetime',
                                                                                               pymongo.ASCENDING))

    return pd.DataFrame(data)


def find_by_code_between_min(code, start_datetime, end_datetime):
    data = list(db.instrumentHourData.find(
        {'code': code, 'datetime': {'$gte': start_datetime, '$lte': end_datetime}}).sort('datetime', pymongo.ASCENDING))

    return pd.DataFrame(data)


def get_today_min(code, date):
    day_end = date.replace(hour=23)
    data = list(db.instrumentHourData.find(
        {'code': code, 'datetime': {'$gte': date, '$lte': day_end}}).sort('datetime', pymongo.ASCENDING))
    return pd.DataFrame(data)
