
import requests
import stock
import pymongo
import pandas as pd
import numpy as np
import json
import db_sync
from datetime import datetime

MONGO_CLIENT = pymongo.MongoClient('mongodb://localhost:27017/')
DB = MONGO_CLIENT['stock']

macd_arg = (12, 26, 9)
sma_rsi_arg = (5, 10)
sma_rsi2_arg = (10, 10)
sar_arg = (0.02, 0.05, 0.3)
sto_arg = (14, 3, 3)
bb_arg = (15, 2)
CL = 0
USER_AGENT = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.102 Safari/537.36'
COOKIES = 'B=9afsuf1dru52r&b=4&d=DC814yhpYF5uEHdqdeHDce7yawQ-&s=bv&i=3LGUhtWvNIVKxl8N32sp; T=z=Lqj4bBL.K9bBv/lTv.ZAzmlMjc3TwY2MDUzNTIxMzc2&a=QAE&sk=DAAedUzqKfxZcS&ks=EAAMItOffvWFyO0n9ODyMecqg--~G&kt=EAA7BwBf1a4ZfWoMI7OQsFvmA--~I&ku=FAASpnX7YK5UthBsJCqLZjI_L.MOFfLSfC6u.T3e6p0C2ZuaweEYqGpfcwGYhvtWBXK6h49KKjZK3VdQaRUnhCKD5eiMEubPEqZQQdZJd1aXPB8Ng5VhWMv8c6gNmkTEaS74YoORGkyENMVkqjHpPJ2vXNNRcN5k9cxksYh7VaUfUg-~A&d=bnMBeWFob28BZwFZT1lPV05aRkFWQ0RRQ1E2NDZNQzZSQldZQQFzbAFOVEF3T0FFeE56STBNalUyTkRBeAFhAVFBRQFhYwFBSklvLkJIbgFjcwEBc2MBZGVza3RvcF93ZWIBZnMBdGE2eV9NQmI0anFMAXp6AUxxajRiQkE3RQ--&af=JnRzPTE1NDE1NTI3NzkmcHM9b3N1a0hsMGN4VWZscm16SUQzSzltZy0t; F=d=BivGc_89vHnWLuragbOdNQuS6kNqtOBd8McpqTPQYQ--; PH=fn=HMt6UzD8UEWyTI2BAKEThT6cpg--&l=id-ID&i=id; Y=v=1&n=4338sej3nta47&l=l0i78ael827/o&p=m2svvid00000000&r=hk&lg=id-ID&intl=id; AO=u=1; GUC=AQEAAQJb44NcukIg3QSk&s=AQAAAGtA_BEV&g=W-I6tA; PRF=t%3DANTM.JK%252BAKRA.JK%252BADRO.JK%252BADHI.JK%252BAALI.JK%252BIDX%252B%255EJKSE'
df = ''


def rules_no():
    return "Select:Simple TP/CL - 9~0.1~0.5"


def rules():
    # return 'BUY on 3 of MACD, SAR, Aroon are crossedover. SELL on 1 of them is crossedunder'
    # return 'BUY on SAR crossedover. SELL on stochastic crossedunder'
    # return 'BUY on SAR(0.02,0.05,0.3) CO and MACD(6,12,4) CO or sto(14,3,3) < 30. SELL on SAR reverse'
    return 'Simple TP/CL - 9~0.1~0.5'


def predict_buy(data):
    global df
    df = data
    # lb_range = 2
    # if (
    # past_lt(close, set(), past_sar, sar_arg, lb_range) and
    # past_lt(past_macd, macd_arg, past_macd_signal, macd_arg, lb_range) and
    # past_gt(past_macd, macd_arg, 0, None)
    # past_lt(stochastic_d, sto_arg, 30, None, lb_range) and
    # past_ema(10) > past_ema(20)
    # ):
    # prices = [
    # gt(next, set(), sar, sar_arg),
    # gt(macd, macd_arg, macd_signal, macd_arg),
    # gt(aroon_up, (14,), aroon_down, (14,))
    #     close()
    # ]
    # return max(prices)
    # if past_gradient(past_bb_mid, bb_arg, 3) > 2:
    #     return close()

    # if past_gradient(past_bb_mid, bb_arg, 3) > -2 and past_bb_bw(*bb_arg) > 0.05 and past_bb_percent(*bb_arg) < 0.25:
    #     return close()

    prices = [
        gt(sma_rsi, (10, 10), 60, set()),
        gt(sma_rsi, (5, 10), sma_rsi, (10, 10))
    ]
    return max(prices)

    # lb_range=1
    # if (past_gt(past_sma_rsi, (10,10), 60, set(), lb_range) and past_gt(past_sma_rsi, (5,10), past_sma_rsi, (10,10), lb_range)):
    #     return 0


def predict_sell(data):
    global df
    df = data
    # prices = [
    # lt(next, set(), sar, sar_arg),
    # lt(macd, macd_arg, macd_signal, macd_arg),
    # lt(aroon_up, (14,), aroon_down, (14,))
    # ]
    # return min(prices)
    # if past_gradient(past_bb_mid, bb_arg, 3) > 2:
    #     return close()

    # if past_gradient(past_bb_mid, bb_arg, 3) > -2 and past_bb_bw(*bb_arg) > 0.05 and past_bb_percent(*bb_arg) > 0.75:
    #     return close()

    if not (
        past_gt(past_sma_rsi, sma_rsi_arg, past_sma_rsi, sma_rsi2_arg) and
        past_gt(past_sma, (5,), past_sma, (10,)) and
        past_gt(past_sma_rsi, sma_rsi2_arg, 30, set())
    ):
        prices = [
            lt(sma_rsi, sma_rsi2_arg, 40, set()),
            lt(sma_rsi, sma_rsi_arg, 30, set())
        ]
        return min(prices)
    return None


def predict():
    db_sync.sync_many(codes)

    print('Analyzing...')
    overall_period = 100
    stock_dfs = get_stock_dfs(codes, overall_period)
    for code in stock_dfs:
        global df
        df = stock_dfs[code]

        lb_range = 2
        if (
            # past_lt(close, set(), past_sar, sar_arg, lb_range) and
            past_lt(past_macd, macd_arg, past_macd_signal, macd_arg, lb_range) and
            past_gt(past_macd, macd_arg, 0, None)
            # past_lt(stochastic_d, sto_arg, 30, None, lb_range) and
            # past_ema(10) > past_ema(20)
        ):
            prices = [
                gt(next, set(), sar, (0.02, 0.02, 0.2)),
                gt(macd, (12, 26, 9), macd_signal, (12, 26, 9)),
                gt(aroon_up, (14,), aroon_down, (14,))
            ]
            max_price = max(prices)
            if max_price >= 1.01*close() and max_price < 1.05*close():
                print(code)
                print(close())
                print(max_price)


TPaccum = 0.0
CLaccum = 0.0


def sell_signal(data, buy_trx):
    global df
    df = data
    # met = (
    # (
    # not buy_signal(data) and
    # past_lt(past_sma_rsi, sma_rsi2_arg, 40, set()) and
    # past_lt(past_sma_rsi, sma_rsi_arg, 30, set())
    # ) or
    # close() < cl(buy_price)
    # out_up(data) and out_up(data, 1)
    # )

    global TPaccum, CLaccum
    TPaccum += 0.1 if close() > past_ema(12) else 0.5
    CLaccum += 0.5 if close() > past_ema(12) else 0.1

    TP = buy_trx['price'] * (100 + 9 - TPaccum)/100
    CL = buy_trx['price'] * (100 - 9 + CLaccum)/100
    return [(TP, 'TP'), (CL, 'CL')]


def buy_signal(data):
    global df
    df = data
    met = (
        # past_gt(past_sma_rsi, sma_rsi_arg, past_sma_rsi, sma_rsi2_arg) and
        # past_gt(past_sma, (5,), past_sma, (10,)) and
        # past_gt(past_sma_rsi, sma_rsi2_arg, 30, set())
        # in_up(data) and not out_up(data, 1)
        in_(data) and not in_(data, 1)
    )
    if met:
        global TPaccum, CLaccum
        TPaccum, CLaccum = 0.0, 0.0
    return 'open' if met else None


def in_(data, lb=0):
    return (
        past_macd_hist(*macd_arg, lb) > past_macd_hist(*macd_arg, lb+1) and
        past_macd_hist(*macd_arg, lb+1) <= past_macd_hist(*macd_arg, lb+2) and
        close(lb) > open(lb) and
        close(lb+1) > open(lb+1) and
        close() > past_sma(50)
    )


def in_up(data, lb=0):
    return (
        past_macd_hist(*macd_arg, lb) > past_macd_hist(*macd_arg, lb+1) and
        past_sma_rsi(*sma_rsi_arg, lb) > past_sma_rsi(*sma_rsi2_arg, lb)
    )


def out_up(data, lb=0):
    return (
        past_macd_hist(*macd_arg, lb) < past_macd_hist(*macd_arg, lb+1) and
        past_sma_rsi(*sma_rsi2_arg, lb) < 40 and
        past_sma_rsi(*sma_rsi_arg, lb) < 30
    )


def screen(codes):
    db_sync.sync_many(codes)

    print('Analyzing...')
    overall_period = 30
    stock_dfs = get_stock_dfs(codes, overall_period)
    for code in stock_dfs:
        global df
        df = stock_dfs[code]
        if past_crossover(past_aroon_up, (25,), past_aroon_down, (25,), 5):
            print(code)


def precalculate(data):
    global df
    df = data
    # calculate_macd(*macd_arg)
    # calculate_sma_rsi(*sma_rsi_arg)
    # calculate_sma_rsi(*sma_rsi2_arg)
    # calculate_ema(12)
    # calculate_sma(50)


def cl(buy_price):
    rough = (1-CL)*buy_price
    rounded = round(rough/stock.tick(buy_price))*stock.tick(buy_price)
    return rounded


def get_stock_dfs(codes, overall_period):
    dfs = {}
    for code in codes:
        data = list(DB[code+'.D'].find().sort('date',
                                              direction=pymongo.DESCENDING).limit(overall_period))[::-1]
        df = pd.DataFrame(data)
        dfs[code] = df
    return dfs


def past_lt(f1, f1_arg, f2, f2_arg, lb_range=0):
    is_exist = False
    for lb in range(0, lb_range+1):
        if type(f2) is not int and type(f2) is not float:
            if f1(*f1_arg, lb) < f2(*f2_arg, lb):
                is_exist = True
        else:
            if f1(*f1_arg, lb) < f2:
                is_exist = True
    return is_exist


def past_gt(f1, f1_arg, f2, f2_arg, lb_range=0):
    is_exist = False
    for lb in range(0, lb_range+1):
        if type(f2) is not int and type(f2) is not float:
            if f1(*f1_arg, lb) > f2(*f2_arg, lb):
                is_exist = True
        else:
            if f1(*f1_arg, lb) > f2:
                is_exist = True
    return is_exist


def gt(f1, f1_arg, f2, f2_arg):
    next_price = low()
    if type(f2) is not int and type(f2) is not float:
        while f1(*f1_arg, next_price) <= f2(*f2_arg, next_price):
            next_price += stock.tick(next_price)
            if next_price >= stock.ara(close()):
                break
        else:
            return next_price
    else:
        while f1(*f1_arg, next_price) <= f2:
            next_price += stock.tick(next_price)
            if next_price >= stock.ara(close()):
                break
        else:
            return next_price
    return 999999999999


def lt(f1, f1_arg, f2, f2_arg):
    next_price = high()
    if type(f2) is not int and type(f2) is not float:
        while f1(*f1_arg, next_price) >= f2(*f2_arg, next_price):
            next_price -= stock.tick(next_price)
            if next_price <= stock.arb(close()):
                break
        else:
            return next_price
    else:
        while f1(*f1_arg, next_price) >= f2:
            next_price -= stock.tick(next_price)
            if next_price <= stock.arb(close()):
                break
        else:
            return next_price
    return -1


def past_crossover(f1, f1_arg, f2, f2_arg, lb_range=0):
    is_exist = False
    for lb in range(0, lb_range+1):
        if type(f2) is not int and type(f2) is not float:
            if f1(*f1_arg, lb) > f2(*f2_arg, lb) and f1(*f1_arg, lb+1) <= f2(*f2_arg, lb+1):
                is_exist = True
        else:
            if f1(*f1_arg, lb) > f2 and f1(*f1_arg, lb+1) <= f2:
                is_exist = True
    return is_exist


def past_crossunder(f1, f1_arg, f2, f2_arg, lb_range=0):
    is_exist = False
    for lb in range(0, lb_range+1):
        if type(f2) is not int and type(f2) is not float:
            if f1(*f1_arg, lb) < f2(*f2_arg, lb) and f1(*f1_arg, lb+1) >= f2(*f2_arg, lb+1):
                is_exist = True
        else:
            if f1(*f1_arg, lb) < f2 and f1(*f1_arg, lb+1) >= f2:
                is_exist = True
    return is_exist


def past_gradient(f, f_arg, lb=1):
    diff = f(*f_arg) - f(*f_arg, lb)
    percent_diff = diff/f(*f_arg)*100
    return percent_diff


def open(lb=0):
    return df['open'].iloc[-1-lb]


def high(lb=0):
    return df['high'].iloc[-1-lb]


def low(lb=0):
    return df['low'].iloc[-1-lb]


def close(lb=0):
    return df['close'].iloc[-1-lb]

def volume(lb=0):
    return df['volume'].iloc[-1-lb]

def next(next_price):
    return next_price


def sma(period, next_price):
    if sma_col(period) not in df:
        calculate_sma(period)

    col_name = sma_col(period)
    sma = (df[col_name].iloc[-period+1:].sum() + next_price) / period
    return sma


def past_sma(period, lb=0):
    if sma_col(period) not in df:
        calculate_sma(period)
    return df[sma_col(period)].iloc[-1-lb]


def calculate_sma(period):
    col_name = sma_col(period)
    df[col_name] = df['close'].rolling(period).mean()


def sma_col(period):
    return 'sma(%d)' % period


def ema(period, next_price):
    if ema_col(period) not in df:
        calculate_ema(period)

    col_name = ema_col(period)
    weight = 2/(period+1)
    ema = (next_price-df[col_name].iloc[-1])*weight+df[col_name].iloc[-1]
    return ema


def past_ema(period, lb=0):
    if ema_col(period) not in df:
        calculate_ema(period)
    return df[ema_col(period)].iloc[-1-lb]


def calculate_ema(period):
    col_name = ema_col(period)
    ema = pd.Series(np.nan, index=df.index)
    ema.iloc[period-1] = df['close'].iloc[:period].mean()
    weight = 2/(period+1)
    for i in df.index[period:]:
        ema[i] = (df['close'][i]-ema[i-1])*weight+ema[i-1]
    df[col_name] = ema


def ema_col(period):
    return 'ema(%d)' % period


def rsi(period, next_price):
    if rsi_col(period) not in df:
        calculate_rsi(period)

    gain_col_name = rsi_gain_col(period)
    loss_col_name = rsi_loss_col(period)
    avg_gain = df[gain_col_name]
    avg_loss = df[loss_col_name]
    if next_price > df['close'].iloc[-1]:
        diff = next_price - df['close'].iloc[-1]
        avg_gain = (df[gain_col_name].iloc[-1] *
                    (period-1) + diff) / period
        avg_loss = (df[loss_col_name].iloc[-1] *
                    (period-1)) / period
    elif next_price < df['close'].iloc[-1]:
        diff = df['close'].iloc[-1] - next_price
        avg_gain = (df[gain_col_name].iloc[-1] *
                    (period-1)) / period
        avg_loss = (df[loss_col_name].iloc[-1] *
                    (period-1) + diff) / period
    else:
        avg_gain = (df[gain_col_name].iloc[-1] *
                    (period-1)) / period
        avg_loss = (df[loss_col_name].iloc[-1] *
                    (period-1)) / period
    rs = avg_gain/avg_loss
    rsi = 100 - (100/(1+rs))
    return rsi


def past_rsi(period, lb=0):
    if rsi_col(period) not in df:
        calculate_rsi(period)
    return df[rsi_col(period)].iloc[-1-lb]


def calculate_rsi(period):
    col_name = rsi_col(period)
    gain_col_name = rsi_gain_col(period)
    loss_col_name = rsi_loss_col(period)
    delta = df['close'].diff()
    gain, loss = delta.copy(), delta.copy()
    gain[gain < 0] = 0
    loss[loss > 0] = 0
    avg_gain = pd.Series(np.nan, df.index)
    avg_gain[period-1] = gain[:period].mean()
    avg_loss = pd.Series(np.nan, df.index)
    avg_loss[period-1] = abs(loss[:period].mean())
    for i in df.index[period:]:
        avg_gain[i] = (avg_gain[i-1] *
                       (period-1) + gain[i]) / period
        avg_loss[i] = (avg_loss[i-1]*(period-1) +
                       abs(loss[i])) / period
    rs = avg_gain/avg_loss
    rsi = 100 - (100/(1+rs))
    df[col_name] = rsi
    df[gain_col_name] = avg_gain
    df[loss_col_name] = avg_loss


def rsi_col(period):
    return 'rsi(%d)' % period


def rsi_gain_col(period):
    return 'rsi(%d):gain' % period


def rsi_loss_col(period):
    return 'rsi(%d):loss' % period


def sma_rsi(sma_period, rsi_period, next_price):
    if sma_rsi_col(sma_period, rsi_period) not in df:
        calculate_sma_rsi(sma_period, rsi_period)

    sma_col_name = sma_col(sma_period)
    gain_col_name = sma_rsi_gain_col(sma_period, rsi_period)
    loss_col_name = sma_rsi_loss_col(sma_period, rsi_period)
    avg_gain = df[gain_col_name]
    avg_loss = df[loss_col_name]
    next_sma = sma(sma_period, next_price)
    if next_sma > df[sma_col_name].iloc[-1]:
        diff = next_sma - df[sma_col_name].iloc[-1]
        avg_gain = (df[gain_col_name].iloc[-1] *
                    (rsi_period-1) + diff) / rsi_period
        avg_loss = (df[loss_col_name].iloc[-1] *
                    (rsi_period-1)) / rsi_period
    elif next_sma < df[sma_col_name].iloc[-1]:
        diff = df[sma_col_name].iloc[-1] - next_sma
        avg_gain = (df[gain_col_name].iloc[-1] *
                    (rsi_period-1)) / rsi_period
        avg_loss = (df[loss_col_name].iloc[-1] *
                    (rsi_period-1) + diff) / rsi_period
    else:
        avg_gain = (df[gain_col_name].iloc[-1] *
                    (rsi_period-1)) / rsi_period
        avg_loss = (df[loss_col_name].iloc[-1] *
                    (rsi_period-1)) / rsi_period
    rs = avg_gain/avg_loss
    rsi = 100 - (100/(1+rs))
    return rsi


def past_sma_rsi(sma_period, rsi_period, lb=0):
    if sma_rsi_col(sma_period, rsi_period) not in df:
        calculate_sma_rsi(sma_period, rsi_period)
    return df[sma_rsi_col(sma_period, rsi_period)].iloc[-1-lb]


def calculate_sma_rsi(sma_period, rsi_period):
    if sma_col(sma_period) not in df:
        calculate_sma(sma_period)

    col_name = sma_rsi_col(sma_period, rsi_period)
    sma_col_name = sma_col(sma_period)
    gain_col_name = sma_rsi_gain_col(sma_period, rsi_period)
    loss_col_name = sma_rsi_loss_col(sma_period, rsi_period)
    delta = df[sma_col_name].diff()
    gain, loss = delta.copy(), delta.copy()
    gain[gain < 0] = 0
    loss[loss > 0] = 0
    avg_gain = pd.Series(np.nan, df.index)
    avg_gain.iloc[sma_period+rsi_period -
                  2] = gain.iloc[sma_period-1:sma_period+rsi_period-1].mean()
    avg_loss = pd.Series(np.nan, df.index)
    avg_loss.iloc[sma_period+rsi_period -
                  2] = abs(loss.iloc[sma_period-1:sma_period+rsi_period-1].mean())
    for i in df.index[sma_period+rsi_period-1:]:
        avg_gain[i] = (avg_gain[i-1] *
                       (rsi_period-1) + gain[i]) / rsi_period
        avg_loss[i] = (avg_loss[i-1]*(rsi_period-1) +
                       abs(loss[i])) / rsi_period
    rs = avg_gain/avg_loss
    rsi = 100 - (100/(1+rs))
    df[col_name] = rsi
    df[gain_col_name] = avg_gain
    df[loss_col_name] = avg_loss


def sma_rsi_col(sma_period, rsi_period):
    return 'sma_rsi(%d,%d)' % (sma_period, rsi_period)


def sma_rsi_gain_col(sma_period, rsi_period):
    return 'sma_rsi(%d,%d):gain' % (sma_period, rsi_period)


def sma_rsi_loss_col(sma_period, rsi_period):
    return 'sma_rsi(%d,%d):loss' % (sma_period, rsi_period)


def stochastic_k(period, k_smoothing, d_smoothing, lb=0):
    if stochastic_k_col(period, k_smoothing, d_smoothing) not in df:
        calculate_stochastic(period, k_smoothing, d_smoothing)
    return df[stochastic_k_col(period, k_smoothing, d_smoothing)].iloc[-1-lb]


def stochastic_d(period, k_smoothing, d_smoothing, lb=0):
    if stochastic_d_col(period, k_smoothing, d_smoothing) not in df:
        calculate_stochastic(period, k_smoothing, d_smoothing)
    return df[stochastic_d_col(period, k_smoothing, d_smoothing)].iloc[-1-lb]


def calculate_stochastic(period, k_smoothing, d_smoothing):
    k_name = stochastic_k_col(period, k_smoothing, d_smoothing)
    d_name = stochastic_d_col(period, k_smoothing, d_smoothing)
    l = df['low'].rolling(period).min()
    h = df['high'].rolling(period).max()
    fast_k = 100 * (df['close'] - l) / (h - l)
    k = fast_k.rolling(k_smoothing).mean()
    d = k.rolling(d_smoothing).mean()
    df[k_name] = k
    df[d_name] = d


def stochastic_k_col(period, k_smoothing, d_smoothing):
    return 'stochastic(%d,%d,%d):%%K' % (period, k_smoothing, d_smoothing)


def stochastic_d_col(period, k_smoothing, d_smoothing):
    return 'stochastic(%d,%d,%d):%%D' % (period, k_smoothing, d_smoothing)


def past_bb_mid(period, mul, lb=0):
    if bb_mid_col(period, mul) not in df:
        calculate_bb(period, mul)
    return df[bb_mid_col(period, mul)].iloc[-1-lb]


def past_bb_up(period, mul, lb=0):
    if bb_up_col(period, mul) not in df:
        calculate_bb(period, mul)
    return df[bb_up_col(period, mul)].iloc[-1-lb]


def past_bb_low(period, mul, lb=0):
    if bb_low_col(period, mul) not in df:
        calculate_bb(period, mul)
    return df[bb_low_col(period, mul)].iloc[-1-lb]


def past_bb_percent(period, mul, lb=0):
    if bb_percent_col(period, mul) not in df:
        calculate_bb(period, mul)
    return df[bb_percent_col(period, mul)].iloc[-1-lb]


def past_bb_bw(period, mul, lb=0):
    if bb_bw_col(period, mul) not in df:
        calculate_bb(period, mul)
    return df[bb_bw_col(period, mul)].iloc[-1-lb]


def calculate_bb(period, mul):
    mid_name = bb_mid_col(period, mul)
    upp_name = bb_up_col(period, mul)
    low_name = bb_low_col(period, mul)
    pct_b_name = bb_percent_col(period, mul)
    bw_name = bb_bw_col(period, mul)
    mid = df['close'].rolling(period).mean()
    upp = mid + mul*df['close'].rolling(period).std()
    low = mid - mul*df['close'].rolling(period).std()
    pct_b = (df['close'] - low) / (upp - low)
    bw = (upp - low) / mid
    df[mid_name] = mid
    df[upp_name] = upp
    df[low_name] = low
    df[pct_b_name] = pct_b
    df[bw_name] = bw


def bb_mid_col(period, mul):
    return 'bb(%d,%d):middle' % (period, mul*10)


def bb_up_col(period, mul):
    return 'bb(%d,%d):upper' % (period, mul*10)


def bb_low_col(period, mul):
    return 'bb(%d,%d):lower' % (period, mul*10)


def bb_percent_col(period, mul):
    return 'bb(%d,%d):%%b' % (period, mul*10)


def bb_bw_col(period, mul):
    return 'bb(%d,%d):bw' % (period, mul*10)


def macd(fast, slow, smoothing, next_price):
    if macd_col(fast, slow, smoothing) not in df:
        calculate_macd(fast, slow, smoothing)

    fast_name = macd_fast_col(fast, slow, smoothing)
    slow_name = macd_slow_col(fast, slow, smoothing)
    f_alpha = 2 / (fast + 1)
    s_alpha = 2 / (slow + 1)
    f = (next_price-df[fast_name].iloc[-1])*f_alpha+df[fast_name].iloc[-1]
    s = (next_price-df[slow_name].iloc[-1])*s_alpha+df[slow_name].iloc[-1]
    macd = f - s
    return macd


def macd_signal(fast, slow, smoothing, next_price):
    if macd_signal_col(fast, slow, smoothing) not in df:
        calculate_macd(fast, slow, smoothing)

    macd_name = macd_col(fast, slow, smoothing)
    fast_name = macd_fast_col(fast, slow, smoothing)
    slow_name = macd_slow_col(fast, slow, smoothing)
    f_alpha = 2 / (fast + 1)
    s_alpha = 2 / (slow + 1)
    f = (next_price-df[fast_name].iloc[-1])*f_alpha+df[fast_name].iloc[-1]
    s = (next_price-df[slow_name].iloc[-1])*s_alpha+df[slow_name].iloc[-1]
    macd = f - s
    signal = (df[macd_name].iloc[-smoothing+1:].sum() + macd) / smoothing
    return signal


def past_macd(fast, slow, smoothing, lb=0):
    if macd_col(fast, slow, smoothing) not in df:
        calculate_macd(fast, slow, smoothing)
    return df[macd_col(fast, slow, smoothing)].iloc[-1-lb]


def past_macd_signal(fast, slow, smoothing, lb=0):
    if macd_signal_col(fast, slow, smoothing) not in df:
        calculate_macd(fast, slow, smoothing)
    return df[macd_signal_col(fast, slow, smoothing)].iloc[-1-lb]


def past_macd_hist(fast, slow, smoothing, lb=0):
    if macd_signal_col(fast, slow, smoothing) not in df:
        calculate_macd(fast, slow, smoothing)
    return df[macd_col(fast, slow, smoothing)].iloc[-1-lb] - df[macd_signal_col(fast, slow, smoothing)].iloc[-1-lb]


def calculate_macd(fast, slow, smoothing):
    macd_name = macd_col(fast, slow, smoothing)
    signal_name = macd_signal_col(fast, slow, smoothing)
    fast_name = macd_fast_col(fast, slow, smoothing)
    slow_name = macd_slow_col(fast, slow, smoothing)
    f_alpha = 2 / (fast + 1)
    s_alpha = 2 / (slow + 1)
    f = pd.Series(np.nan, index=df.index)
    s = pd.Series(np.nan, index=df.index)
    f.iloc[fast-1] = df['close'].iloc[:fast].mean()
    s.iloc[slow-1] = df['close'].iloc[:slow].mean()
    for i in df.index[fast:]:
        f[i] = (df['close'][i]-f[i-1])*f_alpha+f[i-1]
    for i in df.index[slow:]:
        s[i] = (df['close'][i]-s[i-1])*s_alpha+s[i-1]
    macd = f - s
    signal = macd.rolling(smoothing).mean()
    # signal_alpha = 2 / (smoothing + 1)
    # signal[slow+smoothing-2] = macd[slow-1:slow+smoothing-1].mean()
    # for i in df.index[slow+smoothing-1:]:
    #     signal[i] = (macd[i]-signal[i-1])*signal_alpha+signal[i-1]
    df[macd_name] = macd
    df[signal_name] = signal
    df[fast_name] = f
    df[slow_name] = s


def macd_col(fast, slow, smoothing):
    return 'macd(%d,%d,%d):macd' % (fast, slow, smoothing)


def macd_signal_col(fast, slow, smoothing):
    return 'macd(%d,%d,%d):signal' % (fast, slow, smoothing)


def macd_fast_col(fast, slow, smoothing):
    return 'macd(%d,%d,%d):fast' % (fast, slow, smoothing)


def macd_slow_col(fast, slow, smoothing):
    return 'macd(%d,%d,%d):slow' % (fast, slow, smoothing)


def sar(start, increment, maximum, next_price):
    if sar_col(start, increment, maximum) not in df:
        calculate_sar(start, increment, maximum)

    sar_name = sar_col(start, increment, maximum)
    return df[sar_name].iloc[-1]


def past_sar(start, increment, maximum, lb=0):
    if sar_col(start, increment, maximum) not in df:
        calculate_sar(start, increment, maximum)
    return df[sar_col(start, increment, maximum)].iloc[-1-lb]


def calculate_sar(start, increment, maximum):
    sar_name = sar_col(start, increment, maximum)
    sar = pd.Series(np.nan, index=df.index)
    if (df['high'].iloc[0] < df['high'].iloc[1]):
        rising = True
        sar.iloc[0] = ep = min(df['low'].iloc[0], df['low'].iloc[1])
    else:
        rising = False
        sar.iloc[0] = ep = max(df['high'].iloc[0], df['high'].iloc[1])
    af = start
    for i in df.index[1:]:
        if rising and df['low'][i] < sar[i-1]:
            sar[i] = ep
            rising = False
            ep = df['low'][i]
            af = start
        elif not rising and df['high'][i] > sar[i-1]:
            sar[i] = ep
            rising = True
            ep = df['high'][i]
            af = start
        else:
            if rising:
                if df['high'][i] > ep:
                    ep = df['high'][i]
                    af += increment
                    if af > maximum:
                        af = maximum
                temp = sar[i-1]+af*(ep-sar[i-1])
                sar[i] = df['low'][i] if temp > df['low'][i] else temp
            else:
                if df['low'][i] < ep:
                    ep = df['low'][i]
                    af += increment
                    if af > maximum:
                        af = maximum
                temp = sar[i-1]+af*(ep-sar[i-1])
                sar[i] = df['high'][i] if temp < df['high'][i] else temp
    df[sar_name] = sar


def sar_col(start, increment, maximum):
    return 'sar(%d,%d,%d)' % (start*1000, increment*1000, maximum*1000)


def aroon_up(period, next_price):
    if aroon_up_col(period) not in df:
        calculate_aroon(period)

    ser = list(df['high'].iloc[-period:]) + [next_price]
    val = 0
    for i in range(0, len(ser)):
        if ser[i] >= val:
            idx = i
            val = ser[i]
    u = idx/period*100
    return u


def aroon_down(period, next_price):
    if aroon_down_col(period) not in df:
        calculate_aroon(period)

    ser = list(df['low'].iloc[-period:]) + [next_price]
    val = 9999999999
    for i in range(0, len(ser)):
        if ser[i] <= val:
            idx = i
            val = ser[i]
    d = idx/period*100
    return d


def past_aroon_up(period, lb=0):
    if aroon_up_col(period) not in df:
        calculate_aroon(period)
    return df[aroon_up_col(period)].iloc[-1-lb]


def past_aroon_down(period, lb=0):
    if aroon_down_col(period) not in df:
        calculate_aroon(period)
    return df[aroon_down_col(period)].iloc[-1-lb]


def calculate_aroon(period):
    up_name = aroon_up_col(period)
    down_name = aroon_down_col(period)
    u = df['high'].rolling(
        period+1).apply(lambda x: (period-x[::-1].argmax())/period*100, raw=True)
    d = df['low'].rolling(
        period+1).apply(lambda x: (period-x[::-1].argmin())/period*100, raw=True)
    df[up_name] = u
    df[down_name] = d


def aroon_up_col(period):
    return 'aroon(%d):up' % period


def aroon_down_col(period):
    return 'aroon(%d):down' % period


# def obv(lb=0):
#     if obv_col() not in df:
#         calculate_obv()
#     return df[obv_col()].iloc[-1-lb]


# def calculate_obv():
#     obv_name = obv_col()
#     obv = pd.Series(0, index=df.index)
#     for i in df.index[1:]:
#         if df['close'][i] > df['close'][i-1]:
#             obv[i] = obv[i-1] + df['volume'][i]
#         elif df['close'][i] < df['close'][i-1]:
#             obv[i] = obv[i-1] - df['volume'][i]
#         else:
#             obv[i] = obv[i-1]
#     df[obv_name] = obv


# def obv_col():
#     return 'obv'


# def adl(lb=0):
#     if adl_col() not in df:
#         calculate_adl()
#     return df[adl_col()].iloc[-1-lb]


# def calculate_adl():
#     adl_name = adl_col()
#     adl = pd.Series(np.nan, index=df.index)
#     for i in df.index:
#         prev = adl[i-1] if i > 0 else 0
#         close = df['close'][i]
#         high = df['high'][i]
#         low = df['low'][i]
#         volume = df['volume'][i]

#         if high == low:
#             adl[i] = prev
#         else:
#             adl[i] = prev + ((close-low) - (high-close))/(high-low)*volume
#     df[adl_name] = adl


# def adl_col():
#     return 'adl'


# predict()
codes = stock.JII70
screen(codes)
