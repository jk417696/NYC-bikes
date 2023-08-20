import os
import zipfile
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import matplotlib.ticker as ticker
from datetime import datetime


def input_csv_from_zip(month: str):
    """
    :param month: format yyyymm
    """
    print(month)
    if int(month) < 201700:
        zip_file_path = 'data/' + month[:4] + '/' + month + '-citibike-tripdata.zip'
        csv_file_name = month + '-citibike-tripdata.csv'
    else:
        zip_file_path = 'data/' + month[:4] + '/' + month + '-citibike-tripdata.csv.zip'
        csv_file_name = month + '-citibike-tripdata.csv'

    with zipfile.ZipFile(zip_file_path, 'r') as zip_ref:
        # Extract the CSV file from the ZIP archive
        zip_ref.extract(csv_file_name, 'temp_extracted_folder')

    # Read the CSV file using pandas
    csv_path = 'temp_extracted_folder/' + csv_file_name
    if int(month) < 202102:
        data = pd.read_csv(csv_path, low_memory=False, usecols=['tripduration'])
    else:
        data = pd.read_csv(csv_path, low_memory=False, usecols=['started_at', 'ended_at'])
        data['tripduration'] = (pd.to_datetime(data.ended_at) - pd.to_datetime(data.started_at)).dt.total_seconds()
        data = data.drop(['started_at', 'ended_at'], axis=1)

    # Clean up - remove the temporary extracted folder
    os.remove(csv_path)
    os.rmdir('temp_extracted_folder')
    return data


def iterate_over_files_year(year: str):
    """
    :param year: year to analyse
    """
    directory_path = 'data/' + year
    files = os.listdir(directory_path)
    files = sorted(files)
    data_year = pd.DataFrame()
    for file in files:
        if os.path.isfile(os.path.join(directory_path, file)):
            month = str(file[:6])
            data_year = pd.concat([data_year, input_csv_from_zip(month)])
    return data_year


def duration_histogram_year(year: str):
    data = iterate_over_files_year(year)
    # if int(year)>2020:
    #     # data['starttime'] = data[['started_at']].apply(lambda x: x[0].timestamp(), axis=1).astype(int)
    #     # data['endtime'] = data[['ended_at']].apply(lambda x: x[0].timestamp(), axis=1).astype(int)
    #     data['tripduration'] = (pd.to_datetime(data.ended_at) - pd.to_datetime(data.started_at)).dt.total_seconds()

    # times = [(data.tripduration < 60*i).sum() - (data.tripduration < 60*(i-1)).sum() for i in range(1, 61)]
    # print(times, (data.tripduration > 3600).sum())
    # print(data.columns)
    plt.style.use('ggplot')
    fig, ax = plt.subplots(figsize=(12, 10))
    n, bins, patches = plt.hist(data.tripduration/60, bins=np.arange(0, 63),
                                color='#73c6b6')
    n_outliers = (data.tripduration > 3660).sum()
    patches[-1].set_height(patches[-1].get_height() + n_outliers)
    most_pop_duration = bins[n.argmax()]
    plt.axvline(x=most_pop_duration+0.5, color='black', alpha=0.5)
    plt.text(most_pop_duration+1, 10000,
             'Most popular trip duration ('+str(int(n.max()))+' trips):  '+str(int(most_pop_duration))+' min',
             rotation=90)
    avg_duration = np.mean(data.tripduration)/60
    plt.axvline(x=int(avg_duration)+0.5, color='darkred', alpha=0.5)
    plt.text(int(avg_duration)+1, 10000, 'Average duration: '+str(int(avg_duration))+' min', rotation=90)
    plt.title('Trip duration in '+year, fontsize=32)
    plt.xlabel('Duration (in min)', fontsize=20)
    plt.xticks(ticks=np.append(np.arange(5.5, 59, 5), [61.5]),
               labels=np.append(np.arange(5, 59, 5), ['60+']))
    plt.xlim(1, 62)
    plt.ylim(0, 2000000)
    ticks_y = ticker.FuncFormatter(lambda x, pos: '{0:g}MLN'.format(x/1000000))
    ax.yaxis.set_major_formatter(ticks_y)
    plt.tight_layout()
    plt.savefig('./output_files/plots/yearly_duration_histogram_'+year+'.png')

for year in range(2016, 2024):
    duration_histogram_year(str(year))


