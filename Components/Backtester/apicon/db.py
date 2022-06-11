from distutils.log import error
from sqlalchemy import create_engine
import psycopg2
import streamlit as st
import pandas as pd
import sys
import os
from sqlalchemy import create_engine, MetaData, Table, Column, Numeric, Integer, VARCHAR, update, bindparam, and_


class Database:
    def __init__(self):
        """_summary_
            - set up enironment varibles for database connection
        """
        # set up db connection
        self.hostname = os.environ.get('AWS_DB_HOSTNAME', '-1')
        self.port_id = int(os.environ.get('AWS_DB_PORT_ID', '-1'))
        self.database = os.environ.get('AWS_DB_DATABASE', '-1')
        self.pwd = os.environ.get('AWS_DB_PWD', '-1')
        self.username = os.environ.get('AWS_DB_USERNAME', '-1')
        self.url = f"postgresql://{self.username}:{self.pwd}@{self.hostname}:{self.port_id}/{self.database}"
        self.last_action_index = None
        self.last_action_row = None
        
        # helper variables for stats
        self.buy_sell_signal = None
        self.last_buy_sell_signal = None
        
        self.hoff_buy_entry = None
        self.hoff_buy_exit = None

        self.buy_stop_loss = None
        self.hoff_sell_exit = None

    def select_bs_historical(self, strategy, ticker_label):
        """
        _summary_
            Select raw historical data and b_s based on ticker ID
        
        Args:
            stratagy (int): specify strategy based on strategy
            ticker_label (string): specify ticker label to run strategy
            
        Returns:
            pd.Dataframe: raw historical data
        """
        if  strategy == 1:
            table_name1 = 'psar_macd_ema_b_s_table'
            table_name2 = 'historical_data_30_table'

        elif strategy == 2:
            table_name1 = 'st_rsi_ema_b_s_table'
            table_name2 = 'historical_data_15_table'

        elif strategy == 4:
            table_name1 = 'hoffman_b_s_table'
            table_name2 = 'historical_data_15_table'
        # open connection
        myeng = create_engine(self.url)
        dbConnection = myeng.connect()
        query = f"""
                SELECT 
                    bs.datetime, 
                    bs.ticker_id, 
                    bs.b_s, 
                    h.open, 
                    h.close, 
                    h.low, 
                    h.high, 
                    h.volume
                FROM 
                    {table_name1} bs
                LEFT JOIN 
                    {table_name2} h
                ON 
                    bs.datetime = h.datetime AND
                    bs.ticker_id = h.ticker_id
                WHERE 
                    bs.ticker_id = '{ticker_label}'
                ORDER BY bs.datetime;
                """ 

        # get raw historical data table as pandas df
        exsisting_df = pd.read_sql(query, dbConnection)
        dbConnection.close()
        # close connection
        return exsisting_df

    def select_historical_data(self, stratagy, ticker_label):
        """
        _summary_
            Select raw historical data based on ticker ID
        
        Args:
            stratagy (int): specify strategy based on strategy
            ticker_label (string): specify ticker label to run strategy
            
        Returns:
            pd.Dataframe: raw historical data
        """
        # get raw historical data table name based on ticker timeframe 
        if stratagy == 1:
            table_name = 'historical_data_30_table'
        elif stratagy == 2 or stratagy == 4:
            table_name = 'historical_data_15_table'
        # open connection
        myeng = create_engine(self.url)
        dbConnection = myeng.connect()
        query = f"""
                    SELECT 
                        * 
                    FROM 
                        {table_name}  
                    WHERE 
                        ticker_id = '{ticker_label}'
                    ORDER BY datetime;
                """ 

        # get raw historical data table as pandas df
        exsisting_df = pd.read_sql(query, dbConnection)
        dbConnection.close()
        # close connection
        return exsisting_df
    
    def select_strat_data(self, stratagy, ticker_label):
        """
        _summary_
            Select strat data based on ticker ID and strat
        
        Args:
            stratagy (int): specify strategy based on strategy
            ticker_label (string): specify ticker label to run strategy
            
        Returns:
            pd.Dataframe: raw historical data
        """
        # set varible parameters for select statments
        if stratagy == 1:
            table_name1 = 'historical_data_30_table'
            table_name2 = 'psar_macd_ema_table'
            query = f"""
                        SELECT 
                            h.datetime, h.ticker_id, h.open, 
                            h.high, h.low, h.close,
                            h.volume, s.psarl, s.psars,
                            s.psaraf, s.psarr, s.macd,
                            s.macdh, s.macds, s.ema_200
                        FROM 
                            {table_name1} AS h
                        LEFT JOIN 
                            {table_name2} AS s
                        ON 
                            h.datetime = s.datetime AND
                            h.ticker_id = s.ticker_id
                        WHERE
                            h.ticker_id = '{ticker_label}'
                        ORDER BY 
                            h.datetime;
                    """ 
        elif stratagy == 2:
            table_name1 = 'historical_data_15_table'
            table_name2 = 'st_rsi_ema_table'
            query = f"""
                        SELECT 
                            h.datetime, h.ticker_id, h.open, 
                            h.high, h.low, h.close,
                            h.volume, s.supert, s.supertd,
                            s.supertl, s.superts, s.rsi_14,
                            s.rsi_14_a_70, s.rsi_14_b_30, s.ema_200
                        FROM 
                            {table_name1} AS h
                        LEFT JOIN 
                            {table_name2} AS s
                        ON 
                            h.datetime = s.datetime AND
                            h.ticker_id = s.ticker_id
                        WHERE
                            h.ticker_id = '{ticker_label}'
                        ORDER BY 
                            h.datetime;
                    """ 
        elif  stratagy == 4:
            table_name1 = 'historical_data_15_table'
            table_name2 = 'hoffman_table'
            query = f"""
                        SELECT 
                            h.datetime, h.ticker_id, h.open, 
                            h.high, h.low, h.close,
                            h.volume, s.sma_5, s.ema_18,
                            s.ema_20, s.sma_50, s.sma_89,
                            s.ema_144, s.ema_35, s.ku,
                            s.a, s.b, s.c, s.rv, s.y, s.x,
                            s.sl, s.ss
                        FROM 
                            {table_name1} AS h
                        LEFT JOIN 
                            {table_name2} AS s
                        ON 
                            h.datetime = s.datetime AND
                            h.ticker_id = s.ticker_id
                        WHERE
                            h.ticker_id = '{ticker_label}'
                        ORDER BY 
                            h.datetime;
                    """ 
        # set varible parameters for select statments ---------
        
        # open connection
        myeng = create_engine(self.url)
        dbConnection = myeng.connect()
        # get raw historical data table as pandas df
        exsisting_df = pd.read_sql(query, dbConnection)
        dbConnection.close()
        # close connection
        return exsisting_df
    
    def min_max_date(self, stratagy, ticker_label):
        """
        _summary_
            Select min and max datetime in table based on strat and ticker id
        
        Args:
            stratagy (int): specify strategy based on strategy
            ticker_label (string): specify ticker label to run strategy
            
        Returns:
            pd.Dataframe: raw historical data
        """
        if stratagy == 1:
            table_name1 = 'historical_data_30_table'

        elif stratagy == 2 or stratagy == 4:
            table_name1 = 'historical_data_15_table'

        # open connection
        myeng = create_engine(self.url)
        dbConnection = myeng.connect()
        query = f"""
                    SELECT 
                        MAX(datetime), 
                        MIN(datetime) 
                    FROM 
                        "public"."{table_name1}";
                """ 


        # get raw historical data table as pandas df
        exsisting_df = pd.read_sql(query, dbConnection)
        dbConnection.close()
        # close connection
        return exsisting_df
        
    def check_if_table_exists(self, conn, ticker):
        """
        _summary_
            check if table exsists
         
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
    
    def create_new_table(self, df, table_name): 
        """
        _summary_
            create new table 
        Args:
            df (pd.Dataframe): raw candle stick data
            table_name (string): table name
        """
        try: 
            df = df.set_index('datetime')
        except Exception as error:
            print('create_new_table: ' + table_name + ' : ' + str(error))
        myeng = create_engine(self.url)
        dbConnection = myeng.connect()
        df.to_sql(con=myeng, name=table_name,  if_exists='fail', index=True)
        dbConnection.close()
        return df
    
    def fast_is_buy_signal_pme(self, df):
        """
        _summary_
            find PSAR MACD EMA buy and sell signals

        Args:
            df (pd.DataFrame): Strat df

        Returns:
            pd.DataFrame: PSAR MACD EMA buy and sell signals
        """
        # make buy rows
        df['b0'], df['b1'], df['b2'] = None, None, None
        df.loc[((df['close'] > df['ema_200']) & (df['macdh'] > 0)), 'b1'] = True
        df.loc[(df['close'] > df['psarl']), 'b2'] = True
        df.loc[((df['b1'] == True) &  (df['b2'] == True)), 'b0'] = True
        
        
        # make sell rows
        df['s0'], df['s1'], df['s2'] = None, None, None
        df.loc[((df['close'] < df['ema_200']) & (df['macdh'] < 0)), 's1'] = True
        df.loc[(df['close'] < df['psars']), 's2'] = True
        df.loc[((df['s1'] == True) & (df['s2'] == True)), 's0'] = True
        
        return df
        
    def fast_is_buy_signal_res(self, df):
        """
        _summary_
            Find RSI EMA ST buy and sell signals

        Args:
            df (_type_): Strat df

        Returns:
            pd.DataFrame: RSI EMA ST buy and sell signals
        """
        temp = df.copy()
        temp['b0'], temp['b1'], temp['b2'], temp['b3'] = None, None, None, None
        temp.loc[(temp['close'] > temp['ema_200']), 'b1'] = True
        temp.loc[(temp['supertd'] == 1), 'b2'] = True
        temp.loc[(temp['rsi_14_b_30'] == 1), 'b3'] = True
        temp.loc[((temp['b1'] == True) & (temp['b2'] == True) & (temp['b3'] == True)), 'b0'] = True
        
        temp['s0'], temp['s1'], temp['s2'], temp['s3'] = None, None, None, None
        temp.loc[(temp['close'] <  temp['ema_200']), 's1'] = True
        temp.loc[(temp['supertd'] == -1), 's2'] = True
        temp.loc[(temp['rsi_14_a_70'] == 1), 's3'] = True
        temp.loc[((temp['s1'] == True) & (temp['s2'] == True) & (temp['s3'] == True)), 's0'] = True
        
        return temp
    
    def is_buy_signal_hoff(self, r, i):
        """
        _summary_
            HOFF buy sig
        Args:
            r (pd.Dataframe): row
            i (pd.index): index
        Returns:
            dict: row
        """
        try:
            if (r['sma_5'] > r['ema_18'] and r['sma_5'] > r['ema_20'] and r['sma_5'] > r['sma_50'] and r['sma_5'] > r['sma_89'] and r['sma_5'] > r['ema_144'] and r['sma_5'] > r['ema_35'] and r['sma_5'] > r['ku']):
                if (r['ema_18'] < r['sma_5'] and r['ema_18'] > r['ema_20'] and r['ema_18'] > r['sma_50'] and r['ema_18'] > r['sma_89'] and r['ema_18'] > r['ema_144'] and r['ema_18'] > r['ema_35'] and r['ema_18'] > r['ku']):
                    if r['sma_5'] < r['low'] and r['sl'] == 1:
                        self.hoff_buy_entry = r['high']
                        self.hoff_buy_exit = r['ema_18']
                        return True
        except:
            return None
    
    def is_sell_signal_hoff(self, r, i):
        """
        _summary_
            HOFF sell sig
        Args:
            r (pd.Dataframe): row
            i (pd.index): index
        Returns:
            dict: row
        """
        try:
            if (r['sma_5'] < r['ema_18'] and r['sma_5'] < r['ema_20'] and r['sma_5'] < r['sma_50'] and r['sma_5'] < r['sma_89'] and r['sma_5'] < r['ema_144'] and r['sma_5'] < r['ema_35'] and r['sma_5'] < r['ku']):
                if (r['ema_18'] > r['sma_5'] and r['ema_18'] < r['ema_20'] and r['ema_18'] < r['sma_50'] and r['ema_18'] < r['sma_89'] and r['ema_18'] < r['ema_144'] and r['ema_18'] < r['ema_35'] and r['ema_18'] < r['ku']):
                    if r['sma_5'] > r['high'] and r['ss'] == 1:
                        self.hoff_sell_exit = r['low']
                        return True        
        except: 
            return None
    
    def hoff_stoploss(self, r):
        """
        _summary_
            hoffman strat stop loss
        
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
        """
        _summary_
            default stop loss
            
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
        """
        _summary_
            default buy signal
        Args:
            r (pd.Dataframe): row
            i (pd.index): index
        Returns:
            dict: row
        """
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
        """
        _summary_
            default sell signal
        Args:
            r (pd.Dataframe): row
            i (pd.index): index
        Returns:
            dict: row
        """
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
        
    def strat_pme_b_s(self, strategy_df):
        """
        _summary_
            Find Buy and Sell signals for PSAR MACD EMA
        Args:
            strategy_df (pd.DataFrame): strat df
        Returns:
            list: list containing rows that are buy and sell
        """
        buy_sell_list = []
        for i, r in strategy_df.iterrows():
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
        return buy_sell_list
    
    def strat_res_b_s(self, strategy_df):
        """
        _summary_
            Find Buy and Sell signals for RSI EMA ST
        Args:
            strategy_df (pd.DataFrame): strat df
        Returns:
            list: list containing rows that are buy and sell
        """
        buy_sell_list = []
        # buy_sig, sell_sig = None, None
        # check stop loss
        for i, r in strategy_df.iterrows():
            buy_sig, sell_sig = None, None
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
        return buy_sell_list
                    
    def strat_hoff_b_s(self, strategy_df):
        """
        _summary_
            Find Buy and Sell signals for Hoffman
        Args:
            strategy_df (pd.DataFrame): strat df
        Returns:
            list: list containing rows that are buy and sell
        """
        buy_sell_list = []
        for i, r in strategy_df.iterrows():
            buy_sig = self.is_buy_signal_hoff(r, i)
            sell_sig = self.is_sell_signal_hoff(r, i)
            # if stop loss triggered
            if buy_sig and self.buy_stop_loss != None:
                print('stop loss triggered')
                result = self.hoff_stoploss(r)
                buy_sig = result[0]
                sell_sig = result[1]
            # buy sig
            if buy_sig:
                temp = self.default_buysig(r, i) 
                if temp != None:
                    buy_sell_list.append(temp)
            # sell sig
            elif sell_sig:
                temp = self.default_sellsig(r, i)
                if temp != None:
                    buy_sell_list.append(temp)
                    
            del buy_sig, sell_sig
        return buy_sell_list
    
    def create_table_historical_db_empty(self, df, table_name):
        """
        _summary_
            Create table if doesnt exsist
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
        myeng = create_engine(self.url)
        dbConnection = myeng.connect()
        df.to_sql(con=myeng, name=table_name,  if_exists='append', index=True)
        dbConnection.close()
        return df
    
    def update_b_s_table(self, c_df , h_df, table_name):
        """
        _summary_
            Append the difference to historical table
        Args:
            c_df (pd.Datframe): raw candle stick data
            h_df (pd.Dataframe): historical db table info
            table_name (string): table name
        Returns:
            pd.DataFrame: table containing the elements that arent already in the database 
        """

        # dont input duplicate elements into table
        hist = h_df.drop_duplicates(subset=['datetime'])
        last_hist_datetime = pd.to_datetime(hist.tail(1)['datetime'].values[0], format='%Y%m%d %H:%M:%S',utc=True).tz_convert('US/Pacific')
        c_df['datetime'] = c_df.apply(lambda row: row['datetime'].tz_convert('US/Pacific'), axis=1)
        new = c_df[~(c_df['datetime'] <= last_hist_datetime)]
        
        # make sure datetime is the index
        try: 
            diff = new.set_index(['datetime']).sort_index()
            
        except Exception as error:
                print('insert_historical_data ' + str(error))    

        # check difference is not empty
        if not diff.empty:
            myeng = create_engine(self.url)
            dbConnection = myeng.connect()
            diff.to_sql(con=myeng, name=table_name,  if_exists='append', index=True)
            dbConnection.close()
            return diff
        
    def select_strategy_b_s(self, table_name, ticker_label):
        """
        _summary_
            Select raw buy_sell strategy database table using strat and ticker id
        Args:
            table_name (string): table name
            ticker_label (string): ticker id
        Returns:
            pd.Dateframe: raw buy_sell strategy data
        """
        myeng = create_engine(self.url)
        dbConnection = myeng.connect()
        query = f"""
                    SELECT 
                        * 
                    FROM 
                        {table_name} 
                    WHERE 
                        ticker_id = '{ticker_label}'
                    ORDER BY 
                        datetime;
                """ 
        exsisting_df = pd.read_sql(query, dbConnection)
        dbConnection.close()
        return exsisting_df     
    
    def get_buy_sell_times_df(self, strat_df, strategy, ticker):
        """
        _summary_
            create raw buy_sell strategy data based on strategy
        Args:
            strat_df (pd.Dateframe): buy and sell list of datetimes based on strategy
            strategy (int): value of strategy to run
            ticker (string): name of ticker
        Returns:
            pd.Dataframe: buy_sell strategy data
        """
        buy_sell_list = []
        
        # get
        if strategy == 1:
            # table_name= 'psar_macd_ema_b_s_table'
            strategy_df = self.fast_is_buy_signal_pme(strat_df)
            buy_sell_list = self.strat_pme_b_s(strategy_df)
            raw_buy_sell_df = pd.DataFrame(buy_sell_list, columns =['datetime', 'ticker_id', 'b_s'])
        
        elif strategy == 2:
            # table_name= 'st_rsi_ema_b_s_table'
            strategy_df = self.fast_is_buy_signal_res(strat_df)
            buy_sell_list = self.strat_res_b_s(strategy_df)
            raw_buy_sell_df = pd.DataFrame(buy_sell_list, columns =['datetime', 'ticker_id', 'b_s'])
           
        elif strategy == 4:
            # table_name = 'hoffman_b_s_table'
            strategy_df = None
            buy_sell_list = self.strat_hoff_b_s(strat_df)
            raw_buy_sell_df = pd.DataFrame(buy_sell_list, columns =['datetime', 'ticker_id', 'b_s'])
            
        # delete unused variables 
        del strategy_df, buy_sell_list

        # no buy or sell cues
        if raw_buy_sell_df.empty:
            pass
        
        else:
            raw_buy_sell_df['datetime'] = pd.to_datetime(raw_buy_sell_df['datetime'], utc=True)
            raw_buy_sell_df['datetime']  = raw_buy_sell_df.apply(lambda row: row['datetime'].tz_convert('US/Pacific'), axis=1)
            
            # future implementation
            # # helper function to check if table exsists
            # conn = self.open_db()
            # db_open = self.check_if_table_exists(conn, table_name)
            # db_open[1].close()
            # self.close_db(conn)
            
            # if db_open[0]:
            #     # make buy_sell_sig into pandas df     
            #     historical_strategy_b_s_df = self.select_strategy_b_s(table_name, ticker)
            #     # if table_name exists append data to it
            #     if historical_strategy_b_s_df.empty:
            #         self.create_table_historical_db_empty(raw_buy_sell_df, table_name)
                
            #     # if historical_strategy_b_s_df has data  find the difference
            #     else:
            #         # get difference from current df and historical db df append difference
            #         self.update_b_s_table(raw_buy_sell_df, historical_strategy_b_s_df, table_name)
            # # if strat b_s table doesnt exists create table
            # else:
            #     self.create_new_table(raw_buy_sell_df, table_name)
        return raw_buy_sell_df

    def create_table_empty(self, df, table_name):
        """
        _summary_
            Create table if doesnt exsist
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
        myeng = create_engine(self.url)
        dbConnection = myeng.connect()
        df.to_sql(con=myeng, name=table_name,  if_exists='append', index=True)
        dbConnection.close()
        return df
    
    def append_table_not_empty(self, c_df , h_df, table_name, strategy):
            """
            _summary_
                Append the difference of current candle stick data and 
                historical current candle stick data to historical table
            Args:
                c_df (pd.Datframe): raw candle stick data
                h_df (pd.Dataframe): historical data  
                table_name (string): table name
            """
            price_values = h_df[['open', 'high', 'low', 'close', 'volume']]
            h_df.drop(columns=['open', 'high', 'low', 'close', 'volume'], inplace=True)
            c_df['datetime'] = c_df.apply(lambda row: row['datetime'].tz_convert('US/Pacific'), axis=1)
            h_df['datetime'] = h_df.apply(lambda row: row['datetime'].tz_convert('US/Pacific'), axis=1)
            diff = pd.concat([c_df,h_df]).drop_duplicates(subset=['datetime'], keep='first')

            if not diff.empty:
                # get the last element in hist as the starting element in c_df and make that diff
                # add new rows from the last 60 day raw ticker data 
                myeng = create_engine(self.url)

                dbConnection = myeng.connect()
                diff.to_sql(con=myeng, name=table_name,  if_exists='append', index=False)
                dbConnection.close()

    def insert_strat_table(self, df, strategy):
        """
        _summary_
            Updates or Creates Raw Historical strategy data based on strategy
        Args:
            df (pd.Dataframe): insert strategy table based on strategy
            strategy (int): signal for what strategy to run
        """
        # set ticker id
        ticker_label = str(df['ticker_id'].iloc[-1])
        
        # get raw strategy data table name based on strategy
        if strategy == 1:
            table_name = 'psar_macd_ema_table'
        elif strategy == 2:
            table_name = 'st_rsi_ema_table'
        elif strategy == 4:
            table_name = 'hoffman_table'
            
        # check if table exsists
        conn = self.open_db()
        db_open = self.check_if_table_exists(conn, table_name)
        db_open[1].close()
        self.close_db(conn)
        
        # change index to datetime
        try:
            df['datetime'] = pd.to_datetime(df['datetime'], utc=True)
            df['datetime']  = df.apply(lambda row: row['datetime'].tz_convert('US/Pacific'), axis=1)
        except:
            print('insert_strat_table: df could not set datetime')
        # if strategy table exists
        if db_open[0]:
            
            # select raw strategy data from db
            historical_strat_df = self.select_strat_data(strategy, ticker_label)
            
            if historical_strat_df.empty:
                # make sure datetime is the index
                self.create_table_empty(df, table_name)
                
            # if the raw strategy data from db is not empty
            else:
                # get the difference between current raw strategy data and historical raw strategy data from db
                self.append_table_not_empty(df, historical_strat_df, table_name, strategy)
            
        # if raw strategy data table doesn not exists
        else:
            self.create_new_table(df, table_name)
        
    def open_db(self):
        """
        _summary_
            open current connection
        Returns:
            psycopg: conn
        """
        conn = psycopg2.connect(host = self.hostname, port=self.port_id, password = self.pwd, user=self.username, dbname=self.database)
        return conn

    def close_db(self, conn):
        """
        _summary_
            close current connection
        Args:
            conn (psycopg): connection
        """
        conn.close()