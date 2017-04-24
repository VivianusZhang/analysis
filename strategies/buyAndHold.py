from datetime import datetime

import matplotlib.dates as mdates
import matplotlib.pyplot as plt
import pandas as pd
from pymongo import MongoClient

client = MongoClient('localhost', 27017)
db = client['stock']

years = mdates.YearLocator()  # every year
months = mdates.MonthLocator()  # every month
yearsFmt = mdates.DateFormatter('%Y')


def compute(code):
    print(code)
    mongo = db.instrumentDailyData.find({'code': code})
    data = list(mongo)

    df = pd.DataFrame(data)
    if not df.empty:
        x = range(len(df))
        ax = plt.subplot()
        ax.plot(df.date, df.close)

    return plt


compute('603999').show()
