# -*- coding: utf-8 -*-
"""
Created on Wed May  6 12:27:30 2015

@author: ptorre
"""


import fractaltrade as ft
global db
db=ft.fractal_db.fractal_db()

import xmltodict
import pandas as pd
import pandas.io.data as web
import urllib2   
import datetime

class edgar_index():
    """
    this class holds the edgar files for 1 company
    
        
    
    
    """
    def __init__(self, ticker, include_ammend=False):
        """
        initializes the class for a given ticker. 
        
        """
        self.include_ammend=include_ammend
        self.ticker = ticker
        self._get_index(ticker, owner=False)
        self._get_14a()
        

    def _get_index(self, ticker, owner=False):
        """
        this method gets the information about the company 
        as well as the filings on record. 
        
        It uses edgar's XML feed. 
        
        
        we need to get the hour for the filing to check if they were reported
        before, during or after the market.         
            following the link to the report provides a field that states: 
                Accepted
                    2015-04-23 16:09:01
                this can be scrapped. 
                
        >for prototype we will manually choose stocks that report at the close only. 
        
        """
        #%%

        url = 'http://www.sec.gov/cgi-bin/browse-edgar?company=&match=&CIK={0}'
        if owner:
            url +='&owner=include'
        else:             
            url +='&owner=exclude'
        url += '&Find=Find+Companies&action=getcompany&start={1}&count={2}&output=xml'
        #%%
        filings = pd.DataFrame()
        start=0
        count = 100
        while True:
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
        self.idx = filings
        # process all the results
    def _get_14a(self ):
        """
        this method gets the dates for the 10K and 10Q reports. 
        
        """
        #%%
        matchDEF14A = self.idx.type=='DEF 14A'
        if self.include_ammend:
            matchDEFA14A = self.idx.type=='DEFA14A'
            self.DEF14A = self.idx[matchDEF14A + matchDEFA14A]
        else: 
            self.DEF14A = self.idx[matchDEF14A]
        #%%
        



        #%%

if __name__ == "__main__":
    excel_file = pd.ExcelFile('NewTickersProxy.xlsx')
    file_in= excel_file.parse(excel_file.sheet_names[0])
    
    for i in range(len(file_in)):

        
        ticker = file_in.TICKER[i]
        try:
            self = edgar_index(ticker)
            DEF14A = self.DEF14A
            if len(DEF14A) > 0: 
                url = DEF14A.filingHREF.iloc[0]
                date = DEF14A.dateFiled.iloc[0]
                print ticker, date, url
                file_in['PROXY URL'][i] = url 
                file_in['DATE POSTED'][i] = date
        except: 
            print ticker ," not found"
            
            
        
        
        #%%
    file_in.to_csv('file_out.csv')