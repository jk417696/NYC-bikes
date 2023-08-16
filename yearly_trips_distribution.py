import os
import zipfile
import pandas as pd
import calendar


def iterate_over_files_year(year: str):
    """
    :param year: year to analyse
    """
    directory_path = 'data/' + year
    files = os.listdir(directory_path)
    files = sorted(files)
    monthly_trips = []
    for file in files:
        if os.path.isfile(os.path.join(directory_path, file)):
            month = str(file[:6])
            monthly_trips.append(trips_number_month(month))
    return monthly_trips


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


months = list(calendar.month_name)[1:]
columns = ['months', '2014', '2015', '2016', '2017', '2018', '2019', '2020', '2021', '2022']

y_2014 = iterate_over_files_year('2014')
y_2015 = iterate_over_files_year('2015')
y_2016 = iterate_over_files_year('2016')
y_2017 = iterate_over_files_year('2017')
y_2018 = iterate_over_files_year('2018')
y_2019 = iterate_over_files_year('2019')
y_2020 = iterate_over_files_year('2020')
y_2021 = iterate_over_files_year('2021')
y_2022 = iterate_over_files_year('2022')

df = pd.DataFrame({'months': months, '2014': y_2014, '2015': y_2015, '2016': y_2016, '2017': y_2017, '2018': y_2018,
                   '2019': y_2019, '2020': y_2020, '2021': y_2021, '2022': y_2022},
                  columns=columns)
df.to_csv('output_files/csv_files/yearly_distributions.csv')
print(df)
