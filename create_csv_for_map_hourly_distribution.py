import pandas as pd
import os
import zipfile


def daily_distribution_month(month: str):
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
    if 'starttime' in data:
        data['starttime'] = pd.to_datetime(data['starttime'])
        data['start_hour'] = data['starttime'].dt.hour
    else:
        data['started_at'] = pd.to_datetime(data['started_at'])
        data['start_hour'] = data['started_at'].dt.hour
    if 'endtime' in data:
        data['endtime'] = pd.to_datetime(data['endtime'])
        data['end_hour'] = data['endtime'].dt.hour
    else:
        data['ended_at'] = pd.to_datetime(data['ended_at'])
        data['end_hour'] = data['ended_at'].dt.hour
    start_hourly_counts = data.groupby(['start_hour', 'start_station_name']).size().reset_index(name='count')
    end_hourly_counts = data.groupby(['end_hour', 'end_station_name']).size().reset_index(name='count')
    start_hourly_counts = start_hourly_counts.rename(columns={'start_station_name': 'station_name', 'start_hour': 'hour'})
    end_hourly_counts = end_hourly_counts.rename(columns={'end_station_name': 'station_name', 'end_hour': 'hour'})
    merged_data = pd.merge(start_hourly_counts, end_hourly_counts, on=['station_name', 'hour'], how='outer')
    merged_data = merged_data.fillna(0)
    merged_data = merged_data.rename(columns={'count_x': 'start_count', 'count_y': 'end_count'})
    merged_data['deficit'] = merged_data['start_count'] - merged_data['end_count']
    merged_data.to_csv('output_files/csv_files/' + month + '_hourly_rent_return.csv')
    # end_hourly_counts = data.groupby('end_hour').size().reset_index(name='count')
    # distribution = hourly_counts['count'].tolist()
    # Clean up - remove the temporary extracted folder
    os.remove(csv_path)
    os.rmdir('temp_extracted_folder')


daily_distribution_month('202212')
