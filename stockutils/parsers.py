#!/usr/bin/python3

import sys
import os

from stockutils.readers import *

class AssetQuantityRange:
    def __init__(self, startDate, endDate, assets):
        self.startDate = startDate # start of range, incluse
        self.endDate = endDate # start of range, exclusive
        self.quantity = {}
        
        for asset in assets:
            self.quantity[asset] = 0
            
    def __str__(self):
        return "[startDate = {}, endDate = {}, {}".format(self.startDate, self.endDate,
            ["{}: {} ".format(key, self.quantity[key]) for key in self.quantity.keys()])

    def __repr__(self):
        return str(self)

def calculateDailyPortifolioValue(days, assets, assetDayQuantity, stockPrice):
    """
    Calculates the portifolio value for a range of days, given the executed transactions for that 
    period and the daily asset values.
    
    Parameters
    ----------
    days: list
        List of days as strings in "YYYYMMDD".

    assets: list
        List of assets (as strings) present in at least one transaction.
    
    assetDayQuantity: list
        List of AssetQuantityRange, representing quantities for each asset over the period comprehended
        by the days list.
        
    stockPrice: dict
        Dictionary with ticker strings as keys where each entry is a dictionary of prices with days 
        (strings in "YYYYMMDD" format) as keys.
        
    Return
    ----------
    dailyportifoliovalue: dict
        Dictionary of float values. The keys are strings in "YYYYMMDD" format and each value represents
        the portifolio value for that day.
    """
    
    dailyportifoliovalue = {}
    
    firstRun = True
    for adq in assetDayQuantity:
        # calculate days before first transaction
        if firstRun:
            for dayIndex in range(0, days.index(adq.startDate)):
                dailyportifoliovalue[days[dayIndex]] = 0
            firstRun = False

        for dayIndex in range(days.index(adq.startDate), days.index(adq.endDate)):
            sum = 0
            for asset in assets:
                try:
                    qtty = adq.quantity[asset]
                    if qtty is not 0:
                        price = stockPrice[asset][days[dayIndex]]
                        sum += qtty * price
                except:
                    print('error for asset {}, day {}'.format(asset, days[dayIndex]))

            dailyportifoliovalue[days[dayIndex]] = sum

    # calculate last day of dataset
    sum = 0
    for asset in assets:
        qtty = adq.quantity[asset]
        price = stockPrice[asset][days[-1]]
        sum += qtty * price

    dailyportifoliovalue[days[-1]] = sum
    
    return dailyportifoliovalue

def calculateDailyAssetQuantity(days, assets, transactions):
    """
    Calculates quantity of assets over time.
    
    Parameters
    ----------
    days: list
        List of days as strings in "YYYYMMDD".
        
    assets: list
        List of assets (as strings) present in at least one transaction.
    
    transactions: dict 
        Dictionary of lists of transactions. The keys of the dictionary are dates ("YYYYMMDD" format)
        and the lists represents all the transactions for that day.
    
    Return
    ----------
    assetDayQuantity: list
        List of AssetQuantityRange, ordered by crescent date. Each instance of AssetQuantityRange
        represents a fixed quantity of each asset for a given period of time.
    """
    assetDayQuantity = []
    
    transactionDays = [str(d) for d in transactions.keys()]

    # create first entry for days before first transaction
    if len(transactionDays) != 0:
        lastAqr = AssetQuantityRange(days[0], transactionDays[0], assets)
        assetDayQuantity.append(lastAqr)

        for i in range(0, len(transactionDays)):
            aqr = AssetQuantityRange(transactionDays[i], days[-1], assets)
            dayTransactions = transactions[transactionDays[i]]

            if i != len(transactionDays) - 1:
                aqr.endDate = transactionDays[i+1]

            # compute variation of that day
            for t in dayTransactions:
                aqr.quantity[t.ticker] += (t.buyQtty - t.sellQtty)

            # add variation to last value
            for asset in assets:
                aqr.quantity[asset] += lastAqr.quantity[asset]

            assetDayQuantity.append(aqr)
            lastAqr = aqr
            
    return assetDayQuantity

'''
User story: given a specific day and a specific buy transaction of a given ticker, I want to simulate 
what would have happened to my portifolio value over time if I had executed a 
different transaction, i.e., if I had spent the transaction value buying another given asset.
''' 
def differentTickerBuySim(days, assets, stockPrice, transactions, tday, tticker, newticker):
    """
    Simulates a scenario where newticker was bought instead of tticker. The total value spent is kept
    the same as the original transaction, thus the asset quantity may be a non integer value. The 
    value of newticker to be considered will be the day closing value.
    
    Parameters
    ----------
    days: list
        List of days as strings in "YYYYMMDD".

    assets: list
        List of assets (as strings) present in at least one transaction.
    
    stockPrice: dict
        Dictionary with ticker strings as keys where each entry is a dictionary of prices with days 
        (strings in "YYYYMMDD" format) as keys.
        
    transactions: dict 
        Dictionary of lists of transactions. The keys of the dictionary are dates ("YYYYMMDD" format)
        and the lists represents all the transactions for that day.
    
    tday: str
        Date string in "YYYYMMDD" format, representing the day where the given transaction will be 
        altered.
        
    tticker: str
        Ticker whose buying transactions on the tday date will be altered.
        
    newticker: str
        Ticker that will replace all tticker transactions on tday date.
        
    Return
    ----------
    newdailyportifoliovalue: dict
        Dictionary of float values. The keys are strings in "YYYYMMDD" format and each value represents
        the portifolio value for that day.
    """
    
    newtransactions = transactions.copy()
    
    if tday not in transactions:
        return None
    
    # alter tday transactions relative to tticker
    tdaytransactions = transactions[tday]
    for t in tdaytransactions:
        if t.ticker == tticker:
            t.ticker = newticker
            tamount = t.buyQtty * t.buyPrice
            t.buyPrice = stockPrice[newticker][tday]
            t.buyQtty = tamount / t.buyPrice
    
    newAssetDayQuantity = calculateDailyAssetQuantity(days, assets, newtransactions)

    for newadq in newAssetDayQuantity:
        print(newadq)
    
    newdailyportifoliovalue = calculateDailyPortifolioValue(days, assets, newAssetDayQuantity, stockPrice)

    return newdailyportifoliovalue