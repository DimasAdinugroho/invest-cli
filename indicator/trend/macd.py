import os
import sys
from ta.trend import MACD


p = os.path.abspath('../..')
if p not in sys.path:
    sys.path.append(p)

from utils import param

def macdIndicator(self):
        ''' MACD indicator is a trend indicator, it provides BUY and SELL signal.
        MACD is a lagging indicator: so in order to correct it, BUY/SELL signal also trigger when histogram reach the peak/bottom
        There are two lines: macd lines and signal lines
        SELL Signal:
            - Death cross: MACD line moves from above to below the signal line                        
            - (MACD - Signal):macd_diff has a big negative difference value: min(MACD - signal)
        BUY Signal
            - Golden cross: MACD line moves from below to above signal line            
            - (MACD - signal):macd_diff has a big positive difference value: max(MACD - signal)
        Trend Signal:        
            - Sideway: Average of (macd - signall) is between - 15 < x < 15
            - Uptrend:  Average of (macd - signall) is x > 15
            - Downtrend:  Average of (macd - signall) is x < - 15 
        '''
        def trend(macd_diff, min_macd_val):
            avg = sum(macd_diff[-10:]) / 10  # two weeks is 10 days
            # print(avg)
            if avg > min_macd_val:
                return 'Uptrend'
            elif avg < -min_macd_val:
                return 'Downtrend'
            else:
                return 'sideway'

        macd_signal = 'NEUTRAL'    

        # load parameter        
        n_fast = param('macd', 'n_fast', 10)
        n_slow = param('macd','n_slow', 30)
        n_sign = param('macd','n_sign', 9)
        min_macd_val = param('macd','min_macd_val', 25)

        exp1 = self.df.close.ewm(span=n_fast, adjust=False).mean()
        exp2 = self.df.close.ewm(span=n_slow, adjust=False).mean()
        macd = exp1-exp2
        signal = macd.ewm(span=n_sign, adjust=False).mean()

        macd_diff = list(macd - signal)    
        macd_desc = trend(macd_diff, min_macd_val)

        # golden cross
        if macd_diff[-3] < 0 and macd_diff[-1] > 0:
            macd_signal = 'BUY'   
            self.add_signal('macd', 'buy')
            # self.signal_df['buy_signal'] += 1
        # death cross
        if macd_diff[-3] > 0 and macd_diff[-1] < 0:
            macd_signal = 'SELL'
            self.add_signal('macd', 'sell')
            # self.signal_df['sell_signal'] += 1

        # macd_diff    
        # a low macd_diff value means it is a sideways: macd will often be cross
        if macd_diff[-1] > min_macd_val or macd_diff[-1] < -min_macd_val:
            # macd_hist < 0 -> buy signal
            if macd_diff[-1] < 0 and macd_diff[-2] < 0:
                if macd_diff[-2] < macd_diff[-1] and macd_diff[-3] > macd_diff[-2]:
                    macd_signal = 'BUY'   
                    self.add_signal('macd', 'buy')
            # macd_hist > 0 -> sell signal
            elif macd_diff[-1] > 0 and macd_diff[-2] > 0:
                if macd_diff[-2] > macd_diff[-1] and macd_diff[-3] < macd_diff[-2]:
                    macd_signal = 'SELL'
                    self.add_signal('macd', 'sell')

        self.signal_df['macd'] = {}
        self.signal_df['macd']['signal'] = macd_signal
        self.signal_df['macd']['trend'] = macd_desc
        self.signal_df['macd']['histogram'] = macd_diff[-1]