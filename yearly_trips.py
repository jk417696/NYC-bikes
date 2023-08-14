import os
import zipfile
import pandas as pd


def trips_number_month(month: str):
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
    trips = len(data)
    # Clean up - remove the temporary extracted folder
    os.remove(csv_path)
    os.rmdir('temp_extracted_folder')
    return trips


def iterate_over_files_year(year: str, df_func):
    """
    :param year: year to analyse
    :param df_func: function that produces output with a structure same as in "parse_local_csv_file"
    """
    directory_path = 'data/' + year
    files = os.listdir(directory_path)
    files = sorted(files)
    yearly_trips = 0
    for file in files:
        if os.path.isfile(os.path.join(directory_path, file)):
            month = str(file[:6])
            yearly_trips += df_func(month)
    return yearly_trips


def iterate_over_all_files(df_func):
    directory_path = 'data/'
    years = os.listdir(directory_path)
    years = sorted(years)
    yearly_trips = []
    for year in years:
        yearly_trips.append((year, iterate_over_files_year(year, df_func)))
    return yearly_trips


df = iterate_over_all_files(trips_number_month)
columns = ['Year', 'Yearly_trips']
df = pd.DataFrame(df, columns=columns)
df.to_csv('output_files/csv_files/yearly_trips.csv')
