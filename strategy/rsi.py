import talib
from pandas import DataFrame

def calculate_rsi(df, period: int = 14):
    result = DataFrame({
        'time': df['time'],
        'RSI': talib.RSI(df['close'], period)
    })
    result.set_index(result['time'], inplace=True)

    return result

def calculate_latest_rsi(data: DataFrame, period: int):
    values = data['close']
    values = values[-(period + 1):]

    if len(values) < period + 1:
        return None

    return float(talib.RSI(values, period)[-1:])
