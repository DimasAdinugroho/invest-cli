import pymongo
import pandas as pd
import numpy as np
import stock
import predictor
from datetime import datetime, timedelta

# STOCKS = stock.JII30
# STOCKS = ['MSFT']
STOCKS = ['AKRA', 'EXCL', 'INTP', 'ITMG', 'JSMR', 'SMGR', 'TLKM', 'UNVR']

MONGO_CLIENT = pymongo.MongoClient('mongodb://localhost:27017/')
DB = MONGO_CLIENT['stock']
SIM_COLL = DB['simulation']
SIM_DETAILS_COLL = DB['simulation_details']
TRX = {}
SELL_SIGNALS = {}
BUY_SIGNALS = {}
buy_fee = 0.0015
sell_fee = 0.0025


def generate_sell_signal(stock, df):
    signals = predictor.sell_signal(df, last_buy_trx(stock))
    SELL_SIGNALS[stock] = signals


def generate_buy_signal(stock, df):
    buy_price = predictor.buy_signal(df)
    if buy_price != None:
        BUY_SIGNALS[stock] = buy_price


def last_buy_trx(stock):
    if stock not in TRX or not len(TRX[stock]) or TRX[stock][-1]['action'] != 'buy':
        raise('belom beli')
    return TRX[stock][-1]


def save_data(date_start='1980-01-01'):
    trx_summary = summarize_trx()
    summary = summarize(trx_summary, date_start)
    if (date_start != '1980-01-01'):
        id = '%s: %s' % (predictor.rules_no(), date_start)
    else:
        id = predictor.rules_no()

    try:
        DB['simulation'].delete_one({'_id': id})
        DB['simulation_details'].delete_one({'_id': id})
    except:
        pass

    SIM_COLL.insert_one({
        '_id': id,
        'rules': predictor.rules(),
        **summary
    })
    SIM_DETAILS_COLL.insert_one({
        '_id': id,
        'stocks': STOCKS,
        'transactions': TRX,
        'trx_summary': trx_summary,
    })


def summarize_trx():
    trades = []
    for stock in TRX:
        for buy, sell in buy_sell_trx_pairs(TRX[stock]):
            trades.append({
                'stock': stock,
                'buy_date': buy['date'],
                'buy_price': float(buy['price']),
                'sell_date': sell['date'],
                'sell_price': float(sell['price']),
                'hold_period': (sell['date']-buy['date']).days,
                'margin': float(sell['price']-buy['price']),
                'margin_percentage': float(((1-sell_fee)*sell['price']-(1+buy_fee)*buy['price'])/buy['price']*100),
                'sell_condition': sell['status']
            })
    return trades


def summarize(trades, date_start):
    margin_avg = np.mean([t['margin_percentage'] for t in trades])
    margin_med = np.median([t['margin_percentage'] for t in trades])
    margin_std = np.std([t['margin_percentage'] for t in trades])
    total_margin = np.sum([t['margin_percentage'] for t in trades])
    per_month_avg = total_margin / \
        ((datetime.today()-datetime.strptime(date_start, '%Y-%m-%d')) / timedelta(days=30))
    hold_avg = np.mean([t['hold_period'] for t in trades])
    hold_med = np.median([t['hold_period'] for t in trades])
    hold_std = np.std([t['hold_period'] for t in trades])

    return {
        'trade_count': len(trades),
        'margin_avg': '%.2f%%' % margin_avg,
        'margin_med': '%.2f%%' % margin_med,
        'margin_std': '%.2f%%' % margin_std,
        'total_margin': '%.2f%%' % total_margin,
        'per_month_avg': '%.2f%%' % per_month_avg,
        'hold_avg': '%d days' % hold_avg,
        'hold_med': '%d days' % hold_med,
        'hold_std': '%.2f days' % hold_std,
        'fee': 'buy: %.2f%%, sell %.2f%%' % (buy_fee*100, sell_fee*100)
    }


def simulate(stock, date_start='1980-01-01'):
    coll = get_collection(stock, 'D')
    df = pd.DataFrame(list(coll.find({'date': {'$gte': datetime.fromtimestamp(
        datetime.strptime(date_start, '%Y-%m-%d').timestamp())}}).sort('date')))
    predictor.precalculate(df)
    for idx in df.index[:-100]:
        sliced = pd.DataFrame(df.iloc[idx:idx+100])
        if is_holding(stock):
            sold = try_sell(stock, sliced)
            if sold:
                generate_buy_signal(stock, sliced)
            else:
                generate_sell_signal(stock, sliced)
        else:
            bought = try_buy(stock, sliced)
            if bought:
                generate_sell_signal(stock, sliced)
            else:
                generate_buy_signal(stock, sliced)


def has_sell_signal(stock):
    return stock in SELL_SIGNALS and SELL_SIGNALS[stock]


def has_buy_signal(stock):
    return stock in BUY_SIGNALS and BUY_SIGNALS[stock]


def sell_price_hit(price, signal_price, signal_status):
    if signal_status == 'CL' and price['low'] <= signal_price:
        return min(price['open'], signal_price)
    elif signal_status == 'TP' and price['high'] >= signal_price:
        return max(price['open'], signal_price)
    else:
        return False


def buy_price_hit(stock, df):
    price = df.iloc[-1]
    return price['high'] >= BUY_SIGNALS[stock]


def try_sell(stock, df):
    if not has_sell_signal(stock):
        return False

    for signal in SELL_SIGNALS[stock]:
        signal_price, signal_status = signal
        price = df.iloc[-1]
        if not isinstance(signal[0], (int, float)):
            trx = {
                'action': 'sell',
                'date': price['date'],
                'price': float(price[SELL_SIGNALS[stock]]),
                'status': signal_status,
                'idx': df.index[-1]
            }
            TRX[stock].append(trx)
            SELL_SIGNALS.pop(stock)
            return True
        else:
            hit_price = sell_price_hit(price, signal_price, signal_status)
            if hit_price:
                trx = {
                    'action': 'sell',
                    'date': price['date'],
                    'price': float(hit_price),
                    'status': signal_status,
                    'idx': df.index[-1]
                }
                TRX[stock].append(trx)
                SELL_SIGNALS.pop(stock)
                return True
    return False


def try_buy(stock, df):
    if not has_buy_signal(stock):
        return False

    if stock not in TRX:
        TRX[stock] = []

    if not isinstance(BUY_SIGNALS[stock], (int, float)):
        price = df.iloc[-1]
        trx = {
            'action': 'buy',
            'date': price['date'],
            'price': float(price[BUY_SIGNALS[stock]]),
            'idx': df.index[-1]
        }
        TRX[stock].append(trx)
        BUY_SIGNALS.pop(stock)
        return True
    elif buy_price_hit(stock, df):
        price = df.iloc[-1]
        buy_price = max(price['open'], BUY_SIGNALS[stock])
        trx = {
            'action': 'buy',
            'date': price['date'],
            'price': int(buy_price),
            'idx': df.index[-1]
        }
        TRX[stock].append(trx)
        return True
    else:
        return False


def is_holding(stock):
    return stock in TRX and TRX[stock][-1]['action'] == 'buy'


def get_collection(stock, period):
    return DB[stock + '.' + period]


def buy_sell_trx_pairs(trx):
    it = iter(trx)
    return zip(it, it)


start = datetime.today()
date_start = '2002-01-01'
for stock in STOCKS:
    simulate(stock, date_start)
    print('%s: %s (%d/%d)' %
          (predictor.rules_no(), stock, STOCKS.index(stock)+1, len(STOCKS)))
save_data(date_start)
end = datetime.today()
print('%.2fs' % timedelta.total_seconds(end-start))
