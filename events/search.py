from candle import get_bar_data

def on_search(chart, search):
    start = '2022-10-01 00:00:00'
    end = '2023-01-01 00:00:00'
    chart.spinner(True)
    data = get_bar_data(search, chart.topbar["timeframe"].value, start, end)
    chart.spinner(False)
    chart.topbar['symbol'].set(search)
    chart.set(data)
