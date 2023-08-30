import warnings
import itertools
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import statsmodels.api as sm
import matplotlib
import pmdarima as pm
from pylab import rcParams
from statsmodels.tsa.stattools import adfuller
import matplotlib.ticker as ticker


data = pd.read_csv('./output_files/csv_files/daily_trips.csv', parse_dates=['date'])
data = data.set_index('date')
avg_trips_month = data.trips.resample('MS').mean()
print(avg_trips_month)
plt.style.use('bmh')

def decompose(data):
    rcParams['figure.figsize'] = 18, 8
    decomposition = sm.tsa.seasonal_decompose(avg_trips_month, model='additive')
    fig = decomposition.plot()
    fig.savefig('output_files/plots/sarima/decomposed.png')


# def adf_test(timeseries):
#     #Perform Dickey-Fuller test:
#     print ('Results of Dickey-Fuller Test:')
#     dftest = adfuller(timeseries, autolag='AIC')
#     dfoutput = pd.Series(dftest[0:4], index=['Test Statistic', 'p-value', '#Lags Used',
#                                              'Number of Observations Used'])
#     for key, value in dftest[4].items():
#         dfoutput['Critical Value (%s)'%key] = value
#     print(dfoutput)


def forecast(data, ARIMA_model, periods=24):
    plt.style.use('ggplot')

    # Forecast
    n_periods = periods
    fitted, confint = ARIMA_model.predict(n_periods=n_periods, return_conf_int=True)
    index_of_fc = pd.date_range(data.index[-1] + pd.DateOffset(months=1), periods = n_periods, freq='MS')

    # make series for plotting purpose
    fitted_series = pd.Series(fitted, index=index_of_fc)
    lower_series = pd.Series(confint[:, 0], index=index_of_fc)
    upper_series = pd.Series(confint[:, 1], index=index_of_fc)

    # Plot
    fig, ax = plt.subplots(figsize=(15,7))
    plt.plot(data, color='#008575', label='Smoothed data')
    plt.plot(fitted_series, color='darkred', label='Forecast')
    plt.fill_between(lower_series.index,
                    lower_series,
                    upper_series,
                    color='#695d46', alpha=.15)
    ticks_y = ticker.FuncFormatter(lambda x, pos: '{0:g}K'.format(x / 1000))
    ax.yaxis.set_major_formatter(ticks_y)
    plt.legend(fontsize=16)
    plt.title("SARIMA - Forecast of daily trips", color='#ff5e0e', fontsize=32)
    plt.xticks(fontsize=20)
    plt.yticks(fontsize=20)
    plt.ylim(0, 470000)
    plt.tight_layout()
    plt.savefig('./output_files/plots/sarima/forecast_2030.png')


sarima_model = pm.auto_arima(avg_trips_month, start_p=1, start_q=1, max_p=3, max_q=3, m=12, start_P=0, seasonal=True,
                      d=1, D=1, trace=True, error_action='ignore',  suppress_warnings=True, stepwise=True)
# sarima_model.plot_diagnostics(figsize=(15, 12))
# plt.show()
forecast(avg_trips_month, sarima_model, 12*6+7)



