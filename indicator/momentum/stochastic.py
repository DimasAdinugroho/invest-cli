import os
import sys
from ta.momentum import StochasticOscillator


p = os.path.abspath('../..')
if p not in sys.path:
    sys.path.append(p)

from utils import param


def stochasticIndicator(self):
    ''' Stochastic Indicator is a momentum indicator, it provides BUY and SELL signal.
    There are two lines: stoch() and stoch_signal()
    SELL Signal:
     - both lines should be > overbought
     - stoch() line cross the stoch_signal()
    BUY Signal:
     - both lines should be < oversold
     - stoch() line cross the stoch_signal()
    '''
    s_signal = "NEUTRAL"
    # load parameter        
    overbought = param('stochastic', 'overbought', 80)
    oversold = param('stochastic', 'oversold', 20)
    n = param('stochastic', 'n', 14) 
    d_n = param('stochastic', 'd_n', 3)         
    
    # stochastic line
    stoch = StochasticOscillator(high=self.df.high, low=self.df.low, close=self.df.close, n=n, d_n=d_n, fillna=True)
    stoch_diff = stoch.stoch() - stoch.stoch_signal()
    
    last_stoch = list(stoch.stoch())[-1]
    last_signal_line = list(stoch.stoch_signal())[-1]
    last_stoch_diff = list(stoch_diff)[-1]
    if last_stoch >= overbought and last_signal_line >= overbought:
        if last_stoch_diff < 2:
            s_signal = "SELL"    
            self.add_signal('stoch', 'sell')  
            # self.signal_df['sell_signal'] += 1
    elif last_stoch <= oversold and last_signal_line <= oversold:
        if last_stoch_diff > 2:
            s_signal = "BUY"
            self.add_signal('stoch', 'buy')
            # self.signal_df['buy_signal'] += 1
    self.signal_df['stochastic'] = {}
    self.signal_df['stochastic']['signal'] = s_signal
    self.signal_df['stochastic']['stoch_line'] = last_stoch
    self.signal_df['stochastic']['signal_line'] = last_signal_line
    return s_signal