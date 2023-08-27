import os
import zipfile
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import matplotlib.ticker as ticker
from datetime import datetime
import math
import plotly.express as px
import imageio



def input_csv_from_zip(month: str):
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
    if int(month) >= 202102:
        member_colname = 'member_casual'
    elif 201610 <= int(month) <= 201703:
        member_colname = 'User Type'
    else:
        member_colname = 'usertype'
    csv_path = 'temp_extracted_folder/' + csv_file_name
    if int(month) < 202102:
        data = pd.read_csv(csv_path, low_memory=False, usecols=['tripduration', member_colname])
        data.tripduration = data.tripduration/60
    else:
        data = pd.read_csv(csv_path, low_memory=False, usecols=['started_at', 'ended_at', member_colname])
        data['tripduration'] = (pd.to_datetime(data.ended_at) - pd.to_datetime(data.started_at)).dt.total_seconds()/60
        data = data.drop(['started_at', 'ended_at'], axis=1)
    data = data.rename(columns={member_colname: 'usertype'})
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
            data_year = pd.concat([data_year, input_csv_from_zip(month)])
    return data_year

def duration_vs_member(year: str):
    data = iterate_over_files_year(year)
    membertypes = ['Subscriber', 'Customer']
    # print(membertypes)
    df = []
    # for type in membertypes:
    #     print(data.tripduration[data.usertype.isin([type])].to_list())
    df.append(data.tripduration[data.usertype.isin(['member', 'Subscriber'])].to_list())
    df.append(data.tripduration[data.usertype.isin(['casual', 'Customer'])].to_list())
    # Create boxplots
    plt.style.use('ggplot')

    fig = plt.boxplot(df, labels=membertypes, patch_artist=True)
    for element in ['boxes', 'whiskers', 'fliers', 'medians', 'caps']:
        plt.setp(fig[element], color='black')
    plt.setp(fig['means'], color='darkred')
    for patch in fig['boxes']:
        patch.set(facecolor='#73c6b6')
    plt.title('Trip duration for different types of users in ' + year, color='#ff5e0e')
    plt.xlabel('User type', color='#695d46')
    plt.ylabel('Duration (in min)', color='#695d46')
    plt.ylim(0, 60)
    plt.savefig('./output_files/plots/duration_member/duration_member_'+year+'.png')
    plt.close()
    # fig.write_image('./output_files/plots/duration_member_' + year + '.png')


# duration_vs_member('2022')
figure = []
for year in range(2014, 2023):
    image = imageio.v2.imread('./output_files/plots/duration_member/duration_member_' + str(year) + '.png')
    figure.append(image)
imageio.mimsave('./output_files/gifs/duration_member.gif', figure, duration=300, loop=10)


