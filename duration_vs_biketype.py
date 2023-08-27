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

    # Create boxplots
    fig = px.box(data, x="rideable_type", y="tripduration")
    fig.update_yaxes(range=[0, 60])
    fig.show()

    return data


duration_vs_type('202105')