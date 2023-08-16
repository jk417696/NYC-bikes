import zipfile
import pandas as pd
import os
import calendar


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
        data['hour'] = data['starttime'].dt.hour
    else:
        data['started_at'] = pd.to_datetime(data['started_at'])
        data['hour'] = data['started_at'].dt.hour
    hourly_counts = data.groupby('hour').size().reset_index(name='count')
    distribution = hourly_counts['count'].tolist()
    # Clean up - remove the temporary extracted folder
    os.remove(csv_path)
    os.rmdir('temp_extracted_folder')
    return distribution


def daily_distribution_over_year(year: str):
    """
    :param year: year to analyse
    """
    directory_path = 'data/' + year
    files = os.listdir(directory_path)
    files = sorted(files)
    yearly_distibution = []
    for file in files:
        if os.path.isfile(os.path.join(directory_path, file)):
            month = str(file[:6])
            yearly_distibution.append(daily_distribution_month(month))
    return yearly_distibution


def create_dataframe_monthly_distribution(year: str):
    columns = ['Hour']
    months = list(calendar.month_name)[1:]
    for month in months:
        columns.append(month)
    hour = [x for x in range(24)]
    lst = []
    lst.append(hour)
    df = daily_distribution_over_year(year)
    for month in df:
        lst.append(month)
    lst = list(map(list, zip(*lst)))
    df = pd.DataFrame(lst, columns=columns)
    return df


# df_2015 = create_dataframe_monthly_distribution('2015')
# df_2020 = create_dataframe_monthly_distribution('2020')
# df_2021 = create_dataframe_monthly_distribution('2021')
# df_2022 = create_dataframe_monthly_distribution('2022')

# df_2015.to_csv('output_files/csv_files/daily_distribution_2015')
# df_2020.to_csv('output_files/csv_files/daily_distribution_2020')
# df_2021.to_csv('output_files/csv_files/daily_distribution_2021')
# df_2022.to_csv('output_files/csv_files/daily_distribution_2022')
