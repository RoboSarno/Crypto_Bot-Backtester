import pandas as pd
import datetime
import numpy as np
from binance.client import Client

class Binance:
    def __init__(self):
        """_summary_
            - init Binance object
        """
        self.client=Client()

    def get_historical_ohlc_data(self, symbol, past_days=None,interval=None):
        """_summary_
            - Returns historcal klines from past for given symbol and interval

        Returns:
            pd.Dataframe: historcal klines from past
        """
        if not interval:
            interval='1h' # default interval 1 hour
        if not past_days:
            past_days=30  # default past days 30.

        start_str=str((pd.to_datetime('today')-pd.Timedelta(str(past_days)+' days')).date())
        
        current_candl_df=pd.DataFrame(self.client.get_historical_klines(symbol=symbol,start_str=start_str,interval=interval))

        return self.covert_historical_ohlc_data(current_candl_df, symbol)
    
    def covert_historical_ohlc_data(self, temp, symbol):
        """_summary_
            - add aditional columns to current candle stick data
        Args:
            temp (pd.Dataframe): current candle stick data
            symbol (string): ticker id

        Returns:
            pd.Dataframe: current candle stick data
        """
        df = temp.copy()
        df.columns = ['open_time','open', 'high', 'low', 'close', 'volume', 'close_time', 'qav', 'num_trades', 'taker_base_vol', 'taker_quote_vol','is_best_match']
        df['datetime'] = [datetime.datetime.fromtimestamp(x/1000) for x in df.open_time]
        df['ticker_id'] = symbol
        df = df[['ticker_id','datetime','open', 'high', 'low', 'close', 'volume']]
        df['open'] = df['open'].astype(np.float64)
        df['high'] = df['high'].astype(np.float64)
        df['low'] = df['low'].astype(np.float64)
        df['close'] = df['close'].astype(np.float64)
        df['volume'] = df['volume'].astype(np.float64)
        return df

        