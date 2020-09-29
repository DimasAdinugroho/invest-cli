from .dmi import dmiIndicator
from .macd import macdIndicator
from .ma import maIndicator


def trendIndicator(self):
    dmiIndicator(self)
    macdIndicator(self)
    maIndicator(self)