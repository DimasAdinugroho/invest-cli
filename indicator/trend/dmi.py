import os
import sys
from ta.trend import ADXIndicator


p = os.path.abspath('../..')
if p not in sys.path:
    sys.path.append(p)

from utils import param


def dmiIndicator(self):
    ''' DMI Indicator is a trend indicator, it provides BUY and SELL signal, also Trend signal.
    There are three lines: dmi+, dmi- and signal
    BUY Signal:     
     - dmi+ line cross dmi- from below to above
    SELL Signal:
     - dmi+ line cross dmi- from above to below
    TREND Signal:
     - 
    '''
    adx_signal = "NEUTRAL"
    desc = "sideway"
    # parameter
    n = param('adx', 'n', 14)
    period = param('adx', 'period', 5)

    # ADX Line
    line = ADXIndicator(high=self.df.high, low=self.df.low, close=self.df.close, n=n, fillna=False)
    adx_diff = list(line.adx_pos() - line.adx_neg())
    signal_line = list(line.adx())

    if adx_diff[-period] < 0 and adx_diff[-1] > 0:
        adx_signal = 'BUY'
        self.add_signal('adx', 'buy')
        # self.signal_df['buy_signal'] += 1
    if adx_diff[-period] > 0 and adx_diff[-1] < 0:
        adx_signal = 'SELL'
        self.add_signal('adx', 'sell')
        # self.signal_df['sell_signal'] += 1
    # trend desc          
    if (signal_line[-n] - signal_line[-1]) < 0 and signal_line[-1] <= 23 and signal_line[-1] > 20:
        if adx_diff[-1] >= 0:
            desc = "uptrend"
        else:
            desc = "downtrend"
        desc += ": trend may be developing"
    elif (signal_line[-n] - signal_line[-1]) > 0 and signal_line[-1] >= 25 and signal_line[-1] < 30:        
        if adx_diff[-1] >= 0:
            desc = "uptrend"
        else:
            desc = "downtrend"
        desc += ": trend may coming to and end"
    
    if desc == 'sideway':
        if adx_diff[-1] > 15:
            desc = "uptrend"
        if adx_diff[-1] < -15:
            desc = "downtrend"
    
    self.signal_df['adx'] = {}
    self.signal_df['adx']['trend'] = desc
    self.signal_df['adx']['signal'] = adx_signal