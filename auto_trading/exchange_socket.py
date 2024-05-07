import asyncio
from datetime import datetime
from binance.enums import KLINE_INTERVAL_1MINUTE
from binance import AsyncClient, BinanceSocketManager

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
            res = await ks.recv()
            handle_candlestick(res)

asyncio.run(binance_ws_client())
