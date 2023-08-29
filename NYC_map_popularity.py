import folium
import webbrowser
import pandas as pd
from get_station_list_from_csv import get_station_list
import branca.colormap as cm


# NYC coordinates
nyc_coords = (40.7128, -74.0060)

station_data = get_station_list('202212')

data = pd.read_csv('output_files/csv_files/202212_bike_deficit.csv')

nyc_map = folium.Map(location=nyc_coords, zoom_start=12)
folium.TileLayer('cartodbdark_matter').add_to(nyc_map)
min_val = data['popularity'].min()
max_val = data['popularity'].max()

# color_palette = ['#ff5e0e', '#ffa172', '#ffdfcf', '#c3eee9', '#60d1c3', '#008575']
color_palette = ['#008575', '#c3eee9', '#ffa172', '#ff5e0e']


# Index values are quantiles
colormap = cm.StepColormap(colors=color_palette,
                           index=[min_val, 400, 1000, 2800, max_val],
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

title_html = '''
<h3 align="center" style="font-size:20px"><b>Bike stations popularity in NYC</b></h3>
'''
nyc_map.get_root().html.add_child(folium.Element(title_html))

legend_html = '''
<div style="position: fixed; bottom: 50px; left: 50px; z-index: 1000; padding: 10px; background-color: gainsboro; border: 2px solid grey; border-radius: 5px;">
  <p><strong>LEGEND</strong></p>
  <p>Number of bikes rented and return in a month</p>
'''

color_palette = ['#008575', '#c3eee9', '#ffa172', '#ff5e0e']

legend_data = {
    '< 400': '#008575',
    '400 to 1000': '#c3eee9',
    '1000 to 2800': '#ffa172',
    '> 2800': '#ff5e0e'
}

for category, color in legend_data.items():
    legend_html += f'<p><i class="fa fa-circle" style="color:{color};"></i> {category}</p>'

legend_html += '</div>'
nyc_map.get_root().html.add_child(folium.Element(legend_html))

nyc_map.save("output_files/maps/nyc_map_popularity_dark.html")
webbrowser.open("output_files/maps/nyc_map_popularity_dark.html")
