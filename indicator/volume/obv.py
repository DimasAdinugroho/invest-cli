from ta.trend import SMAIndicator
from ta.volume import OnBalanceVolumeIndicator, AccDistIndexIndicator


def OBVIndicator(self):
    volumeSMA60 = SMAIndicator(self.df.volume, 60).sma_indicator()
    closeSMA65 = SMAIndicator(self.df.close, 65).sma_indicator()
    closeSMA60 = SMAIndicator(self.df.close, 60).sma_indicator()
    closeSMA20 = SMAIndicator(self.df.close, 20).sma_indicator()


    accDistLine = AccDistIndexIndicator(self.df.high, self.df.low, self.df.close, self.df.volume).acc_dist_index()
    accDistLineSMA65 = SMAIndicator(accDistLine, 65).sma_indicator()
    accDistLineSMA20 = SMAIndicator(accDistLine, 20).sma_indicator()

    OBVLine = OnBalanceVolumeIndicator(self.df.close, self.df.volume).on_balance_volume()
    OBVLineSMA65 = SMAIndicator(OBVLine, 65).sma_indicator()
    OBVLineSMA20 = SMAIndicator(OBVLine, 20).sma_indicator()

    # Bullish Divergence: buy signal
    obv_signal = 'NEUTRAL'

    if (volumeSMA60[-1] > 100000 and closeSMA60[-1] > 10):
        #Buy signal
        signal1 = self.df.close[-1] < closeSMA65[-1]
        signal2 = accDistLine[-1] > accDistLineSMA65[-1]
        signal3 = OBVLine[-1] > OBVLineSMA65[-1]
        signal4 = self.df.close[-1] < closeSMA20[-1]
        signal5 = accDistLine[-1] > accDistLineSMA20[-1]
        signal6 = OBVLine[-1] > OBVLineSMA20[-1]

        if signal1 and signal2 and signal3 and signal4 and signal5 and signal6:
            obv_signal = 'BUY'
            self.add_signal('obv', 'buy')
            # self.signal_df['buy_signal'] += 1
        if not signal1 and not signal2 and not signal3 and not signal4 and not signal5 and not signal6:
            obv_signal ='SELL'
            self.add_signal('obv', 'sell')
            # self.signal_df['sell_signal'] += 1

    self.signal_df['obv'] = {}
    self.signal_df['obv']['signal'] = obv_signal