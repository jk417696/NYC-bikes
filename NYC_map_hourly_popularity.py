import folium
import webbrowser
import pandas as pd
import branca.colormap as cm
import os
import zipfile


def hourly_popularity_map_over_weekday(month: str, day_of_week: int):
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

    deficit_data = pd.read_csv('output_files/csv_files/' + month + '_hourly_rent_return_' + str(day_of_week) + '.csv')
    station_names = data['start_station_name'].unique()

    min_val = deficit_data['popularity'].min()
    max_val = deficit_data['popularity'].max()
    color_palette = ['#008575', '#c3eee9', '#ffa172', '#ff5e0e']
    color_palette = ['#008575', '#ffa172', '#ff5e0e']

    colormap = cm.StepColormap(colors=color_palette,
                               # colors=['red', 'orangered', 'orange', 'yellowgreen', 'lawngreen', 'green'],
                               index=[0, 1, 4, max_val],
                               vmin=min_val,
                               vmax=max_val)

    new_dir = 'output_files/maps/maps_for_gif/' + month + '_day_of_week_' + str(day_of_week)
    # os.mkdir(new_dir)

    for hour in range(24):
        temp_data = deficit_data[deficit_data['hour'] == hour]
        nyc_map = folium.Map(location=nyc_coords, zoom_start=12)
        folium.TileLayer('cartodbdark_matter').add_to(nyc_map)

        for item in station_names:
            lat = data[data['start_station_name'] == item]['start_lat'].tolist()[0]
            lon = data[data['start_station_name'] == item]['start_lng'].tolist()[0]
            if temp_data[temp_data['station_name'] == item]['popularity'].tolist():
                value = temp_data[temp_data['station_name'] == item]['popularity'].tolist()[0]
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
        hour_1 = hour+1
        legend_html = f'''
        <div style="position: fixed; bottom: 50px; left: 50px; z-index: 1000; padding: 10px; background-color: gainsboro; border: 2px solid grey; border-radius: 5px;">
          <p><strong>LEGEND</strong></p>
          <p><strong>Average station popularity on Monday in July 2022</strong></p>
          <p><strong>{hour}:00 - {hour_1}:00</strong></p>
          <p>Bike station popularity</p>
        '''

        color_palette = ['#008575', '#c3eee9', '#ffa172', '#ff5e0e']
        legend_data = {
            '< 2': '#008575',
            '2 to 5': '#ffa172',
            '> 5': '#ff5e0e'
        }

        for category, color in legend_data.items():
            legend_html += f'<p><i class="fa fa-circle" style="color:{color};"></i> {category}</p>'

        legend_html += '</div>'
        nyc_map.get_root().html.add_child(folium.Element(legend_html))
        file_dir = new_dir + '/' + month + 'day_of_week_' + str(day_of_week) + '_hour_' + str(hour) + ".html"
        nyc_map.save(file_dir)

    # Clean up - remove the temporary extracted folder
    os.remove(csv_path)
    os.rmdir('temp_extracted_folder')
    return data


# hourly_popularity_map_over_weekday('202208', day_of_week=3)
hourly_popularity_map_over_weekday('202207', day_of_week=0)
