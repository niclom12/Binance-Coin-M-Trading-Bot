from helper import Binance
from logmaker import log_trade, log_start, log_error
import schedule
import time
from Hull import logic
import datetime
import pandas as pd
from binance.exceptions import BinanceAPIException



tokens = ["BTCUSD_PERP", "DOGEUSD_PERP","SOLUSD_PERP", "LINKUSD_PERP", "BNBUSD_PERP", "ETHUSD_PERP"]
def algo(data):
    return logic(data)


def run_algo():
    time.sleep(3)
    client_info = pd.read_excel('Users.xlsx')
    first_row = client_info.iloc[0]
    binance = Binance(str(first_row['api']), str(first_row['private']))
    for token in tokens:
        try:
            data = binance.get_klines(token, 150)
            side, hull = algo(data)
            if (side == "Buy"):
                for index, row in client_info.iterrows():
                    try:
                        client = Binance(row.api, row.private)
                        quant = int(client.get_buy_amount(token, hull))
                        client.make_trade_market("Buy", token, quant)
                        positions = row.positions.split(",")
                        for i, position in enumerate(positions):
                            if token in position:
                                positions[i] = token + str(quant)
                        client_info.loc[index, 'positions'] = ",".join(positions)
                    except BinanceAPIException as e:
                        log_error(e)
                    
            elif (side == "Sell"):
                for index, row in client_info.iterrows():
                    try:
                        client = Binance(row.api, row.private)
                        positions = row.positions.split(",")
                        for i, position in enumerate(positions):
                            if token in position:
                                parts = position.split(token)
                                quant = int(parts[-1])  # get the last part after splitting
                                client.make_trade_market("Sell", token, quant)
                                positions[i] = token + '0'
                        client_info.loc[index, 'positions'] = ",".join(positions)
                    
                    except BinanceAPIException as e:
                        log_error(e)
            
        except BinanceAPIException as e:
            log_error(e)
            
    client_info.to_excel('Users.xlsx', index=False)



log_start()
schedule.every().day.at("02:00").do(run_algo)
schedule.every().day.at("06:00").do(run_algo)
schedule.every().day.at("10:00").do(run_algo)
schedule.every().day.at("14:00").do(run_algo)
schedule.every().day.at("18:00").do(run_algo)
schedule.every().day.at("22:00").do(run_algo)


while True:
    schedule.run_pending()
    time.sleep(1)
        

"""
log_start()
now = datetime.datetime.now()
seconds_until_half_hour = (30 - (now.minute % 30)) * 60 - now.second
time.sleep(seconds_until_half_hour)
run_algo()
schedule.every(30).minutes.do(run_algo)
while True:
    schedule.run_pending()
    time.sleep(1)
"""  

  
"""
def run_job_at_next_minute():
    current_time = datetime.datetime.now()
    delay = 60 - current_time.second + 2
    time.sleep(delay)
    run_algo()  # run job immediately after sleep

log_start()
while True:
    run_job_at_next_minute()



"""
