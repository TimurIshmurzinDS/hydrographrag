import geopandas as gpd
import pandas as pd
from shapely.geometry import Point
import folium

# 1. Подготовка данных
def prepare_data(river_height_data, toi_points):
    # Load river height data and TOI points into GeoDataFrame
    rivers_gdf = gpd.GeoDataFrame(river_height_data, geometry=gpd.points_from_xy(river_height_data['lon'], river_height_data['lat']))
    toi_gdf = gpd.GeoDataFrame(toi_points, geometry=[Point(xy) for xy in toi_points])

    # Merge TOI points with river height data based on location
    merged_gdf = gpd.sjoin(toi_gdf, rivers_gdf, how='left', op='within')

    return merged_gdf

# 2. Анализ риска
def analyze_risk(merged_gdf):
    # Calculate flood risk for each TOI point based on river height and other factors
    merged_gdf['flood_risk'] = merged_gdf.apply(lambda row: calculate_flood_risk(row), axis=1)

    return merged_gdf

# 3. Визуализация результатов
def visualize_results(merged_gdf):
    # Create a folium map centered on the average location of TOI points
    m = folium.Map(location=[merged_gdf['lat'].mean(), merged_gdf['lon'].mean()], zoom_start=8)

    # Add TOI points to the map with different colors based on flood risk level
    for _, row in merged_gdf.iterrows():
        color = 'green' if row['flood_risk'] <= 0.3 else 'yellow' if row['flood_risk'] <= 0.6 else 'orange' if row['flood_risk'] <= 0.9 else 'red'
        folium.CircleMarker(location=[row['lat'], row['lon']], radius=5, color=color).add_to(m)

    # Save the map as HTML file
    m.save("159.html")

# Example usage:
river_height_data = pd.read_csv('river_height_data.csv')
toi_points = [(56.02, 63.01), (55.98, 63.04), ...] # List of TOI points as tuples of (lat, lon)

merged_gdf = prepare_data(river_height_data, toi_points)
analyzed_gdf = analyze_risk(merged_gdf)
visualize_results(analyzed_gdf)