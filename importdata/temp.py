from datetime import datetime

from pymongo import MongoClient

from utils.MongoUtils import find_by_code_between


def find_fluctuate_sotck():
    client = MongoClient('localhost', 27017)
    db = client['stock']

    cursor = db.instrument.find({})
    for document in cursor:
        code = document['code']
        start_date = datetime.strptime('2017/09/01', '%Y/%m/%d')
        end_date = datetime.strptime('2017/10/31', '%Y/%m/%d')
        daily_data = find_by_code_between(code, start_date, end_date)

        counter = 0
        for i, row in daily_data.iterrows():
            if (row.high - row.low)/row.close > 0.03:
                counter = counter + 1

        if counter > 30:
            print ('code %s, times: %d' % (code, counter))


if __name__ == "__main__":
    find_fluctuate_sotck()
