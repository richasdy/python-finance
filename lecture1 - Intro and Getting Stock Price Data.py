import datetime as dt
import matplotlib.pyplot as plt
from matplotlib import style
import pandas as pd
import pandas_datareader.data as web

style.use('ggplot')

start = dt.datetime(1912, 1, 1)
end = dt.datetime.now()

#https://www.quora.com/Using-Python-whats-the-best-way-to-get-stock-data

#error
#df = web.DataReader("TSLA", 'morningstar', start, end)
#aapl = web.DataReader("AAPL", "yahoo")
#kosong
#tops = web.DataReader(["GS", "AAPL"], "iex-tops")
#gs = web.DataReader("GS", "iex-book")
#oke
#vix = web.DataReader("VIXCLS", "fred")
#ff = web.DataReader("F-F_Research_Data_Factors_weekly", "famafrench")

# https://finance.yahoo.com/quote/TLKM.JK/
#df = web.DataReader("TSLA", 'yahoo', start, end)
df = web.DataReader("ASII.JK", 'yahoo', start, end)
#df = web.DataReader("BRK.B", 'yahoo', start, end)

#pdr = web.get_data_fred('GS10')


#untuk data morningstar
#df.reset_index(inplace=True)
#df.set_index("Date", inplace=True)
#df.index= pd.to_datetime(df.index)
#df = df.drop("Symbol", axis=1)

print(df.head())