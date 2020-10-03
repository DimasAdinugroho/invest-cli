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

def get_trx_summary(rules_no):
    return pd.DataFrame(DB['simulation_details'].find_one({'_id':rules_no})['trx_summary'])

def get_stock_chunk(stock, date_start, date_end, offset=0):
    return pd.DataFrame(list(DB['%s.D' % stock].find({'date':{'$gte':datetime.fromtimestamp((date_start - timedelta(days=offset)).timestamp()), '$lte':datetime.fromtimestamp((date_end + timedelta(days=offset)).timestamp())}})))

def get_trade_chunk(trx, idx, offset=3):
    return pd.DataFrame(list(DB['%s.D' % trx.loc[idx]['stock']].find({'date':{'$gte':datetime.fromtimestamp((trx.loc[idx]['buy_date'] - timedelta(days=offset)).timestamp()), '$lte':datetime.fromtimestamp((trx.loc[idx]['sell_date'] + timedelta(days=offset)).timestamp())}}).sort('date')))

def plot(df, overlays, *chart_list):
    plot_candlestick(df, overlays)
    for charts in chart_list:
        for chart in charts:
            plt.plot(df['date'], df[chart])
        plt.show()





def plot_candlestick(df, overlays):
    fig, ax = plt.subplots()
    candlestick2_ohlc(ax,df['open'],df['high'],df['low'],df['close'],width=0.6)
    for overlay in overlays:
        ax.plot(df[overlay])

    xdate = [datetime.fromtimestamp(i.timestamp()) for i in df['date']]

    ax.xaxis.set_major_locator(ticker.MaxNLocator(6))

    def mydate(x,pos):
        try:
            return xdate[int(x)]
        except IndexError:
            return ''

    ax.xaxis.set_major_formatter(ticker.FuncFormatter(mydate))

    fig.autofmt_xdate()
    fig.tight_layout()

    plt.show()