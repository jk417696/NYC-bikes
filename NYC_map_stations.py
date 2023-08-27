import folium
import webbrowser
import pandas as pd
from get_station_list_from_csv import get_station_list
import branca.colormap as cm


# NYC coordinates
nyc_coords = (40.7128, -74.0060)

nyc_map = folium.Map(location=nyc_coords, zoom_start=12)
folium.TileLayer('cartodbdark_matter').add_to(nyc_map)

station_data = get_station_list('202212')

# Add markers for each station
# for station in station_data:
#     folium.CircleMarker(
#         location=[station["latitude"], station["longitude"]],
#         radius=8,
#         color=colormap(station["deficit_normalized"]),
#         fill=True,
#         fill_color=colormap(station['deficit_normalized']),
#         fill_opacity=1,
#         popup=station["deficit_normalized"]
#     ).add_to(nyc_map)

# marker_cluster = MarkerCluster().add_to(nyc_map)

data = pd.read_csv('output_files/csv_files/202212_bike_deficit.csv')
deficit_normalized = data['deficit_normalized'].tolist()

nyc_map = folium.Map(location=nyc_coords, zoom_start=12)
folium.TileLayer('cartodbdark_matter').add_to(nyc_map)
min_val = data['deficit'].min()
max_val = data['deficit'].max()

colormap = cm.StepColormap(colors=['red', 'orangered', 'orange', 'yellowgreen', 'lawngreen', 'green'],
                           index=[min_val, -30, -10, 0, 10, 30, max_val],
                           vmin=min_val,
                           vmax=max_val)

for item in station_data:
    lat = item['latitude']
    lon = item['longitude']
    value = item['deficit']
    color = colormap(item['deficit'])

    # Create a CircleMarker
    folium.Circle(
        location=[lat, lon],
        radius=20,  # Adjust the radius as needed
        color=color,
        fill=True,
        popup=f"Number of rented/returned bikes: {value}"
    ).add_to(nyc_map)

nyc_map.save("nyc_map_deficit.html")
webbrowser.open("output_files/maps/nyc_map_deficit.html")
