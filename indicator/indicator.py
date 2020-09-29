import os
import json
import pandas as pd
from utils import getStock
from trend import trendIndicator
from momentum import momentumIndicator
from volatility import volatilityIndicator
from volume import volumeIndicator


class TechnicalIndicator:
    ''' All technical indicator for stocks and the signal for buy and sell:
    momentum indicator
    trend indicator
    oscillator indicator
    volatility indicator

    args:
        df: Datafram, includes: Open, High, Close, Low
        isLower: lower the columns name (default: False)
    '''
    def __init__(self, df, isLower=False):
        self.df = df
        if len(self.df) < 30:
            raise Exception("The data time frame is less than a month, require to atleast 3 month")
        
        if isLower:
            self.df.index.name = str.lower(df.index.name)
            self.df.rename(columns=str.lower, inplace=True)

        self.df['average'] = (self.df.close + self.df.high + self.df.low) / 3
        self.last_update = self.df.date.max()
        self.last_updated_data = self.df[self.df.date == self.last_update]        
        self.signal_df = self.last_updated_data.to_dict('r')[0]
        self.signal_df['buy_signal'] = 0
        self.signal_df['buy_indicator'] = ''                
        self.signal_df['sell_signal'] = 0
        self.signal_df['sell_indicator'] = ''

    def add_signal(self, indicator, signal_type):
        if signal_type == 'sell':
            self.signal_df['sell_signal'] += 1
            self.signal_df['sell_indicator'] += indicator +','
        
        if signal_type == 'buy':
            self.signal_df['buy_signal'] += 1
            self.signal_df['buy_indicator'] += indicator +','


def make_signal(df, isLower):
    # from pprint import pprint
    ti = TechnicalIndicator(df, isLower)
    ti.trendIndicator = trendIndicator.__get__(ti)
    ti.momentumIndicator = momentumIndicator.__get__(ti)
    ti.volatilityIndicator = volatilityIndicator.__get__(ti)
    ti.volumeIndicator = volumeIndicator.__get__(ti)
    ti.trendIndicator()
    ti.momentumIndicator()
    ti.volatilityIndicator()
    ti.volumeIndicator()
    return ti.signal_df
    # pprint(ti.signal_df)

# df = getStock('IKAN', '6mo')
# df['date'] = df.index
# make_signal(df, True)