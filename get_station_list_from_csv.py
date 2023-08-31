import pandas as pd
import os
import zipfile


def get_station_list(month: str):
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
    data = data.fillna(0)
    data = data.rename(columns={'start station name': 'start_station_name', 'start station latitude': 'end_lat',
                                'start station longitude': 'end_lng'})
    data = data.dropna()
    data_deficit = pd.read_csv('output_files/csv_files/' + month + '_bike_deficit.csv')
    data_deficit = data_deficit.fillna(0)
    station_names_lst = data_deficit['start_station_name'].tolist()
    stations = []
    for station_name in station_names_lst:
        station = {}
        station['name'] = station_name
        station['latitude'] = data[data['start_station_name'] == station_name]['end_lat'].tolist()[0]
        station['longitude'] = data[data['start_station_name'] == station_name]['end_lng'].tolist()[0]
        station['deficit'] = data_deficit[data_deficit['start_station_name'] == station_name]['deficit'].tolist()[0]
        station['popularity'] = data_deficit[data_deficit['start_station_name'] == station_name]['popularity'].tolist()[0]
    # Clean up - remove the temporary extracted folder
    os.remove(csv_path)
    os.rmdir('temp_extracted_folder')
    return stations


