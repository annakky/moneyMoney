from lightweight_charts.widgets import QtChart
from candle import get_bar_data
from strategy.MyStrategy import MyStrategy
from strategy.Strategy import Position

class Chart(QtChart):
    def __init__(self, strategy=None, start='2022-01-01 00:00:00', end='2023-01-01 00:00:00'):
        self.width = 1
        self.height = 1
        super().__init__(inner_width=self.width, inner_height=self.height)
        self.start = start
        self.end = end
        self.strategy = strategy

        self.set_topbar('BTC/USDT', '1h')
        self.bars = get_bar_data(self.symbol, self.timeframe, self.start, self.end)

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

    def set_strategy(self, strategy: MyStrategy):
        self.strategy = strategy

    def set_datetime(self, start, end):
        self.start = start
        self.end = end

    def draw(self):
        self.clear_all()
        self.bars = get_bar_data(self.symbol, self.timeframe, self.start, self.end)
        self.set(self.bars)

        if self.strategy is not None:
            self.draw_mark()
            self.draw_indicator()

    def draw_indicator(self):
        self.strategy.draw_indicators(self)

    def clear_all(self):
        self.set(None)
        self.clear_horizontal_lines()
        self.clear_markers()
        self.clear_indicators()

    def clear_indicators(self):
        self.clear_markers()
        self.strategy.clear_indicators(self)

    def draw_mark(self):
        self.clear_markers()

        for i in range(0, len(self.bars)):
            data = self.bars.iloc[[i]]
            self.strategy.append_data(data)
            position = self.strategy.position()

            if position is Position.BUY:
                self.draw_long(data)
            elif position is Position.SELL:
                self.draw_short(data)

    def draw_long(self, data):
        self.marker(time=data.iloc[0]["time"], text='Long', position='below', shape='arrow_up', color='#990000')

    def draw_short(self, data):
        self.marker(time=data.iloc[0]["time"], text='Short', position='above', shape='arrow_down', color='#003399')

def on_search(chart, search):
    chart.spinner(True)
    chart.draw()
    chart.spinner(False)
    chart.topbar['symbol'].set(search)


def timeframe_selection(chart):
    chart.spinner(True)
    chart.draw()
    chart.spinner(False)

