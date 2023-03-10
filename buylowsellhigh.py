import numpy
import pandas as pd
# loading the class data from the package pandas_datareader
from pandas_datareader import data
# loading the yfinance library to override reading for pandas_datareader
import yfinance as yfin
import numpy as np
import matplotlib.pyplot as plt

# Call this method to make pandas_datareader use Yahoo as the default data source
yfin.pdr_override()
# First day
start_date = '2014-01-01'
# Last day
end_date = '2018-01-01'
goog_data = data.DataReader('GOOG', start_date, end_date)
# print the Google data
# print(goog_data)

# Time to get the signal for actually performing a buy low sell high trade, based on the adjusted closing price
goog_data_signal = pd.DataFrame(index=goog_data.index)
# Set the 'price' column of goog_data_signal data frame equal to goog_data data frame 'adjusted price'
goog_data_signal['price'] = goog_data['Adj Close'].to_numpy()
# Get the daily difference of the 'adjusted price' for each day
goog_data_signal['daily_difference'] = goog_data_signal['price'].diff()
# If the daily difference is positive we're going to set the signal to 1, if negative 0
goog_data_signal['signal'] = 0.0
goog_data_signal['signal'] = np.where(goog_data_signal['daily_difference'] >= 0, 1.0, 0.0)
# When the signal changes from 1 to 0, that means the upwards trend has stopped, we will close any positions at this point.
goog_data_signal['positions'] = goog_data_signal['signal'].diff()
# Print the goog_data_signal data frame
# print(goog_data_signal)

fig = plt.figure()
# This method allows you to create an axes 1x1 grid subplot in the matlab figure in the first position (row, col, position)
ax1 = fig.add_subplot(111)
# On the axes, plot the google_data_signal price data
goog_data_signal['price'].plot(ylabel='Google price in $', ax=ax1, color='r', linewidth=2.)
# Now we want to plot the points where we bought a share, loc method allows us to get all the rows were position == 1.0,
# and then we are assigning those indices as the x value
# Y value is simply the price at which positions == 1.0
# Color 'm' means magenta
ax1.plot(goog_data_signal.loc[goog_data_signal.positions == 1.0].index,
       goog_data_signal.price[goog_data_signal.positions == 1.0],
       '^', markersize=5, color='m')
# Now we want to plot the points where we sold a share, loc method allows us to get all the rows were position == -1.0,
# and then we are assigning those indices as the x value
# Y value is simply the price at which positions == -1.0
# Color 'k' means black
ax1.plot(goog_data_signal.loc[goog_data_signal.positions == -1.0].index,
       goog_data_signal.price[goog_data_signal.positions == -1.0],
       'v', markersize=5, color='k')
# Show the MathLab figure
# plt.show()

initial_capital = float(1000.0)

positions = pd.DataFrame(index=goog_data_signal.index).fillna(0.0)
portfolio = pd.DataFrame(index=goog_data_signal.index).fillna(0.0)

positions['GOOG'] = goog_data_signal['signal']
portfolio['positions'] = (positions.multiply(goog_data_signal['price'], axis=0))
portfolio['cash'] = initial_capital - (positions.diff().multiply(goog_data_signal['price'], axis=0)).cumsum()
portfolio['total'] = portfolio['positions'] + portfolio['cash']
portfolio.plot()
plt.show()