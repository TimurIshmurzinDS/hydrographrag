import geopandas as gpd
import pandas as pd
from shapely.geometry import Point
import folium

# Load inflation data (Assuming it's a CSV file with columns: 'Region', 'Latitude', 'Longitude', 'Inflation_Rate')
inflation_data = pd.read_csv('inflation_data.csv')

# Create a GeoDataFrame from the inflation data
geometry = [Point(lon, lat) for lon, lat in zip(inflation_data['Longitude'], inflation_data['Latitude'])]
gdf_inflation = gpd.GeoDataFrame(inflation_data, geometry=geometry)
gdf_inflation.crs = 'EPSG:4326'  # Set CRS to WGS84

# Load Sharyn River basin polygon data (Assuming it's a shapefile with the appropriate projection)
river_basin = gpd.read_file('sharyn_river_basin.shp')

# Perform spatial join to get average inflation rates within the river basin
merged = gpd.sjoin(gdf_inflation, river_basin, how='inner', op='intersects')
avg_inflation = merged.groupby('Region')['Inflation_Rate'].mean()

# Create a Folium map centered on Sharyn River
m = folium.Map(location=[50.7481, 69.2385], zoom_start=8)  # Approximate coordinates of Sharyn River

# Add inflation data points to the map with color based on inflation rate
for idx, row in gdf_inflation.iterrows():
    folium.CircleMarker(
        location=[row['Latitude'], row['Longitude']],
        radius=5,
        color='blue',
        fill=True,
        fill_opacity=0.6,
        popup=f'Region: {row["Region"]}\nInflation Rate: {row["Inflation_Rate"]}%'
    ).add_to(m)

# Save the map as HTML
m.save("272.html")