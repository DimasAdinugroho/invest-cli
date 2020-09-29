import pandas as pd
from tapy import Indicators

p = os.path.abspath('../..')
if p not in sys.path:
    sys.path.append(p)

from utils import param


def alligatorIndicator(self):
    '''
    '''

    alig_signal = "NEUTRAL"
    desc = "sideway"

    # parameter
    jaws = param('alig', 'period_jaw', 13)
    teeth = param('alig', 'period_teeth', 8)
    lips = param('alig', 'period_lips', 5)    
    inds = Indicators(self.df, open_col='open', high_col='high', low_col='low', close_col='close', volume_col='volume')
    inds.alligator(
        period_jaws=jaws, period_teeth=teeth, period_lips=5, 
        shift_jaws=8, shift_teeth=5, shift_lips=3, 
        column_name_jaws='alligator_jaw', column_name_teeth='alligator_teeth', column_name_lips='alligator_lips'
    )
    data = inds.df
    data.tail(1)


