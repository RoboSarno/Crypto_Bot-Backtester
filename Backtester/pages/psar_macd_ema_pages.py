from PIL import Image
import streamlit as st
from streamlit_option_menu import option_menu
import datetime 

ticker_label_list = ['ADABTC', 'ONEBTC', 'HBARBTC', 'VETBTC', 'LTCBTC', 'BCHBTC', 'ETHBTC']
def strat1_anal_page(risk, reward):
    # --------------------------------------------------------------------------------
    global ticker_label_list
    selected = option_menu(None, ['HOME - PSAR | MAC | EMA', 'Price Over Time', "Wallet Over Time"], 
        icons=['house', 'list-task', "list-task"], 
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
    if selected == 'HOME - PSAR | MAC | EMA':
        st.write('''
                ## PSAR MACD EMA 30 min:
                
                ### Explain PSAR:
                
                ### Explain MACD:
                
                ### EXPLAIN EMA:
                
                ### SAY THE STRENGTHS AND WEEKNESSES OF THESE STRATAGIES:
                
                #### PRICE OVER TIME PAGE EXPLINATION:
                
                #### WALLET OVER TIME PAGE EXPLAINATION:
                
                
                ''')
    elif selected == "Price Over Time":
        strat1_anal_POT(risk, reward)
    elif selected == "Wallet Over Time":
        strat1_anal_WOT(risk, reward)
def strat1_anal_POT(risk, reward):
    for t in ticker_label_list:
        st.write(f'''
                    # Ticker {t}:  
                ''')

        current_ticker_info, current_preformance, ticker_news = st.columns([30, 40 ,30])
        with current_ticker_info:
            st.write('''
                    ### Current Price:
                    ''')
            image = Image.open('/Users/robertsarno/Documents/Spring_2022/Side_Projects/Crypto_Bot/bot/V1/Backtester/pages/metric.png')
            st.image(image)
            st.write('''
                    ### Current High:
                    ''')
            image = Image.open('/Users/robertsarno/Documents/Spring_2022/Side_Projects/Crypto_Bot/bot/V1/Backtester/pages/metric.png')
            st.image(image)
            st.write('''
                    ### Current Low:
                    ''')
            image = Image.open('/Users/robertsarno/Documents/Spring_2022/Side_Projects/Crypto_Bot/bot/V1/Backtester/pages/metric.png')
            st.image(image)

        with current_preformance:
            st.write('''
                    ### Last 52 wk Volume:
                    ''')
            image = Image.open('/Users/robertsarno/Documents/Spring_2022/Side_Projects/Crypto_Bot/bot/V1/Backtester/pages/metric.png')
            st.image(image)
            st.write('''
                    ### Current Price direction: %
                    ''')
            image = Image.open('/Users/robertsarno/Documents/Spring_2022/Side_Projects/Crypto_Bot/bot/V1/Backtester/pages/metric.png')
            st.image(image)
        with ticker_news:
            with st.expander(f'{t} NEWS:'):
                st.write('''
                    ### News1
                    ''')
                image = Image.open('/Users/robertsarno/Documents/Spring_2022/Side_Projects/Crypto_Bot/bot/V1/Backtester/pages/metric.png')
                st.image(image)
                st.write('''
                    ### News2:
                    ''')
                image = Image.open('/Users/robertsarno/Documents/Spring_2022/Side_Projects/Crypto_Bot/bot/V1/Backtester/pages/metric.png')
                st.image(image)
                st.write('''
                    ### News3:
                    ''')
                image = Image.open('/Users/robertsarno/Documents/Spring_2022/Side_Projects/Crypto_Bot/bot/V1/Backtester/pages/metric.png')
                st.image(image)
        st.write('''
                ### Price and Volume over time Graph:
            ''')      
        image = Image.open('/Users/robertsarno/Documents/Spring_2022/Side_Projects/Crypto_Bot/bot/V1/Backtester/pages/graph.png')
        st.image(image)
        st.write('---')


    # -------------------------------------------------------------
    # what_page = 1
    # my_bar = st.progress(0)
    # pecent_add = round(100 / len(ticker_label_list))
    # progress = 0
    # for t in ticker_label_list:
    #     try:
    #         ticker_obj = tick.Ticker(t, what_page, '30m')
    #         ticker_obj.update_wallet_info(risk, reward)
    #         wallet = ticker_obj.get_wallet_info()
    #         display = ticker_obj.get_display_wallet()
    #         col1, col2, col3 = st.columns([40, 30, 30])
    #         display.anal_page(t, col1, col2, col3)
                
    #         progress += pecent_add
    #         if progress < 100:  
    #             my_bar.progress(progress)  
    #         del wallet, display, ticker_obj
    #     except:
    #         st.error(f'Ticker: {t} does not have any data')
    #         st.markdown('---')
    # my_bar.progress(progress + (100 - progress))
    # st.success('Successfully Finished Running Strategy')
    # my_bar.empty()
    
    
    # https://pub.towardsai.net/time-series-forecasting-in-python-4e7d65580b9

def strat1_anal_WOT(risk, reward):

        start_end_date, current_ticker_select, multi_selector, button = st.columns([30, 30, 30, 10])
        with start_end_date:
            start = st.date_input(
                "Select A Start Date",
                datetime.date(2019, 7, 6))
            end = st.date_input(
                "Select and End Date",
                datetime.date(2019, 7, 6))

        with multi_selector:
            tickers = st.multiselect(
                                    'Tickers you would like to see.',
                                    ticker_label_list
                                    )
        with current_ticker_select:
            st.write('Your start date is:', start)
            st.write('Your end date is:', end)
            st.write('Current Selected:', tickers)
        st.write('---')

        with button:
            b = st.button('Process Request')
            

        if b:
            for t in tickers:
                with st.expander(f'{t} Wallet Info'):
                    col1, col2, col3 = st.columns([15,15,70])
                    with col1:
                        st.write('''
                                ### Shares Ended With:
                            ''')      
                        image = Image.open('/Users/robertsarno/Documents/Spring_2022/Side_Projects/Crypto_Bot/bot/V1/Backtester/pages/metric.png')
                        st.image(image)
                        st.write('''
                                ### Long vs. ShortPosition Ratio:
                            ''')      
                        image = Image.open('/Users/robertsarno/Documents/Spring_2022/Side_Projects/Crypto_Bot/bot/V1/Backtester/pages/metric.png')
                        st.image(image)
                    with col2:
                        st.write('''
                                ### Ending Buy Power from Starting:
                            ''')      
                        image = Image.open('/Users/robertsarno/Documents/Spring_2022/Side_Projects/Crypto_Bot/bot/V1/Backtester/pages/metric.png')
                        st.image(image)
                        st.write('''
                                ### Wins vs losses
                            ''')      
                        image = Image.open('/Users/robertsarno/Documents/Spring_2022/Side_Projects/Crypto_Bot/bot/V1/Backtester/pages/metric.png')
                        st.image(image)
                    with col3:
                        st.write('''
                                ### WaterFall Chart
                            ''')      
                        image = Image.open('/Users/robertsarno/Documents/Spring_2022/Side_Projects/Crypto_Bot/bot/V1/Backtester/pages/graph.png')
                        st.image(image)
                    st.write('''
                        ## Strategy Graphed - Signals Pointed out Graphed.
                    ''')      
                    image = Image.open('/Users/robertsarno/Documents/Spring_2022/Side_Projects/Crypto_Bot/bot/V1/Backtester/pages/graph.png')
                    st.image(image)
        st.write('''
                # ...
                
                
                # ...
                
                
                # ...
                
                
                # ...
                
                
                # n
                ''')
        # ----------------
                
                

    
    # -------------------------------------------------------------
    # st.markdown("""---""")
    # what_page = 1
    # my_bar = st.progress(0)
    # pecent_add = round(100 / len(ticker_label_list))
    # progress = 0
    # for t in ticker_label_list:
    #     try:
    #         ticker_obj = tick.Ticker(t, what_page, '30m')
    #         ticker_obj.update_wallet_info(risk, reward)
    #         wallet = ticker_obj.get_wallet_info()
    #         display = ticker_obj.get_display_wallet()
    #         with st.expander('Ticker: ' + str(t)):
    #             col1, col2, col3 = st.columns([3, 3, 3])
    #             display.wal_header(col1, col2)
    #             display.graph_pie(col3)
    #             display.graph_wallet_info(col1, col2)
    #             display.graph_MPD_ticker()
    #             progress += pecent_add
    #             if progress < 100:  
    #                 my_bar.progress(progress)  
    #         del wallet, display, ticker_obj
    #     except:
    #         st.error(f'Ticker: {t} does not have any data')
    # my_bar.progress(progress + (100 - progress))
    # st.success('Successfully Finished Running Strategy')
    # my_bar.empty()
