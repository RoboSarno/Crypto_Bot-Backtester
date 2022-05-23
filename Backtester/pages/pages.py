from multiprocessing.dummy import current_process
import streamlit as st
import tick
import streamlit_authenticator as stauth
from streamlit_option_menu import option_menu
import pandas as pd
import datetime 
from PIL import Image

ticker_label_list = ['ADABTC', 'ONEBTC', 'HBARBTC', 'VETBTC', 'LTCBTC', 'BCHBTC', 'ETHBTC']
    
def convert_df(df):
       return df.to_csv().encode('utf-8')
   
def download_csv_pafe(df):
    # --------------------------------------------------------------------------------
    # global ticker_label_list
    # strat = st.sidebar.selectbox(
    #     'What Data would you like to Download?',
    #     {'Buy/Sell PSAR + MACD + EMA', 'Buy/Sell ST + RSI + EMA', 'Buy/Sell Hoffman'})
    
    # if strat == 'Buy/Sell PSAR + MACD + EMA':
    #     s = 1
    # elif strat == 'Buy/Sell ST + RSI + EMA':
    #     s = 2
    # elif strat == 'Buy/Sell Hoffman':
    #     s = 4
    # t = st.sidebar.selectbox(
    #     'What Data would you like to Download?',
    #     (ticker_label_list))
    
    
    
    # if strat == 'Buy/Sell PSAR + MACD + EMA':
    #     ticker = tick.Ticker(t, s, '30m')
    #     df = ticker.db_connection.select_historical_buy_sell_table(s, t)
    #     df = df[df['ticker_id'] == t]
    #     csv = convert_df(df)
    #     st.write(df)
    #     st.download_button( "Download CSV", csv,
    #                         f'ST_RSI_EMA_{t}.csv', "text/csv",
    #                         key='download-csv'
    #     )
    # elif strat == 'Buy/Sell ST + RSI + EMA':
    #     ticker = tick.Ticker(t, s, '15m')
    #     df = ticker.db_connection.select_historical_buy_sell_table(s, t)
    #     df = df[df['ticker_id'] == t]
    #     st.write(df)
    #     csv = convert_df(df)
    #     st.download_button( "Download CSV", csv,
    #                         f'ST_RSI_EMA_{t}.csv', "text/csv",
    #                         key='download-csv'
    #     )
    # elif strat == 'Buy/Sell Hoffman':
    #     ticker = tick.Ticker(t, s, '15m')
    #     df = ticker.db_connection.select_historical_buy_sell_table(s, t)
    #     df = df[df['ticker_id'] == t]
    #     st.write(df)
    #     csv = convert_df(df)
    #     st.download_button( "Download CSV", csv,
    #                         f'ST_RSI_EMA_{t}.csv', "text/csv",
    #                         key='download-csv'
    #     )
    pass
   

def strat2_anal_page(risk, reward):
    global ticker_label_list
    st.title('RSI + EMA + ST 15 min')
    selected = option_menu(None, ['Home', 'Price Over Time', "Wallet Over Time", "Buy and Sell Data"], 
        icons=['house', 'list-task', "list-task", 'cloud-upload'], 
        menu_icon="cast", default_index=0, orientation="horizontal",
        styles={
            "container": {"padding": "0!important", "background-color": "#0e3064"},
            "icon": {"color": "#fafafa", "font-size": "25px"}, 
            "nav-link": {"font-size": "25px", "text-align": "left", "margin":"0px", "--hover-color": "#586e75"},
            "nav-link-selected": {"background-color": "green"},
        }
    )
    print(f'Current Sub-Page {selected}')
    st.markdown("""---""")
    if selected == "Wallet Over Time":
        strat2_anal_WOT(risk, reward)
    elif selected == "Price Over Time":
        strat2_anal_POT(risk, reward)
    elif selected ==  "Buy and Sell Data":
        df = pd.DataFrame()
        download_csv_pafe(df)
    elif selected == 'Home':
        st.write('Home page to show quick anlysis on tickers being used and how the strategy works')
        
def strat2_anal_WOT(risk, reward):
    st.markdown("""---""")
    what_page = 2
    my_bar = st.progress(0)
    pecent_add = round(100 / len(ticker_label_list))
    progress = 0
    for t in ticker_label_list:
        try:
            ticker_obj = tick.Ticker(t, what_page, '15m')
            ticker_obj.update_wallet_info(risk, reward)
            wallet = ticker_obj.get_wallet_info()
            display = ticker_obj.get_display_wallet()
            with st.expander('Ticker: ' + str(t)):
                col1, col2, col3 = st.columns([3, 3, 3])
                display.wal_header(col1, col2)
                display.graph_pie(col3)
                display.graph_wallet_info(col1, col2)
                display.graph_MPD_ticker()
                progress += pecent_add
                if progress < 100:  
                    my_bar.progress(progress)  
            del wallet, display, ticker_obj
        except:
            st.error(f'Ticker: {t} does not have any data')
    my_bar.progress(progress + (100 - progress))
    st.success('Successfully Finished Running Strategy')
    my_bar.empty()
    
def strat2_anal_POT(risk, reward):
    what_page = 2
    my_bar = st.progress(0)
    pecent_add = round(100 / len(ticker_label_list))
    progress = 0
    for t in ticker_label_list:
        try:
            ticker_obj = tick.Ticker(t, what_page, '15m')
            ticker_obj.update_wallet_info(risk, reward)
            wallet = ticker_obj.get_wallet_info()
            display = ticker_obj.get_display_wallet()
            col1, col2, col3 = st.columns([40, 30, 30])
            display.anal_page(t, col1, col2, col3)
                
            progress += pecent_add
            if progress < 100:  
                my_bar.progress(progress)  
            del wallet, display, ticker_obj
        except:
            st.error(f'Ticker: {t} does not have any data')
            st.markdown('---')
    my_bar.progress(progress + (100 - progress))
    st.success('Successfully Finished Running Strategy')
    my_bar.empty()

def strat4_anal_page(risk, reward):
    global ticker_label_list
    st.title('HOFFMAN 15 min')
    selected = option_menu(None, ['Home', 'Price Over Time', "Wallet Over Time", "Buy and Sell Data"], 
        icons=['house', 'list-task', "list-task", 'cloud-upload'], 
        menu_icon="cast", default_index=0, orientation="horizontal",
        styles={
            "container": {"padding": "0!important", "background-color": "#0e3064"},
            "icon": {"color": "#fafafa", "font-size": "25px"}, 
            "nav-link": {"font-size": "25px", "text-align": "left", "margin":"0px", "--hover-color": "#586e75"},
            "nav-link-selected": {"background-color": "green"},
        }
    )
    print(f'Current Sub-Page {selected}')
    st.markdown("""---""")
    if selected == "Wallet Over Time":
        strat4_anal_WOT(risk, reward)
    elif selected == "Price Over Time":
        strat4_anal_POT(risk, reward)
    elif selected ==  "Buy and Sell Data":
        df = pd.DataFrame()
        download_csv_pafe(df)
    elif selected == 'Home':
        st.write('Home page to show quick anlysis on tickers being used and how the strategy works')
        
def strat4_anal_WOT(risk, reward):
    st.markdown("""---""")
    what_page = 4
    my_bar = st.progress(0)
    pecent_add = round(100 / len(ticker_label_list))
    progress = 0
    for t in ticker_label_list:
        try:
            ticker_obj = tick.Ticker(t, what_page, '15m')
            ticker_obj.update_wallet_info(risk, reward)
            wallet = ticker_obj.get_wallet_info()
            display = ticker_obj.get_display_wallet()
            with st.expander('Ticker: ' + str(t)):
                col1, col2, col3 = st.columns([3, 3, 3])
                display.wal_header(col1, col2)
                display.graph_pie(col3)
                display.graph_wallet_info(col1, col2)
                display.graph_MPD_ticker()
                progress += pecent_add
                if progress < 100:  
                    my_bar.progress(progress)  
            del wallet, display, ticker_obj
        except:
            st.error(f'Ticker: {t} does not have any data')
    my_bar.progress(progress + (100 - progress))
    st.success('Successfully Finished Running Strategy')
    my_bar.empty()
    
def strat4_anal_POT(risk, reward):
    what_page = 4
    my_bar = st.progress(0)
    pecent_add = round(100 / len(ticker_label_list))
    progress = 0
    for t in ticker_label_list:
        try:
            ticker_obj = tick.Ticker(t, what_page, '15m')
            ticker_obj.update_wallet_info(risk, reward)
            wallet = ticker_obj.get_wallet_info()
            display = ticker_obj.get_display_wallet()
            col1, col2, col3 = st.columns([40, 30, 30])
            display.anal_page(t, col1, col2, col3)
                
            progress += pecent_add
            if progress < 100:  
                my_bar.progress(progress)  
            del wallet, display, ticker_obj
        except:
            st.error(f'Ticker: {t} does not have any data')
            st.markdown('---')
    my_bar.progress(progress + (100 - progress))
    st.success('Successfully Finished Running Strategy')
    my_bar.empty()
    
    
    
    
    
    
# def strat2_anal_page():
#     global ticker_label_list
#     st.title('RSI + EMA + ST 15 min')
#     st.markdown("""---""")
#     what_page = 2
#     my_bar = st.progress(0)
#     pecent_add = round(100 / len(ticker_label_list))
#     progress = 0
#     for t in ticker_label_list:
#         try:
#             ticker_obj = tick.Ticker(t, what_page, '30m')
#             ticker_obj.update_wallet_info(2, 1)
#             wallet = ticker_obj.get_wallet_info()
#             display = ticker_obj.get_display_wallet()
#             col1, col2, col3 = st.columns([40, 30, 30])
#             display.anal_page(t, col1, col2, col3)
                
#             progress += pecent_add
#             if progress < 100:  
#                 my_bar.progress(progress)  
#             del wallet, display, ticker_obj
#         except:
#             st.error(f'Ticker: {t} does not have any data')
#             st.markdown('---')
#     my_bar.progress(progress + (100 - progress))
#     st.success('Successfully Finished Running Strategy')
#     my_bar.empty()
    
# def strat2_wallet_page():
#     global ticker_label_list
#     st.title('Wallet Info RSI + EMA + ST 15 min intervals')
#     st.markdown("""---""")
#     what_page = 2
#     my_bar = st.progress(0)
#     pecent_add = round(100 / len(ticker_label_list))
#     progress = 0
#     for t in ticker_label_list:
#         try:
#             ticker_obj = tick.Ticker(t, what_page, '15m')
#             ticker_obj.update_wallet_info(2, 1)
#             wallet = ticker_obj.get_wallet_info()
#             display = ticker_obj.get_display_wallet()
#             with st.expander('Ticker: ' + str(t)):
#                 col1, col2, col3 = st.columns([3, 3, 3])
#                 display.wal_header(col1, col2)
#                 display.graph_pie(col3)
#                 display.graph_wallet_info(col1, col2)
#                 display.graph_MPD_ticker()
#                 progress += pecent_add
#                 if progress < 100:  
#                     my_bar.progress(progress)  
#             del wallet, display, ticker_obj
#         except:
#             st.error(f'Ticker: {t} does not have any data')
#     my_bar.progress(progress + (100 - progress))
#     st.success('Successfully Finished Running Strategy')
#     my_bar.empty()
    
# def strat4_anal_page():
#     global ticker_label_list
#     st.title('HOFFMAN 15 min')
#     st.markdown("""---""")
#     what_page = 4
#     my_bar = st.progress(0)
#     pecent_add = round(100 / len(ticker_label_list))
#     progress = 0
#     for t in ticker_label_list:
#         try:
#             ticker_obj = tick.Ticker(t, what_page, '30m')
#             ticker_obj.update_wallet_info(2, 1)
#             wallet = ticker_obj.get_wallet_info()
#             display = ticker_obj.get_display_wallet()
#             col1, col2, col3 = st.columns([40, 30, 30])
#             display.anal_page(t, col1, col2, col3)
                
#             progress += pecent_add
#             if progress < 100:  
#                 my_bar.progress(progress)  
#             del wallet, display, ticker_obj
#         except:
#             st.error(f'Ticker: {t} does not have any data')
#             st.markdown('---')
#     my_bar.progress(progress + (100 - progress))
#     st.success('Successfully Finished Running Strategy')
#     my_bar.empty()
    
# def strat4_wallet_page():
#     global ticker_label_list
#     st.title('Wallet Info HOFFMAN 15 min intervals')
#     st.markdown("""---""")
#     what_page = 4
#     my_bar = st.progress(0)
#     pecent_add = round(100 / len(ticker_label_list))
#     progress = 0
#     for t in ticker_label_list:
#         try:
#             ticker_obj = tick.Ticker(t, what_page, '15m')
#             ticker_obj.update_wallet_info(2, 1)
#             wallet = ticker_obj.get_wallet_info()
#             display = ticker_obj.get_display_wallet()
#             with st.expander('Ticker: ' + str(t)):
#                 col1, col2, col3 = st.columns([3, 3, 3])
#                 display.wal_header(col1, col2)
#                 display.graph_pie(col3)
#                 display.graph_wallet_info(col1, col2)
#                 display.graph_MPD_ticker()
#                 progress += pecent_add
#                 if progress < 100:  
#                     my_bar.progress(progress)  
#             del wallet, display, ticker_obj
#         except:
#             st.error(f'Ticker: {t} does not have any data')
#     my_bar.progress(progress + (100 - progress))
#     st.success('Successfully Finished Running Strategy')
#     my_bar.empty()

# https://towardsdatascience.com/how-to-add-a-user-authentication-service-in-streamlit-a8b93bf02031
names = ['Robert','name']
usernames = ['robosar','name']
passwords = ['123','name']
def signin_page():
    global names
    global usernames
    global passwords
    
    hashed_passwords = stauth.Hasher(passwords).generate()
    authenticator = stauth.Authenticate(names,usernames,hashed_passwords, 'some_cookie_name','some_signature_key',cookie_expiry_days=1)
    name, authentication_status, username = authenticator.login('Login','main')
    if authentication_status:
        st.write('Welcome *%s*' % (name))
        st.title('Some content')
    elif authentication_status == False:
        st.error('Username/password is incorrect')
    elif authentication_status == None:
        st.warning('Please enter your username and password')
    return authentication_status
    # return (name, authentication_status, username)