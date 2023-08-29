import folium
import webbrowser
import pandas as pd
from get_station_list_from_csv import get_station_list
import branca.colormap as cm
import os
import zipfile


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

    nyc_coords = (40.7128, -74.0060)

    deficit_data = pd.read_csv('output_files/csv_files/202212_hourly_rent_return.csv')
    station_names = data['start_station_name'].unique()

    min_val = deficit_data['deficit'].min()
    max_val = deficit_data['deficit'].max()
    color_palette = ['#ff5e0e', '#ffa172', '#ffdfcf', '#c3eee9', '#60d1c3', '#008575']

    colormap = cm.StepColormap(colors=color_palette,
                               # colors=['red', 'orangered', 'orange', 'yellowgreen', 'lawngreen', 'green'],
                               index=[min_val, -30, -10, 0, 10, 30, max_val],
                               vmin=min_val,
                               vmax=max_val)

    for hour in range(24):
        temp_data = deficit_data[deficit_data['hour'] == hour]
        nyc_map = folium.Map(location=nyc_coords, zoom_start=12)
        folium.TileLayer('cartodbdark_matter').add_to(nyc_map)

        for item in station_names:
            lat = data[data['start_station_name'] == item]['start_lat'].tolist()[0]
            lon = data[data['start_station_name'] == item]['start_lng'].tolist()[0]
            if temp_data[temp_data['station_name'] == item]['deficit'].tolist():
                value = temp_data[temp_data['station_name'] == item]['deficit'].tolist()[0]
            else:
                value = 0
            color = colormap(value)

            # Create a CircleMarker
            folium.Circle(
                location=[lat, lon],
                radius=20,  # Adjust the radius as needed
                color=color,
                fill=True,
                popup=f"Number of rented/returned bikes: {value}"
            ).add_to(nyc_map)

        title_html = '''
        <h3 align="center" style="font-size:20px"><b>Bikes deficit across stations in NYC</b></h3>
        '''
        nyc_map.get_root().html.add_child(folium.Element(title_html))

        legend_html = '''
        <div style="position: fixed; bottom: 50px; left: 50px; z-index: 1000; padding: 10px; background-color: gainsboro; border: 2px solid grey; border-radius: 5px;">
          <p><strong>LEGEND</strong></p>
          <p>Bikes rental to return ratio</p>
        '''

        color_palette = ['#ff5e0e', '#ffa172', '#ffdfcf', '#c3eee9', '#60d1c3', '#008575']
        legend_data = {
            '< -30': '#ff5e0e',
            '-30 to -10': '#ffa172',
            '-10 to 0': '#ffdfcf',
            '0 to 10': '#c3eee9',
            '10 to 30': '#60d1c3',
            '> 30': '#008575'
        }

        for category, color in legend_data.items():
            legend_html += f'<p><i class="fa fa-circle" style="color:{color};"></i> {category}</p>'

        legend_html += '</div>'
        nyc_map.get_root().html.add_child(folium.Element(legend_html))

        nyc_map.save("output_files/maps/maps_for_gif/nyc_" + str(hour) + ".html")
        webbrowser.open("output_files/maps/maps_for_gif/nyc_" + str(hour) + ".html")

    # Clean up - remove the temporary extracted folder
    os.remove(csv_path)
    os.rmdir('temp_extracted_folder')
    return data


input_csv_from_zip('202212')


# # NYC coordinates
# nyc_coords = (40.7128, -74.0060)
#
# station_data = pd.read_csv('output_files/csv_files/202212_hourly_rent_return.csv')
# station_names = station_data['station_name'].unique()
# print(station_names[:5])
# stations_dict = get_station_list('202212')
# print(stations_dict[0])
# for hour in range(3):
#     temp_data = station_data[station_data['hour'] == hour]
#     nyc_map = folium.Map(location=nyc_coords, zoom_start=12)
#     folium.TileLayer('cartodbdark_matter').add_to(nyc_map)
#
#     min_val = stations_dict['deficit'].min()
#     max_val = stations_dict['deficit'].max()
#
#     color_palette = ['#ff5e0e', '#ffa172', '#ffdfcf', '#c3eee9', '#60d1c3', '#008575']
#
#     colormap = cm.StepColormap(colors=color_palette,
#                                # colors=['red', 'orangered', 'orange', 'yellowgreen', 'lawngreen', 'green'],
#                                index=[min_val, -30, -10, 0, 10, 30, max_val],
#                                vmin=min_val,
#                                vmax=max_val)
#
#     for item in location_data:
#         lat = item['latitude']
#         lon = item['longitude']
#         value = item['deficit']
#         color = colormap(item['deficit'])
#
#         # Create a CircleMarker
#         folium.Circle(
#             location=[lat, lon],
#             radius=20,  # Adjust the radius as needed
#             color=color,
#             fill=True,
#             popup=f"Number of rented/returned bikes: {value}"
#         ).add_to(nyc_map)
#
#     title_html = '''
#     <h3 align="center" style="font-size:20px"><b>Bikes deficit across stations in NYC</b></h3>
#     '''
#     nyc_map.get_root().html.add_child(folium.Element(title_html))
#
#     legend_html = '''
#     <div style="position: fixed; bottom: 50px; left: 50px; z-index: 1000; padding: 10px; background-color: gainsboro; border: 2px solid grey; border-radius: 5px;">
#       <p><strong>LEGEND</strong></p>
#       <p>Bikes rental to return ratio</p>
#     '''
#
#     color_palette = ['#ff5e0e', '#ffa172', '#ffdfcf', '#c3eee9', '#60d1c3', '#008575']
#     legend_data = {
#         '< -30': '#ff5e0e',
#         '-30 to -10': '#ffa172',
#         '-10 to 0': '#ffdfcf',
#         '0 to 10': '#c3eee9',
#         '10 to 30': '#60d1c3',
#         '> 30': '#008575'
#     }
#
#     for category, color in legend_data.items():
#         legend_html += f'<p><i class="fa fa-circle" style="color:{color};"></i> {category}</p>'
#
#     legend_html += '</div>'
#     nyc_map.get_root().html.add_child(folium.Element(legend_html))
#
#     nyc_map.save("output_files/maps/nyc_map_deficit_dark.html")
#     webbrowser.open("output_files/maps/nyc_map_deficit_dark.html")