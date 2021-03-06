import streamlit as st
from streamlit_option_menu import option_menu
import datetime
from datetime import datetime
import tick
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import requests
from bs4 import BeautifulSoup
import pandas as pd
import numpy as np
import hydralit_components as hc
from numerize.numerize import numerize

# live usd price of bitcoin
response = requests.get('https://api.coindesk.com/v1/bpi/currentprice.json')
data = response.json()
USD_price = data['bpi']['USD']['rate_float']

# list of tickers in database
ticker_label_list = ['ADABTC', 'ONEBTC', 'HBARBTC', 'VETBTC', 'LTCBTC', 'BCHBTC', 'ETHBTC']

def get_news_info(keyticker):
    """
    _summary_
        Function used to webscrape news articles based on sprecifc string.

    Args:
        keyticker (string): string to search on yahoo financial news

    Returns:
        pd.DataFrame: return of quick news articles containing title, source, description, link, time
    """
    # empty list 
    menu_data = []
    # for page number 0, 21, 41
    for page in (0, 21, 41):
        # request url
        url = f'https://news.search.yahoo.com/search?q={keyticker}&b={page}'
        response = requests.get(url)
        # request url ---------------
        # Iniciate Beautiful Soup
        soup = BeautifulSoup(response.text, 'html.parser')
        # loop through class newsarticles and fine divs
        for news_item in soup.find_all('div', class_='NewsArticle'):
            # extract quick news info
            news_title = news_item.find('h4').text
            news_source = news_item.find('span', 's-source').text
            news_description = news_item.find('p', 's-desc').text
            news_link = news_item.find('a').get('href')
            news_time = news_item.find('span', class_='fc-2nd').text
            news_time = news_time.replace('·', '').strip()
            news_title = news_title.replace('*', '').strip()
            # extract quick news info ----------------------
            # append menu info
            menu_data.append([news_title, news_source, news_description,
                            news_link, news_time])
    # convert menu data(news) to pd.DataFrame
    return pd.DataFrame(menu_data, columns=['title', 'source', 'description', 'link', 'time'])

def strat2_anal_page(risk, reward):
    """
    _summary_
        Home and explanation page for RSI EMA ST Strategy.
        
    Args:
        risk (float): scale value to help calculate the number of shares to buy
        reward (float): scale value to help calculate the number of shares to sell
    """
    global ticker_label_list
    selected = option_menu(None, ['SUMMARY- RSI | EMA | SUPERTREND', 'Price Over Time', "Wallet Over Time"], 
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
    # home page
    if selected == 'SUMMARY- RSI | EMA | SUPERTREND':
        st.write('''
                ## RSI EMA SUPERTREND 15 min: (Please Read)
                
                #### RSI Background:
                > Originally developed by by J. Welles Wilder Jr and introduced in his seminal 1978 book, “New Concepts in Technical Trading Systems.”1
                > The relative strength index (RSI) is a momentum indicator used in used in technical analysis that measures the magnitude of recent price changes to evaluate overbought or oversold conditions in the price of a stock or other asset. 
                
                > The RSI is displayed as an oscillator and usually considered overbought when the RSI is above 70% and oversold when it is below 30%.
                > It is a line graph that moves between two extreames and usually has a range from 0 to 100. An asset is usually considered overbought when the RSI is above 70% and oversold when it is below 30%.
                
                > If entering an overbought or oversold territory traditionally this means that a trend reversal is imminent or corrective pullback in price.
                
                > **FIND OUT MORE** - https://www.investopedia.com/terms/r/rsi.asp
                
                
                #### EMA Background:
                > An exponential moving average (EMA) is a type of moving average (MA) that uses the past X number of intervals traditionally used for the close price.  The exponential moving average is also referred to as the exponentially weighted moving average. An exponentially weighted moving average reacts more significantly to recent price changes than a simple moving average simple moving average (SMA), which applies an equal weight to all observations in the period.
                
                > This technical indicator is used to produce buy and sell signals based on crossovers and divergences from the historical average.
                
                > Traders often use several different EMA lengths(X) such as 10-day, 50-day, and 200-day moving averages.
                
                > **FIND OUT MORE** - https://www.investopedia.com/terms/e/ema.asp


                #### SUPERTREND Background:
                > A Super Trend is a trend following indicator similar to moving averages. 
                
                > It is plotted on price and the current trend can simply be determined by its placement vis-a-vis price. It is a very simple indicator and is constructed with the help of just two parameters- period and multiplier.
                
                > Traditionally when we construct the Supertrend indicator strategy, the default parameters are 10 for Average True Range (ATR) and 3 for its multiplier. The average true range (ATR) plays a key role in 'Supertrend' as the indicator uses ATR to compute its value and it signals the degree of price volatility.
                
                > **FIND OUT MORE** - https://www.elearnmarkets.com/blog/supertrend-indicator-strategy-trading/#:~:text=web.stockedge.com-,Key%20Takeaways,accurate%20signals%20on%20precise%20time.
                
                #### PRICE OVER TIME PAGE:
                > This page gives a breakdown of the open, high, low, close preformance of a ticker.
                
                #### WALLET OVER TIME PAGE EXPLAINATION:
                > This page gives a breakdown of the strategy features and the preformance of the buy and sell signals based on a starting buy power amount.
                ''')
        temp = st.button('Update Database Info')
        if temp:
            # update strategy rsi ema database info
            for t in ticker_label_list:
                current_tick = tick.Ticker(t, 2, '15m')
                with st.spinner('Updating Database...'):
                    current_tick.update_strat_tables()         
            st.success(f'updated database info for all tickers.')
            
            
    elif selected == "Price Over Time":
        strat2_anal_POT(risk, reward)
    elif selected == 'Wallet Over Time':
        strat2_anal_WOT(risk, reward)
        
def strat2_anal_POT(risk, reward):
    """
    _summary_
        Price over time page to show you the tickers open, high, low, close preformance over time.
        
    Args:
        risk (float): scale value to help calculate the number of shares to buy
        reward (float): scale value to help calculate the number of shares to sell
    """
    with st.spinner('Loading Tickers Info...'):
        for t in ticker_label_list:
            st.write(f'''
                        # Ticker {t}:  
                    ''')
            current_tick = tick.Ticker(t, 2, '15m')
            
            # select strategy table for ticker t
            strat_df = current_tick.sel_tickstrat_table()
            strat_df = strat_df.drop_duplicates(subset=['datetime'])
            
            # --------------- convert to usd the graph
            strat_df['close'] = strat_df['close'] * USD_price
            strat_df['high'] = strat_df['high'] * USD_price
            strat_df['low'] = strat_df['low'] * USD_price
            strat_df['open'] = strat_df['open'] * USD_price
            # ----------------------------------------

            current_ticker_info, current_preformance, ticker_news = st.columns([30, 40 ,30])
            with current_ticker_info:
                # get the current price from strategy table 
                st.metric(label='Last 30 min Price:', value=f"{strat_df.tail(1)['close'].values[0]} USD")
                # get the current high from strategy table 
                st.metric(label='Last 30 min High:', value=f"{strat_df.tail(1)['high'].values[0]} USD")
                # get the current low from strategy table 
                st.metric(label='Last 30 min Low:', value=f"{strat_df.tail(1)['low'].values[0]} USD")


            with current_preformance:
                # themes for hydralit info cards
                theme_neutral = {'bgcolor': '#363d4a','title_color': '#f9f9f9','content_color': '#f9f9f9','icon_color': '#f9f9f9'}
                theme_bad = {'bgcolor': '#363d4a','title_color': 'red','content_color': 'red','icon_color': 'red', 'icon': 'fa fa-times-circle'}
                theme_good = {'bgcolor': '#363d4a','title_color': 'green','content_color': 'green','icon_color': 'green', 'icon': 'fa fa-check-circle'}

                # get the 2 wk Volume from strategy table
                hc.info_card(title='Last 2 wk Volume:',content=f"{numerize(sum(strat_df.tail(672)['volume']))}",theme_override=theme_neutral) 

                # get the price direction and set theme based on direction
                if round(sum(strat_df['close'].tail(672).pct_change()[1::])*100,2) < 0:
                    hc.info_card(title='Current 2 wk Price Direction/Change:', content=f"{round(sum(strat_df['close'].tail(672).pct_change()[1::])*100,2)} %",theme_override=theme_bad, sentiment='good')
                else:
                    hc.info_card(title='Current 2 wk Price Direction/Change:', content=f"{round(sum(strat_df['close'].tail(672).pct_change()[1::])*100,2)} %",theme_override=theme_good)


            with ticker_news:
                # Get news info
                news = get_news_info(t[:-3]+'Crypto').head(3)
                
                # ticker news expander
                with st.expander(f'{t[:-3]} NEWS:'):
                    st.write(f'''
                        ###### {news.iloc[0]['title']}
                        {news.iloc[0]['description']}
                        
                        Posted: {news.iloc[0]['time']}
                        
                        Checkout Article: {news.iloc[0]['link']}
                        ''')
                    st.write('---')

                    st.write(f'''
                        ###### {news.iloc[1]['title']}
                        {news.iloc[1]['description']}
                        
                        Posted: {news.iloc[1]['time']}
                        
                        Checkout Article: {news.iloc[1]['link']}
                        ''')
                    st.write('---')
                    
                    st.write(f'''
                        ###### {news.iloc[2]['title']}
                        {news.iloc[2]['description']}
                        
                        Posted: {news.iloc[2]['time']}
                        
                        Checkout Article: {news.iloc[2]['link']}
                        ''')
                # ticker news expander ------------------------------
                        
             # graph candle stick chart with close price
            fig = make_subplots(rows=2, cols=1, subplot_titles=("Candle Stick Chart with Close Price", "Volume Amount"), vertical_spacing=0.25, shared_xaxes=True)
            fig.append_trace(go.Candlestick(
                                            x=strat_df['datetime'],
                                            open=strat_df['open'], high=strat_df['high'],
                                            low=strat_df['low'], close=strat_df['close'],
                                            increasing_line_color= 'green', decreasing_line_color= 'red', 
                                            opacity=0.6, line={'width':3}, legendgroup='group1'
                                        ),  
                            row=1, col=1)  
            fig.append_trace(go.Scatter(
                                    x = strat_df['datetime'], y = strat_df['close']-(strat_df['close']*0.1),
                                    line=dict(color='grey', width=3), opacity=0.5, legendgroup='group1', showlegend=False
                                    ), 
                            row=1, col=1)
            fig.data[0].name = '30 min candle sticks' 
            fig.append_trace(go.Bar(x=strat_df['datetime'], y=strat_df['volume'], opacity=.7, marker={'color': 'green'}, legendgroup='group2', name="Volume Amount"), row=2, col=1)
            fig.update_layout(
                height=600)
            plot = st.plotly_chart(fig, use_container_width=True)
            # graph candle stick chart with close price -----------------------------------------------------------
            st.write('---')

def strat2_anal_WOT(risk, reward):
    """_summary_
        Function to set up Wallet over Time page for Strat RSI EMA ST
    Args:
        risk (float): The amount of current shares im willing to risk  
        reward (float): The amount of current shares im willing to sell
    """
    # set up streamlit columns
    start_end_date, current_ticker_select, multi_selector, button = st.columns([30, 30, 30, 10])
    
    # get ticker strategy min and max datetime
    connection = tick.Ticker(strat=2, interval='15m')
    min_max_datetime = connection.get_min_max_datetime()
    # get max date range
    max_datetime = min_max_datetime['max'][0]
    # get min date range
    min_datetime = min_max_datetime['min'][0]
    del min_max_datetime, connection
    # get ticker strategy min and max datetime -------------------------------------------------
    
    # create session state vairable
    if 'min_max_datetime' not in st.session_state:
        st.session_state['min_max_datetime'] = [min_datetime, max_datetime]
    # reset if already created
    elif 'min_max_datetime' in st.session_state:
        st.session_state['min_max_datetime'] = [min_datetime, max_datetime]
    # create session state vairable ----------------------------------------
    
    # get date range to pull from database
    with start_end_date:
        st.session_state['start_date'] = st.date_input(
            "Select A Start Date",
            st.session_state['min_max_datetime'][0].to_pydatetime(),
            min_value=st.session_state['min_max_datetime'][0].to_pydatetime(),
            max_value=st.session_state['min_max_datetime'][1].to_pydatetime())
        st.session_state['end_date'] = st.date_input(
            "Select and End Date",
            st.session_state['min_max_datetime'][0].to_pydatetime(),
            min_value=st.session_state['min_max_datetime'][0].to_pydatetime(),
            max_value=st.session_state['min_max_datetime'][1].to_pydatetime())
    # get date range to pull from database -----------------------------------
    
    # ---------------------------------------------
    # print(pd.Timestamp(st.session_state['start_date']), pd.Timestamp(st.session_state['end_date']))
    # ---------------------------------------------

    # options to select
    with multi_selector:
        tickers = st.multiselect(
                                'Tickers you would like to see.',
                                ticker_label_list
                                )
    with current_ticker_select:
        st.write('Your start date is:', st.session_state['start_date'])
        st.write('Your end date is:', st.session_state['end_date'])
        st.write('Current Selected:', tickers)
    st.write('---')
    with button:
        b = st.button('Process Request')
    # options to select -----------------------------------------------
    
    # if process request is True
    if b:
        # convert start and end date range
        start_date = pd.Timestamp(np.datetime64(datetime.strptime(str(st.session_state['start_date']), '%Y-%m-%d'))).tz_localize('UTC').tz_convert('UTC')
        end_date = pd.Timestamp(np.datetime64(datetime.strptime(str(st.session_state['end_date']), '%Y-%m-%d'))).tz_localize('UTC').tz_convert('UTC')
        
        # for each ticker in multiselector
        for t in tickers:
            
            # set up ticker class object
            current_tick = tick.Ticker(t, 2, '15m')
            
            # select strategy df inbetween start and end date
            strat_df = current_tick.sel_tickstrat_table()
            strat_df.drop_duplicates(inplace=True)
            strat_df['datetime'] = pd.to_datetime(strat_df['datetime'])
            strat_df = strat_df[(strat_df['datetime'] > start_date) & (strat_df['datetime'] < end_date)]
            # select strategy df inbetween start and end date ------------------------------------------

            # update wallet info with strat table
            wallet = current_tick.update_wallet_info(risk, reward)
            
            # if wallet has no buy or sell cues
            if len(wallet) <= 2:
                with st.expander(f'{t[:-3]} Wallet Info'):
                    # make empty waller_buy and sell
                    wallet_buy, wallet_sell = pd.DataFrame(), pd.DataFrame()
                    st.error('No wallet buy or sell signals Triggered')
                        
                    fig = rsi_ema_st_strat_graph(strat_df, wallet_buy, wallet_sell, sig_exists=False)
                    plot = st.plotly_chart(fig, use_container_width=True, height=800)
            # if wallet has buy and sell ques
            if len(wallet) > 2:
                # format wallet to be able to graph buy and sell signals
                final_wallet = pd.DataFrame(wallet)
                final_wallet['diff'] = final_wallet['Total_Buy_Power'].diff()
                inital_wallet = final_wallet.iloc[0]
                last_wallet = final_wallet.iloc[-1]
                final_wallet['Datetime'] = pd.to_datetime(final_wallet['Datetime'], format='%Y%m%d-%H%M%S')
                final_wallet['b_s'] = final_wallet['b_s'].astype(bool)
                final_wallet = final_wallet[(final_wallet['Datetime'] > start_date) & (final_wallet['Datetime'] < end_date)]
                # format wallet to be able to graph buy and sell signals ----------------------------------------------------
                
                with st.expander(f'{t[:-3]} Wallet Info'):
                    # streamlit columns
                    col1, col2, col3 = st.columns([15,15,70])
                    # seperate buy and sell signals
                    wallet_buy = final_wallet[final_wallet['b_s'] == True]
                    wallet_sell = final_wallet[final_wallet['b_s'] == False]
                    # display metric data
                    with col1:
                        st.metric(label="Shares Ended With:", value=f"{last_wallet['Shares']}", delta=f"{last_wallet['Shares'] - inital_wallet['Shares']}")
                        st.metric(label="Long vs. ShortPosition Ratio:", value=f"{last_wallet['Long_Positions']/last_wallet['Short_Poistions']}")
    
                    with col2:
                        st.metric(label="Ending Buy Power:", value=f"{last_wallet['Current_Buy_Power']}", delta=f"{last_wallet['Current_Buy_Power'] - inital_wallet['Current_Buy_Power']}")
                    # display metric data -------------------------------------------------------------------------------------------------------------------------------------------------
                    
                    # display wallet worth over time 
                    with col3:
                        fig = make_subplots(rows=1, cols=1, subplot_titles="Wallet Worth over Time", vertical_spacing=0.1, shared_xaxes=True)
                        fig.append_trace(
                            go.Waterfall(
                                x = final_wallet['Datetime'],y = final_wallet['diff'],
                                decreasing = {"marker":{"color":"red", "line":{'width':4, "color":"red"}}},
                                increasing = {"marker":{"color":"green", "line":{'width':4, "color":"green"}}},
                                connector = {"line":{"color":"#FFFFFF", 'dash': 'dot', 'width':2}},
                            ), row=1, col=1)
                        plot = st.plotly_chart(fig, use_container_width=True, use_container_height=True)   
                    # display wallet worth over time --------------------------------------------------
                    
                    # display strat graph
                    fig = rsi_ema_st_strat_graph(strat_df, wallet_buy, wallet_sell, sig_exists=True)
                    plot = st.plotly_chart(fig, use_container_width=True, height=800)
                    # display strat graph ------------------------------------------
            del strat_df, wallet_buy, wallet_sell

def rsi_ema_st_strat_graph(strat_df, buy_df, sell_df, sig_exists=True):
    """_summary_

    Args:
        strat_df (pd.DataFrame): df that contains the open, high, low, close, volume with additional feature engineering
        buy_df (pd.DataFrame): df contain buy signals
        sell_df (pd.DataFrame): df containing sell signals
        sig_exists (bool, optional): Graph buy and sell signals if it exsists. Defaults to True.

    Returns:
        plotly subplot: plot to display in streamlit
    """
    fig = make_subplots(rows=2, cols=1, subplot_titles=("RSI EMA SUPERTREMD Strategy", ''), vertical_spacing=0.1, shared_xaxes=True)
    fig.append_trace(
        go.Scatter(
            x=strat_df['datetime'], y=strat_df['close'], opacity=0.5, 
            line={'width':3, 'color':'grey'}, legendgroup='group1', name='Close Price'
        ),  row=1, col=1)
    fig.append_trace(
        go.Scatter(
            x=strat_df['datetime'], y=strat_df['ema_200'], opacity=0.4, 
            line={'width':3, 'color':'yellow'}, legendgroup='group1', name='EMA 200'
        ),  row=1, col=1)
    fig.append_trace(
        go.Scatter(
            x=strat_df['datetime'], y=strat_df['supertl'], opacity=0.4, 
            line={'width':3, 'color':'green'}, legendgroup='group1', name='ST +'
        ),  row=1, col=1)
    fig.append_trace(
        go.Scatter(
            x=strat_df['datetime'], y=strat_df['superts'], opacity=0.4, 
            line={'width':3, 'color':'red'}, legendgroup='group1', name='ST -'
        ),  row=1, col=1)
    fig.append_trace(
        go.Scatter(
            x=strat_df['datetime'], y=strat_df['rsi_14'], opacity=0.4, 
            line={'width':3, 'color':'blue'}, legendgroup='group2', name='RSI'
        ),  row=2, col=1)
    if sig_exists:
        wallet_buy = buy_df.copy()
        wallet_sell = sell_df.copy()
        wallet_buy['close'] = wallet_buy.iloc[:, -4]/USD_price
        wallet_sell['close'] = wallet_sell.iloc[:,-4]/USD_price
        fig.append_trace(
            go.Scatter(
                x=wallet_buy["Datetime"], y=wallet_buy["close"], opacity=1, 
                line={'color':'green'}, mode="markers", legendgroup='group3', name='Buy Signal'
            ),  row=1, col=1)
        fig.append_trace(
            go.Scatter(
                x=wallet_sell["Datetime"], y=wallet_sell["close"], opacity=1,
                line={'color':'red'}, mode="markers", legendgroup='group3', name='Sell Signal'
            ),  row=1, col=1)
    fig.update_layout(height=800, width=800, font=dict(size=15, color='#e1e1e1'))
    fig.update_xaxes(title_text="Datetime", gridcolor='#1f292f', 
                    showgrid=True, row=1, col=1)
    fig.update_yaxes(title_text="Price", gridcolor='#1f292f', 
                    showgrid=True, row=1, col=1) 
    fig.update_yaxes(title_text="RSI", 
                    showgrid=True, row=2, col=1) 
    return fig
    