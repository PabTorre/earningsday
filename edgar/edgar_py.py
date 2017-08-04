# -*- coding: utf-8 -*-
"""
Created on Wed Apr 22 10:36:39 2015


This program implements a crawler for the SEC's EDGAR system. 

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



Requirements: 
    Saves data to excel, or pdf formats
    
    Can use DB or csv files to store information about the mapping of edgar
    files. 

    Extract data from a specific section of the files. 
 
Components: 

    EDGAR CRAWLER:
            this program gets the files from edgar.         
        user input: Ticker, date range, selection of files. 
        System maps ticker to CIK code. 
        System gets Files for company
            output: 
                system keeps a folder with the known addresses for each Co. ?
                files organized by folders. 
                files stored in database. 
    
    EDGAR reader: 
        this program digs into the files. 
        Inputs: 
            type of form. 
            sections to extract. 
                # we may need a different method for each form and section?             
    EDGAR writer: 
        writes reports from the information in the files 
            pdf 
            excel
            mysql


Use case/ steps: 

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

EDGAR_CRAWLER.PY seems to be a reasonable starting point for this project. 
@author: ptorre
"""
import re

import xmltodict
import pandas as pd
import urllib2   

class edgar_files():
    """
    this class holds the edgar files for 1 company
    
        
    
    
    """
    def __init__(self, ticker, owner=False):
        """
        initializes the class for a given ticker. 
        
        """
        self._get_index(ticker, owner)
    
    def _get_index(self, ticker, owner=False):
        """
        this method gets the information about the company 
        as well as the filings on record. 
        
        It uses edgar's XML feed. 
        
        """
        #%%
        if __name__ == '__main__':
            ticker = 'GOOG'
            owner=False
        url = 'http://www.sec.gov/cgi-bin/browse-edgar?company=&match=&CIK={0}'
        if owner:
            url +='&owner=include'
        else:             
            url +='&owner=exclude'
        url += '&Find=Find+Companies&action=getcompany&start={1}&count={2}&output=xml'
        
        filings = pd.DataFrame()
        start=0
        count = 100
        while True:
            
            #%
            page = urllib2.urlopen(url.format(ticker, start,count)).read()
            parsed = xmltodict.parse(page)
            if start==0:
                info = pd.DataFrame.from_dict(parsed['companyFilings']['companyInfo']).iloc[0]
            
            if parsed['companyFilings'].has_key('results'):
                results = parsed['companyFilings']['results']['filing']
                for item in results: 
                    filings = filings.append(pd.Series(item), ignore_index=True)
                start += count
            else: 
                break
        #%%
        self.info=info
        self.filings = filings
        # process all the results
        
        


def process_10k():
    """
    process a 10K file. 
    
    """    
    #%%
    from lxml import etree
    from io import StringIO, BytesIO
    #%%
    k10 = 'http://www.sec.gov/Archives/edgar/data/1288776/000128877615000008/0001288776-15-000008-index.htm'
    filing = urllib2.urlopen(k10).read()
    #%%
    filing
    
    #%%
    parser = etree.HTMLParser()#remove_blank_text=True)
    
    html = etree.HTML(filing, parser)
    result = etree.tostring(html, pretty_print=True, method="html")
    #%
    len(result)
    #%%
#def get_cik(ticker):
#    '''
#    get_cik(str)
#
#    this function uses yahoo to translate a ticker into a CIK
#    inputs: 
#        ticker: a ticker for a company listed in the USA exchanges. 
#
#    requirements: 
#        in case ticker is not found print the yahoo url that was used 
#        to screen along with an error message. 
#
#    >>>get_cik('FB')   
#    1326801
#    >>>get_cik('GE')
#    40545
#    >>>get_cik('WRONGTICKER')
#    No CIK found in yahoo.com for WRONGTICKER using 
#    url: http://finance.yahoo.com/q/sec?s=WRONGTICKER+SEC+Filings
#    
#    there are no filings for 'GOOG' available in yahoo or bloomberg. 
#    
#    
#    
#    @credit:
#    this function is based on the code found in:
#        http://quant.stackexchange.com/questions/8099/central-index-key-cik-of-all-traded-stocks
#    
#    
#    '''
#    url = "http://finance.yahoo.com/q/sec?s=%s+SEC+Filings"%(ticker)
#    try:           
#        return int(re.findall('=[0-9]*', 
#                              str(re.findall('cik=[0-9]*', 
#                                             urllib2.urlopen(url).read()
#                                             )[0]))[0][1:])
#    except: 
#        #%% if yahoo doesn't work, default to NASDAQ's page. 
#    
#        #0001288776
#        
#        #url ="http://www.nasdaq.com/symbol/%s/sec-filings"%(ticker)
#        page = urllib2.urlopen(url).read()
#        #%%
#         int(re.findall('=[0-9]*', 
#                              str(re.findall('<cik>[0-9]*</cik>', page)
#                                             )[0]))[0][1:])
#        
#        
#        #%%
#        print "No CIK found in yahoo.com for {0} using \nurl: {1}".format(ticker, url)
        
        
        
        
        
        
        
        
        