from locale import D_T_FMT
import pandas as pd

import sys

import tickobjs
import apicon


class Ticker:
    def __init__(self, ticker_lab, strat=None, interval=None):
        """_summary_
            - init Ticker object varibles

        Args:
            ticker_lab (string): ticker id
            strat (int): strategy
            interval (string): interval
        """
        self.TICKER_ID = ticker_lab
        self.STRAT = strat
        self.INTERVAL = interval
        
        self.binance_connection = apicon.Binance()
        self.db_connection = apicon.Database()
        # self.twilo = apicon.Twilio()
        
        self.last_action = None
    
    def update_historical_info(self):
        raw_historical_data = self.binance_connection.get_historical_ohlc_data(symbol=self.TICKER_ID, past_days=5, interval=self.INTERVAL)
        last_date = raw_historical_data.tail(1)['datetime'].values[0]
        # insert/update historical ticket data into db ticker table
        self.db_connection.insert_ticker(self.TICKER_ID, last_date)

        self.db_connection.insert_historical_data(raw_historical_data, self.TICKER_ID, self.STRAT)
        
        # historical_df = self.db_connection.select_historical_data(self.STRAT,  self.TICKER_ID)
        # if historical_df.empty:
        #     print('no historical data')
        #     pass
        # else:
        #     strategy = tickobjs.Strategy(historical_df, self.TICKER_ID)
        #     # if strategy 1
        #     if self.STRAT == 1:
        #         strategy.psar()
        #         strategy.macd()
        #         strategy.ema()
        #         strategy.add_db_elements()
        #         result = strategy.get_strat_df()  
            # if strategy 2        
            # elif self.STRAT == 2:
            #     strategy.super_trend()
            #     strategy.rsi()
            #     strategy.ema()
            #     strategy.add_db_elements()
            #     result = strategy.get_strat_df()  
                
            # elif self.STRAT == 3:
            #     strategy.Squeeze_momentum()
            #     result = strategy.get_strat_df()  
            #     print(result)
            # if strategy 4     
            # elif self.STRAT == 4:
            #     strategy.sma(5)
            #     strategy.ema(18)
            #     strategy.ema(20)
            #     strategy.sma(50)
            #     strategy.sma(89)
            #     strategy.ema(144)
            #     k = strategy.ema(35)
            #     r = strategy.rma(35)
            #     ku = (r * 0.5) + k
            #     strategy.master_df = pd.concat([strategy.master_df, ku], axis=1, join="inner")
            #     strategy.master_df = strategy.master_df.rename(columns={0: "ku"})
            #     strategy.hoff()
            #     strategy.add_db_elements()
            #     result = strategy.get_strat_df()

            # del strategy 
            # # insert/update strat data into db strat table
            # self.db_connection.insert_strat_table(result, self.STRAT)

        
    def update_database_info(self):
        """_summary_
            - update db information regarding strategy and ticker id
        """
        self.update_historical_info()
        # -------------------------------------
        del raw_historical_data, current_df
        # select db historical data 
        historical_df = self.db_connection.select_historical_data(self.STRAT,  self.TICKER_ID)
        # historical_df
        # # current_df = current_df.reset_index()
        # create a strategy object to make strat
        if historical_df.empty:
            print('no historical data')
            pass
        else:
            strategy = tickobjs.Strategy(historical_df, self.TICKER_ID)
            # if strategy 1
            if self.STRAT == 1:
                strategy.psar()
                strategy.macd()
                strategy.ema()
                strategy.add_db_elements()
                result = strategy.get_strat_df()  
            # if strategy 2        
            elif self.STRAT == 2:
                strategy.super_trend()
                strategy.rsi()
                strategy.ema()
                strategy.add_db_elements()
                result = strategy.get_strat_df()  
                
            elif self.STRAT == 3:
                strategy.Squeeze_momentum()
                result = strategy.get_strat_df()  
                print(result)
            # if strategy 4     
            elif self.STRAT == 4:
                strategy.sma(5)
                strategy.ema(18)
                strategy.ema(20)
                strategy.sma(50)
                strategy.sma(89)
                strategy.ema(144)
                k = strategy.ema(35)
                r = strategy.rma(35)
                ku = (r * 0.5) + k
                strategy.master_df = pd.concat([strategy.master_df, ku], axis=1, join="inner")
                strategy.master_df = strategy.master_df.rename(columns={0: "ku"})
                strategy.hoff()
                strategy.add_db_elements()
                result = strategy.get_strat_df()
                
            # print(result['datetime'])

            del strategy 
            # insert/update strat data into db strat table
            self.db_connection.insert_strat_table(result, self.STRAT)
            
            del result
            
            strategy_df = self.db_connection.select_strat_data(self.STRAT, self.TICKER_ID)

            # # update/insert strat buy and sell data into  db strat_b_s table
            self.last_action = self.db_connection.insert_buy_sell_times(strategy_df, self.STRAT, self.TICKER_ID)
            del strategy_df
        
        

    
    
        