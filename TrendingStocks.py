# -*- coding: utf-8 -*-
# TrendingStocks.py
"""
Version: 4.18.2015
@author: Luke_Wortsmann
"""
from yahoo_finance import Share
import StockScreener as SS
sp500data = SS.getSP500data()
print sp500data.getTrending()
