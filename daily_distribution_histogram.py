import zipfile
import pandas as pd
import os
import calendar
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker


def daily_duration(month: str, year: str):
    data = pd.read_csv('./output_files/csv_files/daily_distribution_' + year, usecols=[month])
    plt.style.use('ggplot')
    fig, ax = plt.subplots(figsize=(12, 10))
    plt.bar(data.index, height = data[month], color='#73c6b6')
    plt.title('Daily trips distribution in ' + month + ' ' + year, fontsize=32, color='#ff5e0e')
    plt.ylabel('Number of trips', fontsize=20, color='#695d46')
    plt.xlabel('Hour', fontsize=20, color='#695d46')
    plt.xticks(fontsize=16)
    plt.yticks(fontsize=16)
    ticks_y = ticker.FuncFormatter(lambda x, pos: '{0:g}K'.format(x / 1000))
    ax.yaxis.set_major_formatter(ticks_y)
    plt.tight_layout()
    num_month = {'January': '01', 'February':'02', 'March':'03', 'April':'04', 'May':'05', 'June':'06',
                 'July':'07', 'August':'08', 'September':'09', 'October':'10', 'November':'11', 'December':'12'}
    plt.savefig('./output_files/plots/daily_distribution/daily_distribution_' + year + num_month[month])
    plt.close()


months = ['January', 'February', 'March', 'April', 'May', 'June',
          'July', 'August', 'September', 'October', 'November', 'December']
years = ['2015', '2020', '2021', '2022']
for year in years:
    for month in months:
        daily_duration(month, year)
