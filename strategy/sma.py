import numpy
import pandas as pd
from pandas import DataFrame

def calculate_sma(df, period: int = 50):
    result = pd.DataFrame({
        'time': df['time'],
        f'SMA': df['close'].rolling(window=period).mean()
    })
    result.set_index(result['time'], inplace=True)

    return result

def calculate_sma_list(df, period: int = 50):
    values = df['close']
    return pd.Series(values).rolling(period).mean()

def calculate_latest_sma(data: DataFrame, period: int):
    values = data['close']
    values = values[-period:]

    if len(values) < period:
        return None

    return numpy.mean(values)
