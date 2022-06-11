import streamlit as st
ticker_label_list = ['ADABTC', 'ONEBTC', 'HBARBTC', 'VETBTC', 'LTCBTC', 'BCHBTC', 'ETHBTC']
def my_home():
    """_summary_
        - Display streamlit home
    """
    # main page info 
    st.title('Stock/Crypto Strategy Back-Tester')
    st.write('''
            
            ### Project Objective:
            > The Stock and Crypto market is very scary and unpredictable. What do I buy? How much do I buy? Why do I keep losing money?  Are all very common question when entering the market.  Unfortunately the answer to all these questions is "It depends."  The goal of this specific project is to give you an edge by using candle stick trend analysis strategies and a machine learning forecaster that predicts the close price to help you understand when to enter the market and when to leave the market.  The main objective is to maximize your gains in your "wallet" or alternatively minimize your losses in your "wallet".
            
            ### Quick Process Explaination:
            > BOT
            1) Go through each ticker id
            2) Go through each strategy id
            2) Get historical ticker information From Biance. (Datetime, Open, High, Low, Close, Volume)
                - Save information into a database organized by the **ticker id** and **strategy id**.
            3) Run every 15 min interval to push historical ticker information into a Database
            > BACKTESTER
            1) Go through each ticker id 
            2) Strategy **Home Page** and **Price Over Time Page**. (POT)
                - Depending on strategy selected by user convert historical ticker information to get strategy specific ticker information. (feature engineering Open, High, Low, Close, Volume)
            3) Strategy **Wallet Over Time Page**
                - Find Buy signals and Sell signals in strategy specific ticker information.
            4) Explore this information on web app.
            
            - Note: Tickers currently allowed to explore are:
                - ADA - https://coinmarketcap.com/currencies/cardano/
                - ONE - https://coinmarketcap.com/currencies/harmony/
                - HBAR - https://coinmarketcap.com/currencies/hedera/
                - VET - https://coinmarketcap.com/currencies/vechain/
                - LTC - https://coinmarketcap.com/currencies/litecoin/
                - BCH - https://coinmarketcap.com/currencies/bitcoin-cash/
                - ETH - https://coinmarketcap.com/currencies/ethereum/
                
            ### Strategies Created: **Click on the Sub menu in the navigation bar to learn more**
            
            > PSAR + MACD + EMA:
            
            > RSI + EMA + Supertrend
            
            > Hoffman

            
            - ** Not easily understood by non-experts. The investments and services offered by us may not be suitable for all investors. If you have any doubts as to the merits of an investment, you should seek advice from an independent financial advisor.**
            ''')
    # main page info ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------