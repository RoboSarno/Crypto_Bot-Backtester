import pandas as pd

import sys

sys.path.append(r'/Users/robertsarno/Documents/Winter_2021/Projects/Stock_Trading/Stock_Stategy_Bot/V2/Backtester/tick')

import funds
import apicon


class Ticker:
    def __init__(self, ticker_lab, strat, interval):
        """_summary_
            - init ticker object
            
        Args:
            ticker_lab (string): ticker label
            strat (int): strategy id
            interval (string): NOT USED
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
        buy_sell_table_df = self.db_connection.select_historical_buy_sell_table(self.STRAT, self.TICKER_ID)
        # print(buy_sell_table_df.groupby(['ticker_id'])['ticker_id'].count())
        historical_buy_sell_table = buy_sell_table_df[(buy_sell_table_df['ticker_id'] == self.TICKER_ID)]
        # print(historical_buy_sell_table.shape)
        del buy_sell_table_df
        
        historical_bs_table_df = historical_buy_sell_table.drop_duplicates()


        historical_bs_table_df = historical_bs_table_df.sort_values(by=['datetime'])
        historical_df = self.db_connection.select_historical_data(self.STRAT,  self.TICKER_ID)
        # print(historical_df, historical_bs_table_df)
        self.wallet = funds.Wallet(historical_bs_table_df,  historical_df, self.TICKER_ID)
        self.wallet.run_wallet_change(risk, reward, self.STRAT)
        
        self.display_wallet = funds.Display_Wallet(self.wallet.wallet_info, historical_bs_table_df, historical_df)

    def get_wallet_info(self):
        """_summary_
            - get wallet obj info
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
        

    
    
        