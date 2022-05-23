from turtle import width
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
import streamlit as st
import matplotlib.pyplot as plt
import json
import requests
#######################################################
#######################################################
#######################################################
#######################################################
#######################################################
#######################################################
# https://discuss.streamlit.io/t/streamlit-option-menu-is-a-simple-streamlit-component-that-allows-users-to-select-a-single-item-from-a-list-of-options-in-a-menu/20514
#######################################################
#######################################################
#######################################################
#######################################################
#######################################################
#######################################################

class Display_Wallet:
    def __init__(self, wallet, buy_sell_df, historical_df):
        """_summary_
            - init object varibles
        Args:
            wallet (wallet obj): _description_
            historical_df (pd.Dataframe): raw histoical data
            buy_sell_df (pd.Dataframe): buy and sell data based on strategy
        """
        self.buy_sell_df = buy_sell_df
        self.historical_df = historical_df
        self.wallet_info = wallet
        response = requests.get('https://api.coindesk.com/v1/bpi/currentprice.json')
        data = response.json()
        self.data = data['bpi']['USD']['rate_float']

    def graph_MPD_ticker(self):
        """_summary_
            - graph waterfall chart of buy and sell ques
            - graph raw historical data candle sticks
        """
        # first graph data
        buy_data = self.buy_sell_df.loc[(self.buy_sell_df['b_s'] == True)]
        sell_data = self.buy_sell_df.loc[(self.buy_sell_df['b_s'] == False)]
        
        # second graph data
        ans = self.buy_sell_df.copy()
        ans['diff'] = ans['close'].diff()
        
        # make figure

        if len(ans['diff']) > 1:
            fig = make_subplots(rows=2, cols=1, subplot_titles=("Price Over Time", "Difference of Each Buy and Sell"), vertical_spacing=0.1, shared_xaxes=True)
            
            # first graph
            # graph1 = go.Figure()
            fig.append_trace(
                go.Candlestick(
                            x=self.historical_df['datetime'],
                            open=self.historical_df['open'], high=self.historical_df['high'],
                            low=self.historical_df['low'], close=self.historical_df['close'],
                            increasing_line_color= 'green', decreasing_line_color= 'red', opacity=0.6, line={'width':3}),  row=2, col=1)
            fig.data[0].name = '30 min candle sticks'
            fig.append_trace(
                go.Candlestick(x=buy_data['datetime'],
                            open=buy_data['open'], high=buy_data['high'],
                            low=buy_data['low'],close=buy_data['close'],
                            increasing_line_color= '#C080FF', decreasing_line_color= '#C080FF', opacity=0.9,line={'width':3}),  row=2, col=1)
            fig.data[1].name = 'buy signals'
            fig.append_trace(
                go.Candlestick(x=sell_data['datetime'],
                            open=sell_data['open'], high=sell_data['high'],
                            low=sell_data['low'],close=sell_data['close'],
                            increasing_line_color= '#FFFF40', decreasing_line_color= '#FFFF40', opacity=0.9, line={'width':4}),  row=2, col=1)
            fig.data[2].name = 'sell signals'
            # text = round(ans['diff'], 4),
            fig.append_trace(go.Waterfall(
                x = ans['datetime'],
                y = ans['diff'],
                decreasing = {"marker":{"color":"#FFFF00", "line":{'width':4, "color":"#FFFF00"}}},
                increasing = {"marker":{"color":"#8000C0", "line":{'width':4, "color":"#8000C0"}}},
                connector = {"line":{"color":"#FFFFFF", 'dash': 'dot', 'width':2}},), row=1, col=1)
            fig.data[3].name = 'Market Price Diff'
            
            fig.update_layout(height=800, width=800, title_text="Price Over Time", margin=dict(l=10,r=10, b=10, t=10), font=dict(size=15, color='#e1e1e1'))
            fig.update_xaxes(title_text="Datetime", gridcolor='#1f292f', 
                            showgrid=True, row=2, col=1)
            
            fig.update_yaxes(title_text="Price", gridcolor='#1f292f', 
                            showgrid=True, row=2, col=1)
            fig.update_yaxes(title_text="Difference", gridcolor='#1f292f', 
                            showgrid=True, row=1, col=1)
            fig.update_layout(legend=dict( yanchor="top", y=-.1,
                                        xanchor="left", x=.33))
        else:
            fig = make_subplots(rows=1, cols=1, subplot_titles=("Price Over Time"), vertical_spacing=0.1, shared_xaxes=True)
            
            # first graph
            # graph1 = go.Figure()
            fig.append_trace(
                go.Candlestick(
                            x=self.historical_df['datetime'],
                            open=self.historical_df['open'], high=self.historical_df['high'],
                            low=self.historical_df['low'], close=self.historical_df['close'],
                            increasing_line_color= 'green', decreasing_line_color= 'red', opacity=0.6, line={'width':3}),  row=1, col=1)
            fig.data[0].name = '30 min candle sticks'
            fig.append_trace(
                go.Candlestick(x=buy_data['datetime'],
                            open=buy_data['open'], high=buy_data['high'],
                            low=buy_data['low'],close=buy_data['close'],
                            increasing_line_color= '#C080FF', decreasing_line_color= '#C080FF', opacity=0.9,line={'width':3}),  row=1, col=1)
            fig.data[1].name = 'buy signals'
            fig.append_trace(
                go.Candlestick(x=sell_data['datetime'],
                            open=sell_data['open'], high=sell_data['high'],
                            low=sell_data['low'],close=sell_data['close'],
                            increasing_line_color= '#FFFF40', decreasing_line_color= '#FFFF40', opacity=0.9, line={'width':4}),  row=1, col=1)
            fig.data[2].name = 'sell signals'
            fig.update_layout(height=800, width=800, title_text="Price Over Time", margin=dict(l=10,r=10, b=10, t=10), font=dict(size=15, color='#e1e1e1'))
            fig.update_xaxes(title_text="Datetime", gridcolor='#1f292f', 
                            showgrid=True, row=1, col=1)
            
            fig.update_yaxes(title_text="Price", gridcolor='#1f292f', 
                            showgrid=True, row=1, col=1)
            fig.update_layout(legend=dict( yanchor="top", y=-.1,
                                        xanchor="left", x=.33))
        # layout options

        # https://www.youtube.com/watch?v=t-f2NDKE8G8
        
        plot = st.plotly_chart(fig, use_container_width=True, height=800)   
        
    # https://towardsdatascience.com/pie-donut-charts-with-plotly-d5524a60295b
    def graph_pie(self, col3):
        """_summary_
            - graph pie chart to show good buys vs bad buys
        Args:
            col3 (streamlit col): page seperator to display on streamlit app
        """
        with col3:
            c = st.container()
            

            fig = px.pie(values=[self.wallet_info['Losses'], self.wallet_info['Wins']], 
                        names=['Bad Exits', 'Good Entries'], 
                        color=['Losses', 'Wins'],
                        hole = 0.6,
                        color_discrete_map={'Losses':'red',
                                            'Wins':'green'},
                        )
            fig.update_layout(
                height=350, width=300,
                legend=dict(yanchor="top", y=0.05, xanchor="left", x=0.6),
                margin=dict(l=10, r=10, b=10, t=10, pad=0))
            fig.add_annotation(x= 0.5, y = 0.5,
                            text = 'Good Vs Bad',
                            font = dict(size=20,family='Verdana', color='white'),
                            showarrow = False)
            plot = c.plotly_chart(fig)
            temp = self.wallet_info['Last_Element'] - self.wallet_info['First_Element']
            c.subheader(f'Time Period Over -- {temp}')
    
    def wal_header(self, col1, col2):
        """_summary_
            Display Wallet Header
        Args:
            col3 (streamlit col): page seperator to display on streamlit app
            col3 (streamlit col): page seperator to display on streamlit app
        """
        with col1:
            c = st.container()
            c.metric(label="Shares Ended With", value=str(round(self.wallet_info['Shares'], 4)))
            c.markdown("""---""")
        with col2:
            c = st.container()
            c.metric(label="Ending Buy Power", value='$ ' + str(round(self.wallet_info['Ending_Buy_Power']*self.data, 5)) + ' USD', delta=str(round(self.wallet_info['Ending_Buy_Power']*self.data - self.wallet_info['Starting_Buy_Power']*self.data,5))+ '')
            c.markdown("""---""")
    def graph_wallet_info(self, col1, col2):
        """_summary_
            - display wallet information on streamlit app
        Args:
            col1 (streamlit col): page seperator to display on streamlit app
            col2 (streamlit col): page seperator to display on streamlit app
        """
        theme_bad = {'bgcolor': '#FFF0F0','title_color': 'red','content_color': 'red','icon_color': 'red', 'icon': 'fa fa-times-circle'}
        theme_neutral = {'bgcolor': '#f9f9f9','title_color': 'orange','content_color': 'orange','icon_color': 'orange', 'icon': 'fa fa-question-circle'}
        theme_good = {'bgcolor': '#EFF8F7','title_color': 'green','content_color': 'green','icon_color': 'green', 'icon': 'fa fa-check-circle'}
        
        # ans = self.buy_sell_df.copy()
        # ans['diff'] = ans['close'].diff()
        with col1:
            c = st.container()
            c.metric(label='Long Position Entries:', value=self.wallet_info['Long_Positions'])
            c.markdown("""---""")
            c.metric(label='Longest Win Streak:', value=str(self.wallet_info['Longest_Win_Streak']))
            c.markdown("""---""")
            c.metric(label='Total Wins:', value=str(round(self.wallet_info['Wins'], 4)))
        with col2:
            c = st.container()
            c.metric(label='Short Position Exits:', value=self.wallet_info['Short_Poistions'])
            c.markdown("""---""")
            c.metric(label='Longest Loss Streak:', value=str(self.wallet_info['Longest_Loss_Streak']))
            c.markdown("""---""")
            c.metric(label='Total Losses:', value=str(round(self.wallet_info['Losses'], 4)))
    
    def anal_page(self, ticker_name, col1, col2 , col3):
        """_summary_
            - display analysis wallet information on streamlit app
        Args:
            col1 (streamlit col): page seperator to display on streamlit app
            col2 (streamlit col): page seperator to display on streamlit app
            col3 (streamlit col): page seperator to display on streamlit app
        """
        st.header(ticker_name + ' Quick Summary')
        with col1:
            c = st.container()
            c.metric(label='Starting Buy Power', value= str(self.wallet_info['Starting_Buy_Power']) + ' BTC')
            c.metric(label="Ending Buy Power", value='$ ' + str(round(self.wallet_info['Ending_Buy_Power']*self.data, 5)) + ' USD', delta=str(round(self.wallet_info['Ending_Buy_Power']*self.data - self.wallet_info['Starting_Buy_Power']*self.data, 5)))
        with col2:
            c = st.container()
            c.metric(label='Shares Started With', value=0)
            c.metric(label="Shares Ended With", value=str(round(self.wallet_info['Shares'], 5)))
            
        with col3:
            c = st.container()
            c.header("First Signal:")
            c.subheader(f"{self.wallet_info['First_Element']} PT")
            c.header("Last Signal:")
            c.subheader(f"{self.wallet_info['Last_Element']} PT")
        # https://plotly.com/python-api-reference/generated/plotly.graph_objects.Bar.html
        c = st.container()
        
        range_y = self.historical_df['datetime'].tail(50).values
        # layout = go.Layout(
        #     xaxis=dict(
        #         range=[range_y[0], range_y[-1]]
        #     )
        # )
        # print(type(range_y[0]))
        # hover_data={"date": "|%B %d, %Y"}
        try:

            fig = make_subplots(rows=2, cols=1, subplot_titles=("Close Price Over Time", "Volume Over Time"), vertical_spacing=0.1, shared_xaxes=True)
            fig.append_trace(go.Scatter(x = self.historical_df['datetime'], y = self.historical_df['close'],line=dict(color='light blue', width=3), opacity=0.7), row=1, col=1)
            fig.data[0].name = 'Close Over Time'
            fig.append_trace(go.Bar(x=self.historical_df['datetime'], y=self.historical_df['volume'], opacity=.7, marker={'color': 'green'}), row=2, col=1)
            fig.data[1].name = 'Volume Over Time'
            fig.update_layout(
                height=600,
                width= 1500)
            plot = c.plotly_chart(fig)
        except:
            st.error('problem graphing')
            
        st.markdown("""---""")