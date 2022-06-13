from copy import deepcopy
import requests
response = requests.get('https://api.coindesk.com/v1/bpi/currentprice.json')
data = response.json()
USD_price = data['bpi']['USD']['rate_float']

class Wallet:
    def __init__(self, buy_sell_df, most_recent_close, ticker):
        """_summary_
            - init object varibles
        Args:
            buy_sell_df (pd.Dataframe): buy and sell data of specific ticker label
            historical_df (pd.Dataframe): raw historical data of specific ticker label
            ticker (string): ticker label
        """
        self.buy_sell_df = buy_sell_df

        self.most_recent_close = most_recent_close
        # satrting wallet is 500 USD
        self.wallet_info = { 
                        'Datetime': None,
                        'Ticker': ticker,
                        'Total_Shares_Bought': 0,
                        'Total_Shares_Sold': 0,
                        
                        'Current_Buy_Power': ((0.01077996*USD_price) + abs((0.01077996*USD_price)-500)), # 500 USD
                        'Last_Buy_Power': 0,
                        
                        'Shares': 0,
                        
                        'Long_Positions': 0,
                        'Short_Poistions': 0,
                        'close': 0
                                       
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
            change wallet information
        Args:
            risk (float): total buy power / risk
            reward (float): risk / reward
            strat (int): strategy
            
        Additonal Notes:
            RISK/REWARD: https://www.investopedia.com/terms/r/riskrewardratio.asp
    
        """
        ans = [deepcopy(self.wallet_info)]

        current = self.wallet_info['Current_Buy_Power']


        for index, row in self.buy_sell_df.iterrows():
            (shares_rsk, shares_rwd) = self.get_bs_shares(row, strat, risk ,reward)
            last = self.wallet_info['Current_Buy_Power']
            # if buy que
            if row['b_s']:
                if self.wallet_info['Current_Buy_Power'] >= (shares_rsk * row['close']):
                    # datetime
                    self.wallet_info['Datetime'] = row['datetime']
                    # increment buy positions
                    self.wallet_info['Long_Positions'] += 1
                    # increment totoal shares bought
                    self.wallet_info['Total_Shares_Bought'] += shares_rsk
                    # increment total shares current in wallet
                    self.wallet_info['Shares'] += shares_rsk
                    # calculate the cost and subtract by buy power
                    cost_of_shares_purchased = (shares_rsk * row['close'])
                    self.wallet_info['Current_Buy_Power'] -= (cost_of_shares_purchased)
                    # close
                    self.wallet_info['close'] = row['close']
                    # signal
                    self.wallet_info['b_s'] = bool(row['b_s'])
                    # append to wallet
                    ans.append(deepcopy(self.wallet_info))
                    # print('Last Buy power', last, 
                    #       'Number of Shares Bought Cost:', (shares_rsk * row['close']),
                    #       'Current Buy power', self.wallet_info['Current_Buy_Power'], 
                    #       'Number of shares Shares', self.wallet_info['Shares'])
            # if sell que
            elif row['b_s'] == False:
                if self.wallet_info['Shares'] > shares_rwd:
                    # datetime
                    self.wallet_info['Datetime'] = row['datetime']
                    # increment sell positions
                    self.wallet_info['Short_Poistions'] += 1
                    # increment total shares sold
                    self.wallet_info['Total_Shares_Sold'] += shares_rwd
                    # decriement total shares current in wallet
                    self.wallet_info['Shares'] -= shares_rwd
                    # calculate the cost and add by buy power
                    cost_of_shares_sold = (shares_rwd * row['close']) 
                    self.wallet_info['Current_Buy_Power'] += cost_of_shares_sold
                    # close
                    self.wallet_info['close'] = row['close']
                    # signal
                    self.wallet_info['b_s'] = bool(row['b_s'])
                    # append to wallet
                    ans.append(deepcopy(self.wallet_info))

                    # print('Last Buy power', last, 
                    #       'Number of Shares Sold Worth:', (shares_rwd * row['close']),
                    #       'Current Buy power', self.wallet_info['Current_Buy_Power'], 
                    #       'Number of shares Shares', self.wallet_info['Shares'])
            self.wallet_info['Total_Buy_Power'] = (self.wallet_info['Shares']*row['close']) + self.wallet_info['Current_Buy_Power']
            # print(f"""The number of shares you currently have is {self.wallet_info['Shares']}. The current worth of those shares is {self.wallet_info['Shares']*row['close']}. The current wallet buy power with out the worth of shares is {self.wallet_info['Current_Buy_Power']}. The current worth of you wallet is {(self.wallet_info['Shares']*row['close']) + self.wallet_info['Current_Buy_Power']}""")
                
            # at the begining of each iteration add the current wallet worth
            # current_wallet_worth = self.wallet_info['Shares'] *  row['close']
            # self.wallet_info['Current_Buy_Power'] += current_wallet_worth

        # get last close
        last_close = ans[-1]['close']
        # calculate last wallet shares + there worth
        final_shares_worth = self.wallet_info['Shares'] * last_close
        # set buy power
        self.wallet_info['Current_Buy_Power'] += final_shares_worth
        # set datetime
        self.wallet_info['Datetime'] = None
        # append last wallet info
        ans.append(deepcopy(self.wallet_info))
        return ans

            
        



        

            

    