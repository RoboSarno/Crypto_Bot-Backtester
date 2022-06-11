
import streamlit as st
import tick
import pandas as pd


def convert_df(df):
    """
    _summary_
        converts df to downloadable file type

    Args:
        df (pd.DataFrame): df to convert 

    Returns:
        utf-8: convert df to csv 
    """
    return df.to_csv(index=False).encode('utf-8')
   
def download_csv_page():
    st.write('''
             This page is used to download the last 500 intervals of open, close, low, high, and volume of a ticker specified.
             ''')
    # options menu
    strat = st.selectbox(
        'What Data would you like to Download?',
        {'Buy/Sell PSAR + MACD + EMA - 30min', 'Buy/Sell ST + RSI + EMA - 15min', 'Buy/Sell Hoffman - 15min'})
    
    if strat == 'Buy/Sell PSAR + MACD + EMA - 30min':
        s = 1
    elif strat == 'Buy/Sell ST + RSI + EMA - 15min':
        s = 2
    elif strat == 'Buy/Sell Hoffman - 15min':
        s = 4
    t = st.selectbox(
        'What Data would you like to Download?',
        ['ADABTC', 'ONEBTC', 'HBARBTC', 'VETBTC', 'LTCBTC', 'BCHBTC', 'ETHBTC'])
    # options menu --------------------------------------------------------------
    
    
    # if Strat 1 get historical data
    if strat == 'Buy/Sell PSAR + MACD + EMA - 30min':
        ticker = tick.Ticker(t, s, '30m')
        df = ticker.db_connection.select_historical_data(s, t)
        df = df[df['ticker_id'] == t]
        csv = convert_df(df.tail(500))
        st.download_button( "Download CSV", csv,
                     f'ST_RSI_EMA_{t}.csv', "text/csv",
                     key='download-csv'
        )
    # if Strat 2 get historical data
    elif strat == 'Buy/Sell ST + RSI + EMA - 15min':
        ticker = tick.Ticker(t, s, '15m')
        df = ticker.db_connection.select_historical_data(s, t)
        df = df[df['ticker_id'] == t]
        csv = convert_df(df.tail(500))
        st.download_button( "Download CSV", csv,
                     f'ST_RSI_EMA_{t}.csv', "text/csv",
                     key='download-csv'
        )
    # if Strat 4 get historical data
    elif strat == 'Buy/Sell Hoffman - 15min':
        ticker = tick.Ticker(t, s, '15m')
        df = ticker.db_connection.select_historical_data(s, t)
        df = df[df['ticker_id'] == t]
        csv = convert_df(df.tail(500))
        st.download_button( "Download CSV", csv,
                     f'ST_RSI_EMA_{t}.csv', "text/csv",
                     key='download-csv'
        )
   