import pandas as pd

def calculate_sma(df, period: int = 50):
    result = pd.DataFrame({
        'time': df['time'],
        f'SMA': df['close'].rolling(window=period).mean()
    }).dropna()
    result.set_index(result['time'], inplace=True)

    return result
