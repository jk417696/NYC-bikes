import zipfile

import numpy as np
import pandas as pd
import os


def create_df_bike_deficit(month: str):
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
    data = pd.read_csv(csv_path)
    data = data.dropna()
    data = data.rename(columns={'start station name': 'start_station_name', 'end station name': 'end_station_name'})
    data_start = data.groupby(['start_station_name']).size().reset_index(name='start_count')
    data_end = data.groupby(['end_station_name']).size().reset_index(name='end_count')
    data_end = data_end.rename(columns={'end_station_name': 'start_station_name'})
    result = pd.merge(data_start, data_end, on='start_station_name', how='outer')
    result['deficit'] = (result['start_count'] - result['end_count'])
    result['popularity'] = (result['start_count'] + result['end_count'])
    # r = np.array(result['deficit'].tolist())
    # r = np.where(r > 0, r / r.max(), np.where(r < 0, -r / r.min(), r))
    # result['deficit_normalized'] = r
    # r = np.array(result['popularity'].tolist())
    # r = np.where(r > 0, r / r.max(), np.where(r < 0, -r / r.min(), r))
    # result['popularity_normalized'] = r
    result.to_csv('output_files/csv_files/' + month + '_bike_deficit.csv')
    # Clean up - remove the temporary extracted folder
    os.remove(csv_path)
    os.rmdir('temp_extracted_folder')
    return result


# def create_df_bike_deficit_hourly(month: str):
#     """
#     :param month: format yyyymm
#     """
#     if int(month) < 201700:
#         zip_file_path = 'data/' + month[:4] + '/' + month + '-citibike-tripdata.zip'
#         csv_file_name = month + '-citibike-tripdata.csv'
#     else:
#         zip_file_path = 'data/' + month[:4] + '/' + month + '-citibike-tripdata.csv.zip'
#         csv_file_name = month + '-citibike-tripdata.csv'
#
#     with zipfile.ZipFile(zip_file_path, 'r') as zip_ref:
#         # Extract the CSV file from the ZIP archive
#         zip_ref.extract(csv_file_name, 'temp_extracted_folder')
#
#     # Read the CSV file using pandas
#     csv_path = 'temp_extracted_folder/' + csv_file_name
#     df = pd.read_csv(csv_path)
#     df = df.dropna()
#     for hour in range(23):
#         data = df[df['']]
#         data_start = data.groupby(['start_station_name']).size().reset_index(name='start_count')
#         data_end = data.groupby(['end_station_name']).size().reset_index(name='end_count')
#         data_end = data_end.rename(columns={'end_station_name': 'start_station_name'})
#         result = pd.merge(data_start, data_end, on='start_station_name')
#         result['deficit'] = result['start_count'] - result['end_count']
#         result['popularity'] = result['start_count'] + result['end_count']
#         result.to_csv('output_files/csv_files/' + month + '_bike_deficit.csv')
#     # Clean up - remove the temporary extracted folder
#     os.remove(csv_path)
#     os.rmdir('temp_extracted_folder')
#     return result


def bike_deficit(data):
    data = data.dropna()
    data_start = data.groupby(['startstation_name']).size().reset_index(name='start_count')
    data_end = data.groupby(['end_station_name']).size().reset_index(name='end_count')
    data_end = data_end.rename(columns={'end_station_name': 'start_station_name'})
    result = pd.merge(data_start, data_end, on='start_station_name')
    result['deficit'] = result['start_count'] - result['end_count']
    result['popularity'] = result['start_count'] + result['end_count']
    return result
#
#
# create_df_bike_deficit('201903')
# create_df_bike_deficit('202003')
# create_df_bike_deficit('202103')
# create_df_bike_deficit('202203')
create_df_bike_deficit('202306')