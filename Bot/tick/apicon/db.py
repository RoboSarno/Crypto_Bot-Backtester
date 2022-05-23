from distutils.log import error
from sqlalchemy import create_engine
import psycopg2
import streamlit as st
import pandas as pd
import sys
import os
from datetime import datetime
import pytz

class Database:
    def __init__(self):
        """_summary_
            - init Datbase object varibles
        """
        self.hostname = os.environ.get('DB_HOSTNAME', '-1')
        self.port_id = int(os.environ.get('DB_PORT_ID', '-1'))
        self.database = os.environ.get('DB_DATABASE', '-1')
        self.pwd = os.environ.get('DB_PWD', '-1')
        self.username = os.environ.get('DB_USERNAME', '-1')
        
        self.last_action_index = None
        self.last_action_row = None
        
        self.buy_sell_signal = None
        self.last_buy_sell_signal = None
        
        self.hoff_buy_entry = None
        self.hoff_buy_exit = None
        self.candle_count_buy = 0
        self.buy_stop_loss = None
        self.hoff_sell_exit = None
        self.candle_count_sell = 0
        
        # create ticker db if it doesnt exsist
        self.create_TickerTable()
    
    """
                                                            __ HELPERS __
    """
    def check_if_table_exists(self, conn, ticker):
        """_summary_
         - check if table exsists
         
        Args:
            conn (psycopg2): conn
            ticker (string): ticker label

        Returns:
            Tupl: ([True/False],curr.conn)
        """
        # open connection
        cur = conn.cursor()
        # postgres select table
        cur.execute('''select exists(select * from information_schema.tables where table_name=%s)''', (str(ticker),))
        return (cur.fetchone()[0], cur)
    
    
    """
                                                            __ CREATE/UPDATE TABLE __
    """
    def create_TickerTable(self):
        """_summary_
            Create Ticker ID Table
        """
        # open connection 
        conn = self.open_db()
        # try to create ticker ID table
        try:
            curr = conn.cursor()
            create_script = ''' CREATE TABLE IF NOT EXISTS ticker_db (
                                    id              serial NOT NULL,
                                    ticker_label    varchar(40) PRIMARY KEY,
                                    last_update     varchar(30));'''
            # execute script
            curr.execute(create_script)
            conn.commit()
            curr.close()
        except Exception as error:
            print('create_TickerTable ' + str(error))
        # close connection
        self.close_db(conn)

    def create_new_table(self, df, table_name): 
        """_summary_
            - create new table 
        Args:
            df (pd.Dataframe): raw candle stick data
            table_name (string): table name
        """
        try: 
            df = df.set_index('datetime')
        except Exception as error:
            print('create_new_table: ' + table_name + ' : ' + str(error))
        myeng = create_engine("postgresql://%s:%s@%s:%s/stock_crypto" % (self.username,self.pwd,self.hostname, self.port_id) )
        dbConnection = myeng.connect()
        df.to_sql(con=myeng, name=table_name,  if_exists='fail', index=True)
        dbConnection.close()
        return df

    def create_table_historical_db_empty(self, df, table_name):
        """_summary_
            - Append to historical table if it exists

        Args:
            df (pd.Dataframe): raw candle stick data
            table_name (string): table name
        """
        if not df.empty:
            try: 
                df = df.set_index('datetime')
            except Exception as error:
                print('insert_strat_table:strat_df.empty:' + str(error))
        # add last 60 day raw strategy data to db
        myeng = create_engine("postgresql://%s:%s@%s:%s/stock_crypto" % (self.username,self.pwd,self.hostname, self.port_id) )
        dbConnection = myeng.connect()
        df.to_sql(con=myeng, name=table_name,  if_exists='append', index=True)
        dbConnection.close()
        return df

    def append_current_historical_db_table(self, c_df , h_df, table_name):
        """_summary_
            - Append the difference to historical table
        Args:
            c_df (pd.Datframe): raw candle stick data
            h_df (pd.Dataframe): historical db table info
            table_name (string): table name
        """


        # right join
        hist = h_df.drop_duplicates(subset=['datetime'])
        last_hist_datetime = pd.to_datetime(hist.tail(1)['datetime'].values[0], format='%Y%m%d %H:%M:%S',utc=True).tz_convert('US/Pacific')
        c_df['datetime'] = c_df.apply(lambda row: row['datetime'].tz_convert('US/Pacific'), axis=1)
        new = c_df[~(c_df['datetime'] <= last_hist_datetime)]

        try: 
            diff = new.set_index(['datetime']).sort_index()
            
        except Exception as error:
                print('insert_historical_data ' + str(error))    
                # make sure datetime is the index
                # check difference is not empty
        if not diff.empty:
            # # get the last element in hist as the starting element in c_df and make that diff
            # print('append_current_historical_db_table::diff')
            # add new rows from the last 60 day raw ticker data 
            myeng = create_engine("postgresql://%s:%s@%s:%s/stock_crypto" % (self.username,self.pwd,self.hostname, self.port_id) )
            dbConnection = myeng.connect()
            diff.to_sql(con=myeng, name=table_name,  if_exists='append', index=True)
            dbConnection.close()
            return diff
        print(f'current and {table_name} have no difference')
        
    
    
    """
                                                            __ INSERT ELEMENTS INTO TABLES __
    """
    def insert_ticker(self, ticker, date):
        """_summary_
            - Insert Element into Ticker ID Table

        Args:
            ticker (string): ticker id
            date (string): string in datetime.datetime format
        """
        # open connection
        conn = self.open_db()
        curr = conn.cursor()
        # insert element
        insert_script = 'INSERT INTO ticker_db (ticker_label, last_update) VALUES (%s, %s) ON CONFLICT (ticker_label) DO UPDATE SET last_update = EXCLUDED.last_update;' 
        insert_value = (str(ticker), str(date))
        curr.execute(insert_script, insert_value)
        conn.commit()
        curr.close()
        # close connection
        self.close_db(conn)

    def insert_historical_data(self, current_df, ticker_label, strategy):
        """_summary_
            - Updates or Creates historical raw data based on ticker

        Args:
            current_df (pd.Dataframe): raw candle stick data
            ticker_label (string): ticker id
            strategy (int): strategy
        """
        # get current raw historical data table name based on ticker timeframe 
        if strategy == 1:
            table_name = 'historical_data_30_table'
        elif strategy == 3:
            table_name = 'historical_data_1h_table'
        elif strategy == 2 or strategy == 4:
            table_name = 'historical_data_15_table'

        current_df['datetime'] = pd.to_datetime(current_df['datetime'], utc=True)
        current_df['datetime']  = current_df.apply(lambda row: row['datetime'].tz_convert('US/Pacific'), axis=1)
        # open connection
        conn = self.open_db()
        db_open = self.check_if_table_exists(conn, table_name)
        
        # close curr connection
        db_open[1].close()
        # close connection
        self.close_db(conn)
        # if table exsists
        if db_open[0]:
            # select the historical raw data from db
            historical_df = self.select_historical_data(strategy, ticker_label)
            # ---
            # if the historical raw data from db is empty
            if historical_df.empty:
                # print('insert_historical_data::added_df::')
                added_df = self.create_table_historical_db_empty(current_df, table_name)
                return added_df
            else:
                # print('insert_historical_data::joined_list')
                joined_list = self.append_current_historical_db_table(current_df, historical_df, table_name)
                return joined_list 
                         
        # if table doesnt exsist
        else:
            # print('insert_historical_data::added_df')
            added_df = self.create_new_table(current_df, table_name) 
            return added_df    
    
    """
                                                            __ INSERT BUY AND SELL TIMES HELPER __
    """
    """
                                        __ STOP LOSS __
    """
    def hoff_stoploss(self, r):
        """_summary_
            - hoffman strat stop loss
        
        Args:
            r (pd.Dataframe): row
        """
        if self.buy_stop_loss < r['close']:
            self.hoff_sell_exit = None
            self.buy_sell_signal = False
            self.candle_count_sell+=1
            self.buy_stop_loss = 0
            buy_sig = False
            sell_sig = True  
            return (buy_sig, sell_sig)
        return (None, None)
 
    def default_stoploss(self, r):
        """_summary_
            - default stop loss
            
        Args:
            r (pd.Dataframe): row 

        Returns:
            Tupl: ([True/False], [True/False])
        """
        if (r['close'] * 0.05) < (r['close'] - self.last_action_row['close']):
            buy_sig = False
            sell_sig = True  
            return (buy_sig, sell_sig)
        return (None, None)
        
    def default_buysig(self, r, i):
        """_summary_
            - default buy signal
        Args:
            r (pd.Dataframe): row
            i (pd.index): index
        Returns:
            dict: row
        """
        # self.last_buy_sell_signal = False
        if self.buy_sell_signal != True:
            self.last_action_index = i
            self.last_action_row = r
            temp = { 
                'datetime': r['datetime'],
                'ticker_id': r['ticker_id'],
                'b_s': True
            }
            self.buy_sell_signal = True
            return temp
    
    def default_sellsig(self, r, i):
        """_summary_
            - default sell signal
        Args:
            r (pd.Dataframe): row
            i (pd.index): index
        Returns:
            dict: row
        """
        # self.last_buy_sell_signal = True
        if self.buy_sell_signal != False:
            self.last_action_index = i
            self.last_action_row = r
            temp = { 
                'datetime': r['datetime'],
                'ticker_id': r['ticker_id'],
                'b_s': False
            }
            self.buy_sell_signal = False
            return temp  

    def insert_buy_sell_times(self, strat_df, strategy, ticker):
        """_summary_
            - Updates or Creates raw buy_sell strategy data based on strategy
        Args:
            strat_df (pd.Dateframe): buy and sell list of datetimes based on strategy
            strategy (int): value of strategy to run
            ticker (string): name of ticker

        Returns:
            pd.Dataframe: last row of strat df
        """
        buy_sell_list = []
        # get raw buy_sell strategy data table name based on strategy
        if strategy == 1:
            table_name= 'psar_macd_ema_b_s_table'
            strategy_df = self.fast_is_buy_signal_pme(strat_df)
        elif strategy == 2:
            table_name= 'st_rsi_ema_b_s_table'
            # strategy_df = strat_df.copy() 
            strategy_df = self.fast_is_buy_signal_res(strat_df)
        elif strategy == 4:
            table_name = 'hoffman_b_s_table'
            strategy_df = strat_df.copy() 
            # strat_df = self.fast_is_buy_signal_h(strategy_df)
        # print(strategy_df.head())
        # https://medium.com/p/805030df4f06
        # get buy and sell signals
        # print('buy----------------------------')
        # print(strategy_df.groupby(['b0'])['b0'].count())
        # print('---')
        # print('sell----------------------------')
        # print(strategy_df.groupby(['s0'])['s0'].count())
        # print('---')
        # add feture that if it drops more sell more maybe
        for i, r in strategy_df.iterrows():
            if strategy == 1:
                buy_sig, sell_sig = None, None
                # check stop loss
                if r['b0'] and self.last_action_index != None:
                    result = self.default_stoploss(r)
                    buy_sig = result[0]
                    sell_sig = result[1]
                # buy sig
                if r['b0'] or buy_sig:
                    # print(r)
                    temp = self.default_buysig(r, i) 
                    if temp != None:
                        buy_sell_list.append(temp)
                # sell sig
                elif r['s0'] or sell_sig:
                    # print(r)
                    temp = self.default_sellsig(r, i)
                    if temp != None:
                        buy_sell_list.append(temp)
                        
            elif strategy == 2:
                buy_sig, sell_sig = None, None
                # check stop loss
                if r['b0'] and self.last_action_index != None:
                    result = self.default_stoploss(r)
                    buy_sig = result[0]
                    sell_sig = result[1]
                # buy sig
                if r['b0'] or buy_sig:
                    temp = self.default_buysig(r, i) 
                    if temp != None:
                        buy_sell_list.append(temp)
                # sell sig
                elif r['s0'] or sell_sig:
                    temp = self.default_sellsig(r, i)
                    if temp != None:
                        buy_sell_list.append(temp)
                        
            elif strategy == 4:
                buy_sig = self.is_buy_signal_hoff(r, i)
                sell_sig = self.is_sell_signal_hoff(r, i)
                # # if stop loss triggered
                # print(buy_sig, sell_sig)
                if buy_sig and self.buy_stop_loss != None:
                    print('stop loss triggered')
                    result = self.hoff_stoploss(r)
                    buy_sig = result[0]
                    sell_sig = result[1]
                # buy sig
                if buy_sig:
                    temp = self.default_buysig(r, i) 
                    # print(temp)
                    if temp != None:
                        buy_sell_list.append(temp)
                # sell sig
                elif sell_sig:
                    temp = self.default_sellsig(r, i)
                    # print(temp)
                    if temp != None:
                        buy_sell_list.append(temp)
                        
                del buy_sig, sell_sig
        # delete unused variables 
        del strategy_df
        
        # # make buy_sell df
        raw_buy_sell_df = pd.DataFrame(buy_sell_list)
        # print('buy and sell table ----------------')
        # print(raw_buy_sell_df)
        # print('---')
        del buy_sell_list
        
        raw_buy_sell_df['datetime'] = pd.to_datetime(raw_buy_sell_df['datetime'], utc=True)
        raw_buy_sell_df['datetime']  = raw_buy_sell_df.apply(lambda row: row['datetime'].tz_convert('US/Pacific'), axis=1)
        conn = self.open_db()
        db_open = self.check_if_table_exists(conn, table_name)
        db_open[1].close()
        self.close_db(conn)
        
        if db_open[0]:
            # make buy_sell_sig into pandas df     
            historical_strategy_b_s_df = self.select_strategy_b_s(table_name, ticker)
            # if table exists and  isnt add it
            if historical_strategy_b_s_df.empty:
                self.create_table_historical_db_empty(raw_buy_sell_df, table_name)
            # if it is find the difference
            else:
                # get difference from current df and historical db df append difference
                self.append_current_historical_db_table(raw_buy_sell_df, historical_strategy_b_s_df, table_name)
        # if strat b_s table doesnt exists
        else:
            self.create_new_table(raw_buy_sell_df, table_name)
        return raw_buy_sell_df.tail(1)

    def insert_strat_table(self, df, strategy):
        """_summary_
            - Updates or Creates Raw Historical strategy data based on strategy
        Args:
            df (pd.Dataframe): insert strategy table based on strategy
            strategy (int): signal for what strategy to run
        """
        # current_data = df.sort_values(by=['datetime'])
        # set ticker id
        ticker_label = str(df['ticker_id'].iloc[-1])
        # get raw strategy data table name based on strategy
        if strategy == 1:
            table_name = 'psar_macd_ema_table'
        elif strategy == 2:
            table_name = 'st_rsi_ema_table'
        elif strategy == 3:
            table_name = 'sqz_mom_table'
        elif strategy == 4:
            table_name = 'hoffman_table'
        # open connection 
        conn = self.open_db()
        db_open = self.check_if_table_exists(conn, table_name)
        # close curr connection
        db_open[1].close()
        # close connection
        self.close_db(conn)
        try:
            df['datetime'] = pd.to_datetime(df['datetime'], utc=True)
            df['datetime']  = df.apply(lambda row: row['datetime'].tz_convert('US/Pacific'), axis=1)
        except:
            print('insert_strat_table: df could not set datetime')
        # if raw strategy data table exists
        if db_open[0]:
            # select raw strategy data from db
            historical_strat_df = self.select_strat_data(strategy, ticker_label)
 
            if historical_strat_df.empty:
                # make sure datetime is the index
                self.create_table_historical_db_empty(df, table_name)
            # if the raw strategy data from db is not empty
            else:
                # get the difference between current raw strategy data and historical raw strategy data from db
                self.append_current_historical_db_table(df, historical_strat_df, table_name)
            
        # if raw strategy data table doesn not exists
        else:
            self.create_new_table(df, table_name)
    
    
    """
                                                            __ SELECT ELEMENTS FROM TABLE __
    """
    def select_historical_data(self, strategy, ticker_label):
        """_summary_
        Select raw historical data based on ticker ID
        
        Args:
            stratagy (int): specify strategy based on strategy
            ticker_label (string): specify ticker label to run strategy
            
        Returns:
            pd.Dataframe: raw historical data
        """
        # get raw historical data table name based on ticker timeframe 
        if strategy == 1:
            table_name = 'historical_data_30_table'
        elif strategy == 3:
            table_name = 'historical_data_1h_table'
        elif strategy == 2 or strategy == 4:
            table_name = 'historical_data_15_table'
        # open connection
        myeng = create_engine("postgresql://%s:%s@%s:%s/stock_crypto" % (self.username,self.pwd,self.hostname, self.port_id))
        dbConnection = myeng.connect()
        query = 'SELECT * FROM '+ table_name +' WHERE ticker_id = %s;' 
        params = (ticker_label, )
        # get raw historical data table as pandas df
        exsisting_df = pd.read_sql(query, dbConnection, params=params)
        dbConnection.close()
        # close connection
        return exsisting_df

    def select_strat_data(self, strategy, ticker_label):
        """_summary_
            - Select raw strategy data table as pandas df

        Args:
            strategy (_type_): strategy
            ticker_label (_type_): ticker id

        Returns:
            pd.Dataframe: strat historical data table
        """
        # get strat table name based on ticker timeframe and strategy
        if strategy == 1:
            table_name = 'psar_macd_ema_table'   
        elif strategy == 2:
            table_name = 'st_rsi_ema_table' 
        elif strategy == 4:
            table_name = 'hoffman_table'
         
        myeng = create_engine("postgresql://%s:%s@%s:%s/stock_crypto" % (self.username,self.pwd,self.hostname, self.port_id))
        dbConnection = myeng.connect()
        
        query = 'SELECT * FROM '+ table_name +' WHERE ticker_id = %s;' 
        params = (ticker_label, )
        # get strat historical data table as pandas df
        exsisting_df = pd.read_sql(query, dbConnection, params=params)
        
        dbConnection.close()
        return exsisting_df

    def select_strategy_b_s(self, table_name, ticker_label):
        """_summary_
            - Select raw buy_sell strategy data table as pandas df

        Args:
            table_name (string): table name
            ticker_label (string): ticker id

        Returns:
            pd.Dateframe: raw buy_sell strategy data
        """
        myeng = create_engine("postgresql://%s:%s@%s:%s/stock_crypto" % (self.username,self.pwd,self.hostname, self.port_id))
        dbConnection = myeng.connect()
        query = 'SELECT * FROM '+ table_name +' WHERE ticker_id = %s;' 
        params = (ticker_label, )
        exsisting_df = pd.read_sql(query, dbConnection, params=params)
        dbConnection.close()
        return exsisting_df     
    
    
    """
                                                            __ BUY AND SELL SIGNAL STRATEGY __
    """
    def fast_is_buy_signal_pme(self, df):
        # make buy rows
        df['b0'], df['b1'], df['b2'] = None, None, None
        df.loc[((df['close'] > df['ema_200']) & (df['macdh_12_26_9'] > 0)), 'b1'] = True
        df.loc[(df['close'] > df['psarl_0.02_0.2']), 'b2'] = True
        df.loc[((df['b1'] == True) &  (df['b2'] == True)), 'b0'] = True
        
        
        # make sell rows
        df['s0'], df['s1'], df['s2'] = None, None, None
        df.loc[((df['close'] < df['ema_200']) & (df['macdh_12_26_9'] < 0)), 's1'] = True
        df.loc[(df['close'] < df['psars_0.02_0.2']), 's2'] = True
        df.loc[((df['s1'] == True) & (df['s2'] == True)), 's0'] = True
        
        # print(df)
        return df
                   
    def fast_is_buy_signal_res(self, df):
        df['b0'], df['b1'], df['b2'] = None, None, None
        df.loc[((df['supertd_14_3.0'] == 1) & (df['rsi_14_a_70'] == 1)), 'b1'] = True
        df.loc[(df['supertl_14_3.0'] > df['ema_200']), 'b2'] = True
        df.loc[((df['b1'] == True) & (df['b2'] == True)), 'b0'] = True
        
        df['s0'], df['s1'], df['s2'] = None, None, None
        df.loc[((df['supertd_14_3.0'] == -1) & (df['rsi_14_a_70'] == 1)), 's1'] = True
        df.loc[(df['superts_14_3.0'] < df['ema_200']), 's2'] = True
        df.loc[((df['s1'] == True) & (df['s2'] == True)), 's0'] = True
        
        return df
        
    # https://www.youtube.com/watch?v=joO1bmGaBys&t=294s
    # def buy_signal_adx_ema(self, r, i):
    #     on first r['low'] < r[ema_20]:
    #           set entry candle which is high
    #     if the r[open] is > entry:
    #           stop loss is the entry

        
        

    
    # HOFFMAN HELPER
    def is_buy_signal_hoff(self, r, i):
        """_summary_
            - HOFF buy sig
        Args:
            r (pd.Dataframe): row
            i (pd.index): index

        Returns:
            dict: row
        """
        # sma_5 = red
        # ema_18 = green
        # buy
        if (r['sma_5'] > r['ema_18'] and r['sma_5'] > r['ema_20'] and r['sma_5'] > r['sma_50'] and r['sma_5'] > r['sma_89'] and r['sma_5'] > r['ema_144'] and r['sma_5'] > r['ema_35'] and r['sma_5'] > r['ku']):
            if (r['ema_18'] < r['sma_5'] and r['ema_18'] > r['ema_20'] and r['ema_18'] > r['sma_50'] and r['ema_18'] > r['sma_89'] and r['ema_18'] > r['ema_144'] and r['ema_18'] > r['ema_35'] and r['ema_18'] > r['ku']):
                if r['sma_5'] < r['low'] and r['sl'] == 1:
                    self.hoff_buy_entry = r['high']
                    self.hoff_buy_exit = r['ema_18']
                    self.candle_count_buy+=1
                    
                    return True

        return None
    def is_sell_signal_hoff(self, r, i):
        """_summary_
            - HOFF sell sig
        Args:
            r (pd.Dataframe): row
            i (pd.index): index

        Returns:
            dict: row
        """
        # sma_5 = red
        # ema_18 = green
        # print(r)
        if (r['sma_5'] < r['ema_18'] and r['sma_5'] < r['ema_20'] and r['sma_5'] < r['sma_50'] and r['sma_5'] < r['sma_89'] and r['sma_5'] < r['ema_144'] and r['sma_5'] < r['ema_35'] and r['sma_5'] < r['ku']):
            if (r['ema_18'] > r['sma_5'] and r['ema_18'] < r['ema_20'] and r['ema_18'] < r['sma_50'] and r['ema_18'] < r['sma_89'] and r['ema_18'] < r['ema_144'] and r['ema_18'] < r['ema_35'] and r['ema_18'] < r['ku']):
                if r['sma_5'] > r['high'] and r['ss'] == 1:
                    self.hoff_sell_exit = r['low']
                    self.candle_count_sell += 1 
                    return True        
                 
        return None

    """
                                                            __ OPEN/CLOSE DATABASE __
    """
    def open_db(self):
        """_summary_
        open current connection
        Returns:
            psycopg: conn
        """
        conn = psycopg2.connect(host = self.hostname, port=self.port_id, password = self.pwd, user=self.username, dbname=self.database)
        return conn
    def close_db(self, conn):
        """_summary_
        close current connection
        Args:
            conn (psycopg): connection
        """
        conn.close()