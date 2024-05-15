import asyncio
from datetime import datetime
from binance.enums import KLINE_INTERVAL_1MINUTE
from binance import AsyncClient, BinanceSocketManager
from pandas import DataFrame

"""
{
  "e": "kline",         // Event type
  "E": 1672515782136,   // Event time
  "s": "BNBBTC",        // Symbol
  "k": {
    "t": 1672515780000, // Kline start time
    "T": 1672515839999, // Kline close time
    "s": "BNBBTC",      // Symbol
    "i": "1m",          // Interval
    "f": 100,           // First trade ID
    "L": 200,           // Last trade ID
    "o": "0.0010",      // Open price
    "c": "0.0020",      // Close price
    "h": "0.0025",      // High price
    "l": "0.0015",      // Low price
    "v": "1000",        // Base asset volume
    "n": 100,           // Number of trades
    "x": false,         // Is this kline closed?
    "q": "1.0000",      // Quote asset volume
    "V": "500",         // Taker buy base asset volume
    "Q": "0.500",       // Taker buy quote asset volume
    "B": "123456"       // Ignore
  }
}
https://developers.binance.com/docs/binance-spot-api-docs/web-socket-streams#klinecandlestick-streams
"""


def timestamp_to_datetime(timestamp):
    dt_object = datetime.fromtimestamp(timestamp / 1000)
    return dt_object.strftime("%Y-%m-%d %H:%M:%S")

def handle_candlestick(msg):
    close_time = msg['k']['T']
    event_time = msg['E']

    if event_time > close_time:
        print("===============")
        print(timestamp_to_datetime(close_time))
        print(msg['k']['c'])
        print("\n")

async def binance_ws_client():
    client = await AsyncClient.create()
    bm = BinanceSocketManager(client)
    ks = bm.kline_socket('BTCUSDT', interval=KLINE_INTERVAL_1MINUTE)

    async with ks as k:
        while True:
            response = await ks.recv()

            data = DataFrame({
                'time': [datetime.fromtimestamp(response['k']['t'] / 1000)],
                'open': [response['k']['o']],
                'high': [response['k']['h']],
                'low': [response['k']['l']],
                'close': [response['k']['c']],
                'volume': [response['k']['v']]
            })
            print(data)
            handle_candlestick(response)

asyncio.run(binance_ws_client())
