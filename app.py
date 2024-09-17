
import yfinance as yf
import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
import pandas as pd
from datetime import datetime
import pandas_ta as ta
import figure
    
st.set_page_config(layout="wide")

# CREATE CARDS---------------------------------------------------------

def create_card (name, ticker, percent_change, curr_val, df):
    with st.container (border = True):
        tl, tr = st.columns  ([2,1])
        bl, br = st.columns ([1,1.5])

        with tl: 
           st.markdown(f'<span style="font-size:20px; font-weight:bold;">{name}</span>', unsafe_allow_html=True)

        with tr: 
            st.html (f'<span class = "ticker"> </span>')
            st.markdown (f'{ticker}')

            negative = float (percent_change) <0
            st.markdown(
                f":{'red' if negative else 'green'}[{'▼' if negative else '▲'} {percent_change} %]"
            )

        with bl: 
            st.write ('Current Val: \n$' + str (curr_val))

        with br: 

            spark = go.Figure (
                data = go.Scatter (
                y = df['Open'],
                mode = 'lines',
                fill = 'tozeroy',
                line_color = 'red',
                fillcolor = 'pink'
                ),
            )

            spark.update_xaxes (visible = False, fixedrange = True)
            spark.update_yaxes (visible = False, fixedrange = True)
            spark.update_layout (showlegend = False,
                                plot_bgcolor='rgba(0,0,0,0)',  # Transparent plot background
                                paper_bgcolor='rgba(0,0,0,0)',  # Transparent figure background
                                height = 50,
                                margin = dict (t=10, l=0,b=0,r=0,pad=0))
            
            st.plotly_chart (spark, use_container_width = True)


# GET THE DATA +  ADD MORE INFORMATION TO DATA ---------------------------------------------------------
def get_data (type):
    stock = type
    stock = yf.Ticker (stock)
    info = stock.info
    df = ''

    if 'start' in st.session_state:
        start_date = st.session_state ['start']
        end_date  = st.session_state ['end']
        

        df = stock.history(period = 'max')
        df.index = df.index.tz_localize(None) 
        start_date = pd.Timestamp(start_date).tz_localize(None)
        end_date = pd.Timestamp(end_date).tz_localize(None)
        df = df[(df.index > start_date) & (df.index < end_date)]
     
    else:

        df = stock.history (period = 'max')


    market_cap = info.get('marketCap', 'N/A')  
    df ['RSI'] = ta.rsi(df['Close'])
    curr_val = round (df ['Close'].iloc [-1],2)
    first_val = df ['Close'].iloc [0]
    percent_change =round (((curr_val - first_val / first_val) * 100),2)

    ticker = info.get ('symbol', 'Not available')
    name = info.get ('shortName', 'Not available')
    df['company'] = ticker

    return market_cap, name, ticker, percent_change, curr_val, df


# SELECT BOX ---------------------------------------------------------

tab1,tab2 = st.tabs (['Compare & Contrast','Individual Stock'])

stocks = [
        "AAPL", "MSFT", "AMZN", "GOOGL", "META", "TSLA", "NVDA", "IBM", "ORCL", 
        "INTC", "CSCO", "AMD", "DIS", "NFLX", "BA", "XOM", "CVX", "WMT", "KO", 
        "PFE", "MRK", "UNH", "JPM", "GS", "MS", "C", "BAC", "HSBC", "T", "VZ", 
        "MCD", "SBUX", "HD", "LOW", "DELL", "HPQ", "TWTR", "SQ", "SHOP", "PAYX", 
        "ADBE", "CMCSA", "TM", "HMC", "BMWYY", "RBLX", "SPOT", "SNOW", "DOCU", 
        "ZM", "UBER", "LYFT", "RBLX", "CRSP", "EDIT", "NTLA", "MRNA", "BNTX", 
        "NVAX"
    ]


with tab1: 

   
    max_selections = 8
    options = st.multiselect (
        '**Select up to 8 stock tickers you would like to see**',
        stocks, 
        ["AAPL", "MSFT", "AMZN", "GOOGL"]    
    )

    if len(options) > max_selections:
        st.error(f"You can only select up to {max_selections} tickers.")
        options = options[:max_selections]

    # Display the selected options
    st.write("**Selected stock tickers:**")

    strVal= ''
    for x in options: 
        strVal+= x + ', '

    st.write (strVal)
    one, two, three, four = st.columns (4)
    five, six, seven, eight = st.columns (4)

    dataframes = []

    with one: 
        #get the data for ticker
        if 0 <= len (options)-1:
            market_cap, name, ticker, percent_change, curr_val, df = get_data (options[0])
            #print the card
            create_card (name, ticker, percent_change, curr_val, df)
            dataframes.append (df)
    

    with two: 
        if 1 <= len (options)-1:
            #get the data for ticker
            market_cap,name, ticker, percent_change, curr_val, df1= get_data (options[1])
            #print the card
            create_card (name, ticker, percent_change, curr_val, df1)
            dataframes.append (df1)

    with three: 
        if 2 <= len (options)-1:
            #get the data for ticker
            market_cap,name, ticker, percent_change, curr_val, df2 = get_data (options[2])
            #print the card
            create_card (name, ticker, percent_change, curr_val, df2)
            dataframes.append (df2)

    with four: 
        if 3 <=len (options)-1:
            #get the data for ticker
            market_cap,name, ticker, percent_change, curr_val, df3 = get_data (options[3])
            #print the card
            create_card (name, ticker, percent_change, curr_val, df3)
            dataframes.append (df3)

    with five: 
        #get the data for ticker

        if 4 <= len (options)-1:
            market_cap,name, ticker, percent_change, curr_val, df4 = get_data (options[4])
            #print the card
            create_card (name, ticker, percent_change, curr_val, df4)
            dataframes.append (df4)

    with six: 
        if 5 <= len (options)-1 :
            #get the data for ticker
            market_cap,name, ticker, percent_change, curr_val, df5 = get_data (options[5])
            #print the card
            create_card (name, ticker, percent_change, curr_val, df5)
            dataframes.append (df5)


    with seven: 
        if 6 <= len (options)-1:
            #get the data for ticker
            market_cap,name, ticker, percent_change, curr_val, df6 = get_data (options[6])
            #print the card
            create_card (name, ticker, percent_change, curr_val, df6)
            dataframes.append (df6)

    with eight: 
        if 7 <= len (options)-1:
            #get the data for ticker
            market_cap,name, ticker, percent_change, curr_val, df7 = get_data (options[7])
            #print the card
            create_card (name, ticker, percent_change, curr_val, df7)
            dataframes.append (df7)


    #SCATTER FOR ALL ---------------------------------------------------------

    all = pd.concat (dataframes,axis = 0)
    totaldf = all

    fig = px.line (totaldf, x = totaldf.index, y = 'Close', color = 'company',
                    title = 'Closing Value of Stocks by Date and Company')

    st.plotly_chart (fig)


    #FIND OUT THE MIN AND MAX DATES-------------------

    minV = pd.Timestamp('1920-01-01')
    maxV = pd.Timestamp('5000-01-01')

    for x in dataframes: 
        #filter = totaldf[totaldf['company'] == x]
        minDate = x.index.min()
        maxDate = x.index.max()

        minDate = x.index.min().tz_localize(None)  # Convert to timezone-naive
        maxDate = x.index.max().tz_localize(None)  # Convert to timezone-naive

        minV = max(minDate, minV.tz_localize(None))  # Ensure minV is timezone-naive
        maxV = min(maxDate, maxV.tz_localize(None))  # Ensure maxV is timezone-naive


        minV = max (minDate, minV)
      
        maxV = min (maxDate, maxV)


    # SLIDER FOR COMPARISON ---------------------------------------------------------
    minV = pd.Timestamp(minV).date()
    maxV = pd.Timestamp(maxV).date()

    if 'start' not in st.session_state: 
        st.session_state ['min'] = minV
        st.session_state ['max'] = maxV
        start_date, end_date = st.slider(
            "Select date range for stocks:",
            min_value=minV,
            max_value=maxV,
            value=(minV, maxV)  # Default range
        )
        start_date = pd.Timestamp(start_date).tz_localize(None)
        end_date = pd.Timestamp(end_date).tz_localize(None)
    else: 
        minV = pd.Timestamp(st.session_state ['start']).date()
        maxV = pd.Timestamp(st.session_state ['end']).date()
        start_date, end_date = st.slider(
            "Select date range for stocks:",
            min_value=st.session_state ['min'],
            max_value=st.session_state ['max'],
            value=(minV,maxV)  # Default range
        )

    st.session_state ['start']  = start_date
    st.session_state ['end'] = end_date


    
    


#SLIDER ---------------------------------------------------------

with tab2: 

    company = st.selectbox ('Which company would you like to see?',
                            stocks
                            )

    market_cap,name, ticker, percent_change, curr_val, df = get_data(company)
    df.index = df.index.date
    minDate = df.index.min()
    maxDate = df.index.max()
    default_start_date = pd.Timestamp('2021-01-01').date()


    start_date, end_date = st.slider(
        "Select date range:",
        min_value=st.session_state ['min'],
        max_value=st.session_state ['max'],
        value=(default_start_date, maxDate)  # Default range
    )

    df = df[(df.index >= start_date) & (df.index <= end_date)]


    # PRINT THE VIZ---------------------------------------------------------

    left_chart, right_chart = st.columns ([3,1.2])

    with left_chart: 
        plt1 = figure.candle(df)
        st.plotly_chart (plt1)


    with right_chart:
       
        l,r = st.columns (2)
       
        def format_metric(value):
            value = round (value,2)
            if value >= 1_000_000:
                return "{:.1f}M".format(value / 1_000_000)
            elif value >= 1_000:
                return "{:.1f}K".format(value / 1_000)
            else:
                return str(value)

        # Streamlit layout and metrics
        with l:
            st.metric('Lowest Volume Day Trade', format_metric(df["Volume"].min()))
            st.metric('Lowest Close Price', format_metric(df["Close"].min()))

        with r:
            st.metric('Highest Volume Day Trade', format_metric(df["Volume"].max()))
            st.metric('Highest Close Price', format_metric(df["Close"].max()))

        with st.container():
            st.metric('Average Daily Value', format_metric(df["Volume"].mean()))
            st.metric('Current Market Cap', format_metric(market_cap))


                

                