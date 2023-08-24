import os
import zipfile
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import matplotlib.ticker as ticker
from datetime import datetime
import math
import plotly.express as px


def duration_vs_member(month: str):
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
    elif int(month) >= 201610 and int(month) <= 201703:
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


    # Clean
    os.remove(csv_path)
    os.rmdir('temp_extracted_folder')

    # Create boxplots
    fig = px.box(data, x=member_colname, y="tripduration")
    fig.update_yaxes(range=[0, 60])
    fig.show()

    return data


print(duration_vs_member('201703'))
