# -*- coding: utf-8 -*-
# StockScreener.py

"""
Version: 03.08.2015

A basic functionality Stock Screener class. Stock Data from yahoo api.
NOTE: needs two supplied .csv files of stock names.

@author: Luke_Wortsmann
"""

import csv
import datetime
import numpy as np
import matplotlib.colors as colors
import matplotlib.finance as finance
import matplotlib.dates as mdates
import matplotlib.ticker as mticker
import matplotlib.mlab as mlab
import matplotlib.pyplot as plt
import matplotlib.font_manager as font_manager
from statistics import mean
from yahoo_finance import Share

class stockScreener:
    def __init__(self):
        self.bySector = {}
        self.bySymbol = {}
        self.byIPOyear = {}

    def addStock(self,Symbol,Name,IPOyear,Sector,industry):
        self.bySymbol[Symbol] = [Symbol,Name,IPOyear,Sector,industry]
        try:
            self.bySector[Sector].append([Symbol,Name,IPOyear,Sector,industry])
        except KeyError:
            self.bySector[Sector] = [[Symbol,Name,IPOyear,Sector,industry]]
        try:
            self.byIPOyear[IPOyear].append([Symbol,Name,IPOyear,Sector,industry])
        except KeyError:
            self.byIPOyear[IPOyear] = [[Symbol,Name,IPOyear,Sector,industry]]

    def metricsForSector(self,Sector, screenParam = ['avgVolume'], screenParamRange = (float("-inf"),float("inf"))):
        outputData = []
        for stock in self.bySector[Sector]:
            try:
                working = stock
                sData = Share(stock[0])
                screenQ = (type(screenParam)==list)

                if 'avgVolume' in screenParam:
                    avgVolume = sData.get_avg_daily_volume()
                    if (screenParamRange[0] <= float(avgVolume) <= screenParamRange[1]) or screenQ:
                        working.append(avgVolume)
                    else:
                        working = None

                if 'mrkCap' in screenParam:
                    mrkCap = sData.get_market_cap()
                    if mrkCap[-1] == 'B':
                        amrkCap = float(mrkCap[:-1])*1000000000
                    if mrkCap[-1] == 'M':
                        amrkCap = float(mrkCap[:-1])*1000000
                    if (screenParamRange[0] <= amrkCap <= screenParamRange[1]) or screenQ:
                        working.append(amrkCap)
                    else:
                        working = None

                outputData.append(working)
            except:
                pass
        return outputData

NYSEdata = stockScreener()
with open('NYSE.csv', 'r') as csvfile:
    filereader = csv.reader(csvfile)
    notFirstRow = False
    for row in filereader:
        Symbol  = row[0]
        Name  = row[1]
        IPOyear = row[4]
        Sector  = row[5]
        industry = row[6]
        if notFirstRow:
            NYSEdata.addStock(Symbol,Name,IPOyear,Sector,industry)
        else:
            notFirstRow = True

NASDAQdata = stockScreener()
with open('NASDAQ.csv', 'r') as csvfile:
    filereader = csv.reader(csvfile)
    notFirstRow = False
    for row in filereader:
        Symbol  = row[0]
        Name  = row[1]
        IPOyear = row[4]
        Sector  = row[5]
        industry = row[6]
        if notFirstRow:
            NASDAQdata.addStock(Symbol,Name,IPOyear,Sector,industry)
        else:
            notFirstRow = True

sectors = NYSEdata.bySector.keys()
print sectors
NYSEdata.metricsForSector(sectors[0], screenParam = ['avgVolume','mrkCap'])
