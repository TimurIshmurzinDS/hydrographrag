import geopandas as gpd
import folium
from shapely import wkt

# Load the basin data
basin = gpd.read_file(r"data/basin_data.shp")
basin = basin.to_crs('EPSG:4326')

# Initialize folium map
m = folium.Map(location=[basin.centroid.y.mean(), basin.centroid.x.mean()], tiles='CartoDB positron')

# Add the basin to the map
folium.GeoJson(basin, style_function=lambda x: {'fillColor': 'green', 'color': 'darkgreen', 'fillOpacity': 0.2}).add_to(m)

# Hardcoded coordinates for demonstration purposes
# In a real-world application, replace these with actual data
terisbuthak_creek = {'name': 'Terisbuthak Creek', 'geometry': wkt.loads('POINT (51.2048 71.4369)')}
talgar_river = {'name': 'Talgar River', 'geometry': wkt.loads('LINESTRING (51.1987 71.4283, 51.2087 71.4383)')}

# Convert to GeoDataFrame
gdf = gpd.GeoDataFrame([terisbuthak_creek, talgar_river], geometry='geometry', crs='EPSG:4326')

# Add the creek and river to the map
for idx, row in gdf.iterrows():
    if row['geometry'].geom_type == 'Point':
        folium.Marker(location=[row['geometry'].y, row['geometry'].x], popup=row['name']).add_to(m)
    elif row['geometry'].geom_type == 'LineString':
        folium.PolyLine(locations=[[p.y, p.x] for p in row['geometry'].coords], color='blue', weight=2.5, opacity=1).add_to(m)

# Calculate the distance between the creek and river
distance = gdf.iloc[0]['geometry'].distance(gdf.iloc[1]['geometry'])
folium.Marker([gdf['geometry'][0].y, gdf['geometry'][0].x], icon=folium.DivIcon(html=f"<div style='font-size: 12; color: red;'>{distance:.2f} km</div>")).add_to(m)

# Save the map
m.save("176.html")