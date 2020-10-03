import requests
import stock
import pymongo
import pandas as pd
import numpy as np
import json
from datetime import datetime

MONGO_CLIENT = pymongo.MongoClient('mongodb://localhost:27017/')
DB = MONGO_CLIENT['stock']



codes = stock.LQ45_JII70
USER_AGENT = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.102 Safari/537.36'
COOKIES = 'B=9afsuf1dru52r&b=4&d=DC814yhpYF5uEHdqdeHDce7yawQ-&s=bv&i=3LGUhtWvNIVKxl8N32sp; T=z=Lqj4bBL.K9bBv/lTv.ZAzmlMjc3TwY2MDUzNTIxMzc2&a=QAE&sk=DAAedUzqKfxZcS&ks=EAAMItOffvWFyO0n9ODyMecqg--~G&kt=EAA7BwBf1a4ZfWoMI7OQsFvmA--~I&ku=FAASpnX7YK5UthBsJCqLZjI_L.MOFfLSfC6u.T3e6p0C2ZuaweEYqGpfcwGYhvtWBXK6h49KKjZK3VdQaRUnhCKD5eiMEubPEqZQQdZJd1aXPB8Ng5VhWMv8c6gNmkTEaS74YoORGkyENMVkqjHpPJ2vXNNRcN5k9cxksYh7VaUfUg-~A&d=bnMBeWFob28BZwFZT1lPV05aRkFWQ0RRQ1E2NDZNQzZSQldZQQFzbAFOVEF3T0FFeE56STBNalUyTkRBeAFhAVFBRQFhYwFBSklvLkJIbgFjcwEBc2MBZGVza3RvcF93ZWIBZnMBdGE2eV9NQmI0anFMAXp6AUxxajRiQkE3RQ--&af=JnRzPTE1NDE1NTI3NzkmcHM9b3N1a0hsMGN4VWZscm16SUQzSzltZy0t; F=d=BivGc_89vHnWLuragbOdNQuS6kNqtOBd8McpqTPQYQ--; PH=fn=HMt6UzD8UEWyTI2BAKEThT6cpg--&l=id-ID&i=id; Y=v=1&n=4338sej3nta47&l=l0i78ael827/o&p=m2svvid00000000&r=hk&lg=id-ID&intl=id; AO=u=1; GUC=AQEAAQJb44NcukIg3QSk&s=AQAAAGtA_BEV&g=W-I6tA; PRF=t%3DANTM.JK%252BAKRA.JK%252BADRO.JK%252BADHI.JK%252BAALI.JK%252BIDX%252B%255EJKSE'
period = 'D'

for code in codes:
# stock.calculate_sma_in_db(code, period, 10)
    stock.calculate_sma_in_db(code, period, 20)
# stock.calculate_sma_in_db(code, period, 50)
    stock.calculate_sma_in_db(code, period, 100)
# stock.calculate_rsi_in_db(code, period, 14)
# stock.calculate_ppsr_in_db(code, period)
    stock.calculate_lowest_low_in_db(code, period, 3)
    stock.calculate_stochastic_in_db(code, period, 14, 3, 3)
# stock.calculate_bb_in_db(code, period, 20, 2)
# stock.calculate_bb_in_db(code, period, 20, 2.5)
# stock.calculate_bb_in_db(code, period, 20, 3)
    # stock.calculate_macd_in_db(code, period, 12, 26, 9)
    # DB[code+'.'+period].update_many({},{'$unset': {'macd(12,26,9)': 0}})
# DB['simulation'].delete_one({'_id': '21'})
# DB['simulation_details'].delete_one({'_id': '21'})
    print('%s (%d/%d)' % (code, codes.index(code)+1, len(codes)))

# trx = list(DB['simulation_details'].find({'_id':'20'}))[0]['trx_summary']


def get_ticker_code(codes):
    with open('ticker_code', 'w') as f:
        for code in codes:
            rs = requests.get('https://tvc4.forexpros.com/ea2618475a7ce7d92246499d0af1c736/1548641140/1/1/8/symbols?symbol=JAKARTA%%20%%3A%s' %
                              (code), verify=False, headers={'User-Agent': USER_AGENT, 'Cookie': COOKIES})
            data = json.loads(rs.text)
            f.write(code + ' ' + data['ticker'])


def get_csv(code, period):
    ticker_code = stock.ticker_codes[code]
    rs = requests.get('https://tvc4.forexpros.com/ea2618475a7ce7d92246499d0af1c736/1548641140/1/1/8/history?symbol=%s&resolution=%s&from=0&to=9999999999' %
                        (ticker_code, period), verify=False, headers={'User-Agent': USER_AGENT, 'Cookie': COOKIES})
    data = json.loads(rs.text)
    with open(code + '.' + period + '.csv', 'w') as f:
        del data['s']
        df = pd.DataFrame(data)
        for idx, row in df.iterrows():
            text = '%s,%s,%s,%s,%s,%s,%s\n' % (datetime.utcfromtimestamp(
                row['t']), row['o'], row['h'], row['l'], row['c'], row['v'], row['vo'])
            f.write(text)


def add_watchlist(code):
    auth = 'Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpYXQiOjE1NDg3MjU4MTEsImp0aSI6InpLaXFhZ242d2JZXC9xOThHajJsNTlnPT0iLCJpc3MiOiJTVE9DS0JJVCIsIm5iZiI6MTU0ODcyNTgxMSwiZXhwIjoxNTQ4NzQwMjExLCJkYXRhIjp7InVzZSI6IlZhc2hpa292aWNoIiwiZW1hIjoid2Fza2l0aG9Ab3V0bG9vay5jb20iLCJmdWwiOiJJbmRlcmEgQWppIFdhc2tpdGhvIiwic2VzIjoiMWF1SXRhMDRYT0dFZWYyaiIsImR2YyI6IiJ9fQ.d95CL0HHgYMwN6JzwFxBx9-omhrynQgKf2nOyTWRB7o'
    rs = requests.get('https://api.stockbit.com/v2.2/search/company?q=%s&p=1' % code, verify=False,
                        headers={'User-Agent': USER_AGENT, 'Cookie': COOKIES, 'Authorization': auth})
    data = json.loads(rs.text)
    id = data['data']['company'][0]['id']
    rs = requests.post('https://api.stockbit.com/v2.2/watchlist/company/item/add/206022', data={
                        'companyid': id}, verify=False, headers={'User-Agent': USER_AGENT, 'Cookie': COOKIES, 'Authorization': auth})


# get_ticker_code(codes)
# for code in codes:
#     period = 'D'
#     # get_csv(code, period)
#     # add_watchlist(code)
#     stock.import_to_db(code, period)
#     stock.create_db_index(code, period)
#     # DB[code + '.' + period].drop()
#     print(code)
