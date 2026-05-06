import pandas as pd
import geopandas as gpd
from shapely.geometry import Point
import folium

# Load historical flood records (Assuming CSV format with columns: 'Year', 'Flood_Event')
flood_data = pd.read_csv('historical_floods.csv')

# Convert data to GeoDataFrame
geometry = [Point(xy) for xy in zip(flood_data['Longitude'], flood_data['Latitude'])]
gdf = gpd.GeoDataFrame(flood_data, geometry=geometry)

# Aggregate data by years and calculate the number of flood events per year
floods_by_year = gdf.groupby('Year').size().reset_index(name='Flood_Count')

# Calculate mean flood count to determine extreme years (e.g., above mean + 1 standard deviation)
mean_flood_count = floods_by_year['Flood_Count'].mean()
std_dev_flood_count = floods_by_year['Flood_Count'].std()

extreme_years = floods_by_year[floods_by_year['Flood_Count'] > (mean_flood_count + std_dev_flood_count)]['Year']

# Create a map centered around the Kishi Osek River
m = folium.Map(location=[43.8563, 39.7021], zoom_start=8)

# Add extreme flood years as markers with custom icons
for year in extreme_years:
    folium.Marker([43.8563, 39.7021], popup=f" Extreme Flood Year: {year}", icon=folium.Icon(color='red')).add_to(m)

# Save the final map as "200.html"
m.save("200.html")