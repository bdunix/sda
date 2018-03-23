#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Remote data access of pandas:
# https://pandas-datareader.readthedocs.io/en/latest/remote_data.html

import pandas as pd
import pandas_datareader.data as web
from datetime import datetime
import matplotlib.pyplot as plt
import numpy as np

if __name__ == "__main__":
    start = datetime(2016, 1, 4)
    # end = datetime.today()
    end = datetime(2016, 9, 1)
    apple = web.DataReader('AAPL', 'morningstar', start, end)

    '''
                        Close     High     Low    Open    Volume
    Symbol Date                                                 
    AAPL   2016-01-04  105.35  105.368  102.00  102.61  67649387
           2016-01-05  102.71  105.850  102.41  105.75  55790992
           2016-01-06  100.70  102.370   99.87  100.56  68457388
           2016-01-07   96.45  100.130   96.43   98.68  81094428
           2016-01-08   96.96   99.110   96.76   98.55  70798016
    '''

    # df['Close'].plot(grid=True)
    # plt.show()

    apple.insert(0, 'Open', apple.pop('Open'))
    apple.insert(3, 'Close', apple.pop('Close'))

    apple["20d"] = np.around(apple["Close"].rolling(20).mean(), 2)
    apple["50d"] = np.around(apple["Close"].rolling(50).mean(), 2)
    apple["200d"] = np.around(apple["Close"].rolling(200).mean(), 2)

    apple['20d-50d'] = apple['20d'] - apple['50d']
    print(apple.tail())

    # np.where() is a vectorized if-else function, where a condition is checked for each component of a vector, and the first argument passed is used when the condition holds, and the other passed if it does not
    apple["Regime"] = np.where(apple['20d-50d'] > 0, 1, 0)
    # We have 1's for bullish regimes and 0's for everything else. Below I replace bearish regimes's values with -1, and to maintain the rest of the vector, the second argument is apple["Regime"]
    apple["Regime"] = np.where(apple['20d-50d'] < 0, -1, apple["Regime"])

    # Remove 'Symbol' from muti-level index.
    apple = apple.reset_index(level='Symbol')

    apple.loc['2016-01-04':'2016-08-07', "Regime"].plot(ylim=(-2, 2)).axhline(y=0, color="black", lw=2)

    # To ensure that all trades close out, I temporarily change the regime of the last row to 0
    regime_orig = apple.ix[-1, 'Regime']
    apple.ix[-1, 'Regime'] = 0
    apple['Signal'] = np.sign(apple['Regime'] - apple['Regime'].shift(1))
    # Restore original regime data
    apple.ix[-1, 'Regime'] = regime_orig

    print(apple.tail())

    apple["Signal"].plot(ylim=(-2, 2))
    # plt.show()

    # Create a DataFrame with trades, including the price at the trade and the regime under which the trade is made.
    apple_signals = pd.concat([pd.DataFrame({"Price": apple.loc[apple["Signal"] == 1, "Close"],
                                             "Regime": apple.loc[apple["Signal"] == 1, "Regime"],
                                             "Signal": "Buy"}),
                               pd.DataFrame({"Price": apple.loc[apple["Signal"] == -1, "Close"],
                                             "Regime": apple.loc[apple["Signal"] == -1, "Regime"],
                                             "Signal": "Sell"})])
    apple_signals.sort_index(inplace=True)
    print(apple_signals)

    # Let's see the profitability of long trades
    apple_long_profits = pd.DataFrame({
        "Price": apple_signals.loc[(apple_signals["Signal"] == "Buy") & apple_signals["Regime"] == 1, "Price"],
        "Profit": pd.Series(apple_signals["Price"] - apple_signals["Price"].shift(1)).loc[apple_signals.loc[
            (apple_signals["Signal"].shift(1) == "Buy") & (apple_signals["Regime"].shift(1) == 1)].index].tolist(),
        "End Date": apple_signals["Price"].loc[apple_signals.loc[
            (apple_signals["Signal"].shift(1) == "Buy") & (apple_signals["Regime"].shift(1) == 1)].index].index})
    print(apple_long_profits)
