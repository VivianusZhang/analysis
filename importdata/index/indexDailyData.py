from  pymongo import MongoClient
from indicator import overlap
from indicator import momentum
from indicator import label
import pandas as pd
import json
import os
import dateutil.parser
import numpy as np

client = MongoClient()
client = MongoClient('localhost', 27017)
db = client['stock']

def import_content(filename):

    save_dir = os.getcwd()
    filepath = os.path.join(save_dir, filename+ '.csv')
    data = pd.read_csv(filepath)
    data['code'] = filename
    data = json.loads(data.to_json(orient='records'))

    for each in data:
        each['date'] = dateutil.parser.parse(each['date'])
    data = sorted(data, key=lambda x: x['date'])

    data = compute_indicator(data)
    db.index.insert(data.to_dict('records'))

def compute_indicator(data):
    feed = reduce(lambda x, y: {key: np.append(x[key], [y[key]]) for key in x}, data,
                  {'close': np.array([]), 'high': np.array([]), 'low': np.array([]), 'open': np.array([]),
                   'volume': np.array([])})

    close_ma = overlap.compute_ma_indicator(feed['close'])
    close_ma.rename(columns=dict(zip(close_ma.columns, map(lambda x: 'close_' + x, close_ma.columns))), inplace=True)
    performance = momentum.compute_performance(feed['close'])

    ret = pd.DataFrame(data)

    ret['label'] = label.compute_label(ret)
    ret[close_ma.columns.values] = close_ma
    ret[performance.columns.values] = performance
    return ret;

#000001:上证指数，所有股票之和
#399300: 沪深300
#399301: 深圳成指
if __name__ == "__main__":
  filepath = '399300'
  import_content(filepath)