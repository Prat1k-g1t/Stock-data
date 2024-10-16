"""
    Stock trends using (simple and exponential) moving averages
"""
"""
    Import dependencies
"""
import datetime as dt 
from datetime import timezone
import pandas as pd
import yfinance as yf
import matplotlib.pyplot as plt
import plotly.offline as plty
import plotly.graph_objects as go
from plotly.subplots import make_subplots
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
stocklist  = ['ABN.AS', 'ING', '^NSEI']

stock_data = yf.download(stocklist, start=start, end=end)

stock_open  = stock_data.Open
stock_high  = stock_data.High
stock_low   = stock_data.Low
stock_close = stock_data.Close
stock_vol   = stock_data.Volume

stock_close['MA50_ABN'] = stock_close['ABN.AS'].rolling(window=50, min_periods=0).mean()
stock_close['MA50_ING'] = stock_close['ING'].rolling(window=50, min_periods=0).mean()
stock_close['MA50_NSE'] = stock_close['^NSEI'].rolling(window=50, min_periods=0).mean()


stock_close['EMA50_ABN'] = stock_close['ABN.AS'].ewm(span=50, adjust=False).mean()
stock_close['EMA50_ING'] = stock_close['ING'].ewm(span=50, adjust=False).mean()
stock_close['EMA50_NSE'] = stock_close['^NSEI'].ewm(span=50, adjust=False).mean()

stock_close['MA200_ABN'] = stock_close['ABN.AS'].rolling(window=200, min_periods=0).mean()
stock_close['MA200_ING'] = stock_close['ING'].rolling(window=200, min_periods=0).mean()
stock_close['MA200_NSE'] = stock_close['^NSEI'].rolling(window=200, min_periods=0).mean()

# print(stock_close.head(20))

fig_ING = make_subplots(rows=2, cols=1, shared_xaxes=True,
                         vertical_spacing=0.1, subplot_titles=('ING', 'Volume'), row_width=[0.2, 0.7])

fig_NSE = make_subplots(rows=2, cols=1, shared_xaxes=True,
                         vertical_spacing=0.1, subplot_titles=('NSE', 'Volume'), row_width=[0.2, 0.7])

fig_ING.add_trace(go.Candlestick(x=stock_data.index, open=stock_open['ING'], high=stock_high['ING'], low=stock_low['ING'], close=stock_close['ING'], name='ING_OHLC'))

fig_NSE.add_trace(go.Candlestick(x=stock_data.index, open=stock_open['^NSEI'], high=stock_high['^NSEI'], low=stock_low['^NSEI'], close=stock_close['^NSEI'], name='NSE_OHLC'), row=1, col=1)

"""
    Adding moving averages
"""
fig_NSE.add_trace(go.Scatter(x=stock_data.index, y=stock_close['MA50_NSE'], marker_color='grey', name='MA50'), row=1, col=1)

fig_NSE.add_trace(go.Scatter(x=stock_data.index, y=stock_close['EMA50_NSE'], marker_color='blue', name='EMA50'), row=1, col=1)

fig_NSE.add_trace(go.Scatter(x=stock_data.index, y=stock_close['MA200_NSE'], marker_color='lightgrey', name='MA200'), row=1, col=1)

fig_NSE.add_trace(go.Bar(x=stock_data.index, y=stock_vol['^NSEI'], marker_color='red', showlegend=False), row=2, col=1)

fig_NSE.update_layout(
    title = 'Nifty 50 historical price chart',
    xaxis_tickfont_size = 12,
    yaxis = dict(
        title='Price (Rs./share)',
        title_font_size=14,
        tickfont_size=12
    ),
    autosize=False,
    width=1000,
    height=800,
    margin=dict(l=50, r=50, b=100, pad=5),
    paper_bgcolor = 'LightSteelBlue'
    )

fig_NSE.show()