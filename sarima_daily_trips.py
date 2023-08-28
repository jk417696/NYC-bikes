import warnings
import itertools
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import statsmodels.api as sm
import matplotlib
import pmdarima as pm
from pylab import rcParams


data = pd.read_csv('./output_files/csv_files/daily_trips.csv', parse_dates=['date'])
data = data.set_index('date')

avg_trips_month = data.trips.resample('MS').mean()
#
plt.style.use('bmh')
fig, ax = plt.subplots(figsize=(12, 10))

rcParams['figure.figsize'] = 18, 8
decomposition = sm.tsa.seasonal_decompose(avg_trips_month, model='additive')
fig = decomposition.plot()
fig.savefig('output_files/plots/sarima/decomposed.png')
