import requests
import stock
import pymongo
import pandas as pd
import numpy as np
import json
from datetime import datetime, timedelta, time

import urllib3
urllib3.disable_warnings()

MONGO_CLIENT = pymongo.MongoClient('mongodb://localhost:27017/')
DB = MONGO_CLIENT['stock']

USER_AGENT = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.102 Safari/537.36'
COOKIES = 'B=9afsuf1dru52r&b=4&d=DC814yhpYF5uEHdqdeHDce7yawQ-&s=bv&i=3LGUhtWvNIVKxl8N32sp; T=z=Lqj4bBL.K9bBv/lTv.ZAzmlMjc3TwY2MDUzNTIxMzc2&a=QAE&sk=DAAedUzqKfxZcS&ks=EAAMItOffvWFyO0n9ODyMecqg--~G&kt=EAA7BwBf1a4ZfWoMI7OQsFvmA--~I&ku=FAASpnX7YK5UthBsJCqLZjI_L.MOFfLSfC6u.T3e6p0C2ZuaweEYqGpfcwGYhvtWBXK6h49KKjZK3VdQaRUnhCKD5eiMEubPEqZQQdZJd1aXPB8Ng5VhWMv8c6gNmkTEaS74YoORGkyENMVkqjHpPJ2vXNNRcN5k9cxksYh7VaUfUg-~A&d=bnMBeWFob28BZwFZT1lPV05aRkFWQ0RRQ1E2NDZNQzZSQldZQQFzbAFOVEF3T0FFeE56STBNalUyTkRBeAFhAVFBRQFhYwFBSklvLkJIbgFjcwEBc2MBZGVza3RvcF93ZWIBZnMBdGE2eV9NQmI0anFMAXp6AUxxajRiQkE3RQ--&af=JnRzPTE1NDE1NTI3NzkmcHM9b3N1a0hsMGN4VWZscm16SUQzSzltZy0t; F=d=BivGc_89vHnWLuragbOdNQuS6kNqtOBd8McpqTPQYQ--; PH=fn=HMt6UzD8UEWyTI2BAKEThT6cpg--&l=id-ID&i=id; Y=v=1&n=4338sej3nta47&l=l0i78ael827/o&p=m2svvid00000000&r=hk&lg=id-ID&intl=id; AO=u=1; GUC=AQEAAQJb44NcukIg3QSk&s=AQAAAGtA_BEV&g=W-I6tA; PRF=t%3DANTM.JK%252BAKRA.JK%252BADRO.JK%252BADHI.JK%252BAALI.JK%252BIDX%252B%255EJKSE'


def sync_many(stock_codes):
    if trading_time():
        print('Trading is currently in progress, syncing last trading data...')
    else:
        print('Syncing...')

    for stock_code in stock_codes:
        sync(stock_code)

def sync(stock_code):
    last_date = get_last_db_date(stock_code)
    if last_date < last_trading_date():
        fetched = fetch_data(stock_code, last_date)
        if fetched != None:
            update_db(stock_code, fetched)


def get_last_db_date(stock_code):
    last_data = list(coll(stock_code).find().sort(
        'date', direction=pymongo.DESCENDING).limit(1))
    return last_data[0]['date'] if len(last_data) > 0 else datetime(1980, 1, 1)


def fetch_data(stock_code, start_date, end_date=datetime(2099,12,31), as_df=False):
    try:
        ticker_code = get_ticker_code(stock_code)
    except:
        return
    end_timestamp = end_date.timestamp()
    start_timestamp = start_date.timestamp()
    try:
        rs = requests.get('https://tvc4.forexpros.com/ea2618475a7ce7d92246499d0af1c736/1548641140/1/1/8/history?symbol=%s&resolution=D&from=%d&to=%d' %
                        (ticker_code, start_timestamp, end_timestamp), verify=False, headers={'User-Agent': USER_AGENT, 'Cookie': COOKIES})
        raw_data = json.loads(rs.text)
        data = [process_raw_data(raw_data, i) for i in range(len(raw_data['t']))]
        if as_df:
            return pd.DataFrame(data)
        else:
            return data
    except:
        print(stock_code)
        print(rs.text)
        raise Exception("error fetch_data")


def get_ticker_code(stock_code):
    ticker_codes = read_ticker_codes()
    if stock_code not in ticker_codes:
        ticker_code = fetch_ticker_code(stock_code)
        ticker_codes[stock_code] = ticker_code
        write_ticker_codes(ticker_codes)
    return ticker_codes[stock_code]


def last_trading_date():
    def d2dt(date):
        return datetime.combine(date, time())

    now = datetime.now()

    if now.weekday() >= 5:
        return d2dt((now - timedelta(days=now.weekday()-4)).date())
    if trading_time():
        return d2dt((now - timedelta(days=1)).date())
    if now.time() < time(8, 45, 0):
        return d2dt((now - timedelta(days=3)).date()) if now.weekday() == 0 else d2dt((now - timedelta(days=1)).date())
    if now.time() > time(16, 15, 0):
        return d2dt(now.date())


def trading_time():
    now = datetime.now()
    return now.weekday() <= 4 and now.time() >= time(8, 45, 0) and now.time() <= time(16, 15, 0)


def update_db(stock_code, data):
    if 'date' not in coll(stock_code).index_information():
        create_db_index(stock_code)

    for data_row in data:
        coll(stock_code).update_one(
            {'date': data_row['date']}, {'$set': data_row}, upsert=True)


def create_db_index(stock_code):
    coll(stock_code).create_index([('date', pymongo.DESCENDING)], name='date')


def process_raw_data(data, idx):
    return {
        'date': datetime.fromtimestamp(data['t'][idx]),
        'open': data['o'][idx],
        'high': data['h'][idx],
        'low': data['l'][idx],
        'close': data['c'][idx],
        'volume': data['v'][idx],
    }


def coll(stock_code):
    return DB[stock_code + '.D']


def fetch_ticker_code(stock_code):
    try:
        rs = requests.get('https://tvc4.forexpros.com/ea2618475a7ce7d92246499d0af1c736/1548641140/1/1/8/symbols?symbol=JAKARTA%%20%%3A%s' %
                        stock_code, verify=False, headers={'User-Agent': USER_AGENT, 'Cookie': COOKIES})
        data = json.loads(rs.text)
        ticker_code = data['ticker']
        return ticker_code
    except:
        print(stock_code)
        print(rs.text)
        raise Exception("error fetch_ticker_code")


def read_ticker_codes():
    with open('ticker_codes') as f:
        json_str = f.readline()
        ticker_codes = json.loads(json_str)
        return ticker_codes


def write_ticker_codes(ticker_codes):
    with open('ticker_codes', 'w') as f:
        json_str = json.dumps(ticker_codes)
        f.write(json_str)

