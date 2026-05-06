import geopandas as gpd
import folium
from shapely import wkt

# Load the shapefile strictly using a raw string
gdf = gpd.read_file(r"data/basin_data.shp")
gdf = gdf.to_crs('EPSG:4326')

# Initialize folium.Map using the centroid of the shapefile and parameter tiles='CartoDB positron'
m = folium.Map(location=gdf.centroid.iloc[0], zoom_start=10, tiles='CartoDB positron')

# Add the basin to the map using folium.GeoJson (fillColor='green', color='darkgreen', fillOpacity=0.2)
folium.GeoJson(data=gdf.to_json(), name='basin').add_to(m)

# Create a hardcoded list of dictionaries for river coordinates
river_coordinates = [
    {'name': 'Каратал', 'length_km': 120, 'coordinates': wkt.loads('POINT(75.0 45.0)')},
    {'name': 'Кокталь', 'length_km': 80, 'coordinates': wkt.loads('POINT(76.0 46.0)')},
    {'name': 'Баянкола', 'length_km': 60, 'coordinates': wkt.loads('POINT(77.0 47.0)')}
]

# Calculate the total length of rivers
total_length = sum(r['length_km'] for r in river_coordinates)

# Add markers to the map for each river
for river in river_coordinates:
    folium.Marker(location=river['coordinates'].coords[0], popup=f"{river['name']}: {river['length_km']} км").add_to(m)

# Save the final map
m.save("93.html")