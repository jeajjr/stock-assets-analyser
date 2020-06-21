#!/bin/python3

import sys
import os

'''
Expected directory history:

.
|
 - raw-input: raw stock history files downloaded from B3 website
 - user-input: user purchase history file location
 - cache: cache storage
'''

class B3HistoryImporter:
    """ Set of methods to deal with raw stock history files from B3

    Contains methods for reading, parsing and caching stock history data.
    Input raw data files are expected to be as defined in B3 (Brazilian stock
    exchange) website.
    """

    

    def __init__(self, assets):
        """Class constructor"""

        # directories names
        self.__RAW_INPUT_DIRECTORY = 'raw-input'
        self.__USER_INPUT_DIRECTORY = 'user-input'
        self.__CACHE_DIRECTORY = 'cache'

        # assets related data
        self.__assetNames = assets
        self.__assetData = {}
        for asset in self.__assetNames:
            self.__assetData[asset] = {}

        # raw input (RI) file constants
        self.__RI_REG_DATE_START = 2
        self.__RI_REG_DATE_END = 10
        self.__RI_REG_TICKER_START = 12
        self.__RI_REG_TICKER_END = 24
        self.__RI_REG_AVG_PRICE_START = 95
        self.__RI_REG_AVG_PRICE_END = 108


    def listRawInputFiles(self):
        """Returns list of files under raw input files directory."""
        
        files = []
        with os.scandir(path=self.__RAW_INPUT_DIRECTORY) as it:
            for entry in it:
                if not entry.name.startswith('.') and entry.is_file():
                    files.append(entry.name)

        return files

    def parseRawInputLine(self, line):
        """Receives a line from a raw input file and returns its parsed data."""
        
        ticker = str.strip(line[self.__RI_REG_TICKER_START:self.__RI_REG_TICKER_END])
        date = line[self.__RI_REG_DATE_START:self.__RI_REG_DATE_END]
        avgPrice = int(line[self.__RI_REG_AVG_PRICE_START:self.__RI_REG_AVG_PRICE_END]) / 100

        return (ticker, date, avgPrice)

    def readAndParseRawInputFile(self):
        """Read all raw input files and parses data for the specified assets upon
        class instance creation."""

        for file in self.listRawInputFiles():
            with open(os.path.join(self.__RAW_INPUT_DIRECTORY, file)) as f:
                for line in f:
                    for asset in self.__assetNames:
                        if asset in line:
                            ticker, date, avgPrice = self.parseRawInputLine(line)
                            self.__assetData[ticker][date] = avgPrice

    def getTickerData(self, ticker):
        """Returns data for specified ticker. Return type is a dictionary with
        dates as keys."""

        if ticker not in self.__assetData:
            print("No data for ticker", ticker)
            return None
        
        return self.__assetData[ticker]

def main():
    print('Starting...')

    assetsList = ['BPAC11F']
    
    hi = B3HistoryImporter(assetsList)
    hi.readAndParseRawInputFile()

    print(hi.getTickerData(assetsList[0]))

if __name__== "__main__":
    main()
