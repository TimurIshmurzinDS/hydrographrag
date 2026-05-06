import geopandas as gpd
import folium
from shapely import wkt

# Load the shapefile
basin_data = gpd.read_file(r"data/basin_data.shp")
basin_data = basin_data.to_crs('EPSG:4326')

# Initialize folium map
m = folium.Map(location=[basin_data['geometry'].centroid.y.mean(), basin_data['geometry'].centroid.x.mean()], tiles='CartoDB positron')

# Add the basin to the map
folium.GeoJson(basin_data, style_function=lambda x: {'fillColor': 'green', 'color': 'darkgreen', 'fillOpacity': 0.2}).add_to(m)

# Hardcoded list of dictionaries with WKT coordinates and population data
regions = [
    {"location": "POLYGON ((...))", "population": 1000},
    # Add more regions as needed
]

# Convert WKT to Shapely geometry objects
for region in regions:
    region['geometry'] = wkt.loads(region['location'])

# Create a GeoDataFrame
gdf = gpd.GeoDataFrame(regions, geometry='geometry')

# Add population data to the map
m.choropleth(geo_data=gdf, data=gdf, columns=['population'], key_on='feature.id', fill_color='YlGnBu', legend_name="Population")

# Save the final map
m.save("278.html")