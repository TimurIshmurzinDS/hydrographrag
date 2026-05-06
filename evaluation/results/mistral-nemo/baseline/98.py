import geopandas as gpd
import psycopg2
from folium import Map, Marker, GeoJson

# Connect to the database
conn = psycopg2.connect(
    dbname="your_database_name",
    user="your_username",
    password="your_password",
    host="your_host",
    port="your_port"
)

cur = conn.cursor()

# Query rivers with names 'Тентек' and 'Быж'
query = "SELECT * FROM rivers WHERE name = 'Тентек' OR name = 'Быж';"
cur.execute(query)
rivers = cur.fetchall()

# Get watersheds for each river
watersheds_query = "SELECT ws.name FROM watersheds ws JOIN rivers r ON ws.id = r.watershed_id WHERE r.id = %s;"
watersheds = []
for river in rivers:
    cur.execute(watersheds_query, (river[0],))
    watershed_name = cur.fetchone()[0]
    watersheds.append(watershed_name)

# Close the database connection
cur.close()
conn.close()

# Load rivers and watersheds data from shapefiles
rivers_gdf = gpd.read_file("path/to/rivers.shp")
watersheds_gdf = gpd.read_file("path/to/watersheds.shp")

# Create a map using folium
m = Map(location=[50, 10], zoom_start=4)

# Add rivers to the map
for _, river in rivers_gdf.iterrows():
    if river['name'] in ['Тентек', 'Быж']:
        GeoJson(river[geometry]).add_to(m)

# Add watersheds to the map with labels
for _, ws in watersheds_gdf.iterrows():
    if ws['name'] in watersheds:
        Marker(location=[ws.geometry.centroid.y, ws.geometry.centroid.x], popup=ws['name']).add_to(m)

# Save the map as HTML file
m.save("98.html")