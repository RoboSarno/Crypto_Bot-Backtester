import util
import tick
import config_ev

# library imports
from datetime import datetime
from datetime import timedelta
import pandas as pd
import pytz


ticker_label_list = ['ADABTC', 'ONEBTC', 'HBARBTC', 'VETBTC', 'LTCBTC', 'BCHBTC', 'ETHBTC']
# ticker_label_list = ['ADABTC']

# strategies_list = [3]
strategies_list = [1, 2, 4]

def check_buy_sell_que(TICKER_LABEL, STRATEGY=None, INTERVAL=None):
    """_summary_
    Args:
        TICKER_LABEL (string): ticker id
        STRATEGY (int): strategy
        INTERVAL (string): interval
    """
    # make a ticker with a specific strategy
    ticker = tick.Ticker(TICKER_LABEL, STRATEGY, INTERVAL)
    # update ticker info
    # print(TICKER_LABEL, STRATEGY, INTERVAL)
    ticker.update_historical_info()

        
    # del ticker
    
def run_bot():
    """_summary_
        - sets environment variables
        - runs a repeated function every 900 seconds (15 min)
    """
    # 1) for each element in ticker list
    # 2) get historical data 
    #   - add trend direction calculation 
    #   - only buy when its up and sell when is decreasing
    # 3) run stratagies on that historical data
    # 4) insert that new strategy run data into database
    # 5) get buy and sell cues from current data
    
    global ticker_label_list
    global strategies_list
    # list of past stratagies
    # for each ticker label in list
    for ticker_lab in ticker_label_list:
        print('Ticker_label:',ticker_lab)
        # for each strategy in list
        for strategies in strategies_list:
            # binance interval value
            if strategies == 1:
                interval = '30m'
            if strategies == 3:
                interval = '1h'
            if strategies == 2 or strategies == 4:
                interval = '15m'
            print('Testing Strategy:', strategies)
            check_buy_sell_que(ticker_lab, strategies, interval)
            
    
def start():
    # run_bot()
    rt = util.RepeatedTimer(900, run_bot)
    
if __name__ == '__main__':
    config_ev.set_environment_variables()
    start()
    
