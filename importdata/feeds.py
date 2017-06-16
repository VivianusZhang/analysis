import tushare as ts
from  pymongo import MongoClient

client = MongoClient('localhost', 27017)
db = client['stock']

cursor = db.instrument.find({})
for document in cursor:
    code = document['code']

    if db.ml.find({'code': code}).count() == 0:
        try:
            print('downloading : ' + code)
            dailyData = ts.get_h_data(code)
            dailyData['code'] = code

            x = dailyData.as_matrix(columns=dailyData.columns[0:5])
            label = []
            for index in range(len(dailyData.index) - 1):
                if dailyData.iloc[index]['close'] < dailyData.iloc[index + 1]['close']:
                    label.append(0)
                else:
                    label.append(1)

            label.append(-1)
            dailyData['label'] = label
            dailyData['date'] = dailyData.index
            db.feed.insert_many(dailyData.to_dict('records'))
        except Exception:
            continue

print('end of import instrument data')
