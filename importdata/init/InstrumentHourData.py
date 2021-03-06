import pymongo
import tushare as ts
from  pymongo import MongoClient

client = MongoClient('localhost', 27017)
db = client['stock']

cons = ts.get_apis()

db.instrumentHourData.create_index([('code', pymongo.ASCENDING)])


def batch():
    cursor = db.instrument.find({})
    for document in cursor:
        code = document['code']

        if db.instrumentDailyData.find({'code': code}).count() == 0:
            try:
                print('downloading : ' + code)
                hourlyData = ts.bar(code, conn=cons, freq='1min', start_date='2017-05-01', end_date='2017/10/31')
                hourlyData['code'] = code
                hourlyData['volume'] = hourlyData['vol']
                hourlyData.drop('vol', 1, inplace=True)
                hourlyData['datetime'] = hourlyData.index
                db.instrumentHourData.insert_many(hourlyData.to_dict('records'))
            except Exception:
                continue

    print('end of import instrument')

def one(code):
    print('downloading : ' + code)
    hourlyData = ts.bar(code, conn=cons, freq='1min', start_date='2017-05-01', end_date='2017/10/31')
    hourlyData['code'] = code
    hourlyData['volume'] = hourlyData['vol']
    hourlyData.drop('vol', 1, inplace=True)
    hourlyData['datetime'] = hourlyData.index
    db.instrumentHourData.insert_many(hourlyData.to_dict('records'))
    print('end of import instrument')

if __name__ == '__main__':
    batch()