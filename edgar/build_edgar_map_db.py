# -*- coding: utf-8 -*-

"""
EDGAR_CRAWLER


This program is designed to extract information from the SEC's EDGAR documents
The objective is to build a software that allows a user to enter a stock
symbol and get fundamental information from the filings made by that company.


### EDGAR
  EDGAR is a web portal where the SEC makes corporate fillings available

  http://www.sec.gov/edgar/quickedgar.htm

### Notes


Searches can be narrowed down by dates.

Types of search supported:


  - FULL text search:
      - goes  over the last 4 years of fillings and attachments.
  - Current Events Analysis:
      - goes over fillings made during the previous week.
      - this allows you for example to search for all 10K (anual)
        or 10Q (quaterly) fillings made in the last week.


### FTP access

  EDGAR supports FTP access

  http://www.sec.gov/edgar/searchedgar/ftpusers.htm

  - To use anonymous FTP to access the EDGAR FTP server, use your
    FTP software to connect to ftp://ftp.sec.gov and
    log in as user "anonymous,"
    using your electronic mail address as the password.

  #### Available Index types:

  Four types of indexes are available:

  - company — sorted by company name

  - form — sorted by form type

  - master — sorted by CIK number

  - XBRL —  list of submissions containing XBRL financial files,
            sorted by CIK number;
            these include Voluntary Filer Program submissions

  Indexes are located in the following folders
    according to time period indexed:

    - /edgar/daily-index — daily index files through the current year;
      previous year folders are available through 1994Q3

    - /edgar/full-index — year folders contain quarterly indexes.
      Full indexes offer a "bridge" between Quarterly and Daily indexes,
      compiling filings for the previous business day through the beginning of
      the current quarter.


  - Feed and Oldloads Folders

  Feed — The Feed directory contains a tar and gzip archive file
        e.g., 20061207.nc.tar.gz;
        nc stands for non-cooked) for each filing day.
        Each filing compressed in the tar is a separate filing submission.



  Created on Wed Jan  8 10:42:51 2014

@author: ptorre
"""

"""
Created on Fri Jan 31 10:28:23 2014


EDGAR



It builds 2 database tables:
    ticker entries for the SEC's CIK codes
    edgar_map -> a table that contains the FTP location of each filing
                as well as some details such as the items contained
                in the filing and the type of filing.


Get 8k Filings from the SEC
User enters ticker, selects 8k filings a system checks that the ticker
belongs to a US listed stock.
 - system queries edgar to get the ticker
system receives RSS file from EDGAR
 - 100 entries per query
 - format = Atom
 - repeat query advancing the starting point until all file
 addresses are obtained
system reads RSS for: a. company info:
 - CIK for stock
 - Industry for stock
     - industry code
     - industry name
 - Stock conformed-name
 - previous names & date of change
b. description of filings:
 - filing date
 - filing type
 - accession number
 - items-desc
 type of filing
 - filing date
system retrives items from FTP site
system process items to extract text
extract the text for the items and make it as clean as possible.
We must look for exhibits and attachments.
process tables
system displays text to user





##############################################################################

Add support for other Electronic EDGAR forms.


##############################################################################
# Add for upgrade:



# IMPORTS
from datetime import datetime
import gzip
from glob import glob
import nucleus as nc

# Imports for URL, FTP and RSS
import feedparser
import re
import pandas as pd
from time import mktime




@author: ptorre
"""





def read_html_files():
    '''
    this function extracts the information from HTML files on the filings.
     OLD VERSION OF THE HTML TABLES READER..
     it takes removes the HTML formatting from the tables.
     we'll keep it around as it may come in handy later.


    change the approach, dont remove all teh HTML tags!! use them!

    '''

def update_edgar_map():
    '''
    this function maintains the edgar map up to date.
    in order to do this it it reads from the current filings RSS
    looking first for
        gets the current map from RSS feed
        process the RSS to extract information
        compares accesions numbers to DB


    why do we need this?

    updating the edgar map from build_edgar_map can be a very slow
    and wasteful process, since most of the downloaded data is later discarted.
    In order to prevent this waste update_edgar_map takes a different approach.
    it doesn't query the edgar db on a per symbol basis, but instead queries
    for all reports of the same type listed chronologically.
    it then goes back through the reports



    get the last date on record for each company.
    then query them for updates since that day.



    '''
    # get the latest timestamp from the db.


    #
    #%%
    print "updating edgar_map"
    missing_cik = open("missing_cik.txt", "a")
    forms = "8-K 6-K F-3 F-10 S-3 S-4 S-8 S-11 8-A 10-12 20-F 40-F 10-Q 10-K".split()
    forms = nc.read_db('SELECT DISTINCT form_type FROM edgar_map;').values.tolist()

    sql_rss = str("http://edgar.sec.gov/cgi-bin/browse-edgar?"+
                  "action=getcurrent&owner=exclude&"
                  "type=%s&start=%s&count=100&output=atom")

def get_new_dates(atom, last_date_in_db):
    '''
    this function checks the date for the last edgar map entry in db, against
    the newly downloaded atom rss feed.
    It removes any duplicates.
    '''

def get_last_stamp_db(cpy_id):
    """
    this fun gets the latest timestamp from DB for a given cpy_id from the
    edgar_map
    """
    sql = "SELECT MAX(edgar_timestamp) FROM edgar_map WHERE cpy_id = %s;"
    stamp = nc.read_db(sql%(cpy_id))
    if len(stamp.dropna()) == 0:
        return pd.datetime(1970,01,01)
    else:
        return stamp.iloc[0,0]
