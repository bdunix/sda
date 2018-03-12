#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Remote data access of pandas:
# https://pandas-datareader.readthedocs.io/en/latest/remote_data.html

import pandas_datareader.data as web
import datetime
import matplotlib.pyplot as plt

start = datetime.datetime(2010, 1, 4)
end = datetime.date.today()

df = web.DataReader('AAPL', 'morningstar', start, end)

print(df.head())

df['Close'].plot(grid = True)

plt.show()