# -*- coding: utf-8 -*-
"""
Created on Thu Feb  6 10:20:12 2014

@author: ptorre


We're going to crawl the EDGAR website instead of using the FTP... 
advantages: 
    the website has files separated by sections and in htm format
    this will be easier than handling the raw .txt from the FTP. 
    
How to do it? 

    0. get the CIK and ACCNO for all files that you need to download. 

    1. build the url 

        

    2. load the SEC url
    3. find the files that are available. 
        exhibits are identified as such in the html index. 
        Add exhibits to items table? 
    4. download the htm files. 
    
    get_file_map -> gets CIK ACCNO and items. 
    get_htm()






"""


import nucleus as nc
import pandas as pd
import urllib2
import build_edgar_map_db as ed_rss

def get_file_map(ticker):
    '''
    this function gets a file map for a given ticker. 
    

    CREATE OR REPLACE FUNCTION fs_get_edgar_map
    (refcursor, VARCHAR) RETURNS refcursor AS $FSPROC$
    BEGIN
    OPEN $1 FOR 
    SELECT cpy_id, tic_ticker, edgar_accno, edgar_timestamp, edgar_item, edgar_map.form_type
        FROM (edgar_map JOIN ticker USING (cpy_id)) 
        LEFT JOIN edgar_item USING (edgar_map_id)
        WHERE tic_ticker = $2;
    RETURN $1;
    END;
    $FSPROC$ LANGUAGE plpgsql;



    '''
    #%%
    sql = "SELECT fs_get_edgar_map('x', '%s'); fetch all in x;"
    file_map = nc.read_db(sql%(ticker))
    #%%
    return file_map

#%%
def get_htm_url(entry):
    '''
    this function gets the htm url for one entry of the file_map
    '''
    url = str("http://www.sec.gov/Archives/edgar/data/%s/%s/%s-index.htm")
    
    url = str("http://www.sec.gov/Archives/edgar/data/%s/%s/")
    
    cik = nc.read_db("SELECT tic_ticker FROM ticker "+
                        "WHERE src_id=11 AND cpy_id = %s"%(entry.cpy_id.iloc[0]
                        )).tic_ticker.iloc[0]
    accno = entry.edgar_accno.iloc[0]
    return url%(cik, accno.replace("-",""))

#%%


def get_htm_docs(html_str):
    '''
    this function gets the .htm documents from an edgar page    
    
    '''
    # get the html page for the selected entry
    #%%
    doc_url = str(html_str+"/%s")
    #%%
    html_page = pd.io.html.read_html(html_str, infer_types=False, 
                         header=0, index_col=0, flavor='html5lib')[0].dropna()
    
    doc_list = []
    for name in html_page.Name:
        if "htm" in name: 
            if "index" not in name:
                doc_list += [doc_url%(name)]
    
    #%%
    return doc_list
    #%%

### FUNCTION TO GET THE HTML FILES FROM EDGAR SITE

def get_files(ticker):
    '''
    this tool gets all the files for a given ticker. 
    
    this function must be translated to C.     
    
    '''
    # first make sure the map is up to date    
    ed_rss.update_edgar_map()
    print "getting file map"
    file_map = get_file_map(ticker)
    file_small = file_map[["cpy_id", "edgar_accno"]].drop_duplicates()
    file_list = []
    for i in range(len(file_small)): 
        #%%
        entry = file_small.iloc[i:i+1]
        print entry
        html_str = get_htm_url(entry)
        file_list += get_htm_docs(html_str)
    return file_map, file_list


###### FUNCTIONS FOR DEMO  -- 
   
def update_edgar_db():
    '''
    this function is a simplet
    '''
    ed_rss.update_edgar_map()
    

def get_files_single_entry(file_map_entry):
    '''
    this function gets the files for 1 entry 
    '''
    #ed_rss.update_edgar_map()
    #%%
    url_list = get_htm_docs(get_htm_url(file_map_entry)) 
    page_list = []    
    for url in url_list:
        page_list += [urllib2.urlopen(url).read()]
    #%%
        
    
    return url_list, page_list
    
    
    