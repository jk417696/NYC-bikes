import folium
import webbrowser
import pandas as pd
from get_station_list_from_csv import get_station_list
import branca.colormap as cm


# NYC coordinates
nyc_coords = (40.7128, -74.0060)

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

nyc_map = folium.Map(location=nyc_coords, zoom_start=12)
folium.TileLayer('cartodbdark_matter').add_to(nyc_map)
min_val = data['deficit'].min()
max_val = data['deficit'].max()

color_palette = ['#ff5e0e', '#ffa172', '#ffdfcf', '#c3eee9', '#60d1c3', '#008575']

colormap = cm.StepColormap(colors=color_palette,

                           # colors=['red', 'orangered', 'orange', 'yellowgreen', 'lawngreen', 'green'],
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

nyc_map.save("output_files/maps/nyc_map_deficit_dark.html")
webbrowser.open("output_files/maps/nyc_map_deficit_dark.html")
