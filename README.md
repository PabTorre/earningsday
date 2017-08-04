A website where investors can find insight from fundamental information. 

    collects data from edgar filings and clusters the companies 
    based on that data. 
        sells analysis on the data
        & excel reports made from the data in format defined by user? 
    
        absolute data
        financial ratios
        relative data (horizontal analysis)
        stock price vs earnings analysis. 
            compare change in fundamentals with change in stock price in the next 
                1, 5, 30, 60, 90 days. 
                correlation? 
components: 

    backend: 
        database holding the earnings data for all stocks in the US. 
            schema based on readme 
                from http://www.sec.gov/dera/data/financial-statement-data-sets.html
            build it from the XLBR datasets. 
            
             
        analysis: 
            clustering analysis/classification. 
    
    
    
    front end: 
        charts showing market structure & clusters. 
        
    
        
        
    email reports: 
        stocks to watch for earnings
        
Minimum viable product: 
    charts that show market structure and clusters based on fundamental info. 
    tables that show financial statements nicely formatted for several years. 
    

Hypothesis: 
    Stocks with similar fundamentals will show similar price trends during the 
    time between earnings releases. 
    
    How  to test this hipothesis? 
        need to get the fundamental #'s for different stocks, and then 
        get their return for the days after the earnings release. 
        
        questions: 
            is the absolute fundamental values that count? 
            or the change from one period to the next? 
        quandl has SEC datasets... will it be easier to use those instead of XBLR?  
        
        
Minimum viable product. 
    get earnings per share from all the files. 
    get the CIK for the sp500 stocks. 
    look at horizontal analisis -> compare the numbers for different stocks on the 
    same period. 
    
    

    
 
    
        
        
        
        
    
