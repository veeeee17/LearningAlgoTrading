import pandas as pd
from pandas_datareader import data
import yfinance as yfin

start_date = '2014-01-01'
end_date = '2018-01-01'
SRC_DATA_FILENAME = 'goog_data.pkl'

try:
    goog_data2 = pd.read_pickle(SRC_DATA_FILENAME)
except FileNotFoundError:
    yfin.pdr_override()
    goog_data2 = data.DataReader('GOOG', start_date, end_date)
    goog_data2.to_pickle(SRC_DATA_FILENAME)

# Get the last 620 rows from goog_data2 dataframe, since these are the days the stock split did not occur.
goog_data = goog_data2.tail(620)
lows = goog_data['Low']
highs = goog_data['High']

import matplotlib.pyplot as plt

fig = plt.figure()
ax1 = fig.add_subplot(111, ylabel='Google price in $')
# Plot the highs and lows
highs.plot(ax=ax1, color='c', lw=2.)
lows.plot(ax=ax1, color='y', lw=2.)
ax1.hlines(highs.head(200).max(), lows.index.values[0], lows.index.values[-1], linewidth=2, color='g')
ax1.hlines(lows.head(200).min(), lows.index.values[0], lows.index.values[-1], linewidth=2, color='r')
ax1.axvline(linewidth=2, color='b', x=lows.index.values[200], linestyle=":")
plt.show()