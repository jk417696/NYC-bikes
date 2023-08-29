import os
import zipfile
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import matplotlib.ticker as ticker
from datetime import datetime
import math
import plotly.express as px


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



def show_colnames(month: str):
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
    data = pd.read_csv(csv_path)
    print(month, ': ', data.columns)

    # Clean up - remove the temporary extracted folder
    os.remove(csv_path)
    os.rmdir('temp_extracted_folder')
    return data


def show_columns_all():
    """
    :param year: year to analyse
    """
    for year_int in range(2014, 2024):
        year = str(year_int)
        directory_path = 'data/' + year
        files = os.listdir(directory_path)
        files = sorted(files)
        data_year = pd.DataFrame()
        for file in files:
            if os.path.isfile(os.path.join(directory_path, file)):
                month = str(file[:6])
                show_colnames(month)
    return data_year


# show_columns_all()

# only for month>=202102
def duration_vs_type(month: str):
    zip_file_path = 'data/' + month[:4] + '/' + month + '-citibike-tripdata.csv.zip'
    csv_file_name = month + '-citibike-tripdata.csv'
    with zipfile.ZipFile(zip_file_path, 'r') as zip_ref:
        # Extract the CSV file from the ZIP archive
        zip_ref.extract(csv_file_name, 'temp_extracted_folder')

    # Read the CSV file using pandas
    csv_path = 'temp_extracted_folder/' + csv_file_name
    data = pd.read_csv(csv_path, low_memory=False, usecols=['rideable_type', 'started_at', 'ended_at'])
    data['tripduration'] = (pd.to_datetime(data.ended_at) - pd.to_datetime(data.started_at)).dt.total_seconds()/60
    data = data.drop(['started_at', 'ended_at'], axis=1)

    # Clean
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
            if int(month)>202101:
                data_year = pd.concat([data_year, duration_vs_type(month)])
    return data_year


def duration_biketype(year: str):
    data = iterate_over_files_year(year)
    biketypes = data.rideable_type.drop_duplicates().dropna().reset_index(drop=True)
    # print(membertypes)
    df = []
    # for type in membertypes:
    #     print(data.tripduration[data.usertype.isin([type])].to_list())
    for type in biketypes:
        df.append(data.tripduration[data.rideable_type.isin([type])].to_list())
    # Create boxplots
    plt.style.use('ggplot')

    fig = plt.boxplot(df, labels=biketypes, patch_artist=True)
    for element in ['boxes', 'whiskers', 'fliers', 'medians', 'caps']:
        plt.setp(fig[element], color='black')
    plt.setp(fig['means'], color='darkred')
    for patch in fig['boxes']:
        patch.set(facecolor='#73c6b6')
    plt.title('Trip duration for different types of users in ' + year, color='#ff5e0e')
    plt.xlabel('Bike type', color='#695d46')
    plt.ylabel('Duration (in min)', color='#695d46')
    plt.ylim(0, 60)
    plt.savefig('./output_files/plots/duration_biketype/duration_biketype_'+year+'.png')
    plt.close()
    # fig.write_image('./output_files/plots/duration_member_' + year + '.png')


duration_biketype('2021')