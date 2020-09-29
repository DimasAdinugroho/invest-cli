import os
import sys
import pandas as pd
from ta.trend import SMAIndicator, EMAIndicator


p = os.path.abspath('../..')
if p not in sys.path:
    sys.path.append(p)

from utils import param


def maIndicator(self):
    ''' SMA dan EMA (Moving Average) is a trend indicator, it provides BUY and SELL signal.
        Signal BUY:
        - sma20 crossing dari bawah ke atas sma50
        - sma20 crossing dari bawah ke atas sma100
        - ema20 crossing dari bawah ke atas ema50
        - ema20 crossing dari bawah ke atas ema100
        Signal SELL:
        - sma20 crossing dari atas ke bawah sma50
        - sma20 crossing dari atas ke bawah sma100
        - ema20 crossing dari atas ke bawah ema50
        - ema20 crossing dari atas ke bawah ema100
    '''
    signal = 'NEUTRAL'
    desc = ''
    
    sma = pd.DataFrame()
    sma['200'] = SMAIndicator(self.df.close, 200).sma_indicator()
    sma['50'] = SMAIndicator(self.df.close, 50).sma_indicator()
    sma['20'] = SMAIndicator(self.df.close, 20).sma_indicator()
    sma['diff_5020'] = sma['50'] - sma['20']
    sma['diff_20020'] = sma['200'] - sma['20']

    ema = pd.DataFrame()
    ema['200'] = EMAIndicator(self.df.close, 200).ema_indicator()
    ema['50'] = EMAIndicator(self.df.close, 50).ema_indicator()
    ema['20'] = EMAIndicator(self.df.close, 20).ema_indicator()
    ema['diff_5020'] = ema['50'] - ema['20']
    ema['diff_20020'] = ema['200'] - ema['20']

    # ----------------- Signal BUY -----------------
    if sma.iloc[-2]['diff_5020'] > 0  and sma.iloc[-1]['diff_5020'] < 3:
        signal = 'BUY'
        self.add_signal('ma', 'buy')
        desc += 'Crossing 20SMA from below to above 50SMA'

    elif sma.iloc[-2]['diff_20020'] > 0  and sma.iloc[-1]['diff_20020'] < 3:
        signal = 'BUY'
        self.add_signal('ma', 'buy')
        desc += 'Crossing 20SMA from below to above 200SMA'
        
    elif ema.iloc[-2]['diff_5020'] > 0  and ema.iloc[-1]['diff_5020'] < 3:
        signal = 'BUY'
        self.add_signal('ma', 'buy')
        desc += 'Crossing 20EMA from below to above 50EMA'

    elif ema.iloc[-2]['diff_20020'] > 0  and ema.iloc[-1]['diff_20020'] < 3:
        signal = 'BUY'
        self.add_signal('ma', 'buy')
        desc += 'Crossing 20EMA from below to above 200EMA'
        
    # ----------------- Signal SELL -----------------
    if sma.iloc[-2]['diff_5020'] < 0  and sma.iloc[-1]['diff_5020'] > -3:
        signal = 'SELL'
        self.add_signal('ma', 'sell')
        desc += 'Crossing 20SMA from above to below 50SMA'

    elif sma.iloc[-2]['diff_20020'] < 0  and sma.iloc[-1]['diff_20020'] > -3:
        signal = 'SELL'
        self.add_signal('ma', 'sell')
        desc += 'Crossing 20SMA from above to below 200SMA'
        
    elif ema.iloc[-2]['diff_5020'] < 0  and ema.iloc[-1]['diff_5020'] > -3:
        signal = 'SELL'
        self.add_signal('ma', 'sell')
        desc += 'Crossing 20EMA from above to below 50EMA'

    elif ema.iloc[-2]['diff_20020'] < 0  and ema.iloc[-1]['diff_20020'] > -3:
        signal = 'SELL'
        self.add_signal('ma', 'sell')
        desc += 'Crossing 20EMA from above to below 200EMA'

    self.signal_df['ma'] = {}
    self.signal_df['ma']['desc'] = desc
    self.signal_df['ma']['signal'] = signal
    self.signal_df['ma']['sma20'] = round(sma.iloc[-1]['20'], 3)
    self.signal_df['ma']['sma50'] = round(sma.iloc[-1]['50'], 3)
    self.signal_df['ma']['sma200'] = round(sma.iloc[-1]['200'], 3)
    self.signal_df['ma']['ema20'] = round(ema.iloc[-1]['20'], 3)
    self.signal_df['ma']['ema50'] = round(ema.iloc[-1]['50'], 3)
    self.signal_df['ma']['ema200'] = round(ema.iloc[-1]['200'], 3)
