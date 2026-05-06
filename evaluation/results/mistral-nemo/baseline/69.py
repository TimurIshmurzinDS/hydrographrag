import pandas as pd
import geopandas as gpd
import folium

# Load data from CSV files
koktal_data = pd.read_csv('koktal_river_sensors.csv')
aksu_data = pd.read_csv('aksu_river_sensors.csv')

# Create lists for each river's sensors
koktal_list = [(row['latitude'], row['longitude'], row['status']) for _, row in koktal_data.iterrows()]
aksu_list = [(row['latitude'], row['longitude'], row['status']) for _, row in aksu_data.iterrows()]

# Create GeoDataFrame for each river's sensors
koktal_gdf = gpd.GeoDataFrame(koktal_list, columns=['Latitude', 'Longitude', 'Status'], geometry=gpd.points_from_xy(koktal_list[0], koktal_list[1]))
aksu_gdf = gpd.GeoDataFrame(aksu_list, columns=['Latitude', 'Longitude', 'Status'], geometry=gpd.points_from_xy(aksu_list[0], aksu_list[1]))

# Create map for Koktal River sensors
koktal_map = folium.Map(location=[koktal_gdf['Latitude'].mean(), koktal_gdf['Longitude'].mean()], zoom_start=8)
for _, row in koktal_gdf.iterrows():
    if row['Status'] == 'active':
        color = 'green'
    else:
        color = 'red'
    folium.CircleMarker(location=[row['Latitude'], row['Longitude']], radius=5, color=color).add_to(koktal_map)
koktal_map.save("koktal.html")

# Create map for Aksu River sensors
aksu_map = folium.Map(location=[aksu_gdf['Latitude'].mean(), aksu_gdf['Longitude'].mean()], zoom_start=8)
for _, row in aksu_gdf.iterrows():
    if row['Status'] == 'active':
        color = 'green'
    else:
        color = 'red'
    folium.CircleMarker(location=[row['Latitude'], row['Longitude']], radius=5, color=color).add_to(aksu_map)
aksu_map.save("aksu.html")