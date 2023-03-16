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

time_period = 20  # number of days over which to average
history = [] # to track history of prices
sma_values = [] # to track history of simple moving average

for close_price in close:
    history.append(close_price)
    if len(history) > time_period: # we remove the oldest time period since we only want to calculate sma for past 20 days at a time
        del(history[0])

    sma_values.append(stats.mean(history)) # get the average for every 20 days

goog_data = goog_data.assign(ClosePrice=pd.Series(close, index=goog_data.index))
goog_data = goog_data.assign(Simple20DayMovingAverage=pd.Series(sma_values, index=goog_data.index))
close_price = goog_data['ClosePrice']
sma = goog_data['Simple20DayMovingAverage']

fig = plt.figure()
ax1 = fig.add_subplot(111, ylabel='Google price in $')
close_price.plot(ax=ax1, color='g', lw=2., legend=True)
sma.plot(ax=ax1, color='r', lw=2., legend=True)
plt.show()
