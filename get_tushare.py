#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import matplotlib.dates as mdates
import matplotlib.pyplot as plt
import mpl_finance as mpf
import pandas as pd
import tushare as ts

quotes = ts.get_k_data('002739', '2017-01-01')
quotes.info()

print(quotes[:3])

'''
DataFrame returned from tushare has below format:
         date    open   close    high     low    volume    code
0  2017-01-03  54.010  54.070  54.110  53.711   30518.0  002739
1  2017-01-04  54.090  56.691  56.771  53.831  103953.0  002739
2  2017-01-05  56.302  56.591  57.080  55.924   65414.0  002739
'''

# Get Numpy representation of NDFrame.
quotes_values = quotes.values

# Convert to float days format for candlestick_ochl.
quotes_values[..., 0] = mdates.date2num(pd.DatetimeIndex(quotes['date']).to_pydatetime())

print(quotes_values[:3])

fig, ax = plt.subplots(figsize=(15, 5))
fig.subplots_adjust(bottom=0.5)
mpf.candlestick_ochl(ax, quotes_values, width=0.6, colorup='g', colordown='r', alpha=1.0)
plt.grid(True)
# 设置日期刻度旋转的角度
plt.xticks(rotation=30)
plt.title('wanda yuanxian 17')
plt.xlabel('Date')
plt.ylabel('Price')
# x轴的刻度为日期
ax.xaxis_date()
###candlestick_ochl()函数的参数
# ax 绘图Axes的实例
# mat_quotes 价格历史数据
# width    图像中红绿矩形的宽度,代表天数
# colorup  收盘价格大于开盘价格时的颜色
# colordown   低于开盘价格时矩形的颜色
# alpha      矩形的颜色的透明度

plt.show()
