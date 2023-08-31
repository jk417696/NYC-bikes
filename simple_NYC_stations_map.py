import folium
import webbrowser
import os
import pandas as pd
import zipfile
from get_station_list_from_csv import get_station_list


# NYC coordinates
nyc_coords = (40.7128, -74.0060)

# station_data = get_station_list('202306')

def input_csv_from_zip(month: str):
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
    station_names = data['start_station_name'].unique()
    print(len(station_names))
    print(data.columns)
    nyc_map = folium.Map(location=nyc_coords, zoom_start=12)
    for item in station_names:
        temp_df = data[data['start_station_name'] == item]
        print(temp_df.head(n=1))
        lat = temp_df['start_lat'].tolist()[0]
        lon = temp_df['start_lng'].tolist()[0]
        # Create a CircleMarker
        folium.Marker(
            location=[lat, lon],
            radius=10,  # Adjust the radius as needed
            fill=True,
            popup=item
        ).add_to(nyc_map)

    title_html = '''
    <h3 align="center" style="font-size:20px"><b>NYC Citi Bikes network as of June 2023</b></h3>
    '''
    nyc_map.get_root().html.add_child(folium.Element(title_html))

    nyc_map.save("output_files/maps/nyc_map_stations.html")
    webbrowser.open("output_files/maps/nyc_map_stations.html")
    # Clean up - remove the temporary extracted folder
    os.remove(csv_path)
    os.rmdir('temp_extracted_folder')

input_csv_from_zip('202306')

# nyc_map = folium.Map(location=nyc_coords, zoom_start=12)
# lat_list = []
# for item in station_data:
#     lat = item['latitude']
#     lon = item['longitude']
#     lat_list.append(lat)
#     # Create a CircleMarker
#     folium.Marker(
#         location=[lat, lon],
#         radius=10,  # Adjust the radius as needed
#         fill=True,
#         popup=item['name']
#     ).add_to(nyc_map)
#
# title_html = '''
# <h3 align="center" style="font-size:20px"><b>NYC Citi Bikes network as of June 2023</b></h3>
# '''
# nyc_map.get_root().html.add_child(folium.Element(title_html))
#
# nyc_map.save("output_files/maps/nyc_map_stations.html")
# webbrowser.open("output_files/maps/nyc_map_stations.html")
