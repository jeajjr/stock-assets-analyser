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

    

    def __init__(self):
        """Class constructor"""

        self.__RAW_INPUT_DIRECTORY = 'raw-input'
        self.__USER_INPUT_DIRECTORY = 'user-input'
        self.__CACHE_DIRECTORY = 'cache'

    def listRawInputFiles(self):
        """Returns list of files under raw input files directory"""
        files = []
        with os.scandir(path=self.__RAW_INPUT_DIRECTORY) as it:
            for entry in it:
                if not entry.name.startswith('.') and entry.is_file():
                    files.append(entry.name)

        return files

def main():
    print('Starting...')

    hi = B3HistoryImporter()
    print(hi.listRawInputFiles())

if __name__== "__main__":
    main()
