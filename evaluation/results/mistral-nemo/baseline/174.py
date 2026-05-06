import geopandas as gpd
from shapely.geometry import Point
import folium

# Load the data of Emel and Tenteck rivers
emel = gpd.read_file('emel.shp')
tenteck = gpd.read_file('tenteck.shp')

# Create a GeoDataFrame for intersection points
intersection_points = gpd.GeoDataFrame(columns=['geometry'], crs='EPSG:4326')

# Find the intersection points between Emel and Tenteck rivers
for idx, row in emel.iterrows():
    if tenteck.intersects(row['geometry']):
        point = Point(row['geometry'].intersection(tenteck.iloc[0]['geometry']).centroid.xy)
        intersection_points = intersection_points.append({'geometry': point}, ignore_index=True)

# Save the intersection points as a shapefile
intersection_points.to_file('intersection_points.shp')

# Load the intersection points data for visualization
points_data = gpd.read_file('intersection_points.shp')

# Create a Folium map centered on the average coordinates of the intersection points
m = folium.Map(location=[points_data['geometry'].centroid.y.mean(), points_data['geometry'].centroid.x.mean()], zoom_start=10)

# Add the intersection points to the map
for idx, row in points_data.iterrows():
    folium.CircleMarker(location=(row['geometry'].y, row['geometry'].x), radius=5).add_to(m)

# Save the final map as an HTML file
m.save("174.html")