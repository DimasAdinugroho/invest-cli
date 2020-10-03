import requests
import stock
import pymongo
import pandas as pd
import numpy as np
import json
import db_sync
from datetime import datetime, timedelta, time

def get_max_idx(df):
    max_idx = []
    if df['close'].iloc[0] >= df['close'].iloc[1]:
        max_idx.append(0)
    for idx in df.index[1:-1]:
        if df['close'].loc[idx] >= df['close'].loc[idx-1] and df['close'].loc[idx] >= df['close'].loc[idx+1]:
            max_idx.append(idx)
    if df['close'].iloc[-1] >= df['close'].iloc[-2]:
        max_idx.append(df.index[-1])
    return max_idx

def get_min_idx(df):
    min_idx = []
    if df['close'].iloc[0] <= df['close'].iloc[1]:
        min_idx.append(0)
    for idx in df.index[1:-1]:
        if df['close'].loc[idx] <= df['close'].loc[idx-1] and df['close'].loc[idx] <= df['close'].loc[idx+1]:
            min_idx.append(idx)
    if df['close'].iloc[-1] <= df['close'].iloc[-2]:
        min_idx.append(df.index[-1])
    return min_idx


data = db_sync.fetch_data('TLKM', datetime(2018,3,15), datetime(2019,1,15), as_df=True)
max_idx = get_max_idx(data)
min_idx = get_min_idx(data)
