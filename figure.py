import plotly.graph_objects as go
from plotly.subplots import make_subplots
import pandas as pd
from datetime import datetime



def candle (df):
    sub = make_subplots (
        rows = 3, 
        cols = 1,
        shared_xaxes = True, 
        row_heights = [.6,.2,.2],
        vertical_spacing = 0.1
    )
    
    sub.add_trace (go.Candlestick (
        x = df.index,
        open = df['Open'],
        high = df ['High'],
        low = df['Low'],
        close = df['Close'], 
        name = 'Dollars'), 
        row = 1, col = 1, 

    )

    sub.update_layout(
    title='Stock Prices Trends',
    yaxis_title='Closing Price'
    )

    sub.update_layout (xaxis_rangeslider_visible=False)
    

    #RSI ---------------------

    sub.add_trace (go.Scatter (
        x = df.index,
        y = df['RSI'],
        mode = 'lines',
        name = 'Relative Strength Index'
    ), row = 3, col = 1)

    sub.add_shape (
        type = 'line',
        x0 = df.index.min(), x1 = df.index.max(),
        y0 = 30, y1 = 30,
        xref = 'x3',
        yref = 'y3',
        line = dict (
        color = 'Green',
        dash = 'dash'
        )
    )

    sub.add_shape (
        type = 'line',
        x0 = df.index.min(), x1 = df.index.max(),
        y0 = 70, y1 = 70,
        xref = 'x3',
        yref = 'y3',
        line = dict (
        color = 'Red',
        dash = 'dash'
        )
    )

    #Volume Trend ---------------------
    sub.add_trace (go.Bar (
        x = df.index,
        y = df['Volume'],
        name = 'Volume Traded'
    ), row = 2, col = 1)

    return sub