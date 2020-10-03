from mpl_finance import candlestick2_ohlc
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
from matplotlib.collections import LineCollection
import pymongo
from datetime import datetime, timedelta
import pandas as pd
import numpy as np

MONGO_CLIENT = pymongo.MongoClient('mongodb://localhost:27017/')
DB = MONGO_CLIENT['stock']

def by_stock(trx_list, start_date = '1990-01-01'):
    groups = {}
    for idx, trx in trx_list.iterrows():
        stock = trx['stock']
        if stock not in groups:
            groups[stock] = []
        if (trx['buy_date'] >= datetime.strptime(start_date, '%Y-%m-%d')):
            groups[stock].append(trx)
    df_groups = {group:pd.DataFrame(groups[group]) for group in groups}
    return df_groups

def summary(groups):
    summaries = []
    for group_key in groups:
        summary = summarize(groups[group_key])
        summary['key'] = group_key
        summaries.append(summary)
    df_summaries = pd.DataFrame(summaries)
    return df_summaries

def summarize(trades):
    margin_avg = trades['margin_percentage'].mean()
    margin_med = trades['margin_percentage'].median()
    margin_std = trades['margin_percentage'].std()
    hold_avg = trades['hold_period'].mean()
    hold_med = trades['hold_period'].median()
    hold_std = trades['hold_period'].std()
    profit_avg = trades['margin_percentage'].where(trades['margin_percentage'] > 0).mean()
    profit_med = trades['margin_percentage'].where(trades['margin_percentage'] > 0).median()
    profit_std = trades['margin_percentage'].where(trades['margin_percentage'] > 0).std()
    loss_avg = trades['margin_percentage'].where(trades['margin_percentage'] <= 0).mean()
    loss_med = trades['margin_percentage'].where(trades['margin_percentage'] <= 0).median()
    loss_std = trades['margin_percentage'].where(trades['margin_percentage'] <= 0).std()
    return {
        'trade_count': len(trades),
        'margin_avg': '%.2f%%' % margin_avg,
        'margin_med': '%.2f%%' % margin_med,
        'margin_std': '%.2f%%' % margin_std,
        'hold_avg': '%d days' % hold_avg,
        'hold_med': '%d days' % hold_med,
        'hold_std': '%.2f days' % hold_std,
        'profit_avg': '%.2f%%' % profit_avg,
        'profit_med': '%.2f%%' % profit_med,
        'profit_std': '%.2f%%' % profit_std,
        'loss_avg': '%.2f%%' % loss_avg,
        'loss_med': '%.2f%%' % loss_med,
        'loss_std': '%.2f%%' % loss_std
    }