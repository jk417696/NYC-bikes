import folium
import webbrowser
from get_station_list_from_csv import get_station_list

# NYC coordinates
nyc_coords = (40.7128, -74.0060)

# Create a map centered on NYC
nyc_map = folium.Map(location=nyc_coords, zoom_start=12)

# Example station data (replace with actual station data)
station_data = [
    {"name": "Station 1", "latitude": 40.1234, "longitude": -73.5678},
    {"name": "Station 2", "latitude": 40.5678, "longitude": -73.1234},
    # Add more station data here...
]

station_data = get_station_list('202212')

# Add markers for each station
for station in station_data:
    folium.Marker(
        location=[station["latitude"], station["longitude"]],
        popup=station["name"]
    ).add_to(nyc_map)

# Display the map
nyc_map.save("nyc_map.html")
webbrowser.open("nyc_map.html")