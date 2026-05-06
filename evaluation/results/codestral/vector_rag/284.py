import geopandas as gpd
import folium
from shapely import wkt

# Load the shapefile and convert to CRS 'EPSG:4326'
gdf = gpd.read_file(r"data/basin_data.shp")
gdf = gdf.to_crs('EPSG:4326')

# Initialize folium map using the centroid of the shapefile
m = folium.Map(location=[gdf['geometry'].centroid.y.mean(), gdf['geometry'].centroid.x.mean()], tiles='CartoDB positron')

# Add the basin to the map
folium.GeoJson(gdf, style_function=lambda x: {'fillColor': 'green', 'color': 'darkgreen', 'fillOpacity': 0.2}).add_to(m)

# Since context does not contain Coordinates (WKT), we assume that the data is already included in the shapefile and can be visualized or analyzed directly from it

# Save the final map
m.save("284.html")