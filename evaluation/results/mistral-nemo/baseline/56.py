import geopandas as gpd
import pandas as pd
from scipy.interpolate import griddata
import folium

# Load data (Assuming you have a CSV file with columns: 'longitude', 'latitude', 'sediment_load')
data = pd.read_csv('sediment_data.csv')

# Create a GeoDataFrame from the data
gdf = gpd.GeoDataFrame(data, geometry=gpd.points_from_xy(data.longitude, data.latitude))

# Interpolate sediment load values to create a surface
xi = [p.x for p in gdf.geometry]
yi = [p.y for p in gdf.geometry]
zi = gdf['sediment_load']
grid_x, grid_y = np.mgrid[min(xi):max(xi):100j, min(yi):max(yi):100j]
interpolated_z = griddata((xi, yi), zi, (grid_x, grid_y), method='cubic')

# Create time slices for the last 5 years and calculate average sediment load
years = ['2017', '2018', '2019', '2020', '2021']
for year in years:
    filtered_data = gdf[gdf['year'] == int(year)]
    avg_sediment_load = filtered_data['sediment_load'].mean()
    print(f"Average sediment load for {year}: {avg_sediment_load}")

# Visualize the results using Folium
m = folium.Map(location=[data.latitude.mean(), data.longitude.mean()], zoom_start=10)

for year in years:
    filtered_data = gdf[gdf['year'] == int(year)]
    avg_sediment_load = filtered_data['sediment_load'].mean()
    color = 'green' if avg_sediment_load < 50 else 'yellow' if avg_sediment_load < 100 else 'red'
    folium.GeoJson(
        data[filtered_data.index],
        style_function=lambda x, yz, z: {'fillColor': color, 'color': 'black', 'weight': 2},
        highlight_function=lambda x: {'fillColor': 'blue'}
    ).add_to(m)

m.save("56.html")