# -*- coding: utf-8 -*-

import bs4 as bs
import datetime as dt
import os
import pandas_datareader.data as web
import pickle
import requests
import pandas as pd 

def save_sp500_tickers():
    resp = requests.get('http://en.wikipedia.org/wiki/List_of_S%26P_500_companies')
    soup = bs.BeautifulSoup(resp.text, 'lxml')
    table = soup.find('table', {'class': 'wikitable sortable'})
    tickers = []
    for row in table.findAll('tr')[1:]:
        ticker = row.findAll('td')[0].text
        ticker = ticker[:-1]
        tickers.append(ticker)
    with open("sp500tickers.pickle", "wb") as f:
        pickle.dump(tickers, f)
    return tickers


# save_sp500_tickers()
def get_data_from_yahoo(reload_sp500=False):
    
    if reload_sp500:
        tickers = save_sp500_tickers()
    else:
        with open("sp500tickers.pickle", "rb") as f:
            tickers = pickle.load(f)
        
    if not os.path.exists('stock_dfs'):
        os.makedirs('stock_dfs')
    
    # read indonesian stock
    issi = pd.read_csv('ISSI-20190712.csv',header=None)
#    issi = pd.read_csv('JII70-201906.csv',header=None)
#    issi = pd.read_csv('JII-201906.csv',header=None)
    issi_code = issi[1].tolist()
    tickers = issi_code
    

    start = dt.datetime(1912, 1, 1)
    end = dt.datetime.now()
    index = 0
#    for ticker in tickers[:100]:
    for ticker in tickers:
                         
        index += 1
        print(index," of ",len(tickers)," : ",ticker)
                
        # just in case your connection breaks, we'd like to save our progress!
        if not os.path.exists('stock_dfs/{}.csv'.format(ticker)):
            
            #error
#            df = web.DataReader(ticker, 'morningstar', start, end)
#            df = web.DataReader("YUM", 'yahoo', start, end)
            df = web.DataReader(ticker, 'yahoo', start, end)
            df.reset_index(inplace=True)
            df.set_index("Date", inplace=True)
            #untuk data morningstar
            #df = df.drop("Symbol", axis=1)
            df.to_csv('stock_dfs/{}.csv'.format(ticker))
            
        else:
            print('Already have {}'.format(ticker))


get_data_from_yahoo()