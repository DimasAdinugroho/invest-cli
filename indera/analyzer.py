import pymongo
import pandas as pd
import numpy as np
import stock
import db_sync
from datetime import datetime, timedelta

stock_name = 'LQ45 + JII70'
STOCKS = stock.JII30

MONGO_CLIENT = pymongo.MongoClient('mongodb://localhost:27017/')
DB = MONGO_CLIENT['stock']


def index_by_time(df):
    new_df = df.set_index(['date']).sort_index()
    return new_df

def get_fixed_high_odds():
        tick = 2
        for stock_code in STOCKS:
                data = db_sync.fetch_data(stock_code, datetime.now() - timedelta(weeks=4))
                data.sort(key=lambda x: x['date'])
                ranges = [(d['high'] - d['open'])/stock.tick(d['close']) for d in data if (d['high'] - d['open'])/stock.tick(d['close']) >= tick]
                print('%s\t%d%%' % (stock_code, len(ranges)/len(data)*100))


########### calculates volatility
# def browse_volatile():
#     for stock_code in STOCKS:
#         data = db_sync.fetch_data(stock_code, datetime.now() - timedelta(weeks=4))
#         data.sort(key=lambda x: x['date'])
#         ranges = [(d['high'] - max(d['open'], d['close']))/max(d['open'], d['close'])*100 for d in data]
#         avg = np.mean(ranges)
#         med = np.median(ranges)
#         std = np.std(ranges)
        # print('%s\t%.2f\t%.2f\t%.2f' % (stock_code, avg, med, std))


############## get summary in mutual funds style
# def analyze(all_df):
#     summary = []
#     for df in all_df:
#         print(df['stock'].iloc[0])
#         st = {
#             'stock': df['stock'].iloc[0],
#             '1 Hr (%)': (df['close'].iloc[-1] - df['close'].iloc[-2]) / df['close'].iloc[-2] * 100,
#             '1 Bln (%)': (df['close'].iloc[-1] - df['close'][datetime(2019,1,4,7,0,0)]) / df['close'][datetime(2019,1,4,7,0,0)] * 100,
#             '1 Th (%)': (df['close'].iloc[-1] - df['close'][datetime(2018,2,6,7,0,0)]) / df['close'][datetime(2018,2,6,7,0,0)] * 100,
#             '3 Th (%)': (df['close'].iloc[-1] - df['close'][datetime(2016,2,4,7,0,0)])/ df['close'][datetime(2016,2,4,7,0,0)] * 100 if df['stock'].iloc[0] != 'WSBP' else np.nan,
#         }
#         summary.append(st)
#     summary_df = pd.DataFrame(summary).sort_values('3 Th (%)', ascending=False)
#     print(summary_df)
    

############## sort stock trading day by change on that day
# def analyze(combines_df):
#     trades = []
#     for idx, row in combined_df.iterrows():
#         if idx < datetime(2017,1,1):
#             continue
#         trade = {
#             'margin': (row['close']-row['open'])/row['open']*100,
#             'date': idx,
#             'stock': row['stock']
#         }
#         if trade['margin'] < 10:
#             continue
#         trades.append(trade)
#     trades.sort(key=lambda t: t['margin'], reverse=True)
#     for trade in trades:
#         print('%s %.2f%% %s' % (trade['stock'], trade['margin'], trade['date']))


# ############# backtest: one day trading for stock that spikes just after opening
# def analyze(combined_df):
#     date = ''
#     what_when = []
#     highs = {9.5: [], 10: [], 10.5: [], 11: [], 11.5: [], 13.5: [],
#              14: [], 14.5: [], 15: [], 15.5: [], 16: []}
#     lows = {9.5: [], 10: [], 10.5: [], 11: [], 11.5: [], 13.5: [],
#             14: [], 14.5: [], 15: [], 15.5: [], 16: []}
#     swings = []
#     count = 0
#     for idx, row in combined_df.iterrows():
#         if date != idx.date():
#             date = idx.date()
#             start = 9999999
#             lowest = 9999999
#             highest = 0
#             focus = False
#         hour = idx.hour + idx.minute/60
#         if hour == 8.5 or hour == 9:
#             start = min(start, row['open'])
#         if hour == 9.5 and row['open'] >= 1.01*start:
#             buy = row['open']
#             focus = True
#             what_when.append((row['stock'], date))
#             count += 1
#         if focus and hour >= 9.5 and hour not in [12, 12.5, 13, 16.5]:
#             highs[hour].append((row['high']/buy - 1)*100)
#             lows[hour].append((row['low']/buy - 1)*100)
#             highest = max(highest, row['high'])
#             lowest = min(lowest, row['low'])
#             if hour == 16:
#                 swing = (highest - lowest) / start * 100
#                 swings.append(swing)
#     print(stock_name)
#     print('count: %d' % count)
#     print('\n')
#     for d_hour in range(19, 33):
#         hour = d_hour/2
#         if hour in [12, 12.5, 13, 16.5]:
#             continue
#         print(hour)
#         print('HIGH avg: %.2f%%' % pd.Series(highs[hour]).mean())
#         print('HIGH median: %.2f%%' % pd.Series(highs[hour]).median())
#         print('HIGH stdev: %.2f%%' % pd.Series(highs[hour]).std())
#         print('HIGH highest: %.2f%%' % pd.Series(highs[hour]).max())
#         print('HIGH lowest: %.2f%%' % pd.Series(highs[hour]).min())
#         print('LOW avg: %.2f%%' % pd.Series(lows[hour]).mean())
#         print('LOW median: %.2f%%' % pd.Series(lows[hour]).median())
#         print('LOW stdev: %.2f%%' % pd.Series(lows[hour]).std())
#         print('LOW highest: %.2f%%' % pd.Series(lows[hour]).max())
#         print('LOW lowest: %.2f%%' % pd.Series(lows[hour]).min())
#         print('MID avg: %.2f%%' %
#               (pd.Series(highs[hour])/2 + pd.Series(lows[hour])/2).mean())
#         print('MID median: %.2f%%' %
#               (pd.Series(highs[hour])/2 + pd.Series(lows[hour])/2).median())
#         print('MID stdev: %.2f%%' %
#               (pd.Series(highs[hour])/2 + pd.Series(lows[hour])/2).std())
#         print('MID highest: %.2f%%' %
#               (pd.Series(highs[hour])/2 + pd.Series(lows[hour])/2).max())
#         print('MID lowest: %.2f%%' %
#               (pd.Series(highs[hour])/2 + pd.Series(lows[hour])/2).min())
#         print('\n')
#     print('SWING avg: %.2f%%' % (pd.Series(swings).mean()))
#     print('SWING median: %.2f%%' % (pd.Series(swings).median()))
#     print('SWING stdev: %.2f%%' % (pd.Series(swings).std()))
#     print('SWING highest: %.2f%%' % (pd.Series(swings).max()))
#     print('SWING lowest: %.2f%%' % (pd.Series(swings).min()))
#     # print(what_when)

# browse_volatile()

# combined_df = pd.DataFrame()
# # all_df = []
# for stock in STOCKS:
#     coll = DB[stock + '.D']
#     df = pd.DataFrame(list(coll.find()))
#     df['stock'] = stock
#     df = index_by_time(df)
#     combined_df = combined_df.append(df)
#     # all_df.append(df)
# analyze(combined_df)
# # analyze(all_df)

get_fixed_high_odds()