from candle import get_bar_data

def timeframe_selection(chart):
    timeframe = chart.topbar["timeframe"].value
    symbol = chart.topbar["symbol"].value

    start = '2022-10-01 00:00:00'
    end = '2023-01-01 00:00:00'
    chart.spinner(True)
    data = get_bar_data(symbol, timeframe, start, end)
    chart.spinner(False)

    chart.set(data, True)
