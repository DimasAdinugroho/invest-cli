import os
import sys
from ta.volatility import DonchianChannel


p = os.path.abspath('../..')
if p not in sys.path:
    sys.path.append(p)

from utils import param


def donchianIndicator(self):
    # Volatility Indicator
    # n: lookback period
    desc = ''
    n = param('donchian', 'n', 20)
    last_price = list(self.df.average)[-1]
    last_high = list(self.df.high)[-1]
    last_close = list(self.df.close)[-1]
    last_low = list( self.df.low)[-1]
    last_open = list( self.df.open)[-1]

    dc = DonchianChannel(self.df.high, self.df.low, self.df.close, n, True)
    hband = round(list(dc.donchian_channel_hband())[-1], 2)
    mband = round(list(dc.donchian_channel_mband())[-1], 2)
    lband = round(list(dc.donchian_channel_lband())[-1], 2)
    wband = round(list(dc.donchian_channel_wband())[-1], 2)
    
    if last_price > mband:
        near_mband = abs(last_price - mband)
        near_hband = abs(last_price - hband)
        if  last_high == hband:
            if  last_close == hband and last_low == last_open:
                desc += 'Break upper donchian with full candle bar'
            else:
                desc += 'Break upper donchian with wicked candle bar'
        elif near_mband > near_hband:
            desc += 'Near upper donchian'
        else:
            desc += 'Above middle donchian'
    else:
        near_mband = abs(last_price - mband)
        near_lband = abs(last_price - lband)
        if last_low == lband:
            if last_close == lband and last_low == last_open:
                desc += 'Break lower donchian with full candle bar'
            else:
                desc += 'Break lower donchian with wicked candle bar'
        elif near_mband > near_lband:
            desc += 'Near lower donchian'
        else:
            desc += 'Below middle donchian'                            
    
    self.signal_df['donchian'] = {}
    self.signal_df['donchian']['desc'] = desc
    self.signal_df['donchian']['hband'] = hband        
    self.signal_df['donchian']['mband'] = mband
    self.signal_df['donchian']['lband'] = lband
    self.signal_df['donchian']['wband'] = wband