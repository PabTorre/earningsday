# -*- coding: utf-8 -*-
# <nbformat>3.0</nbformat>

# <markdowncell>

# ## Project Description
# 
# User requires a system that finds fundamental data on a stock from different sources, particularly from EDGAR fillings. 
# 
# 
# ##User Requirements: 
# 
# - [8:44:32 PM]  J: just a quick q
# - [8:44:41 PM]  J: how difficult would it be, to create a bot, that scans edgar filings
# - [8:44:52 PM]  J: for the words "shares" "warrants" "exercised" etc.
# - [8:45:38 PM]  J: 8-k and 10-Q filings with the sec
# - [8:45:51 PM]  J: so lets say i wake up, i see stock XYZ is up 25%
# - [8:45:54 PM]  J: i say, oh wow nice, good news
# - [8:46:02 PM]  J: i input stock name XYZ into pablo bot
# - [8:46:04 PM]  J: edgar bot tells me:
# - [8:46:15 PM]  J: 1,900,000 warrants come exerciseable today (or tomorrow)
# - [8:46:24 PM]  J: float has increased marginally last month
# - [8:46:29 PM]  J: or blah blah blah blah
# - [8:46:47 PM]  J: basically ive gotten fucking raped this year for at least 50,000$ buying stocks with news
# - [8:47:06 PM]  J: and had i read the filings, i'd have known that there was a group of inviduals exercising, or dumping stock right around the news
# 
# 
# ### Use Case: 
# user enters stock symbol
# system displays fundamental info: 
# 1,900,000 warrants come exerciseable today (or tomorrow)
# float has increased marginally last month
# 
# ### recent case example to find:
# 
# - WPCS
# - "the company had  (?) shares"
# - "common stock"
# - "deemed issued and outstanding"
# - "conversion notices"
# - "upon the conversion"
# - "convertible notes issued"
# - "unregistered sales of equity securities"
# - "issue an aggregate"
# - "sc-13g" (this is a huge alert, no matter what/when/why/how
# - "[x] Rule 13d-1c"
# - "number of shares"
# - "percent of class"

# <markdowncell>

# ## Resources

# <markdowncell>

# ### EDGAR
# EDGAR is a web portal where the SEC makes corporate fillings available 
# 
# http://www.sec.gov/edgar/quickedgar.htm
# 
# ### Notes
# the SEC uses a company code called CIK which uniquelly identifies companies in their system. 
# We should include this code in our DB, since it is necessary to navigate through the filings in FTP mode. 
# 
# http://www.sec.gov/edgar/NYU/cik.coleft.c
# 
# They Also support queries based on SIC codes (these are codes that identify industries) 
# example, if you enter 7370 in the SIC box, you'll retrieve all SEC-registered companies that fall into the Standard Industrial Classification known as "Services-Computer Programming, Data Processing, Etc."
# 
# Searches can also be narrowed down by dates. 
# 
# Types of search supported: 
# 
# 
# - FULL text search:
#     - goes  over the last 4 years of fillings and attachments. 
# - Current Events Analysis: 
#     - goes over fillings made during the previous week. 
#     - this allows you for example to search for all 10K (anual) or 10Q (quaterly) fillings made in the last week. 
# ### FTP access
# 
# EDGAR supports FTP access
# 
# http://www.sec.gov/edgar/searchedgar/ftpusers.htm
# 
# - To use anonymous FTP to access the EDGAR FTP server, use your FTP software to connect to ftp://ftp.sec.gov and log in as user "anonymous," using your electronic mail address as the password.
# 
# #### Available Index types: 
# 
# Four types of indexes are available:
# 
# - company — sorted by company name
#  
# - form — sorted by form type
#  
# - master — sorted by CIK number
#  
# - XBRL — list of submissions containing XBRL financial files, sorted by CIK number; these include Voluntary Filer Program submissions
# 
# Indexes are located in the following folders according to time period indexed:
# 
# - /edgar/daily-index — daily index files through the current year; previous year folders are available through 1994Q3 
# 
# - /edgar/full-index — year folders contain quarterly indexes. Full indexes offer a "bridge" between Quarterly and Daily indexes, compiling filings for the previous business day through the beginning of the current quarter.
# 
# 
# - Feed and Oldloads Folders
# 
# Feed — The Feed directory contains a tar and gzip archive file (e.g., 20061207.nc.tar.gz; nc stands for non-cooked) for each filing day. Each filing compressed in the tar is a separate filing submission.
# 
# ### RSS feeds for interactive fillings
# not necessarily immediatly but worth taking a look later to add real time alerts. 
# 
# - http://www.sec.gov/spotlight/xbrl/filings-and-feeds.shtml
# 
# SEC also supports interactive files with their XBLR format
# - http://xbrl.sec.gov/

# <markdowncell>

# ## Filings
# 8-K -> these indicate significant events. 
# everything from a change in CEO to bankrupcy must be disclosed on an 8k. 
# http://en.wikipedia.org/wiki/Form_8-K
# 
# 
# the items inside the 8k filling have codes that indicate the type of information contained. 
# 
# http://www.sec.gov/answers/form8k.htm
# 
#  - make an interface that allows the user to choose the type of items for the queries. 
#  
#  we will use item 3.02 for our examples. 
#  
#  
#  The fillings are indexed using the CIK codes, so we need to add those to DB. 
#  
#  

# <markdowncell>

# ## Steps to perform query. 
# ### for historical data
# 
# 1. connect to SEC FTP
# 2. get master index
# - 
#     - build a large index with all historic filings
#     - this will allow us to use the event profiler on this data. 
# 
# 
# ## Further Reading. 
# 
# 
# - http://www.elsevier.pt/en/revistas/the-spanish-review-of-financial-economics-332/artigo/crawling-edgar-90140298
# 
# - http://stackoverflow.com/questions/13504278/parsing-edgar-filings

# <markdowncell>

# # Project Goals
# 
# 
# we are interested in the Form 8-K filings. these indicate a variety of significant events that are disclosed by companies to the market. 
# http://en.wikipedia.org/wiki/Form_8-K
# 
# The 8-K filings are divided into Items. These items indicate the type of information contained in the 8-K 
# http://www.sec.gov/answers/form8k.htm
# 
#  
# For this example we will focus on event item 3.02. On the production version we will allow the user to choose the filings to search. 
#  
# The fillings are indexed using the CIK codes, for this example we will use a fixed CIK code, for the production version we will map the tickers to the CIK code through the company name. 
# 
# 
# 
# ## Retrieving the data
# 
# EDGAR provides FTP access to all of their files. 
# There are over 13 million filings available in their site, so downloading them all is not practical for now. 
# They also provide a "masters" file that contains an index of all the filings in the FTP. 
# We will download the complete index from EDGAR and use it to provide search options to the user. 
# This masters file can be updated using daily update files, also provided by the EDGAR FTP site. 
# 
# ## Processing the data. 
# 
# The data from EDGAR is not tidy, it comes in HTML format that is not suitable for machine reading out of the box. 
# In order to process the data, we: 
#     1. cleaned the document to remove all HTML tags and leave only the content. 
#     2. used regex to extract the item names contained in each form. 
#     3. used regex to extract the full text of each item. 
#     4. index the full text to the item name into database. 
# ## Displaying the results.
# 
# For our first version we will display the results as formated text so the user can extract the content out of the filings and read only the items that he is interested in reading. 
# 
#  

# <codecell>

# Imports
from ftplib import FTP
import re
import urllib2
from datetime import datetime
import pandas as pd
import gzip
from glob import glob
from lxml import etree, html
from lxml.html.clean import clean_html
import urllib2

# <markdowncell>

# ## Step 1. Get the data from SEC-EDGAR into a folder (db later) 
# Scripts to Download the indices from EDGAR to a local directory. 

# <codecell>

def manage_edgar_masters(): 
    '''
    this program controls the edgar masters. 
    it checks if db has edgar masters available. 
            if not: get_all_edgar_masters()
            if yes: gets the last_day and runs update_edgar_masters(last_day)
    
    '''
    
def masters_to_db():
    '''
    this function feeds the EDGAR masters to the DB
    it processes the output of get_all_edgar_masters 
    and update_edgar_masters and inserts it into pgsql
    
    db structure: 
    
    CREATE TABLE IF NOT EXISTS EDGAR_MASTERS(
    idx SERIAL NOT NULL,
    cik INT NOT NULL,
    name VARCHAR(256) NOT NULL,
    form_type VARCHAR(32) NOT NULL,
    path VARCHAR(256) NOT NULL);
    
    '''
def get_all_edgar_masters():
    '''
    This program crawls through the SEC FTP site and gets all the historic master files. 
    It is meant to run once when the system is installed. 
    
    '''
    ftp = FTP('ftp.sec.gov')
    ftp.login(user='anonymous', passwd='pablo@fractalsoft.biz')
    # get to the folder containing all the indexes. 
    ftp.cwd('/edgar/full-index')
    # get a list of the years available for download
    years = re.findall('[0-9][0-9][0-9][0-9]', str(ftp.nlst()))
    for year in years:
        ftp.cwd('/edgar/full-index/%s' %(year))
        # get a list of the quaters available for download. 
        quater_list = re.findall('QTR[0-9]', str(ftp.nlst()))
        for quater in quater_list: 
            filename = 'masters/%s_%s_master.gz'%(year, quater)
            try: 
                # download the all the files to a local folder. 
                ftp.retrbinary("RETR /edgar/full-index/%s/%s/%s"%(year, quater,'master.gz'), open(filename, 'wb').write)
            except Exception as e:
                print e

                
                
def update_edgar_masters(start_day): 
    '''
    This program updates the filings from the SEC site. 
    it is meant to run on a daily basis
    it takes as input the last_day found on the DB for the EDGAR masters. 
    it then gets all updates since that day using the daily folder. 
    then updates from the SEC site with all the dates since (including the last date)
    
            
    
    '''
    ftp = FTP('ftp.sec.gov')
    ftp.login(user='anonymous', passwd='pablo@fractalsoft.biz')
    # get the latest index file
    ftp.cwd('/edgar/daily-index')
    files = re.findall('master.[0-9]*.[0-9].idx', str(ftp.nlst()))
    dates = re.findall('[0-9][0-9]*', str(files))
    day_list = pd.Series(files, index = [datetime.strptime(day, '%Y%m%d') for day in dates])
    for day in day_list[day_list > start_day]: 
        ftp.retrbinary("RETR /edgar/daily-index/%s"%(day), open('masters/'+day, 'wb').write)

# <markdowncell>

# ## Step 2. Read the files. 
# 
# 
# 
# The index files name
# masters/master.YYYYMMDD.z

# <codecell>

def get_filings(name, cik, verbose=True):
    '''
    this function gets a list of files from the SEC FTP
    '''
    # connect to the SEC FTP
    ftp = FTP('ftp.sec.gov')
    ftp.login(user='anonymous', passwd='pablo@fractalsoft.biz')
    # check the filings files already downloaded
    existing_files = glob("filings/*.html")
    # create a name for the target file
    target_name = str(cik)+'-'+name[:-3]+"html" 
    # check that the file is not already created
    if "filings/"+target_name not in existing_files:
        if verbose: print 'processing %s'%(target_name)
        print cik
        ftp.cwd('/edgar/data/%s/'%(cik))
        if verbose: print name[i]
        ftp.retrbinary("RETR %s"%(name[i]), open("filings/"+target_name, 'wb').write)
    else:
        if verbose: print target_name + " already exists"
    return target_name


def html_cleaner(html_file):
    '''
    this function removes the tags from an HTML leaving only the content
    !!!!instead of removin the tags, use them! 
    
    '''
    tree = etree.parse(html_file, html.HTMLParser())
    tree = clean_html(tree)
    clean_text =  tree.getroot().text_content()
    # first build a dirty version of the lists, which has newline characters
    items_list = re.findall("\n [ ]*Item [0-9][0-9. ]*",clean_text)
    items_list += re.findall("\nItem [0-9][0-9. ]*",clean_text)
    items_list += re.findall("\nITEM [0-9][0-9. ]*",clean_text)
    items_list += re.findall("\n [ ]*ITEM [0-9][0-9. ]*",clean_text)
    # exhibits are included under item 9.01
    # use the dirty version to build a list of locations in the file. 
    locations = []
    for item in items_list: 
        locations += [clean_text.index(item)]
    
    # add the ending point for Exhibits, where the About Co section start. 
    locations += [len(clean_text)]
    # clean the items list
    
    name_list = re.findall( 'item [0-9.][0-9. ]*', str(items_list).lower())
    filings = {}
    for i in range(len(name_list)): 
        name = name_list[i]
        filings[name] = clean_text[locations[i]:locations[i+1]]
    
    return filings


def process_8k(ticker="WPCS", verbose=True):
    '''
    this function processes 8k fillings. 
    inputs: 
        masters: pd DataFrame containing the information of the fillings masters from the SEC EDGAR site. 
        cik: CIK indentifier for an issuer. 
    '''
    cik = get_cik(ticker)
    # get the masters file
    masters= masters_to_pd(cik=cik)
    # Get the 8K filings. 
    form_8k = masters[masters["Form Type"]=='8-K']
    print form_8k
    # initialize the variable to store the output. 
    forms = pd.DataFrame()
    # iterate over the 8-K filings and add them to the output. 
    for i in range(len(form_8k)): 
        # get 1 filing. 
        item = form_8k.iloc[i:i+1]
        # get the name of the file
        name = re.findall('[0-9]*-[0-9]*-[0-9]*.txt', str(item.Filename))[0]
        
        # get the items out of the HTML code
        details = html_cleaner( 'filings/' + get_filings(name, item.CIK.values[0], verbose))
        for key in details.keys():
            # add each item to the DF
            item[float(re.findall('[0-9]*[0-9.][0-9]*', key)[0])] =details[key]
        # add DF to output. 
        forms= forms.append(item)
    return forms

def masters_to_pd(cik=None):
    '''
    this function gets all the 8k forms together into a single dataframe
    
    '''
    masters = pd.DataFrame()
    masters_list = glob('masters/*.gz')
    for master_file in masters_list:
        masters = masters.append(pd.read_table(master_file, compression='gzip', header=1, skiprows=[0,1,2,3,4,5,6,9], sep='|'))
    masters.index = masters['Date Filed']
    if cik == None:
        return masters
    else: 
        return masters[masters.CIK==cik]
     
def get_cik(ticker):
    '''
    this function uses yahoo to translate a ticker into a CIK
    '''
    url = "http://finance.yahoo.com/q/sec?s=%s+SEC+Filings"%(ticker)
    return int(re.findall('=[0-9]*', str(re.findall('cik=[0-9]*', urllib2.urlopen(url).read())[0]))[0][1:])


if __name__ == "__main__": 
    ticker = "WPCS"
    form_8k = process_8k(ticker)

# <markdowncell>

# ### production version. 
# in the production version of this software we will read the DB so that the user can choose which filing types to download. 
# e.g. the user could choose to DL only the 8-K reports. 
# 
#  - for this version we download all files from 1 stock in the 2013 QTR4. 

# <codecell>

if __name__ == "__main__": 
    print form_8k

