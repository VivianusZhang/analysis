from datetime import datetime

import matplotlib.dates as mdates
import plotly.graph_objs as go
import plotly.plotly as py

from utils.MongoUtils import find_by_code_between_min

code = '002230'
start_date = datetime.strptime('2017/08/01', '%Y/%m/%d')
end_date = datetime.strptime('2017/10/31', '%Y/%m/%d')
df = find_by_code_between_min(code, start_date, end_date)

quotes = []
for index, (date, close) in enumerate(zip(df.datetime, df.close)):
    val = (mdates.date2num(date), close)
    quotes.append(val)
daily_quotes = [tuple([i] + list(quote[1:])) for i, quote in enumerate(quotes)]

data = [go.Scatter(x=[i[0] for i in daily_quotes], y=[i[1] for i in daily_quotes])]

layout = go.Layout(
    xaxis=dict(
        autotick=False,
        range=[mdates.num2date(quotes[index][0]).strftime('%b-%d-%H:%M') for index in range(0, len(daily_quotes), 30)]
    )
)

py.iplot(data)
