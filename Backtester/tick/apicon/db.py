from distutils.log import error
from sqlalchemy import create_engine
import psycopg2
import streamlit as st
import pandas as pd
import sys
import os

class Database:
    def __init__(self):
        """_summary_
            - set up enironment varibles for database connection
        """
        self.hostname = os.environ.get('DB_HOSTNAME', '-1')
        self.port_id = int(os.environ.get('DB_PORT_ID', '-1'))
        self.database = os.environ.get('DB_DATABASE', '-1')
        self.pwd = os.environ.get('DB_PWD', '-1')
        self.username = os.environ.get('DB_USERNAME', '-1')
    
    """
                                                            __ SELECT ELEMENTS FROM TABLE __
    """
    def select_historical_data(self, stratagy, ticker_label):
        """_summary_
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
        myeng = create_engine("postgresql://%s:%s@%s:%s/stock_crypto" % (self.username,self.pwd,self.hostname, self.port_id))
        dbConnection = myeng.connect()
        query = 'SELECT * FROM '+ table_name +' WHERE ticker_id = %s;' 
        params = (ticker_label, )
        # get raw historical data table as pandas df
        exsisting_df = pd.read_sql(query, dbConnection, params=params)
        dbConnection.close()
        # close connection
        return exsisting_df
    
    def select_historical_buy_sell_table(self, strat, label): 
        """_summary_
        Select strat historical data table as pandas df
        
        Args:
            stratagy (int): specify strategy based on strategy

        Returns:
            pd.Dataframe: strat historical data table
        """
        # get strat table name based on ticker timeframe and strategy
        if strat == 1:
            table_name1 = "historical_data_30_table"
            table_name2 = "psar_macd_ema_b_s_table"
        elif strat == 2:
            table_name1 = "historical_data_15_table"
            table_name2 = "st_rsi_ema_b_s_table"
        elif strat == 4:
            table_name1 = "historical_data_15_table"
            table_name2 = "hoffman_b_s_table"
        try:
            # open connection
            myeng = create_engine("postgresql://%s:%s@%s:%s/stock_crypto" % (self.username,self.pwd,self.hostname, self.port_id))
            dbConnection = myeng.connect()
            # query = f'SELECT "h"."datetime", "h"."open", "h"."high", "h"."low", "h"."close", "h"."volume", "h"."ticker_id", "pme"."b_s" FROM {table_name2} AS "pme" LEFT JOIN {table_name1} AS "h" ON "pme"."datetime" = "h"."datetime" WHERE "pme"."datetime" IN (SELECT {table_name2}."datetime" FROM  {table_name2} where  {table_name2}."ticker_id" = '{label}');'
            query = f"SELECT h.datetime, h.open, h.high, h.low, h.close, h.volume, h.ticker_id, pme.b_s FROM {table_name2} AS pme LEFT JOIN {table_name1} AS h ON pme.datetime = h.datetime WHERE pme.datetime IN (SELECT {table_name2}.datetime FROM  {table_name2} where  {table_name2}.ticker_id = '{label}');"
            # get strat historical data table as pandas df
            exsisting_df = pd.read_sql(query, dbConnection)
            # close connection
            dbConnection.close()
            return exsisting_df
        except Exception as error:
            print('select_historical_buy_sell_table:' + f'{str(table_name1)}/{str(table_name2)}'+ ':' + str(error))
            return pd.DataFrame()    
         
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