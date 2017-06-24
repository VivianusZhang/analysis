import time
from datetime import datetime

import tushare as ts
from  pymongo import MongoClient

client = MongoClient()
client = MongoClient('localhost', 27017)
db = client['stock']


ts.get_index()

cursor = db.instrument.find({})
for document in cursor:
    code = document['code']
    print('downloading : ' + code)
    dailyData = ts.get_k_data(code, '2000-01-01', time.strftime("%Y-%m-%d"))

    if not dailyData.empty:
        dailyData_dict = dailyData.to_dict('records');
        for i in range(len(dailyData_dict)):
            dailyData_dict[i]['date'] = datetime.strptime(dailyData_dict[i]['date'].encode('ascii', 'ignore'),'%Y-%m-%d')

        db.instrumentDailyData.insert_many(dailyData_dict)

print('end of import instrument index')
