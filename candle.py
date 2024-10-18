import time
import warnings
import ccxt
import pandas

warnings.simplefilter(action='ignore', category=FutureWarning)
columns = ['time', 'open', 'high', 'low', 'close', 'volume']

def get_bar_data(symbol, timeframe, start, end):
    start_time = time.time()
    binance = ccxt.binance()
    limit = 500
    start = binance.parse8601(start)
    end = binance.parse8601(end)

    result = pandas.DataFrame(columns=columns)
    while start < end:
        data = binance.fetch_ohlcv(symbol, timeframe, start, limit=limit)
        if not len(data):
            break

        df = pandas.DataFrame(data, columns=columns)
        result = pandas.concat([result, df])

        start = data[-1][0] + binance.parse_timeframe(timeframe) * limit

    result['time'] = pandas.to_datetime(result['time'], unit='ms')
    result.set_index(keys='time')
    result.sort_index()

    return result
