import talib
import pandas as pd

def compute_cycte(data):
    ht_dcperiod = talib.HT_DCPERIOD(data)
    return pd.DataFrame({'ht_dcperiod': ht_dcperiod}).to_dict(orient='records')