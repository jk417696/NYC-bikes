import os
import zipfile
import pandas as pd
from datetime import datetime
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import matplotlib.ticker as ticker


def trips_number_day(month: str):
    """
    :param month: format yyyymm
    """
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
    if int(month) >= 202102:
        start_colname = 'started_at'
    elif 201610 <= int(month) <= 201703:
        start_colname = 'Start Time'
    else:
        start_colname = 'starttime'
    data = pd.read_csv(csv_path, usecols=[start_colname], parse_dates=[start_colname]).rename(columns={start_colname: 'date'})
    data = data.groupby([data.date.dt.date]).count()

    # Clean up - remove the temporary extracted folder
    os.remove(csv_path)
    os.rmdir('temp_extracted_folder')
    return data


trips_number_day('202003')


def daily_trips_year(year: str, df_func):
    """
    :param year: year to analyse
    :param df_func: function that produces output with a structure same as in "parse_local_csv_file"
    """
    directory_path = 'data/' + year
    files = os.listdir(directory_path)
    files = sorted(files)
    daily_trips = pd.DataFrame()
    for file in files:
        if os.path.isfile(os.path.join(directory_path, file)):
            month = str(file[:6])
            daily_trips = pd.concat([daily_trips, df_func(month)])
    return daily_trips


# Create plot with number of trips

data = pd.read_csv('./output_files/csv_files/daily_trips.csv')

print(data[data.trips == min(data.trips)])
#
# plt.style.use('ggplot')
# fig, ax = plt.subplots(figsize=(12, 10))
# plt.scatter(data.date, data.trips, color='#008575', s=5)
# plt.title('Daily number of trips', color='#ff5e0e', fontsize=32)
# plt.xlabel('Date', color='#695d46', fontsize=20)
# plt.ylim(0, 150000)
# # plt.ylabel('Number of trips', color='#695d46', fontsize=26)
# # plt.xlim(min(data.date), max(data.date))
# ax.xaxis.set_major_locator(mdates.MonthLocator(interval=3))
# ticks_y = ticker.FuncFormatter(lambda x, pos: '{0:g}K'.format(x / 1000))
# plt.xticks(rotation=90, size=14)
# plt.yticks(size=16)
# ax.yaxis.set_major_formatter(ticks_y)
# plt.tight_layout()
# plt.savefig('output_files/plots/daily_trips.png')

