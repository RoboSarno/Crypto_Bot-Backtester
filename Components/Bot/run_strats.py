import util
import tick
import config_ev

# library imports
from datetime import datetime
from datetime import timedelta
import pandas as pd
import pytz

# from message import Twilio

# ticker_label_list = ['ADABTC', 'ONEBTC', 'HBARBTC', 'VETBTC', 'LTCBTC', 'BCHBTC', 'ETHBTC']
# SLPBTC
ticker_label_list = ['ADABTC']

# strategies_list = [3]
strategies_list = [1, 2, 4]

def get_utc_datetimes(dt, lt):
    """_summary_

    Args:
        dt (int): current time
        lt (int): last buy or sell signal time

    Returns:
        tupl: (
            string of current closest 15 min interval,
            string of last buy and sell signal time
        )
    """
    lt = datetime.utcfromtimestamp(lt.tolist()/1e9)
    dt = dt - timedelta(minutes=dt.minute % 15,
                            seconds=dt.second,
                            microseconds=dt.microsecond)
    local = pytz.timezone("US/Pacific")
    local_dt = local.localize(dt, is_dst=None)
    utc_dt = (local_dt.astimezone(pytz.utc)-timedelta(hours=7)).strftime('%Y-%m-%d %H:%M:%S')
    
    local_lt = local.localize(lt, is_dst=None)
    utc_lt = (local_lt.astimezone(pytz.utc)-timedelta(hours=7)).strftime('%Y-%m-%d %H:%M:%S')
    
    
    return utc_dt, utc_lt

def check_buy_sell_que(TICKER_LABEL, STRATEGY, INTERVAL):
    """_summary_
    Args:
        TICKER_LABEL (string): ticker id
        STRATEGY (int): strategy
        INTERVAL (string): interval
    """
    # set floor value to round current time
    if STRATEGY == 1:
        strat_string = 'PSAR + MACD + EMA'
        floor = 30
    elif STRATEGY == 2:
        strat_string = 'RSI + EMA + ST'
        floor = 15
    elif STRATEGY == 3:
        strat_string = 'SqueezeM'
        floor = 60
    elif STRATEGY == 4:
        strat_string = 'Hoffman'
        floor = 15


    # Converting a to string in the desired format (YYYY-MM-DD HH:MM:SS) using strftime
    # make a ticker with a specific strategy
    ticker = tick.Ticker(TICKER_LABEL, STRATEGY, INTERVAL)
    # update ticker info
    print(TICKER_LABEL, STRATEGY, INTERVAL)
    ticker.update_database_info()
    # get the last 15 min interval
    CURRENT_TIME, LAST_TIME = get_utc_datetimes(datetime.now(), ticker.last_action['datetime'].values[-1])

    # get utc times to compare
    print('Does', CURRENT_TIME,'=', LAST_TIME, CURRENT_TIME == LAST_TIME)
    # send sms message
        # if there is a buy sig or sell sig that == the current time
    if CURRENT_TIME == LAST_TIME:
        # make sms connection
        sms_message = tick.Twil()
        buy_or_sell = ticker.last_action['b_s'].iloc[-1]
        # if its a buy sig send message
        if buy_or_sell:
            message = f'Buy Signal using SRAT: {strat_string} on LABL: {TICKER_LABEL} at TIME: {CURRENT_TIME} PST'
            sms_message.buy_sig_hit(message)
        # if its a sell sig send message
        elif not buy_or_sell:
            message = f'Sell Signal using SRAT: {strat_string} on LABL: {TICKER_LABEL} at TIME: {CURRENT_TIME} PST'
            sms_message.sell_sig_hit(message)
    # dont send sms message
        
    # del ticker
    
def run_stratagies():
    """_summary_
        - run all strategies on list of tickers
    """
    global ticker_label_list
    global strategies_list
    # list of past stratagies
    # for each ticker label in list
    # display_info = pd.DataFrame()
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
            # display_info = display_info.append({'ticker': result[0], 'strat':result[1], 'ticker_id':result[2]}, ignore_index=True)
            # del result
    # send display info to display file
    # return display_info
def run_bot():
    """_summary_
        - sets environment variables
        - runs a repeated function every 900 seconds (15 min)
    """
    run_stratagies()
    # rt = util.RepeatedTimer(900, run_stratagies)
    

    
if __name__ == '__main__':
    config_ev.set_environment_variables()
    run_bot()
    
