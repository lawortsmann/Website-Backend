# -*- coding: utf-8 -*-
# TrendingStocks.py
"""
Version: 4.18.2015
@author: Luke_Wortsmann
"""
from yahoo_finance import Share
import StockScreener as SS
NYSEdata = SS.getNYSEdata()
print NYSEdata.getTrending()
