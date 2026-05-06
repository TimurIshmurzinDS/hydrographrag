import geopandas as gpd
import pandas as pd
from shapely.geometry import Point
import folium

# Step 1: Load data
river_data = pd.read_csv('river_data.csv')
bio_diversity = pd.read_csv('bio_diversity.csv')

# Step 2: Model water level change (This is a simplified example, real modeling would require more complex hydrological models)
def model_water_level_change(current_level, reduction_percentage):
    new_level = current_level * (1 - reduction_percentage/100)
    return new_level

river_data['new_level'] = river_data.apply(lambda row: model_water_level_change(row['current_level'], 20), axis=1)

# Step 3: Analyze impact on flora and fauna
# This is a simplified example, real analysis would require more complex ecological models
def analyze_impact(new_level):
    if new_level < 5:
        return 'High Impact'
    elif new_level >= 5 and new_level < 10:
        return 'Medium Impact'
    else:
        return 'Low Impact'

river_data['impact'] = river_data['new_level'].apply(analyze_impact)

# Step 4: Visualize results on a map
geometry = [Point(xy) for xy in zip(river_data['longitude'], river_data['latitude'])]
gdf = gpd.GeoDataFrame(river_data, geometry=geometry)
map_russia = folium.Map(location=[55.7558, 37.6173], zoom_start=4)

for _, row in gdf.iterrows():
    folium.CircleMarker(
        location=(row['latitude'], row['longitude']),
        radius=5,
        color='blue',
        fill=True,
        fill_color='blue' if row['impact'] == 'Low Impact' else ('orange' if row['impact'] == 'Medium Impact' else 'red'),
        fill_opacity=0.7
    ).add_to(map_russia)

map_russia.save("113.html")