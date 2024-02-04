import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget
from candle import get_bar_data
from events.custom_chart import CustomChart

if __name__ == '__main__':
    # chart = Chart(width=1000, inner_width=0.7, inner_height=1)

    ss = '2022-10-01 00:00:00'
    ee = '2023-01-01 00:00:00'

    data = get_bar_data('BTC/USDT', '1h', ss, ee)

    # chart.set(data)
    # line = chart.create_line('SMA 50')
    # sma_data = calculate_sma(data, period=50)
    # line.set(sma_data)
    #
    # chart.topbar.textbox('symbol', 'BTC/USDT')
    # chart.topbar.switcher(
    #     'timeframe',
    #     ('1m', '5m', '15m', '30m', '1h', '4h', '1d'),
    #     default='1h',
    #     func=timeframe_selection
    # )
    #
    # chart.events.search += on_search
    #
    # table = chart.create_table(width=0.3, height=0.2,
    #                            headings=('Ticker', 'Quantity', 'Status', '%', 'PL'),
    #                            widths=(0.2, 0.1, 0.2, 0.2, 0.3),
    #                            alignments=('center', 'center', 'right', 'right', 'right'),
    #                            position='left')
    #
    # table.format('PL', f'£ {table.VALUE}')
    # table.format('%', f'{table.VALUE} %')
    # table.new_row()
    #
    # table.new_row('SPY', 3, 'Submitted', 0, 0)
    # table.new_row('AMD', 1, 'Filled', 25.5, 105.24)
    # table.new_row('NVDA', 2, 'Filled', -0.5, -8.24)
    #
    # table.footer(2)
    # table.footer[0] = 'Selected:'
    #
    # chart.show(block=True)
    app = QApplication(sys.argv)
    window = QMainWindow()
    layout = QVBoxLayout()
    widget = QWidget()
    widget.setLayout(layout)

    window.resize(800, 500)
    layout.setContentsMargins(0, 0, 0, 0)

    chart = CustomChart()

    layout.addWidget(chart.get_webview())

    window.setCentralWidget(widget)
    window.show()

    sys.exit(app.exec_())
