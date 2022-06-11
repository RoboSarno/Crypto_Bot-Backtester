import pandas_ta as ta
import pandas as pd

class Strategy:
    def __init__(self, raw_df, ticker_id):
        """_summary_
            - init Strategy object varibles

        Args:
            raw_df (pd.Dataframe): current candle stick data
            ticker_id (string): ticker id
        """
        self.master_df = pd.DataFrame()
        self.raw_df = raw_df
        self.ticker_id = ticker_id

         
    def add_db_elements(self):
        """_summary_
            - add db elements to pandas df
        """
        # print(self.master_df.index)
        # print(self.raw_df.index)
        self.master_df = self.master_df.rename(columns=str.lower)
        self.master_df['ticker_id'] = self.ticker_id
        self.master_df['datetime'] = self.raw_df['datetime']
        # print(self.master_df.reindex_like(self.raw_df))
        self.master_df['close'] = self.raw_df['close']
        self.master_df['high'] = self.raw_df['high']
        self.master_df['low'] = self.raw_df['low']
        self.master_df['open'] = self.raw_df['open']
        
 
 
    def get_strat_df(self):
        """_summary_

        Returns:
            pd.dataframe: strat table data
        """
        return self.master_df 
    
    def super_trend(self, period=14, atr_multiplier=3):
        """_summary_
            - supertrend

        Args:
            period (int, optional): period. Defaults to 14.
            atr_multiplier (int, optional): atr_multiplier. Defaults to 3.
        """
        strat_df = ta.supertrend(high=self.raw_df['high'], low=self.raw_df['low'], close=self.raw_df['close'], length=period, multiplier=atr_multiplier)
        # if master df is empty add strat df
        if self.master_df.empty:
            self.master_df = strat_df
        # if master df is not empty add to exsisting df
        else:
            self.master_df = pd.concat([self.master_df, strat_df], axis=1, join="inner")

    def rsi(self, period=14, XA=70, XB=30):
        """_summary_
            - rsi

        Args:
            period (int, optional): period. Defaults to 14.
            XA (int, optional): XA. Defaults to 70.
            XB (int, optional): XB. Defaults to 30.
        """
        strat_df = ta.rsi(close=self.raw_df['close'], length=period, append=True, signal_indicators=True, xa=XA, xb=XB)
        # if master df is empty add strat df
        if self.master_df.empty:
            self.master_df = strat_df
        # if master df is not empty add to exsisting df
        else:
            self.master_df = pd.concat([self.master_df, strat_df], axis=1, join="inner")
    
    def ema(self, period=200):
        """_summary_
            - ema

        Args:
            period (int, optional): period. Defaults to 200.

        Returns:
            pd.series: ema
        """
        strat_df = ta.ema(close=self.raw_df['close'], length=period)
        # if master df is empty add strat df
        if self.master_df.empty:
            self.master_df = strat_df
        # if master df is not empty add to exsisting df
        else:
            self.master_df = pd.concat([self.master_df, strat_df], axis=1, join="inner")
        return strat_df
            
    def psar(self):
        """_summary_
            - psar 
        """
        strat_df = ta.psar(high=self.raw_df['high'], low=self.raw_df['low'])
        # if master df is empty add strat df
        if self.master_df.empty:
            self.master_df = strat_df
        # if master df is not empty add to exsisting df
        else:
            self.master_df = pd.concat([self.master_df, strat_df], axis=1, join="inner")
        
    def macd(self):
        """_summary_
            - macd
        """
        strat_df = ta.macd(close=self.raw_df['close'])
        # if master df is empty add strat df
        if self.master_df.empty:
            self.master_df = strat_df
        # if master df is not empty add to exsisting df
        else:
            self.master_df = pd.concat([self.master_df, strat_df], axis=1, join="inner")
    
    def stocastic(self, k_period=14, d_period=3):
        """_summary_
            - stocastic
        Args:
            k_period (int, optional): k_period. Defaults to 14.
            d_period (int, optional): d_period. Defaults to 3.
        """
        strat_df = ta.stoch(high=self.raw_df['high'], low=self.raw_df['low'], k=14, d=3, append=True)
        # if master df is empty add strat df
        if self.master_df.empty:
            self.master_df = strat_df
        # if master df is not empty add to exsisting df
        else:
            self.master_df = pd.concat([self.master_df, strat_df], axis=1, join="inner")
            
    def sma(self, period):
        """_summary_
            - sma
        Args:
            period (int): period
        """
        strat_df = ta.sma(self.raw_df['close'], length=period)
        # if master df is empty add strat df
        if self.master_df.empty:
            self.master_df = strat_df
        # if master df is not empty add to exsisting df
        else:
            self.master_df = pd.concat([self.master_df, strat_df], axis=1, join="inner")
    
    def atr(self, period):
        """_summary_
            - atr
        Args:
            period (int): period

        Returns:
            pd.series: atr
        """
        strat_df = ta.atr(self.raw_df['high'], self.raw_df['low'], self.raw_df['close'], length=period)
        return strat_df
    
            
    def rma(self, period):
        """_summary_
            - rma
        Args:
            period (int): period

        Returns:
            pd.series: rma
        """
        temp = self.atr(35)
        strat_df = ta.rma(temp, length=period)
        return strat_df
    
    def adx_di(self, length=14, th=20):
        strat_df = pd.DataFrame()
        TrueRange = max(
                            max(
                                    self.raw_df['high']-self.raw_df['low'], abs(self.raw_df['high']-pd.isna(self.raw_df['close'[1]]))
                                ), 
                            abs(self.raw_df['low']-pd.isna(self.raw_df['close'[1]]))
                        )
        
        return strat_df
    
    def Squeeze_momentum(self, length=20, mult=2.0, lengthKC=20, multKC=1.5, useTrueRange=True):
        pass

        # Calculate BB
        basis = self.sma(length)
        print(basis)
        # dev = multKC * stdev(source, length)
        # upperBB = basis + dev
        # lowerBB = basis - dev

        # // Calculate KC
        # ma = sma(source, lengthKC)
        # range = useTrueRange ? tr : (high - low)
        # rangema = sma(range, lengthKC)
        # upperKC = ma + rangema * multKC
        # lowerKC = ma - rangema * multKC

        # sqzOn  = (lowerBB > lowerKC) and (upperBB < upperKC)
        # sqzOff = (lowerBB < lowerKC) and (upperBB > upperKC)
        # noSqz  = (sqzOn == false) and (sqzOff == false)

        # val = linreg(source  -  avg(avg(highest(high, lengthKC), lowest(low, lengthKC)),sma(close,lengthKC)), 
        #             lengthKC,0)
            
    def hoff(self, period=45):
        """_summary_
            - hoff

        Args:
            period (int, optional): period. Defaults to 45.
        """
        strat_df = pd.DataFrame()
        strat_df['a'] =  abs(self.raw_df['high'] - self.raw_df['low'])
        strat_df['b'] = abs(self.raw_df['close'] - self.raw_df['open'])
        strat_df['c'] = period/100
        
        strat_df['rv'] = strat_df['b'] < (strat_df['c']*strat_df['a'])
        strat_df.loc[strat_df['rv'] == True, 'rv'] = 1
        strat_df.loc[strat_df['rv'] == False, 'rv'] = 0

        
        strat_df['y'] = self.raw_df['high'] - (strat_df['c'] * strat_df['a'])
        strat_df['x'] = self.raw_df['low'] + (strat_df['c'] * strat_df['a'])

        
        strat_df['sl'] = (strat_df['rv'] == 1) & (self.raw_df['high'] > strat_df['y']) & (self.raw_df['close'] < strat_df['y']) & (self.raw_df['open'] < strat_df['y'])
        strat_df.loc[strat_df['sl'] == True, 'sl'] = 1
        strat_df.loc[strat_df['sl'] == False, 'sl'] = 0
        
        strat_df['ss'] = (strat_df['rv'] == 1) & (self.raw_df['low'] < strat_df['x']) & (self.raw_df['close'] > strat_df['x']) & (self.raw_df['open'] > strat_df['x'])
        strat_df.loc[strat_df['ss'] == True, 'ss'] = 1
        strat_df.loc[strat_df['ss'] == False, 'ss'] = 0
        
        
        # if master df is empty add strat df
        if self.master_df.empty:
            self.master_df = strat_df
        # if master df is not empty add to exsisting df
        else:
            self.master_df = pd.concat([self.master_df, strat_df], axis=1, join="inner")