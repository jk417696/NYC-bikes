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

data = pd.read_csv('output_files/csv_files/202212_bike_deficit.csv')

nyc_map = folium.Map(location=nyc_coords, zoom_start=12)
folium.TileLayer('cartodbdark_matter').add_to(nyc_map)
min_val = data['popularity'].min()
max_val = data['popularity'].max()


# Index values are quantiles
colormap = cm.StepColormap(colors=['greenyellow', 'yellow', 'orangered', 'red'],
                           index=[min_val, 403, 981, 2798, max_val],
                           vmin=min_val,
                           vmax=max_val)

for item in station_data:
    lat = item['latitude']
    lon = item['longitude']
    value = item['popularity']
    color = colormap(item['popularity'])

    # Create a CircleMarker
    folium.Circle(
        location=[lat, lon],
        radius=20,  # Adjust the radius as needed
        color=color,
        fill=True,
        popup=f"Total number of rented and returned bikes: {value}"
    ).add_to(nyc_map)

nyc_map.save("nyc_map_popularity.html")
webbrowser.open("output_files/maps/nyc_map_popularity.html")
