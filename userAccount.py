# -*- coding: utf-8 -*-
# userAccount.py
"""
Version: 4.18.2015
@author: Luke_Wortsmann
"""
import datetime as dt
from yahoo_finance import Share

class userAccount:
    def __init__(self,newuserName,email,newfirstName,newlastName,encrypPass):
        private self.userEmail = email
        self.userName = newuserName
        self.firstName = newfirstName
        self.lastName = newlastName
        self.password = encrypPass
        self.accountData = AssetsHeld()
        self.accountData.addCash(100000.)

    def changePassword(self,oldPass,newPass,newPassConfirm):
        if self.password == oldPass:
            if newPass == newPassConfirm:
                self.password = newPass
            else:
                print "Error: Passwords do not match."
                break
        else:
            print "Wrong password, please try again."

    def purchaseAsset(self,asset,amount):
        self.accountData.buyAsset(asset,amount)

    def StocksOwned(self):
        owned = {}
        for asset in self.accountData.trades:
            amount = 0
            value = 0
            netValue = 0
            spent = 0
            for trade in self.accountData.trades[asset]:
                amount += trade.amountHeld
                value += trade.currentValue
                netValue += (trade.currentValue - trade.purchaseValue)
                spent += trade.purchaseValue
            if amount != 0:
                owned[asset] = (amount,value,netValue,spent)
        return owned

    def percentReturn(self):
        owned = self.StocksOwned()
        gains = 0
        spent = 0
        for stock in owned:
            gains += owned[stock][1]
            spent += owned[stock][3]
        percentReturn = (1.0 - (gains/spent))*100.0
        self.pReturn = percentReturn
        return percentReturn

class AssetsHeld:
    def __init__(self):
        self.trades = {}
        self.cash = 0
        self.purchaseValue = 0
        self.valueOfAssets

    def addCash(self, amount):
        self.cash += amount

    def buyAsset(self,asset,amount):
        value = (asset.getPrice()*amount)
        if value > self.cash:
            print "Insufficent Funds"
        else:
            self.cash -= value
            self.purchaseValue += value
            thisTrade = Trade(asset,amount)
            if asset.ticker in self.trades:
                self.trades[asset.ticker].append(thisTrade)
            else:
                self.trades[asset.ticker] = [thisTrade]

    def sellAsset(self,asset,amount):
        if asset.ticker in self.trades:
            totalHeld = 0
            for trade in self.trades[asset.ticker]:
                totalHeld += trade.amountHeld
            if totalHeld < amount:
                print "Quantity Error"
            else:
                ind = 0
                while amount >= 0 and i < len(self.trades[asset.ticker]):
                    amount = self.trades[asset.ticker][i].sell(amount)
                    i += 1;
                self.cash += amount*asset.getPrice()
        else:
            print "Error: Asset not held"

    def recalculateValue(self):
        newValue = 0
        for assetHeld in self.trades:
            newValue += assetHeld[0].getPrice()
        self.valueOfAssets = newValue
        return newValue + self.cash


def Asset:
    def __init__(self,newticker):
        self.ticker = ticker


    def getPrice(self):
        # return current price
        stock = Share(self.ticker)
        try:
            price = float(stock.get_price())
            return price
        except:
            print "ERROR: Invalid Asset"
            return

    def getTime(self):
        currentTime = dt.datetime.now()
        return currentTime

class Trade:
    def __init__(self,asset,amount):
        self.asset = asset
        self.purchasePrice = asset.getPrice()
        self.amountBought = amount
        self.amountHeld = amount
        self.assetName = asset.ticker
        self.purchaseValue = amount*self.purchasePrice
        self.currentValue = amount*asset.getPrice()

    def sell(self,amount):
        if amount <= self.amountHeld:
            self.amountHeld -= amount
            return 0
        if amount > self.amountHeld:
             amount -= self.amountHeld
             self.amountHeld = 0
             return amount

def LeaderBoard(dataBase, byReturn = True):
    if byReturn:
        leaders = sorted(dataBase, key = lambda x: x.accountData.percentReturn())
        disp = [(user.userName,user.accountData.percentReturn()) for user in leaders]
    else:
        leaders = sorted(dataBase, key = lambda x: x.accountData.recalculateValue())
        disp = [(user.userName,user.accountData.recalculateValue()) for user in leaders]

    return disp
