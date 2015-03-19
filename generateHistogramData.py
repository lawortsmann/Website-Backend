# -*- coding: utf-8 -*-
# generateHistogramData.py

"""
Version: 03.18.2015

A function that returns data to plot a smooth histogram of the stock price for
the previous year. Provided with sample plotting code.

@author: Luke_Wortsmann
"""

import datetime as dt
import numpy as np
from yahoo_finance import Share
from scipy.interpolate import spline
# Only needed for plotting:
import matplotlib.pyplot as plt

def gatherHistogramData(stockName, pastXdays=365, bin0=15, returnCurrent = True):
    """
    Takes a stock ticker as a string, returns an array containing:
    * X-axis values or the stock price
    * Y-axis values that are unitless and normed
    * An array containing the points of a line at the current stock price, provided
        returnCurrent is True.
    """
    # Get date range:
    today = dt.date.today()
    oneYear = dt.timedelta(days = pastXdays)
    today-oneYear
    d2 = today.isoformat()
    d1 = (today-oneYear).isoformat()

    # Get stock data:
    stock = Share(stockName)
    importedData = stock.get_historical(d1, d2)
    closeData = [float(dateSet['Adj_Close']) for dateSet in importedData]

    # Build histogram:
    bD = np.histogram(closeData, bins = bin0, normed=True)
    xMids = np.array([((bD[1][k]+bD[1][k+1])/2.0) for k in xrange(len(bD[1])-1)])
    deltaX =(xMids[1] - xMids[0])/2.0

    # Build Spline:
    xNew = np.linspace(xMids.min(),xMids.max(),100)
    yNew = spline(xMids,bD[0],xNew)

    # Add endpoints:
    yNew = np.insert(yNew,0,0)
    yNew = np.insert(yNew,yNew.shape[0],0)
    xNew = np.insert(xNew,0,xNew[0]-deltaX)
    xNew = np.insert(xNew,xNew.shape[0],xNew[-1]+deltaX)

    # Get current/return
    if returnCurrent:
        currentP = float(stock.get_price())
        minval = min(enumerate(xNew),key = lambda x: abs(x[1] - currentP))[0]
        ycurrent = yNew[minval]
        currentVal = [[currentP,currentP],[0,ycurrent]]
        return [list(xNew),list(yNew),currentVal]
    else:
        return [xNew,yNew]

# Basic example of concept:
histData = gatherHistogramData('goog')
plt.plot(histData[2][0],histData[2][1],linewidth = 3.0,color='darkblue')
plt.plot(histData[0],histData[1],linewidth = 5.0,color='black')
# Turn off y-axis
frame1 = plt.gca()
frame1.axes.get_yaxis().set_visible(False)
plt.xlabel('Stock Price')
plt.show()
