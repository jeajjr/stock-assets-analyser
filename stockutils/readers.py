#!/usr/bin/python3

import sys
import os

class Transaction:
    """
    Single transaction data placeholder.
    """

    def __init__(self, ticker='', date='', buyQtty=0, sellQtty=0, buyPrice=0.00, sellPrice=0.00):
        """Class constructor"""
        self.ticker = ticker
        self.date = date
        self.buyQtty = buyQtty
        self.sellQtty = sellQtty
        self.buyPrice = buyPrice
        self.sellPrice = sellPrice

    def __str__(self):
        return "[ticker = {}, date = {}, buyQtty = {}, sellQtty = {}, \
buyPrice = {:.2f}, sellPrice = {:.2f}]".format(self.ticker, self.date,
        self.buyQtty, self.sellQtty, self.buyPrice, self.sellPrice)

class IBOVDayData:
    """
    Single day IBOV data placeholder.
    """
    
    def __init__(self, opening=0, closing=0, variation=0.00, minimum=0, maximum=0, volume=0):
        """Class constructor"""
        self.opening = opening
        self.closing = closing
        self.variation = variation
        self.minimum = minimum
        self.maximum = maximum
        self.volume = volume

    def __str__(self):
        return "[opening = {}, closing = {}, variation = {}, minimum = {}, \
maximum = {:.2f}, volume = {:.2f}]".format(self.opening, self.closing,
        self.variation, self.minimum, self.maximum, self.volume)

class B3HistoryImporter:
    """ Set of methods to deal with raw stock history files from B3

    Contains methods for reading, parsing and caching stock history data.
    Input raw data files are expected to be as defined in B3 (Brazilian stock
    exchange) website.
    """

    def __init__(self, assets, inputdir):
        """Class constructor
       
        Sould receive the list of assets the user. Only data for the specified
        assets will be processed from the input raw data files."""

        # assets related data
        self.__assetNames = assets
        self.__assetData = {}
        for asset in self.__assetNames:
            self.__assetData[asset] = {}

        # input files directory
        self.inputdir = inputdir

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
        with os.scandir(path=self.inputdir) as it:
            for entry in it:
                if not entry.name.startswith('.') and entry.name.startswith('COTA') and entry.is_file():
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
            with open(os.path.join(self.inputdir, file)) as f:
                for line in f:
                    for asset in self.__assetNames:
                        if asset in line:
                            ticker, date, avgPrice = self.parseRawInputLine(line)

                            # a given ticker in the canonical format (say ABEV3,
                            # BPAC11) may have variations, such as the fractional
                            # market (ABEV3F, BPAC11F). Discard if is a different
                            # variation
                            if asset == ticker:
                                self.__assetData[ticker][date] = avgPrice

    def getTickerData(self, ticker):
        """Returns data for specified ticker. Return type is a dictionary with
        dates as keys."""

        if ticker not in self.__assetData:
            print("No data for ticker", ticker)
            return None
       
        return self.__assetData[ticker]

class UserDataImporter:
    """ Set of methods to deal with user data

    Contains methods for reading, parsing and caching user stock transaction
    history data. Input raw data files are expected to be in the following format:
    - ASCII text file
    - one transaction per line
    - each line should have the following data in the specified order, separated
        by spaces or tabs:
        1. Ticker
        2. Date (YYYY-MM-DD format)
        3. Buy quantity
        4. Sell quantity
        5. Buy average price (with or without leading $)
        5. Sell average price (with or without leading $)
    """

    def __init__(self, inputdir):
        """Class constructor"""

        # input files directory
        self.inputdir = inputdir

    def listUserInputFiles(self):
        """Returns list of files under user input files directory."""

        files = []
        with os.scandir(path=self.inputdir) as it:
            for entry in it:
                if not entry.name.startswith('.') and entry.is_file():
                    files.append(entry.name)

        return files

    def parseUserInputLine(self, line):
        """Receives a line from a user input file and returns its parsed data as
        a Transaction instance."""
       
        t = Transaction()
        tokens = line.split()

        t.ticker = tokens[0]
        t.date = tokens[1]
        t.buyQtty = tokens[2]
        t.sellQtty = tokens[3]
        t.buyPrice = float(tokens[4].lstrip('$'))
        t.sellPrice = float(tokens[5].lstrip('$'))

        return t

    def getUserInputData(self):
        """Read all user input files, parses their data and return a list of
        transactions."""

        transactions = []
        for file in self.listUserInputFiles():
            with open(os.path.join(self.inputdir, file)) as f:
                for line in f:
                    transactions.append(self.parseUserInputLine(line))

        return transactions

class IBOVHistoryImporter:
    """ Set of methods to deal with IBOV history files

    Contains methods for reading, parsing and caching IBOV history data. Files
    should be named IBOV*, and be a CSV with fields:
    "date","opening","closing","variation","minimum","maximum","volume"
    """

    def __init__(self, inputdir):
        """Class constructor
       
        Should receive directory where IBOV data CSV files will be.
        """

        # input files directory
        self.inputdir = inputdir

    def listIBOVInputFiles(self):
        """Returns list of files under raw input files directory."""

        files = []
        with os.scandir(path=self.inputdir) as it:
            for entry in it:
                if not entry.name.startswith('.') and entry.name.startswith('IBOV') and entry.is_file():
                    files.append(entry.name)

        return files

    def parseIBOVInputLine(self, line):
        """Receives a content line from a IBOV input file and returns its parsed data."""
       
        line = line.strip('\n')
        lineTokens = [p.strip('"') for p in line.split(',')]

        dateParts = lineTokens[0].split('/')
        date = "{}{}{}".format(dateParts[2], dateParts[1], dateParts[0])

        idd = IBOVDayData()
        try:
            idd.opening = int(lineTokens[1].replace('.', ''))
        except:
            pass

        try:
            idd.closing = int(lineTokens[2].replace('.', ''))
        except:
            pass

        try:
            idd.variation = float("{}.{}".format(lineTokens[3], lineTokens[4]))
        except:
            pass

        try:
            idd.minimum = int(lineTokens[5].replace('.', ''))
        except:
            pass

        try:
            idd.maximum = int(lineTokens[6].replace('.', ''))
        except:
            pass

        
        #dicEntry[self.VOLUME] = lineTokens[6].replace('.', '')

        return date, idd 

    def readAndParseIBOVInputFile(self):
        """Read all IBOV input files and parses data for the specified assets upon
        class instance creation.
       
        Return a dictionary within another dictionary, where data is accessed like:
        result[DATE][PARAMETER], where:
        - DATE is in "YYYY-MM-DD" format
        - PARAMETER is one of the following:
            - IBOVHistoryImporter.OPENING
            - IBOVHistoryImporter.CLOSING
            - IBOVHistoryImporter.VARIATION
            - IBOVHistoryImporter.MINIMUM
            - IBOVHistoryImporter.MAXIMUM
            - IBOVHistoryImporter.VOLUME
        """

        result = {}

        for file in self.listIBOVInputFiles():
            firstLine = True
            with open(os.path.join(self.inputdir, file)) as f:
                for line in f:
                    if firstLine:
                        firstLine = False
                        pass
                    else:
                        date, idd = self.parseIBOVInputLine(line)
                        result[date] = idd

        return result
