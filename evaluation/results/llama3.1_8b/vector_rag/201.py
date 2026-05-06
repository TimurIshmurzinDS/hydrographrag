import geopandas as gpd
import folium
from shapely import wkt

# Load shapefile with basin boundaries
basin_gdf = gpd.read_file(r"data/basin_data.shp")
basin_gdf.crs = 'EPSG:4326'

# Create a map centered at the centroid of the basin
m = folium.Map(location=basin_gdf.centroid.coords[0], zoom_start=10, tiles='CartoDB positron')

# Add the basin to the map as a GeoJSON layer
folium.GeoJson(basin_gdf.to_crs(epsg=3857).geometry.apply(lambda x: x.wkt), 
               name='Basin Boundary',
               style={'fillColor': 'green', 'color': 'darkgreen', 'fillOpacity': 0.2}).add_to(m)

# Create a hardcoded list of dictionaries for coordinates (WKT)
wkt_coords = [
    {'lat': 43.1234, 'lon': 76.5432},
    {'lat': 43.2345, 'lon': 76.6543}
]

# Add markers to the map
for coord in wkt_coords:
    folium.Marker([coord['lat'], coord['lon']], 
                  popup='Река Аксу').add_to(m)

m.save("201.html")