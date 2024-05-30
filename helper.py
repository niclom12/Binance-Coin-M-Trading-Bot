from binance.client import Client
from binance.exceptions import BinanceAPIException
import time
from logmaker import log_error


leverage = {"BTCUSD_PERP": 5.0, "ETHUSD_PERP":3.25, "SOLUSD_PERP": 3.0, "DOGEUSD_PERP": 2.0, "BNBUSD_PERP": 3.7, "LINKUSD_PERP": 3.0}
class Binance:
    
    def __init__(self, api, secret):
        self.api = api
        self.secret = secret
        try:
            self.session = Client(api, secret)
            server_time = self.session.get_server_time()
            time_diff = server_time['serverTime'] - int(time.time() * 1000)
            self.session.timestamp_offset = time_diff
            self.session = Client(api, secret)
            self.session.API_URL = 'https://dapi.binance.com/dapi'
            self.session.timestamp_offset = time_diff
        except BinanceAPIException as e:
            log_error(e)
            
    def get_klines(self, symbol, size):
        try:
            data = self.session.futures_coin_klines(symbol=symbol, interval=Client.KLINE_INTERVAL_4HOUR, limit=size)
            closing_prices = [float(kline[4]) for kline in data]
            closing_prices.reverse()
            return closing_prices[1:]
        except BinanceAPIException as e:
            log_error(e)
        
    
    def get_balance(self, type):
        try:
            balance_info = self.session.futures_coin_account_balance()
            for asset in balance_info:
                if asset['asset'] == type:
                    return float(asset['balance'])
        except BinanceAPIException as e:
            log_error(e)       
            
    def get_buy_amount(self, symbol, hull):
        try:
            contract_info = self.session.futures_coin_exchange_info()
            contract_size = 0
            for symbol_info in contract_info['symbols']:
                if symbol_info['symbol'] == symbol:
                    contract_size = float(symbol_info['contractSize'])
                    break
            coin = symbol.split("USD")[0]
            
            coin_balance = self.get_balance(coin)
            print(coin_balance)
            data = self.session.futures_coin_klines(symbol=symbol, interval=Client.KLINE_INTERVAL_30MINUTE, limit=1)
            closing_price = float(data[0][4])
            b3 = abs(((closing_price - hull) / closing_price) * 100)
            amount = (closing_price * coin_balance) / contract_size
            lev = (100 / (9 * (b3 * 0.9206 + 1.4126)))
            if (lev >= 10):
                lev = 10
            amount = round(amount * lev)
            return amount
        except BinanceAPIException as e:
            log_error(e)

            
    def make_trade_market(self, side, symbol, quant):
        try:
            resp = 1
            if(side == "Buy"):
                order = self.session.futures_coin_create_order(
                symbol=symbol,
                side=Client.SIDE_BUY,
                type=Client.ORDER_TYPE_MARKET,
                quantity=quant
                )
                if order['status'] == 'FILLED':
                    resp = 0
            else:
                order = self.session.futures_coin_create_order(
                symbol=symbol,
                side=Client.SIDE_SELL,
                type=Client.ORDER_TYPE_MARKET,
                quantity=quant
                )
                if order['status'] == 'FILLED':
                    resp = 0
            return resp
        except BinanceAPIException as e:
            log_error(e)
 
