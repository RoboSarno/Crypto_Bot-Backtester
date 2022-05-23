class Wallet:
    def __init__(self, buy_sell_df, historical_df, ticker):
        """_summary_
            - init object varibles
        Args:
            buy_sell_df (pd.Dataframe): buy and sell data of specific ticker label
            historical_df (pd.Dataframe): raw historical data of specific ticker label
            ticker (string): ticker label
        """
        self.buy_sell_df = buy_sell_df
        self.historical_df = historical_df

        # df_new = self.buy_sell_df[self.buy_sell_df.groupby('b_s')['datetime'].max()]
        temp1 = self.buy_sell_df.groupby(['b_s'])['datetime'].max()
        temp2 = self.buy_sell_df.groupby(['b_s'])['datetime'].min()
        last_day = temp1.max()
        first_day = temp2.min()
        self.wallet_info = { 
                        'Ticker': ticker,
                        'Total_Shares_Bought': 0,
                        'Total_Shares_Sold': 0,
                        
                        'Starting_Buy_Power': 0.01077996, # 500 USD
                        'Current_Buy_Power': 0.01077996, # 500 USD
                        'Ending_Buy_Power': 0,
                        'Last_Buy_Power': 0,
                        
                        'Shares': 0,
                        
                        'Long_Positions': 0,
                        'Short_Poistions': 0,
                        
                        'Wins': 0,
                        'Losses': 0,
                        
                        'Longest_Win_Streak': 0,
                        'Longest_Loss_Streak': 0,
                        
                        'First_Element':  first_day,
                        'Last_Element' : last_day
                        
                    }
    def get_bs_shares(self, row, strat, rsk, rwd):
        """_summary_
            based on current buy power in wallet get the number of shares to sell and buy
        Args:
            row (pd.DataFrame): current row
            strat (int): strategy id
            rsk (int): risk
            rwd (int): reward
        Returns:
            tupl: (
                # shares to buy,
                # shares to sell
            )
        """
        # when risk is greater then reward
        if self.wallet_info['Current_Buy_Power'] >= 0 and (strat == 1 or strat == 2):
            shares_bought = (self.wallet_info['Current_Buy_Power'] / rsk) / row['close'] 
            shares_sold = self.wallet_info['Current_Buy_Power'] / rwd 
            
        # when risk is less then reward
        elif self.wallet_info['Current_Buy_Power'] > 0 and (strat == 4):
            shares_bought = (self.wallet_info['Current_Buy_Power'] / rsk) / row['close'] 
            shares_sold = self.wallet_info['Current_Buy_Power'] / rwd 
        
        return (round(float(shares_bought), 6), round(float(shares_sold), 6))

    def run_wallet_change(self, risk, reward, strat):
        """_summary_
            - change wallet information
        Args:
            risk (float): total buy power / risk
            reward (float): risk / reward
            strat (int): strategy
            
        Additonal Notes:
            RISK/REWARD: https://www.investopedia.com/terms/r/riskrewardratio.asp
    
        """
        current_win_streak = 0
        current_loss_streak = 0
        for index, row in self.buy_sell_df.iterrows():
            
            (shares_rsk, shares_rwd) = self.get_bs_shares(row, strat, risk ,reward) 
                    
            self.wallet_info['Last_Buy_Power'] = self.wallet_info['Current_Buy_Power']
            # if buy que
            if row['b_s']:
                if self.wallet_info['Current_Buy_Power'] >= (shares_rsk * row['close']):
                    self.wallet_info['Total_Shares_Bought'] += shares_rsk
                    # temp = self.wallet_info['Shares']
                    self.wallet_info['Shares'] += shares_rsk
                    self.wallet_info['Current_Buy_Power'] -= (shares_rsk * row['close'])
                    # print('current_shares', round(temp, 4), 'shares bought', round(shares_bought, 4), 'for ', round(shares_bought * row['close'], 4), 'current buy power is', round(self.wallet_info['Current_Buy_Power'], 4))
                    self.wallet_info['Long_Positions'] += 1
                
                
                
            # if sell que
            elif row['b_s'] == False:
                # print(self.wallet_info['Shares'], self.wallet_info['Shares'], shares_sold)
                if self.wallet_info['Shares'] > shares_rwd:
                    self.wallet_info['Total_Shares_Sold'] += shares_rwd
                    # temp = self.wallet_info['Shares']
                    self.wallet_info['Shares'] -= shares_rwd
                    self.wallet_info['Current_Buy_Power'] = self.wallet_info['Current_Buy_Power'] + (shares_rwd * row['close'])
                    # print('current_shares', round(temp, 4), 'shares sold', round(shares_sold, 4), 'for ', round(shares_sold * row['close'], 4), 'current buy power is', round(self.wallet_info['Current_Buy_Power'], 4))
                    self.wallet_info['Short_Poistions'] += 1
                # print(self.wallet_info['Current_Buy_Power'])
            
            # self.wallet_info['Current_Buy_Power'] += self.wallet_info['Shares'] * row['close']
            
            
            
            if self.wallet_info['Last_Buy_Power'] > self.wallet_info['Current_Buy_Power']:
                self.wallet_info['Longest_Win_Streak'] = max(current_win_streak, self.wallet_info['Longest_Win_Streak'])
                current_win_streak = 0
                
                self.wallet_info['Losses'] += 1
                current_loss_streak += 1
            
            elif self.wallet_info['Last_Buy_Power'] < self.wallet_info['Current_Buy_Power']:
                self.wallet_info['Longest_Loss_Streak'] = max(current_loss_streak, self.wallet_info['Longest_Loss_Streak'])
                current_loss_streak = 0
                
                self.wallet_info['Wins'] += 1
                current_win_streak += 1
            else:
                pass

        last_datetime_close = self.historical_df['close'].iloc[-1]
        self.wallet_info['Ending_Buy_Power'] =  self.wallet_info['Current_Buy_Power'] + (self.wallet_info['Shares'] * last_datetime_close)



        

            

    