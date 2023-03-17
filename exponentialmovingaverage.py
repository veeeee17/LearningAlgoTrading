import statistics as stats
import pandas as pd
from pandas_datareader import data
import yfinance as yfin
import matplotlib.pyplot as plt

start_date = '2014-01-01'
end_date = '2018-01-01'
SRC_DATA_FILENAME = 'goog_data.pkl'

try:
    goog_data = pd.read_pickle(SRC_DATA_FILENAME)
except FileNotFoundError:
    yfin.pdr_override()
    goog_data = data.DataReader('GOOG', start_date, end_date)
    goog_data.to_pickle(SRC_DATA_FILENAME)

close = goog_data['Close']

num_periods = 20 # number of days on which to average
K = 2 / (num_periods + 1)
ema_p = 0
ema_values = [] # to hold the EMA values

for close_price in close:
    if (ema_p == 0): # first observation, EMA = current price
        ema_p = close_price
    else:
        ema_p = (close_price - ema_p) * K + ema_p

    ema_values.append(ema_p)

goog_data = goog_data.assign(ClosePrice=pd.Series(close, index=goog_data.index))
goog_data = goog_data.assign(Exponential20DayMovingAverage=pd.Series(ema_values, index=goog_data.index))
close_price = goog_data['ClosePrice']
ema = goog_data['Exponential20DayMovingAverage']

fig = plt.figure()
ax1 = fig.add_subplot(111, ylabel='Google price in $')
close_price.plot(ax=ax1, color='g', lw=2., legend=True)
ema.plot(ax=ax1, color='b', lw=2., legend=True)
plt.savefig('ema.png')
plt.show()
