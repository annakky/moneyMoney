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

    if len(values) < period:
        return None

    return float(talib.RSI(values, period)[-1:])
