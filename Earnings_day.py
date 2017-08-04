# -*- coding: utf-8 -*-
"""
Created on Tue Apr 28 10:22:38 2015





Earnings day is a portal that gives forecasts for price movements based
on fundamental analysis of a company's SEC filings.






@author: ptorre
"""

import xmltodict
import pandas as pd
import pandas.io.data as web
import urllib2
import datetime

class edgar_index():
    """
    this class holds the edgar files for 1 company




    """
    def __init__(self, ticker, owner=False):
        """
        initializes the class for a given ticker.

        """
        self.ticker = ticker
        self._get_index(ticker, owner)
        self._get_earning_dates()
        self._get_price_data()
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

    def _get_earning_dates(self):
        """
        this method gets the dates for the 10K and 10Q reports.

        """
        #%%
        match10Q = self.idx.type=='10-Q'
        match10K = self.idx.type=='10-K'
        #%%
        self.earnings = self.idx[match10Q + match10K]
        self.earning_dates = self.earnings.dateFiled
        #%%

    def _get_price_data(self):
        """
        this method gets price data from yahoo.
        """
        #%%
        start = '1900-01-01' # get history going all the way back.
        end = max(self.earning_dates)
        self.ohlc = web.DataReader(self.ticker, 'yahoo', start)#,end)
        self.next_day = self.ohlc.shift(-1)
        #%%

    def _get_earning_day_prices(self):
        """
        this method gets price data for days that had earnings.

        On this prototype we will focus on stocks that deliver earnings
        after the market closes.

        In these stocks we care about the overnight gap in prices
        We are going to correlate it to the close to close move.


        we need to get:
            the closing price on the day of the earnings.
            the opening price on the next day.
                the gap = t1_open - t_close
                the magnitude = max(t1_high- t_close, t_close-t1_low)
                the move = t1_close - t_close

        """
        #%%
        price_list = []

        for date in self.earning_dates:
            t_close = self.ohlc.loc[date].Close
            #
            open_gap  = (self.next_day.loc[date].Open /t_close)-1
            close_move= (self.next_day.loc[date].Close/t_close)-1
            high_move = (self.next_day.loc[date].High / t_close)-1
            low_move  = (self.next_day.loc[date].Low  / t_close)-1
            price_list += [[date, open_gap, close_move, high_move, low_move]]

        price_df = pd.DataFrame(price_list, columns= "date gap toclose tohigh tolow".split())
        price_df.set_index('date', inplace=True)
        #%%
self = edgar_index('MSFT')
