import pandas as pd
import funds
import apicon
import tickobjs
import requests

response = requests.get('https://api.coindesk.com/v1/bpi/currentprice.json')
data = response.json()
bitcoin_price_USD = data['bpi']['USD']['rate_float']


class Ticker:
    def __init__(self, ticker_lab='', strat=0, interval=''):
        """_summary_
            - init ticker object
            
        Args:
            ticker_lab (string): ticker label
            strat (int): strategy id
            interval (string): used to signal what table to pull from
        """
        self.TICKER_ID = ticker_lab
        self.STRAT = strat
        self.INTERVAL = interval
        
        self.db_connection = apicon.Database()
        
        self.wallet = None
        
        self.last_action = None
        self.display_wallet = None
        
    def update_wallet_info(self, risk, reward):
        """_summary_
            - Updates wallet information based on risk and reward floats given
        Args:
            risk (float): is the amount of money your will to risk based on current wallets worth
            reward (float): is the amount of money your willing to sell based on current wallets worth
        """
        # select strat table
        s_df = self.db_connection.select_strat_data(self.STRAT, self.TICKER_ID)
        
        # drop duplicates
        if self.STRAT == 1 or self.STRAT == 2:
            s_df = s_df.drop_duplicates()
        if self.STRAT == 4:
            s_df = s_df.drop_duplicates().dropna()
            
        # NEED TO RESTRUCTURE STRATEGY TABLE SCHEMA !!!!!!!!!!!!!!!!!!!!!!
        # print(s_df.drop_duplicates().dropna())
        # !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
        
        # create buy and sell df
        bs_loch_df = self.db_connection.get_buy_sell_times_df(strat_df=s_df, strategy=self.STRAT,ticker=self.TICKER_ID)
        
        # select raw historical data based on ticker id
        historical_df = self.db_connection.select_historical_data(self.STRAT, self.TICKER_ID)

        # left join the historical df (open close, hight, low) and Buy and sell signals df (datetime, ticker_id,  b_s)
        bs_loch_df = pd.merge(bs_loch_df, historical_df, left_on='datetime', right_on='datetime', how='left').drop(columns=['ticker_id_y'])
        bs_loch_df.rename(columns={'ticker_id_x': 'ticker_id'}, inplace=True)
        # get USD Currency
        bs_loch_df [['open', 'high', 'low', 'close' ]]= bs_loch_df[['open', 'high', 'low', 'close' ]] * bitcoin_price_USD

        # create fake wallet instance
        if bs_loch_df.empty:
            self.wallet = funds.Wallet(bs_loch_df,  None, self.TICKER_ID)
            wallet = self.wallet.run_wallet_change(risk, reward, self.STRAT)
            return wallet
        else:
            last_datetime_close = bs_loch_df['close'].iloc[-1]
            self.wallet = funds.Wallet(bs_loch_df,  last_datetime_close, self.TICKER_ID)
            wallet = self.wallet.run_wallet_change(risk, reward, self.STRAT)
            return wallet
        # create fake wallet instance --------------------------------------
        
        
    def update_strat_tables(self):
        # get buy and sell table
        buy_sell_table_df = self.db_connection.select_historical_data(self.STRAT, self.TICKER_ID)
        
        # get strategy dataframe
        strat = tickobjs.Strategy(raw_df=buy_sell_table_df, ticker_id=self.TICKER_ID)
        if self.STRAT == 1:
            strat.psar()
            strat.macd()
            strat.ema()
            strat.add_db_elements(self.STRAT)
            result = strat.get_strat_df()
            # push strategy df to strategy table db 
            self.db_connection.insert_strat_table(df=result, strategy=self.STRAT)

        elif self.STRAT == 2:
            strat.super_trend()
            strat.rsi()
            strat.ema()
            strat.add_db_elements(self.STRAT)
            result = strat.get_strat_df() 
            # push strategy df to strategy table db 
            self.db_connection.insert_strat_table(df=result, strategy=self.STRAT) 
            
        elif self.STRAT == 4:
            strat.sma(5)
            strat.ema(18)
            strat.ema(20)
            strat.sma(50)
            strat.sma(89)
            strat.ema(144)
            k = strat.ema(35)
            r = strat.rma(35)
            ku = (r * 0.5) + k
            strat.master_df = pd.concat([strat.master_df, ku], axis=1, join="inner")
            strat.master_df = strat.master_df.rename(columns={0: "ku"})
            strat.hoff()
            strat.add_db_elements(self.STRAT)
            result = strat.get_strat_df()
            # push strategy df to strategy table db 
            self.db_connection.insert_strat_table(df=result, strategy=self.STRAT)
        # get strategy dataframe ------------------------------------------------
            
    def sel_tickstrat_table(self):
        """
        Returns:
            pd.DataFrame: strat table by strat interval and ticker id
        """
        strat_df = self.db_connection.select_strat_data(self.STRAT, self.TICKER_ID)
        return strat_df
    
    def get_min_max_datetime(self):
        """
        Returns:
            pd.DataFrame: min and max datetimes in table
        """
        min_max_df = self.db_connection.min_max_date(self.STRAT, self.TICKER_ID)
        return min_max_df
            
    def get_wallet_info(self):
        """_summary_
            get wallet obj info
        Returns:
            dict: wallet object
        """
        return self.wallet
    
    def get_display_wallet(self):
        """_summary_
            - get wallet display object
        Returns:
            dict: display wallet object
        """
        return self.display_wallet
    
    def reset_wallet_info(self):
        """_summary_
            - delete wallet 
        """
        del self.wallet
        

    
    
        