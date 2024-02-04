from PyQt5.QtWidgets import QWidget
from lightweight_charts.widgets import QtChart
from pandas import DataFrame
from candle import get_bar_data
from events.search import on_search
from events.timeframe import timeframe_selection
from strategy.sma import calculate_sma

class Chart(QWidget):
    def __init__(self):
        super().__init__()
        self.chart = QtChart(self)
        self.init_ui()

    def init_ui(self):
        start = '2022-10-01 00:00:00'
        end = '2023-01-01 00:00:00'
        data = get_bar_data('BTC/USDT', '1h', start, end)

        self.chart.topbar.textbox('symbol', 'BTC/USDT')
        self.chart.topbar.switcher(
            'timeframe',
            ('1m', '5m', '15m', '30m', '1h', '4h', '1d'),
            default='1h',
            func=timeframe_selection
        )

        self.chart.events.search += on_search

        self.chart.set(data)

        line_sma5 = self.chart.create_line(name='SMA')
        line_sma20 = self.chart.create_line(name='SMA')
        sma5 = calculate_sma(data, 5)
        sma20 = calculate_sma(data, 20)
        line_sma5.set(sma5)
        line_sma20.set(sma20)

        self.mark(data)

    def get_view(self):
        return self.chart.get_webview()

    def mark(self, data: DataFrame):
        self.chart.clear_markers()
        sma5 = calculate_sma(data, 5)
        sma20 = calculate_sma(data, 20)

        in_position = False

        for i in range(0, len(sma20) - 1):
            time = sma20.iloc[i]['time']
            sma5_value = sma5.loc[time]['SMA']
            sma20_value = sma20.iloc[i]['SMA']

            if sma5_value > sma20_value and not in_position:
                self.chart.marker(time=time, text='Long', position='below', shape='arrow_up', color='#990000')
                in_position = True
            elif sma5_value < sma20_value and in_position:
                self.chart.marker(time=time, text='Short', position='above', shape='arrow_down', color='#003399')
                in_position = False
