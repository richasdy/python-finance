#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Aug 17 17:30:48 2019

@author: richasdy
"""

import bs4 as bs
import datetime as dt
import os
import pandas as pd
import pandas_datareader.data as web
import pickle
import requests


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

    start = dt.datetime(2010, 1, 1)
    end = dt.datetime.now()
    for ticker in tickers:
        # just in case your connection breaks, we'd like to save our progress!
        if not os.path.exists('stock_dfs/{}.csv'.format(ticker)):
            df = web.DataReader(ticker, 'yahoo', start, end)
#            df = web.DataReader(ticker, 'morningstar', start, end)
            df.reset_index(inplace=True)
            df.set_index("Date", inplace=True)
            df = df.drop("Symbol", axis=1)
            df.to_csv('stock_dfs/{}.csv'.format(ticker))
        else:
            print('Already have {}'.format(ticker))


def compile_data():
    with open("sp500tickers.pickle", "rb") as f:
        tickers = pickle.load(f)
    
    # read indonesian stock
    issi = pd.read_csv('ISSI-20190712.csv',header=None)
#    issi = pd.read_csv('JII70-201906.csv',header=None)
#    issi = pd.read_csv('JII-201906.csv',header=None)
    issi_code = issi[1].tolist()
    tickers = issi_code
    
    main_df = pd.DataFrame()

#    for count, ticker in enumerate(tickers[:71]):
    for count, ticker in enumerate(tickers):
#        df = pd.read_csv('stock_dfs/{}.csv'.format(ticker))
        df = pd.read_csv('ISSI-20190712[1912]/{}.csv'.format(ticker))
#        df = pd.read_csv('JII70-201906[1912]/{}.csv'.format(ticker))
#        df = pd.read_csv('JII-201906[1912]/{}.csv'.format(ticker))
        
        df.set_index('Date', inplace=True)

        df.rename(columns={'Adj Close': ticker}, inplace=True)
        df.drop(['Open', 'High', 'Low', 'Close', 'Volume'], 1, inplace=True)

        if main_df.empty:
            main_df = df
        else:
            main_df = main_df.join(df, how='outer')

        if count % 10 == 0:
            print(count)
    print(main_df.head())
#    main_df.to_csv('sp500_joined_closes.csv')
    main_df.to_csv('issi_joined_closes.csv')
#    main_df.to_csv('jii70_joined_closes.csv')
#    main_df.to_csv('jii_joined_closes.csv')


compile_data()