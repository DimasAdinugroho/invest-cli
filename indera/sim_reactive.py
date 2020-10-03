import pymongo
import pandas as pd
import numpy as np
import stock
import predictor
from datetime import datetime

# STOCKS = stock.LQ45_JII70
STOCKS = ['AKRA']

MONGO_CLIENT = pymongo.MongoClient('mongodb://localhost:27017/')
DB = MONGO_CLIENT['stock']
SIM_COLL = DB['simulation']
SIM_DETAILS_COLL = DB['simulation_details']
TRX = {}
SELL_PRICES = {}
BUY_PRICES = {}


def update_sell_price(stock, df):
    SELL_PRICES[stock] = predictor.predict_sell(df)

def update_buy_price(stock, df):
    BUY_PRICES[stock] = predictor.predict_buy(df)

def save_data(date_start='1990-01-01'):
    trx_summary = summarize_trx()
    summary = summarize(trx_summary)
    if (date_start != '1990-01-01'):
        id = '%s: %s' % (RULES_NO, date_start)
    else:
        id = RULES_NO

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
                'buy_price': int(buy['price']),
                'sell_date': sell['date'],
                'sell_price': int(sell['price']),
                'hold_period': (sell['date']-buy['date']).days,
                'margin': int(sell['price']-buy['price']),
                'margin_percentage': float((sell['price']-buy['price'])/buy['price']*100)
            })
    return trades


def summarize(trades):
    margin_avg = np.mean([t['margin_percentage'] for t in trades])
    margin_med = np.median([t['margin_percentage'] for t in trades])
    margin_std = np.std([t['margin_percentage'] for t in trades])
    hold_avg = np.mean([t['hold_period'] for t in trades])
    hold_med = np.median([t['hold_period'] for t in trades])
    hold_std = np.std([t['hold_period'] for t in trades])
    size = 10000000

    def calculate_margin(trade):
        qty = round(size/trade['buy_price'], -2)
        buy_fee = 0.0019
        sell_fee = 0.0019
        margin = qty * \
            ((1-sell_fee)*trade['sell_price'] - (1+buy_fee)*trade['buy_price'])
        return margin

    return {
        'trade_count': len(trades),
        'gross_profit': np.sum([calculate_margin(t) for t in trades if t['sell_price'] > t['buy_price']]),
        'gross_loss': np.sum([calculate_margin(t) for t in trades if t['sell_price'] <= t['buy_price']]),
        'net_profit': np.sum([calculate_margin(t) for t in trades]),
        'margin_avg': '%.2f%%' % margin_avg,
        'margin_med': '%.2f%%' % margin_med,
        'margin_std': '%.2f%%' % margin_std,
        'hold_avg': '%d days' % hold_avg,
        'hold_med': '%d days' % hold_med,
        'hold_std': '%.2f days' % hold_std,
        'assumptions': '%d per position' % size
    }


def simulate(stock, date_start='1990-01-01'):
    coll = get_collection(stock, 'D')
    df = pd.DataFrame(list(coll.find({'date': {'$gte': datetime.fromtimestamp(
        datetime.strptime(date_start, '%Y-%m-%d').timestamp())}}).sort('date')))
    for idx in df.index[:-100]:
        sliced = pd.DataFrame(df.iloc[idx:idx+100])
        if is_holding(stock):
            if sell_price_hit(stock, sliced):
                sell(stock, sliced)
                update_buy_price(stock, sliced)
            else:
                update_sell_price(stock, sliced)
        else:
            if buy_price_hit(stock, sliced):
                buy(stock, sliced)
                update_sell_price(stock, sliced)
            else:
                update_buy_price(stock, sliced)


def sell_price_hit(stock, df):
    if stock not in SELL_PRICES or SELL_PRICES[stock] == None:
        return False

    price = df.iloc[-1]
    return price['low'] <= SELL_PRICES[stock]

def buy_price_hit(stock, df):
    if stock not in BUY_PRICES or BUY_PRICES[stock] == None:
        return False

    price = df.iloc[-1]
    return price['high'] >= BUY_PRICES[stock]


def sell(stock, df):
    price = df.iloc[-1]
    sell_price = min(price['open'], SELL_PRICES.pop(stock))
    trx = {
        'action': 'sell',
        'date': price['date'],
        'price': int(sell_price)
    }
    TRX[stock].append(trx)


def buy(stock, df):
    if stock not in TRX:
        TRX[stock] = []
        
    price = df.iloc[-1]
    buy_price = max(price['open'], BUY_PRICES.pop(stock))
    trx = {
        'action': 'buy',
        'date': price['date'],
        'price': int(buy_price)
    }
    TRX[stock].append(trx)


def is_holding(stock):
    return stock in TRX and TRX[stock][-1]['action'] == 'buy'


def get_collection(stock, period):
    return DB[stock + '.' + period]


def buy_sell_trx_pairs(trx):
    it = iter(trx)
    return zip(it, it)


RULES_NO = predictor.rules_no()
date_start = '2010-01-01'
TRX = {}
SELL_PRICES = {}
BUY_SIGNALS = set()
for stock in STOCKS:
    simulate(stock, date_start)
    print('%s: %s (%d/%d)' %
            (RULES_NO, stock, STOCKS.index(stock)+1, len(STOCKS)))
save_data(date_start)
