import time
from openpyxl import Workbook
import pandas as pd
from datetime import datetime



def log_start():
    out = '[SESSION START] ' + str(time.ctime(time.time()))
    file = open('bot_log.txt', 'a', encoding='utf-8')
    file.write(out + '\n')
    file.close()
    column_names = ['Date', 'Ticker','quantity', 'Open Price', 'Close Price', 'Profit($)', 'Profit(%)']
    data = [["", "", 0.0, 0.0, 0.0, 0.0, 0.0]]
    trades = pd.DataFrame(columns = column_names, data=data)
    trades['Profit($)'] = trades['Profit($)'].astype(float)
    trades['Profit(%)'] = trades['Profit(%)'].astype(float)
    trades['quantity'] = trades['quantity'].astype(float)
    trades['Open Price'] = trades['Open Price'].astype(float)
    trades['Close Price'] = trades['Close Price'].astype(float)
    trades.to_excel('Trades.xlsx', index=False)



def log_error(errmsg):
    out = '[SESSION ERROR] ' + str(time.ctime(time.time())) + ' (' + str(errmsg) + ')'
    with open('bot_log.txt', 'a', encoding='utf-8') as file:
        file.write(out + '\n')
        file.close()


def log_trade(side, symbol, Quant, price):
    trade_data = pd.read_excel('Trades.xlsx')
    if side == "Buy":
        instance = {
            'Date': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            'Ticker': symbol,
            'quantity': float(Quant),
            'Open Price': float(price),
            'Close Price': 0.0,
            'Profit($)': 0.0,
            'Profit(%)': 0.0
        }
        instance_df = pd.DataFrame([instance])
        trade_data = pd.concat([trade_data, instance_df], ignore_index=True)

    else:
        #Should make this less clunky
        trade_reversed = trade_data[::-1]
        index = trade_reversed.loc[trade_reversed['Ticker'] == symbol].first_valid_index()
        trade_data['Close Price'] = trade_data['Close Price'].astype(float)
        trade_data.loc[index, 'Close Price'] = float(price)        
        open = float(trade_data.loc[index, 'Open Price'])
        Quant = float(trade_data.loc[index, 'quantity'])
        price = float(price)
        trade_data['Profit($)'] = trade_data['Profit($)'].astype(float)
        trade_data['Profit(%)'] = trade_data['Profit(%)'].astype(float)
        trade_data.loc[index, 'Profit($)'] = float(((price - open) / open) * Quant)
        trade_data.loc[index, 'Profit(%)'] = float(((price - open) / open) * 100)

    trade_data.to_excel('Trades.xlsx', index=False)


def log_response(response):
    out = '[RESPONSE] ' + str(time.ctime(time.time())) + ' ' + response
    file = open('bot_log.txt', 'a')
    file.write(out + '\n')
    file.close()

    
    

