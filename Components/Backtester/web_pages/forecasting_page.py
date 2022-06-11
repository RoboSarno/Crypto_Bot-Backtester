import streamlit as st
import tensorflow as tf
import numpy as np
import pandas as pd
import apicon


def forecasting_page():  
    st.write('''
                ### Welcome to my Neural Network Forcaster:
                
                - Please select a ticker below
                - Will try to predict the price for the next week.
                - Note: This is still in beta 
                
                ''')
    col1, col2 = st.columns(2)
    with col1:
        strat = st.selectbox(
            'What Strategy would you like to forecast?',
            ['Strat 1', 'Strat 2', 'Strat 4'])
        close_Price = st.number_input('Select Close Price:')
        
        open_Price = st.number_input('Select Open Price:')
    with col2:
        ticker = st.selectbox(
            'What ticker would you like to forecast?',
            ['HBARBTC', 'VETBTC', 'ONEBTC', 'ADABTC', 'ETHBTC', 'BCHBTC', 'LTCBTC'])
        high_Price = st.number_input('Select High Price:')
        
        low_Price = st.number_input('Select Low Price:')

    b = st.button('Process Request')
    if b:
        if strat == 'Strat 1':
            
            st.write(f'''
                    ### Forcast Image for {strat}
                    ''')

            # conn = apicon.Database()
            # df = conn.select_strat_data(1, ticker)
            # cols = list(df.columns)
            # for i in ['HBARBTC', 'VETBTC', 'ONEBTC', 'ADABTC', 'ETHBTC', 'BCHBTC', 'LTCBTC']
            #     for col in list(df.columns):
            #         if col in ['datetime', ticker_id]
            # print({i:0 for i in cols})
            # print(pd.DataFrame(list(range(len(cols))), columns=cols))
            # df.dropna(subset=['ema_200'], inplace=True)
            # last_element = df.tail(1).copy()
            # st.write(np.reshape(last_element.to_numpy(), (1, -1, 1)))

            

            # model = tf.saved_model.load(r'./Models_Saved/df_30_strat1_model')
        if strat == 'Strat 2':
            st.write(f'''
                    ### Forcast Image for {strat}
                    ''')
            pred = pd.DataFrame.from_dict({'datetime': None, 'open':[open_Price], 'close':[close_Price], 'high':[high_Price], 'low':[low_Price]})
            # make prediction format
            # model = tf.saved_model.load(r'./Models_Saved/df_15_strat2_model')
            
        if strat == 'Strat 4':
            st.write(f'''
                    ### Forcast Image for {strat}
                    ''')
            pred = pd.DataFrame.from_dict({'datetime': None, 'open':[open_Price], 'close':[close_Price], 'high':[high_Price], 'low':[low_Price]})
            # make prediction format
            
            # model = tf.saved_model.load(r'./Models_Saved/df_15_strat4_model')
def get_column_format_strat1(df):
    datetime = df['datetime'].iloc[0]
    temp = df[['ticker_id', 'open', 'high', 'low', 'close', 'volume', 'psarl', 'psars', 'psarr', 'psaraf', 'macd', 'macdh', 'macds', 'ema_200']]
    
    ans = []
    for i, r in temp.iterrows():
        ticker = r['ticker_id']
        temp = {'datetime': datetime, 'ticker_id': ticker}
        for curr_col in ['ticker_id', 'open', 'high', 'low', 'close', 'volume', 'psarl', 'psars', 'psarr', 'psaraf', 'macd', 'macdh', 'macds', 'ema_200']:
            temp[f"{curr_col}_{ticker}"] = [r[curr_col]]
            del temp['ticker_id']
            ans.append(temp)
    ans = {k: v for d in ans for k, v in d.items()}
    return pd.DataFrame(ans)