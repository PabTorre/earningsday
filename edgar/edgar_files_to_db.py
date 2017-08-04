# -*- coding: utf-8 -*-
"""
Created on Mon Feb  3 13:52:09 2014


This program handles the filing files from the EDGAR FTP. 

For now our focus is on the 8-K filings. 

It requires the database to have a map of EDGAR's files built by the 
edgar_map_from_rss program. 


it must prepare the data for human consumption. 
    -> we will prepare the data for machine consumption on a later version. 
    



This program will: 
    1. download the filings in txt format from FTP 
    2. read the files to extract:
        tables representing financial statements
        text statements
        references to dates

requirements: 
    must have specific handlers for each type of form 8-k filing. 
    





NEW ANGLE  ####################################################################


'''


@author: ptorre
"""
## IMPORTS
#from datetime import datetime
#import gzip
#from glob import glob
import nucleus as nc

# Imports for URL, FTP and RSS
from ftplib import FTP
import feedparser
import re
import pandas as pd
# HTML Parsers
from lxml import etree, html
from lxml.html.clean import clean_html
    
#%%
### FUNCTIONS FOR GETTING THE FTP FILES

def edgar_connect():
    ' This is a generic function to establish a connection with the edgar FTP '
    ftp = FTP('ftp.sec.gov')
    ftp.login(user='anonymous', passwd='pablo@fractalsoft.biz')
    # get to the folder containing all the indexes. 
    return ftp

def get_filings_db(ticker, item, start_day):
    '''
    this function retrieves the filings from edgar FTP. 
    inputs: 
        ticker -> a valid US ticker symbol. 
        item -> the type of item requested by the user. 
        start_day -> the oldest day to include ftp query 
    output:     
        function writes into DB. 
    
    Function gets ftp addresses from DB. 
    if not found, then it calls ed_rss.build_8k_map()
    
    retrictions: 
        function must check if files already exist in DB before downloading. 
            key: edgar_map.edgar_ftp
            
        ticker must be in BTRD format    
        ticker must belong to a US stock. 
    
    
    '''
    break




##########
def get_filings(files_8k):
    '''
    This function gets an html file from db. 
    eliminate 8k_files... the only input will be a ticker. 
        -> all details come from DB. 
        
    
    We need to: 
        1. Extract tables from the filings
        2. find the tables that contain table data and remove them 
            from the file        
        3. remove html formatting on the remaining file
        4. save everything in the DB. 
        
        

    '''
    # get all the files that have the same ftp address:
    for path in files_8k.ftp.drop_duplicates():    
        item_list = list(files_8k[files_8k.ftp == path].item.values)
        print path
        #
        # financial statements are found on items:
        # 7.01, 9.01, 2.01 - 2.06
        #
        ftp=edgar_connect()
        ftp.retrbinary("RETR "+path, open("filing.html", 'wb').write)
        tables = get_html_tables()
        ## make 2 buckets. 
        fin_stat = []
        for table in tables: 
            #            if len(table) < 3:
            #                #'tables with len == 1 are raw text'
            #                # get the table location in the html
            #                # once you have all locations, cut them from html
            #                # into a new html file. 
            #                #
            
            if len(table) > 10: 
                #these are financial statements
                # we must process them separately
                fin_stat += [table]
        ## Do we need the code below? what for? when do we use a table and when
        ## do we use the unformated text? 

        
        tree = clean_html(etree.parse("filing.html", html.HTMLParser()))
        clean_text =  tree.getroot().text_content()
        
        # first build a dirty version of the lists, which has newline characters
        locations = []
        for item in item_list: 
            locations += [clean_text.index(item)]
        locations += [len(clean_text)]
        # find attachments
        # this filings is a very weak approach        
        filings = {}
        for i in range(len(item_list)): 
            filings["item %s"%(item_list[i])
            ] = clean_text[locations[i]:locations[i+1]]
        
        #####  WE NEED TO AGGREGATE THE RESULTS INTO A DB OR FILE. 
    return filings, fin_stat, tables
        # we need functions to process each filing item     
#



def get_html_tables():
    '''
    this function gets html tables into a pd.dataframe
    '''
    html_str = open("filing.html", 'r').read()
    tables = pd.io.html.read_html(html_str, infer_types=False, 
                                  flavor='html5lib')
    return tables