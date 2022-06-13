import util
import tick
import config_ev

# library imports
from datetime import datetime
from datetime import timedelta
import pandas as pd
import pytz


ticker_label_list = ['ADABTC', 'ONEBTC', 'HBARBTC', 'VETBTC', 'LTCBTC', 'BCHBTC', 'ETHBTC']
strategies_list = [1, 2, 4]

def check_buy_sell_que(TICKER_LABEL, STRATEGY=None, INTERVAL=None):
    """
    _summary_
        updates databse with historical ticker info
    Args:
        TICKER_LABEL (string): ticker id
        STRATEGY (int): strategy
        INTERVAL (string): interval
    """
    # make a tickerobject specified by ticker id
    ticker = tick.Ticker(TICKER_LABEL, STRATEGY, INTERVAL)
    # update ticker open high low close info
    ticker.update_historical_info()
    
def run_bot():
    """
    _summary_
        sets environment variables
        runs a repeated function every 900 seconds (15 min)
    """

    global ticker_label_list
    global strategies_list
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
    rt = util.RepeatedTimer(900, run_bot)
    
if __name__ == '__main__':
    config_ev.set_environment_variables()
    start()
    
