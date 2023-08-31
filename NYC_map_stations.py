import folium
import webbrowser
import pandas as pd
from get_station_list_from_csv import get_station_list
import branca.colormap as cm


# NYC coordinates
nyc_coords = (40.7128, -74.0060)

station_data = get_station_list('202203')

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

data = pd.read_csv('output_files/csv_files/202203_bike_deficit.csv')

nyc_map = folium.Map(location=nyc_coords, zoom_start=12)
folium.TileLayer('cartodbdark_matter').add_to(nyc_map)
min_val = data['popularity'].min()
max_val = data['popularity'].max()

color_palette = ['#ff5e0e', '#ffa172', '#ffdfcf', '#c3eee9', '#60d1c3', '#008575']
color_palette = ['#008575', '#c3eee9', '#ffa172', '#ff5e0e']

colormap = cm.StepColormap(colors=color_palette,

                           # colors=['red', 'orangered', 'orange', 'yellowgreen', 'lawngreen', 'green'],
                           index=[min_val, 500, 1500, 3000, max_val],
                           vmin=0,
                           vmax=max_val)

for item in station_data:
    lat = item['latitude']
    lon = item['longitude']
    value = item['popularity']
    color = colormap(item['popularity'])
    station = item['name']
    # Create a CircleMarker
    folium.Circle(
        location=[lat, lon],
        radius=20,  # Adjust the radius as needed
        color=color,
        fill=True,
        popup=f"{station} Popularity: {value}"
    ).add_to(nyc_map)

title_html = '''
<h3 align="center" style="font-size:20px"><b>Bike stations popularity in NYC</b></h3>
'''
nyc_map.get_root().html.add_child(folium.Element(title_html))

legend_html = '''
<div style="position: fixed; bottom: 50px; left: 50px; z-index: 1000; padding: 10px; background-color: gainsboro; border: 2px solid grey; border-radius: 5px;">
  <p><strong>LEGEND</strong></p>
  <p>Bike stations popularity in March 2022</p>
'''

color_palette = ['#ff5e0e', '#ffa172', '#ffdfcf', '#c3eee9', '#60d1c3', '#008575']
legend_data = {
    '0 to 500': '#008575',
    '501 to 1500': '#c3eee9',
    '1501 to 3000': '#ffa172',
    '> 3000': '#ff5e0e'
}

for category, color in legend_data.items():
    legend_html += f'<p><i class="fa fa-circle" style="color:{color};"></i> {category}</p>'

legend_html += '</div>'
nyc_map.get_root().html.add_child(folium.Element(legend_html))

nyc_map.save("output_files/maps/nyc_map_popularity_202203.html")
webbrowser.open("output_files/maps/nyc_map_popularity_202203.html")
