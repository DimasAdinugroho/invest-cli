import pandas as pd


def crossover(df, idx, col1, col2, mul=1):
    if type(col2) is str:
        return df.loc[idx][col1] > df.loc[idx][col2]*mul and df.loc[idx - 1][col1] <= df.loc[idx - 1][col2]*mul if idx > 0 else False
    return df.loc[idx][col1] > col2*mul and df.loc[idx - 1][col1] <= col2*mul if idx > 0 else False


def crossunder(df, idx, col1, col2, mul=1):
    if type(col2) is str:
        return df.loc[idx][col1] < df.loc[idx][col2]*mul and df.loc[idx - 1][col1] >= df.loc[idx - 1][col2]*mul if idx > 0 else False
    return df.loc[idx][col1] < col2*mul and df.loc[idx - 1][col1] >= col2*mul if idx > 0 else False


def positive_gradient(df, idx, col, points=2):
    if idx < points:
        return False
    sum = 0
    for i in range(1, points+1):
        sum += df.loc[idx][col] - df.loc[idx-i][col]
    return sum/points > 0


def buy_idx(trx, stock):
    return trx[stock][-1]['idx']


def buy_price(trx, stock):
    return trx[stock][-1]['price']


rules = {
    '1': {
        'rules': [
            'BUY',
            'Buy on Next Opening Price',
            'Last Closing Price > SMA(100)',
            'SMA(20) > SMA(100)',
            'RSI(14) < 30',
            '',
            'SELL',
            'Cut Loss = Pivot Point Support 2 When Buying',
            'Trailing Stop = Lowest Low Last 3 Candles'
        ],
        'buy_condition': lambda df, idx: (
            df.loc[idx]['close'] > df.loc[idx]['sma(100)'] and
            df.loc[idx]['sma(20)'] > df.loc[idx]['sma(100)'] and
            df.loc[idx]['rsi(14)'] < 30
        ),
        'sell_price': lambda stock, df, idx, trx_list: (
            # buy_price = trx_list[stock][-1]['price']
            max(df.loc[idx]['pp:s2'], df.loc[idx]['lowest_low(3)'])
        )
    },
    '2': {
        'rules': [
            'BUY',
            'Buy on Next Opening Price',
            'Last Closing Price > SMA(100)',
            'SMA(20) > SMA(100)',
            'RSI(14) < 30',
            '',
            'SELL',
            'Cut Loss = Pivot Point Support 1 When Buying',
            'Trailing Stop = Lowest Low Last 3 Candles'
        ],
        'buy_condition': lambda df, idx: (
            df.loc[idx]['close'] > df.loc[idx]['sma(100)'] and \
            df.loc[idx]['sma(20)'] > df.loc[idx]['sma(100)'] and \
            df.loc[idx]['rsi(14)'] < 30
        ),
        'sell_price': lambda stock, df, idx, trx_list: (
            # buy_price = trx_list[stock][-1]['price']
            max(df.loc[idx]['pp:s1'], df.loc[idx]['lowest_low(3)'])
        )
    },
    '3': {
        'rules': [
            'BUY',
            'Buy on Next Opening Price',
            'Last Closing Price > SMA(100)',
            'SMA(20) > SMA(100)',
            'Stochastic(14,3,3):%K < 30',
            'Crossover Stochastic(14,3,3):%K to Stochastic(14,3,3):%D',
            '',
            'SELL',
            'Trailing Stop = Cut Los = Lowest Low Last 3 Candles'
        ],
        'buy_condition': lambda df, idx: (
            df.loc[idx]['close'] > df.loc[idx]['sma(100)'] and \
            df.loc[idx]['sma(20)'] > df.loc[idx]['sma(100)'] and \
            df.loc[idx]['stochastic(14,3,3):%K'] < 30 and \
            crossover(df, idx, 'stochastic(14,3,3):%K',
                      'stochastic(14,3,3):%D')
        ),
        'sell_price': lambda stock, df, idx, trx_list: (
            # buy_price = trx_list[stock][-1]['price']
            df.loc[idx]['lowest_low(3)']
        )
    },
    '4': {
        'rules': [
            'BUY',
            'Buy on Next Opening Price',
            'Last Closing Price > SMA(100)',
            'SMA(20) > SMA(100)',
            'Stochastic(14):%K < 30',
            'Stochastic(14):%D < 30',
            'Stochastic(14):%K > Stochastic(14):%D',
            '',
            'SELL',
            'Cut Loss = Pivot Point Support 1 When Buying',
            'Trailing Stop = Lowest Low Last 3 Candles'
        ],
        'buy_condition': lambda df, idx: (
            df.loc[idx]['close'] > df.loc[idx]['sma(100)'] and \
            df.loc[idx]['sma(20)'] > df.loc[idx]['sma(100)'] and \
            df.loc[idx]['stochastic(14):%K'] < 30 and \
            df.loc[idx]['stochastic(14):%D'] < 30 and \
            df.loc[idx]['stochastic(14):%K'] > df.loc[idx]['stochastic(14):%D']
        ),
        'sell_price': lambda stock, df, idx, trx_list: (
            # buy_price = trx_list[stock][-1]['price']
            max(df.loc[idx]['pp:s1'], df.loc[idx]['lowest_low(3)'])
        )
    },
    '5': {
        'rules': [
            'BUY',
            'Buy on Next Opening Price',
            'Last Closing Price > SMA(100)',
            'SMA(20) > SMA(100)',
            'Last Closing Price <= Lower Bollinger Bands(20,2)'
            '',
            'SELL',
            'Cut Loss <= Lower Bollinger Bands(20,3)',
            'Trailing Stop = Lowest Low Last 3 Candles'
        ],
        'buy_condition': lambda df, idx: (
            df.loc[idx]['close'] > df.loc[idx]['sma(100)'] and \
            df.loc[idx]['sma(20)'] > df.loc[idx]['sma(100)'] and \
            df.loc[idx]['close'] <= df.loc[idx]['bb(20,20):lower']
        ),
        'sell_price': lambda stock, df, idx, trx_list: (
            # buy_price = trx_list[stock][-1]['price']
            max(df.loc[idx]['bb(20,30):lower'], df.loc[idx]['lowest_low(3)'])
        )
    },
    '6': {
        'rules': [
            'BUY',
            'Buy on Next Opening Price',
            'Last Closing Price > SMA(100)',
            'SMA(20) > SMA(100)',
            'Last Closing Price <= Lower Bollinger Bands(20,2)'
            '',
            'SELL',
            'Cut Loss <= Lower Bollinger Bands(20,2.5)',
            'Trailing Stop = Lowest Low Last 3 Candles'
        ],
        'buy_condition': lambda df, idx: (
            df.loc[idx]['close'] > df.loc[idx]['sma(100)'] and \
            df.loc[idx]['sma(20)'] > df.loc[idx]['sma(100)'] and \
            df.loc[idx]['close'] <= df.loc[idx]['bb(20,20):lower']
        ),
        'sell_price': lambda stock, df, idx, trx_list: (
            # buy_price = trx_list[stock][-1]['price']
            max(df.loc[idx]['bb(20,25):lower'], df.loc[idx]['lowest_low(3)'])
        )
    },
    '7': {
        'rules': [
            'BUY',
            'Buy on Next Opening Price',
            'Last Closing Price > SMA(100)',
            'SMA(20) > SMA(100)',
            'Last Closing Price <= Lower Bollinger Bands(20,2.5)'
            '',
            'SELL',
            'Cut Loss <= Lower Bollinger Bands(20,3)',
            'Trailing Stop = Lowest Low Last 3 Candles'
        ],
        'buy_condition': lambda df, idx: (
            df.loc[idx]['close'] > df.loc[idx]['sma(100)'] and \
            df.loc[idx]['sma(20)'] > df.loc[idx]['sma(100)'] and \
            df.loc[idx]['close'] <= df.loc[idx]['bb(20,25):lower']
        ),
        'sell_price': lambda stock, df, idx, trx_list: (
            # buy_price = trx_list[stock][-1]['price']
            max(df.loc[idx]['bb(20,30):lower'], df.loc[idx]['lowest_low(3)'])
        )
    },
    '8': {
        'rules': [
            'BUY',
            'Buy on Next Opening Price',
            'Last Closing Price > SMA(100)',
            'RSI(14) < 30',
            '',
            'SELL',
            'Cut Loss = Pivot Point Support 2 When Buying',
            'Trailing Stop = Lowest Low Last 3 Candles'
        ],
        'buy_condition': lambda df, idx: (
            df.loc[idx]['close'] > df.loc[idx]['sma(100)'] and \
            df.loc[idx]['rsi(14)'] < 30
        ),
        'sell_price': lambda stock, df, idx, trx_list: (
            # buy_price = trx_list[stock][-1]['price']
            max(df.loc[idx]['pp:s2'], df.loc[idx]['lowest_low(3)'])
        )
    },
    '9': {
        'rules': [
            'BUY',
            'Buy on Next Opening Price',
            'Last Closing Price > SMA(100)',
            'RSI(14) < 30',
            '',
            'SELL',
            'Cut Loss = Pivot Point Support 1 When Buying',
            'Trailing Stop = Lowest Low Last 3 Candles'
        ],
        'buy_condition': lambda df, idx: (
            df.loc[idx]['close'] > df.loc[idx]['sma(100)'] and \
            df.loc[idx]['rsi(14)'] < 30
        ),
        'sell_price': lambda stock, df, idx, trx_list: (
            # buy_price = trx_list[stock][-1]['price']
            max(df.loc[idx]['pp:s1'], df.loc[idx]['lowest_low(3)'])
        )
    },
    '10': {
        'rules': [
            'BUY',
            'Buy on Next Opening Price',
            'Last Closing Price > SMA(100)',
            'Stochastic(14):%K < 30',
            'Stochastic(14):%D < 30',
            'Stochastic(14):%K > Stochastic(14):%D',
            '',
            'SELL',
            'Cut Loss = Pivot Point Support 2 When Buying',
            'Trailing Stop = Lowest Low Last 3 Candles'
        ],
        'buy_condition': lambda df, idx: (
            df.loc[idx]['close'] > df.loc[idx]['sma(100)'] and \
            df.loc[idx]['stochastic(14):%K'] < 30 and \
            df.loc[idx]['stochastic(14):%D'] < 30 and \
            df.loc[idx]['stochastic(14):%K'] > df.loc[idx]['stochastic(14):%D']
        ),
        'sell_price': lambda stock, df, idx, trx_list: (
            # buy_price = trx_list[stock][-1]['price']
            max(df.loc[idx]['pp:s2'], df.loc[idx]['lowest_low(3)'])
        )
    },
    '11': {
        'rules': [
            'BUY',
            'Buy on Next Opening Price',
            'Last Closing Price > SMA(100)',
            'Stochastic(14):%K < 30',
            'Stochastic(14):%D < 30',
            'Stochastic(14):%K > Stochastic(14):%D',
            '',
            'SELL',
            'Cut Loss = Pivot Point Support 1 When Buying',
            'Trailing Stop = Lowest Low Last 3 Candles'
        ],
        'buy_condition': lambda df, idx: (
            df.loc[idx]['close'] > df.loc[idx]['sma(100)'] and \
            df.loc[idx]['stochastic(14):%K'] < 30 and \
            df.loc[idx]['stochastic(14):%D'] < 30 and \
            df.loc[idx]['stochastic(14):%K'] > df.loc[idx]['stochastic(14):%D']
        ),
        'sell_price': lambda stock, df, idx, trx_list: (
            # buy_price = trx_list[stock][-1]['price']
            max(df.loc[idx]['pp:s1'], df.loc[idx]['lowest_low(3)'])
        )
    },
    '12': {
        'rules': [
            'BUY',
            'Buy on Next Opening Price',
            'Last Closing Price > SMA(100)',
            'Last Closing Price <= Lower Bollinger Bands(20,2)'
            '',
            'SELL',
            'Cut Loss <= Lower Bollinger Bands(20,3)',
            'Trailing Stop = Lowest Low Last 3 Candles'
        ],
        'buy_condition': lambda df, idx: (
            df.loc[idx]['close'] > df.loc[idx]['sma(100)'] and \
            df.loc[idx]['close'] <= df.loc[idx]['bb(20,20):lower']
        ),
        'sell_price': lambda stock, df, idx, trx_list: (
            # buy_price = trx_list[stock][-1]['price']
            max(df.loc[idx]['bb(20,30):lower'], df.loc[idx]['lowest_low(3)'])
        )
    },
    '13': {
        'rules': [
            'BUY',
            'Buy on Next Opening Price',
            'Last Closing Price > SMA(100)',
            'Last Closing Price <= Lower Bollinger Bands(20,2)'
            '',
            'SELL',
            'Cut Loss <= Lower Bollinger Bands(20,2.5)',
            'Trailing Stop = Lowest Low Last 3 Candles'
        ],
        'buy_condition': lambda df, idx: (
            df.loc[idx]['close'] > df.loc[idx]['sma(100)'] and \
            df.loc[idx]['close'] <= df.loc[idx]['bb(20,20):lower']
        ),
        'sell_price': lambda stock, df, idx, trx_list: (
            # buy_price = trx_list[stock][-1]['price']
            max(df.loc[idx]['bb(20,25):lower'], df.loc[idx]['lowest_low(3)'])
        )
    },
    '14': {
        'rules': [
            'BUY',
            'Buy on Next Opening Price',
            'Last Closing Price > SMA(100)',
            'Last Closing Price <= Lower Bollinger Bands(20,2.5)'
            '',
            'SELL',
            'Cut Loss <= Lower Bollinger Bands(20,3)',
            'Trailing Stop = Lowest Low Last 3 Candles'
        ],
        'buy_condition': lambda df, idx: (
            df.loc[idx]['close'] > df.loc[idx]['sma(100)'] and \
            df.loc[idx]['close'] <= df.loc[idx]['bb(20,25):lower']
        ),
        'sell_price': lambda stock, df, idx, trx_list: (
            # buy_price = trx_list[stock][-1]['price']
            max(df.loc[idx]['bb(20,30):lower'], df.loc[idx]['lowest_low(3)'])
        )
    },
    '15': {
        'rules': [
            'BUY',
            'Buy on Next Opening Price',
            'Last Closing Price > SMA(50)',
            'SMA(10) > SMA(20)'
            '',
            'SELL',
            'Cut Loss = Pivot Point Support 1 When Buying',
            'Trailing Stop = Lowest Low Last 3 Candles'
        ],
        'buy_condition': lambda df, idx: (
            df.loc[idx]['close'] > df.loc[idx]['sma(50)'] and \
            df.loc[idx]['sma(10)'] > df.loc[idx]['sma(20)']
        ),
        'sell_price': lambda stock, df, idx, trx_list: (
            # buy_price = trx_list[stock][-1]['price']
            max(df.loc[idx]['pp:s1'], df.loc[idx]['lowest_low(3)'])
        )
    },
    '16': {
        'rules': [
            'BUY',
            'Buy on Next Opening Price',
            'Last Closing Price > SMA(50)',
            'SMA(10) = 100% ~ 110% SMA(20)'
            '',
            'SELL',
            'Cut Loss = Pivot Point Support 1 When Buying',
            'Trailing Stop = Lowest Low Last 3 Candles'
        ],
        'buy_condition': lambda df, idx: (
            df.loc[idx]['close'] > df.loc[idx]['sma(50)'] and \
            df.loc[idx]['sma(10)'] > df.loc[idx]['sma(20)'] and \
            df.loc[idx]['sma(10)'] < 1.1*df.loc[idx]['sma(20)']
        ),
        'sell_price': lambda stock, df, idx, trx_list: (
            # buy_price = trx_list[stock][-1]['price']
            max(df.loc[idx]['pp:s1'], df.loc[idx]['lowest_low(3)'])
        )
    },
    '17': {
        'rules': [
            'BUY',
            'Buy on Next Opening Price',
            'MACD(12,26,9) Signal Crossover',
            '',
            'SELL',
            'Cut Loss = Pivot Point Support 1',
            'Trailing Stop = Lowest Low Last 3 Candles'
        ],
        'buy_condition': lambda df, idx: (
            crossover(df, idx, 'macd(12,26,9):macd', 'macd(12,26,9):signal')
        ),
        'sell_price': lambda stock, df, idx, trx_list: (
            # buy_price = trx_list[stock][-1]['price']
            max(df.loc[idx]['pp:s1'], df.loc[idx]['lowest_low(3)'])
        )
    },
    '18': {
        'rules': [
            'BUY',
            'Buy on Next Opening Price',
            'MACD(12,26,9) Signal Crossover',
            '',
            'SELL',
            'Cut Loss = Pivot Point Support 2',
            'Trailing Stop = Lowest Low Last 3 Candles'
        ],
        'buy_condition': lambda df, idx: (
            crossover(df, idx, 'macd(12,26,9):macd', 'macd(12,26,9):signal')
        ),
        'sell_price': lambda stock, df, idx, trx_list: (
            # buy_price = trx_list[stock][-1]['price']
            max(df.loc[idx]['pp:s2'], df.loc[idx]['lowest_low(3)'])
        )
    },
    '19': {
        'rules': [
            'BUY',
            'Buy on Next Opening Price',
            'MACD(12,26,9) Signal Crossover',
            '',
            'SELL',
            'MACD(12,26,9) Signal Crossunder',
        ],
        'buy_condition': lambda df, idx: (
            crossover(df, idx, 'macd(12,26,9):macd', 'macd(12,26,9):signal')
        ),
        'sell_price': lambda stock, df, idx, trx_list: (
            10**6 if crossunder(df, idx, 'macd(12,26,9):macd',
                                'macd(12,26,9):signal') else -1
        )
    },
    '20': {
        'rules': [
            'BUY',
            'Buy on Next Opening Price',
            'MACD(12,26,6) Signal Crossover',
            '',
            'SELL',
            'if [MACD(12,26,6) Signal Crossunder] or [Support 1 broken]',
        ],
        'buy_condition': lambda df, idx: (
            crossover(df, idx, 'macd(12,26,9):macd', 'macd(12,26,9):signal')
        ),
        'sell_price': lambda stock, df, idx, trx_list: (
            10**6 if crossunder(df, idx, 'macd(12,26,6):macd',
                                'macd(12,26,6):signal') else df.loc[idx]['pp:s1']
        )
    },
    '21': {
        'rules': [
            'Bollinger Bands'
        ],
        'buy_condition': lambda df, idx: (
            crossover(df, idx, 'bb(20,20):%b', 0.1)
        ),
        'sell_price': lambda stock, df, idx, trx_list: (
            10**6 if \
            crossunder(df, idx, 'bb(20,20):%b', 1) or \
            crossunder(df, idx, 'bb(20,20):%b', 0.5) or \
            crossunder(df, idx, 'bb(20,20):%b', 0) or \
            crossunder(df, idx, 'close', buy_price(trx_list, stock)*0.95) \
            else -1
        )
    },
    '22': {
        'rules': [
            'MACD'
        ],
        'buy_condition': lambda df, idx: (
            crossover(df, idx, 'macd(12,26,9):macd', 'macd(12,26,9):signal')
        ),
        'sell_price': lambda stock, df, idx, trx_list: (
            10**6 if \
            crossunder(df, idx, 'macd(12,26,9):macd', 'macd(12,26,9):signal') \
            else -1
        )
    },
    '23': {
        'rules': [
            'BUY',
            'Buy on Next Opening Price',
            'Last Closing Price > SMA(100)',
            'SMA(20) > SMA(100)',
            'Stochastic(14):%D < 30',
            'Stochastic(14):%K Crossovers Stochastic(14):%D',
            '',
            'SELL',
            'Cut Loss = Pivot Point Support 2 When Buying',
            'Trailing Stop = Lowest Low Last 3 Candles'
        ],
        'buy_condition': lambda df, idx: (
            df.loc[idx]['close'] > df.loc[idx]['sma(100)'] and \
            df.loc[idx]['sma(20)'] > df.loc[idx]['sma(100)'] and \
            df.loc[idx]['stochastic(14):%K'] < 30 and \
            df.loc[idx]['stochastic(14):%D'] < 30 and \
            crossover(df, idx, 'stochastic(14):%K', 'stochastic(14):%D')
        ),
        'sell_price': lambda stock, df, idx, trx_list: (
            max(df.loc[buy_idx(trx_list, stock)]
                ['pp:s2'], df.loc[idx]['lowest_low(3)'])
        )
    },
    '24': {
        'rules': [
            'BUY',
            'Buy on Next Opening Price',
            'S1',
            '',
            'SELL',
            'R1'
        ],
        'buy_condition': lambda df, idx: (
            crossunder(df, idx, 'close', 'pp:s1')
        ),
        'sell_price': lambda stock, df, idx, trx_list: (
            df.loc[idx]['pp:r1']
        )
    },
}
