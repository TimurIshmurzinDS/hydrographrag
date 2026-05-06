import requests
from folium import FeatureGroup, Icon, Map, Marker

# Replace this URL with the actual API or web scraping endpoint for Koktal River monitoring station status
url = "https://example.com/api/monitoring_stations/koktal_river/status"

response = requests.get(url)
status = response.json()["status"]

# Create a map centered at Koktal River location (replace lat and lon with actual coordinates)
m = Map(location=[43.2, 76.9], zoom_start=15)

fg_stations = FeatureGroup(name="Monitoring Stations")

if status == "active":
    icon_color = "green"
else:
    icon_color = "red"

icon = Icon(icon="info-sign", prefix="fa", color=icon_color)
marker = Marker(location=[43.2, 76.9], popup="Koktal River Monitoring Station<br>Status: {}".format(status), icon=icon)

fg_stations.add_child(marker)
m.add_child(fg_stations)

# Save the map as HTML file
m.save("4.html")