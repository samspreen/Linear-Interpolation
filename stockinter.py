#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
# Stock Market Analysis using Linear Interpolation
#
#
@author: samspreen
"""

import pandas as pd
import numpy as np
import datetime 
import glob 


####
#### Refer to the zip file titled "stocks" for the required datasets 
####


filelist = glob.glob('*.csv') # 'glob.glob' is the directory search
filelist

for f in filelist:       #read in each filename into a csv
    df = pd.read_csv(f)
  
# We can concatenate the dataframes into one large dataframe
df = pd.DataFrame()

for f in filelist:              #loop through each file an add it to the new df
    newdf = pd.read_csv(f)
    newdf['ticker'] = f[:-4]    #create a column with the ticker of each stock (name of csv excluding last 4 str characters ".csv")
    df = pd.concat([df,newdf])  #combine the dataframes

stocks = df                     

##  The time interval covered varies from stock to stock. There are some 
##  missing records, so the data is incomplete. Note that some dates are not 
##  present because the exchange is closed on weekends and holidays. Those 
##  are not missing records. Dates outside the range reported for a given 
##  stock are also not missing records, these are just considered to be 
##  unavailable. Answer the questions below based on the data available in 
##  the files.



##  Here I will use the collective data to determine when the market was open 
##  from January 1, 2008 to December 31, 2015. (Without the use of external 
##  data) and report the number of days the market was open for 
##  each year in 2008-2015. 

stocks['Timestamp'] = pd.to_datetime(stocks['Date'])                 #create column of datetime objects
open_mark = stocks[stocks['Timestamp'] >= '2008-01-01']              #subset the DF by dates
open_mark = open_mark[open_mark['Timestamp'] <= '2015-12-31']        #subset the DF bydates
dates = open_mark['Timestamp']                                       #take out the datetime objects
dates = dates.drop_duplicates()                                      #drop duplicates
dates = pd.Series(dates)                                             #convert dates to a series
df = {'dates':dates}                                                 #create df of the dates
df = pd.DataFrame(df)

def year(x):             #this function will output the year given a datetime object
    year = x.year
    return year

df['year'] = df['dates'].apply(year)       #apply the function and create a new column
df['dates'].groupby(df['year']).count()    #groupby each year and take the counts



##
##  Here I will determine the total number of missing records for all stocks 
##  for the period 2008-2015.
##

ticks = pd.Series(stocks['ticker']).drop_duplicates()             #drop duplicates
tickers = list(ticks)                                             #convert to list

dates_mark = stocks['Date'].drop_duplicates()                                   #find unique dates 

missing_recs = pd.DataFrame(columns=['Date', 'ticker'])                         #create a df
for ticker in tickers: 
    subset = stocks.loc[stocks['ticker'] == ticker]                           #subset to that stock 
    first = subset['Date'].min()                                                  #find max and min 
    last = subset['Date'].max() 
    stocks_subset = dates_mark.loc[(dates_mark >= first) & (dates_mark <= last)]  #subset the dates again 
    days_stocks = np.setdiff1d(stocks_subset, subset['Date'])                                  
    missing_df = pd.DataFrame({'Date':days_stocks, 'ticker': ticker})             #create a df with missing date and associated stock
    missing_recs = pd.concat([missing_recs, missing_df], ignore_index = True)     #concat the df's



miss = missing_recs[missing_recs['Date'] >= '2008-01-01']       #subset by the dates
miss = miss[miss['Date'] <= '2015-12-31']             #subset by the dates
len(miss)




##  For the period 2008-2015, I will find the 10 stocks (plus ties) that had 
##  the most missing records, and the 10 stocks (plus ties) with the fewest 
##  missing records. 


def year(x):
    year = x.year
    return year

stocks['year'] = stocks['Timestamp'].apply(year)          #creae a column of years for the whole df 

open_mark = stocks[stocks['Date'] >= '2008-01-01']          #subset by dates
open_mark = open_mark[open_mark['Date'] <= '2015-12-31']
ticks = pd.Series(open_mark['ticker']).drop_duplicates()    #find unique stocks within the dates
tickers = stocks['ticker'].unique()                           
tickers = list(tickers)    #put unique stocks into a list
                         
missing_dates = [] 
for ticker in tickers: 
    subset = open_mark[open_mark['ticker'] == ticker]      #subset by stock 
    first_day = subset['Timestamp'].min()                  #find the max and min date for the stock 
    last_day = subset['Timestamp'].max() 
    stocks_subset = open_mark[(open_mark['Timestamp'] >= first_day) & (open_mark['Timestamp'] <= last_day)] #subset the bounds again
    days_stocks = pd.Series(stocks_subset['Date'].unique())      #find unique dates the market was open
    days_ticker = pd.Series(subset['Date'].unique())             #find unique dates the stock has records for
    for i in days_stocks:                                        #loop through the days the market was open 
        if i not in list(days_ticker):                           #if the day the market was open isnt in the stock's records put it in a list
            missing_dates.append(i)   
    
missing_dates = pd.Series(missing_dates)        
missing_dates.value_counts()

###########################
##  LINEAR INTERPOLATION ##
###########################
##  For each stock, compute (fill in) the missing records using linear 
##  interpolation. For instance, suppose d1 < d2 < d3 are dates, and P1 
##  and P3 are known Open prices on dates d1 and d3, respectively, with
##  P2 missing.  Then we estimate P2 (the Open price on date d2) with
##
##    P2 = ((d3 − d2)P1 + (d2 − d1)P3)/(d3 − d1)
##
##  The same formula is used for the other missing values of High, Low, Close, 
##  and Volume. Note that weekends and holidays are not missing records, so we 
##  don't compute those. 


stocksb5 = stocks[(stocks['year'] >= 2008) & (stocks['year'] != 2016)]          #subset to 2008-2015
tickers = stocksb5['ticker'].unique()                                           #find unique stocks
dates_mark = stocks['Date'].drop_duplicates()                                   #find unique dates 


stocksb5 = stocks
missing_recs = pd.DataFrame(columns=['Date', 'ticker'])                         #create a df
for ticker in tickers: 
    subset = stocksb5.loc[stocksb5['ticker'] == ticker]                           #subset to that stock 
    first = subset['Date'].min()                                                  #find max and min 
    last = subset['Date'].max() 
    stocks_subset = dates_mark.loc[(dates_mark >= first) & (dates_mark <= last)]  #subset the dates again 
    days_stocks = np.setdiff1d(stocks_subset, subset['Date'])                                  
    missing_df = pd.DataFrame({'Date':days_stocks, 'ticker': ticker})             #create a df with missing date and associated stock
    missing_recs = pd.concat([missing_recs, missing_df], ignore_index = True)     #concat the df's


missing_recs['Date']  = pd.to_datetime(missing_recs['Date'])                      #convert to datetime


stocksb5 = stocks[(stocks['year'] >= 2008) & (stocks['year'] !=2016)]             #subset to years we need 
tickers = stocksb5['ticker'].unique()                                      


stocksb5 = miss
tickers = stocksb5['ticker'].unique()   

missing = pd.DataFrame(columns= ['ticker', 'Date', 'Open', 'Close', 'High', 'Low', 'Volume'])  #create a df to store calculated values
dates_market = stocks['Date'].drop_duplicates()                                                #find unique dates
index = 0 
  

list_missing = []   
for ticker in tickers: 
    #stocks2 = stocks[(stocks['year'] >= 2008) & (stocks['year'] !=2016)]                       #subset by dates
    subset = stocksb5[stocksb5['ticker'] == ticker]                                            #subset by stocks
    first = subset['Date'].min() 
    last = subset['Date'].max()                            
    stocks_subset = dates_market.loc[(dates_market >= first) & (dates_market <= last)]         #subset by bounds of the stock's records

    missing_subset = missing_recs.loc[missing_recs['ticker'] == ticker]                        
    
    for i in range(len(missing_subset['Date'])) :                                              #loop through each date

        d2 = pd.to_datetime(missing_subset['Date'].iloc[i])                                    #the missing date
        d1 = subset[subset['Timestamp'] < d2 ].max()['Timestamp']                              #subset to the date before the missing date
        d3 = subset[subset['Timestamp'] > d2].min()['Timestamp']                               #subset to date after missing date

        # this code finds the open price and calculates the interpolated price
        P1_open = subset.loc[subset['Timestamp'] == d1, 'Open' ]                                
        P3_open = subset.loc[subset['Timestamp'] == d3, 'Open' ]                                 
        open_interp = float(  ((d3-d2)/(d3-d1)) *P1_open )  +  float(  [(d2-d1)/(d3-d1)] *P3_open )   
        
        # this code finds the close price and calculates the interpolated price
        P1_close = subset.loc[subset['Timestamp'] == d1, 'Close' ]                                
        P3_close = subset.loc[subset['Timestamp'] == d3, 'Close' ]                                 
        close_interp = float((  ((d3-d2)/(d3-d1)) *P1_close ))  +  float((  [(d2-d1)/(d3-d1)] *P3_close )  )
        
        # this code finds the high price and calculates the interpolated price
        P1_high = subset.loc[subset['Timestamp'] == d1, 'High' ]                                
        P3_high = subset.loc[subset['Timestamp'] == d3, 'High' ]                                 
        high_interp = float((  ((d3-d2)/(d3-d1)) *P1_high ))  +  float((  [(d2-d1)/(d3-d1)] *P3_high )  )  
        
        # this code finds the low price and calculates the interpolated price
        P1_low = subset.loc[subset['Timestamp'] == d1, 'Low' ]                                
        P3_low = subset.loc[subset['Timestamp'] == d3, 'Low' ]                                 
        low_interp = float((  ((d3-d2)/(d3-d1)) *P1_low ))  +  float((  [(d2-d1)/(d3-d1)] *P3_low )  )  
        
        # this code finds the volume and calculates the interpolated volume
        P1_vol = subset.loc[subset['Timestamp'] == d1, 'Volume' ]                                
        P3_vol = subset.loc[subset['Timestamp'] == d3, 'Volume' ]                                 
        vol_interp = float((  ((d3-d2)/(d3-d1)) *P1_vol ))  +  float((  [(d2-d1)/(d3-d1)] *P3_vol )  )  
        
        #this code adds each value to the dataframe created before this loop 
        missing.loc[index, 'ticker']   = ticker
        missing.loc[index, 'Date']     = d2 
        missing.loc[index, 'Open']     = open_interp 
        missing.loc[index, 'Close']    = close_interp
        missing.loc[index, 'High']     = high_interp 
        missing.loc[index, 'Low']      = low_interp 
        missing.loc[index, 'Volume']   = vol_interp 
        
        index += 1 

df_inter = pd.concat([missing, stocksb5]) #concat the missing records to the records we already have










