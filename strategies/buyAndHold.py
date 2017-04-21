import matplotlib.pyplot as plt
import pandas as pd
from datetime import datetime
from pymongo import MongoClient

client = MongoClient('localhost', 27017)
db = client['stock']


def compute(code):
    print(code)
    mongo = db.instrumentDailyData.find({'code': code})
    data = list(mongo)
    df = pd.DataFrame(data)
    if not df.empty:
        x = range(len(df))
        date_list=[i['date'].encode('ascii','ignore') for i in data]
        date_min = data[0]['date']
        date_max = data[-1]['date']
        datetime_min = datetime.strftime(date_min, '%Y-%m-%d')
        datetime_max = datetime.strftime(date_max, '%Y-%m-%d')
        plt.
        plt.xticks(x, set([i['date'].encode('ascii','ignore')[:7] for i in data]))
        plt.plot(x, df['close'])
        return plt


compute('603999').show()
