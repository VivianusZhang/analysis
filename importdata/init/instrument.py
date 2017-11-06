import tushare as ts
from  pymongo import MongoClient

client = MongoClient('localhost', 27017)
db = client['stock']

instrument = ts.get_stock_basics()
instrument['code'] = instrument.index
db.instrument.insert_many(instrument.to_dict('records'))
