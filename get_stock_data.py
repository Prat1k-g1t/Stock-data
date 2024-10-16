"""
    Import dependencies
"""
import datetime as dt 
from datetime import timezone
import pandas as pd
# from pandas_datareader import data as pdr
import yfinance as yf
import matplotlib.pyplot as plt
import plotly.offline as plty
pd.options.plotting.backend = 'plotly'

"""
    Prescribe start and end dates 
"""
end = dt.datetime.now(timezone.utc)
start = end - dt.timedelta(days=5000)
print(start, end)
# print(start.strftime("%Z"))

"""
    Stock tickers to analyze
"""
stocklist = ['ABN.AS', 'ING', '^NSEI']

# stock_ticks = yf.Ticker('ABN.AS') #; print(type(stock_ticks))

# stock_info   = stock_ticks.info
# stock_shares = stock_ticks.get_shares_full(start=start, end=end)
# for key,value in stock_info.items():
#     print(key, ":", value)

stock_data = yf.download(stocklist, start=start, end=end)
# print(stock_data.head())
# print(stock_data.index)
# print(stock_data.columns)

stock_close = stock_data.Close # Subcategory closing prices as pandas dataframe
print(stock_close.index)
print(stock_close.describe())

"""
    Printing closing stock price for the past 100 days
    Using Pandas' describe function to generate statistical info.
"""
print(stock_close[stock_close.index > end - dt.timedelta(days=100)].describe())

fig = stock_close.plot()
fig.show()
# fig.close()

fig = stock_close.pct_change().plot(kind='hist')
fig.show()