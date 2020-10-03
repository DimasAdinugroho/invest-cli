import pymongo
import pandas as pd
import numpy as np
from datetime import datetime
from simulator_rules import rules

STOCKS = ['WSKT', 'PTPP','WIKA']

MONGO_CLIENT = pymongo.MongoClient('mongodb://localhost:27017/')
DB = MONGO_CLIENT['stock']
SIM_COLL = DB['simulation']
SIM_DETAILS_COLL = DB['simulation_details']
TRX = {}
SELL_PRICES = {}
BUY_SIGNALS = set()
RULES_NO = 'zzz'


def update_sell_price(stock, df, idx):
    SELL_PRICES[stock] = 10**6


def buy_condition_met(df, idx):
    return rules[RULES_NO]['buy_condition'](df, idx)


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
        'rules': 'zzz',
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
                'buy_price': buy['price'],
                'sell_date': sell['date'],
                'sell_price': sell['price'],
                'hold_period': (sell['date']-buy['date']).days,
                'hold_bars': (sell['idx']-buy['idx']),
                'margin': sell['price']-buy['price'],
                'margin_percentage': (sell['price']-buy['price'])/buy['price']*100
            })
    return trades


def summarize(trades):
    margin_avg = np.mean([t['margin_percentage'] for t in trades])
    margin_med = np.median([t['margin_percentage'] for t in trades])
    margin_std = np.std([t['margin_percentage'] for t in trades])
    hold_avg = np.mean([t['hold_period'] for t in trades])
    hold_med = np.median([t['hold_period'] for t in trades])
    hold_std = np.std([t['hold_period'] for t in trades])
    return {
        'trade_count': len(trades),
        'margin_avg': '%.2f%%' % margin_avg,
        'margin_med': '%.2f%%' % margin_med,
        'margin_std': '%.2f%%' % margin_std,
        'hold_avg': '%d days' % hold_avg,
        'hold_med': '%d days' % hold_med,
        'hold_std': '%.2f days' % hold_std
    }


def simulate(stock, date_start='1990-01-01'):
    coll = get_collection(stock, 'daily')
    df = pd.DataFrame(list(coll.find({'date':{'$gte':datetime.fromtimestamp(datetime.strptime(date_start, '%Y-%m-%d').timestamp())}}).sort('date')))
    for idx in df.index:
        date = df.loc[idx]['date']
        if is_holding(stock):
            if date.month == 1 and date.day >= 26 and date.day <= 31:
                sell(stock, df, idx)
            else:
                update_sell_price(stock, df, idx)
        else:
            if date.month == 11 and date.day >= 26 and date.day <= 31:
                buy(stock, df, idx)
                update_sell_price(stock, df, idx)
            else:
                pass


def has_buy_signal(stock):
    return stock in BUY_SIGNALS


def set_buy_signal(stock):
    BUY_SIGNALS.add(stock)


def sell_price_hit(stock, df, idx):
    if SELL_PRICES[stock] == -1:
        return False

    price = df.loc[idx]
    return price['low'] <= SELL_PRICES[stock]


def sell(stock, df, idx):
    price = df.loc[idx]
    sell_price = min(price['open'], SELL_PRICES.pop(stock))
    trx = {
        'action': 'sell',
        'date': price['date'],
        'price': sell_price,
        'idx': idx
    }
    TRX[stock].append(trx)


def buy(stock, df, idx):
    if stock not in TRX:
        TRX[stock] = []

    price = df.loc[idx]
    trx = {
        'action': 'buy',
        'date': price['date'],
        'price': price['open'],
        'idx': idx
    }
    TRX[stock].append(trx)


def is_holding(stock):
    return stock in TRX and TRX[stock][-1]['action'] == 'buy'


def get_collection(stock, period):
    return DB[stock + '.' + period]


def buy_sell_trx_pairs(trx):
    it = iter(trx)
    return zip(it, it)


date_start = '2009-11-01'
TRX = {}
SELL_PRICES = {}
BUY_SIGNALS = set()
for stock in STOCKS:
    simulate(stock, date_start)
    print('%s: %s (%d/%d)' % (RULES_NO, stock, STOCKS.index(stock)+1, len(STOCKS)))
save_data(date_start)
