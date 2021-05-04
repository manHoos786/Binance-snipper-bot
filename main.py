import json
import websocket
from binance.client import Client
from binance.enums import *
import config
import time as time

Trade_symbol = 'TRXUSDT'
Trade_amount = '10'


SOCKET = f"wss://stream.binance.com:9443/ws/{Trade_symbol.lower()}@trade"

client = Client(config.API_KEY, config.API_SECRET)
print(client.get_order_book(symbol=Trade_symbol))

def order(symbol, quantity, price):
    try:        
        order = client.order_limit_sell(symbol= symbol, quantity = quantity, price = '0.13600')
        # order = client.create_test_order(symbol = symbol, side = SIDE_BUY, type = ORDER_TYPE_MARKET, quantity = quantity, price = price)
        print(order)
    except :
        return False
    return True


def on_message(ws, message):
    # j = round(time.time()*1000)
    # print(j)
    json_message = json.loads(message)
    c = float(json_message['p'])
    candle = round((c+0.04*c), 5) #========================================================= ENTER HERE THE PERCENTAGE===============================================
    quantity = (float(Trade_amount)/(c))
    k = round(quantity,1)
    
    order_succeeded = order(Trade_symbol,k,candle) #================================================= CHANGE C TO CANDLE FOR PERCENTAGE======================

    if order_succeeded:
        print("\n\nOrder succeeded successfully.")
        exit()
    else:
        print("\n\nInsufficient balance. Please try again.")
        exit()

ws = websocket.WebSocketApp(SOCKET,on_message=on_message).run_forever()

