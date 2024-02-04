from lightweight_charts.widgets import QtChart
from candle import get_bar_data
from strategy.sma import calculate_sma

class CustomChart(QtChart):
    def __init__(self, symbol='BTC/USDT', timeframe='1h', start='2022-10-01 00:00:00', end='2023-01-01 00:00:00'):
        super().__init__()
        self.start = start
        self.end = end
        self.bars = get_bar_data(symbol, timeframe, start, end)
        self._indicators = []

        self.set_topbar(symbol, timeframe)

        self.events.search += on_search
        self.draw()

    @property
    def timeframe(self):
        return self.topbar["timeframe"].value

    @property
    def symbol(self):
        return self.topbar["symbol"].value

    def set_topbar(self, symbol, timeframe):
        self.topbar.textbox('symbol', symbol)
        self.topbar.switcher(
            'timeframe',
            ('1m', '5m', '15m', '30m', '1h', '4h', '1d'),
            default=timeframe,
            func=timeframe_selection
        )

    def draw(self):
        self.clear_all()
        self.bars = get_bar_data(self.symbol, self.timeframe, self.start, self.end)
        self.set(self.bars)
        self.draw_indicator()
        self.draw_mark()

    def draw_indicator(self):
        self.clear_indicators()

        line_sma5 = self.create_line(name='SMA', price_line=False, price_label=False)
        line_sma20 = self.create_line(name='SMA', price_line=False, price_label=False)
        sma5 = calculate_sma(self.bars, 5)
        sma20 = calculate_sma(self.bars, 20)
        line_sma5.set(sma5)
        line_sma20.set(sma20)

        self._indicators.append(line_sma5)
        self._indicators.append(line_sma20)

    def clear_all(self):
        self.set(None)
        self.clear_horizontal_lines()
        self.clear_markers()
        self.clear_indicators()

    def clear_indicators(self):
        for indicator in self._indicators:
            indicator.delete()

        self._indicators = []

    def draw_mark(self):
        self.clear_markers()

        sma5 = calculate_sma(self.bars, 5)
        sma20 = calculate_sma(self.bars, 20)

        in_position = False

        for i in range(0, len(sma20) - 1):
            time = sma20.iloc[i]['time']
            sma5_value = sma5.loc[time]['SMA']
            sma20_value = sma20.iloc[i]['SMA']

            if sma5_value > sma20_value and not in_position:
                self.marker(time=time, text='Long', position='below', shape='arrow_up', color='#990000')
                in_position = True
            elif sma5_value < sma20_value and in_position:
                self.marker(time=time, text='Short', position='above', shape='arrow_down', color='#003399')
                in_position = False

def on_search(chart, search):
    chart.spinner(True)
    chart.draw()
    chart.spinner(False)
    chart.topbar['symbol'].set(search)


def timeframe_selection(chart):
    chart.spinner(True)
    chart.draw()
    chart.spinner(False)

