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
import time

class stockScreener:
    def __init__(self):
        self.bySector = {}
        self.bySymbol = {}

    def addStock(self,Symbol,Name,Sector):
        self.bySymbol[Symbol] = [Symbol,Name,Sector]
        try:
            self.bySector[Sector].append([Symbol,Name,Sector])
        except KeyError:
            self.bySector[Sector] = [[Symbol,Name,Sector]]

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

    def getTrending(self):
        trending = []
        k = 0
        retry = 0
        maxRetries = 3
        while k < len(self.bySymbol.keys()):
            ticker = self.bySymbol.keys()[k]
            try:
                sData = Share(ticker)
                sData.get_avg_daily_volume()
                avgVolume = float(sData.get_avg_daily_volume())
                pVolume = float(sData.get_volume())
                sdVolume = (avgVolume)**0.5
                trendingP = (pVolume - avgVolume)/sdVolume
                trending.append((ticker,trendingP))
                k += 1
            except:
                time.sleep(0.05)
                retry+=1
                if retry >= maxRetries:
                    retry = 0
                    k += 1

        trending.sort(key=lambda x: x[1], reverse = True)
        trending = [s for s in trending if s[1]>0]
        return trending


def getNYSEdata():
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
                NYSEdata.addStock(Symbol,Name,Sector)
            else:
                notFirstRow = True
    return NYSEdata

def getSP500data():
    sp500data = stockScreener()
    with open('sp500.csv', 'r') as csvfile:
        filereader = csv.reader(csvfile)
        notFirstRow = False
        for row in filereader:
            Symbol  = row[0]
            Name  = row[1]
            Sector  = row[2]
            if notFirstRow:
                sp500data.addStock(Symbol,Name,Sector)
            else:
                notFirstRow = True
    return sp500data

def getNASDAQdata():
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
                NASDAQdata.addStock(Symbol,Name,Sector)
            else:
                notFirstRow = True
    return NASDAQdata
