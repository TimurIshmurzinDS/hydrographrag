import geopandas as gpd
import pandas as pd
from shapely.geometry import Point
import folium

# 1. Load hydropost data and create a GeoDataFrame
hydroposts = pd.read_csv('hydroposts.csv')  # Assuming CSV file with columns: 'id', 'name', 'latitude', 'longitude', 'discharge'
geometry = [Point(lon, lat) for lon, lat in zip(hydroposts['longitude'], hydroposts['latitude'])]
gdf_hydroposts = gpd.GeoDataFrame(hydroposts, geometry=geometry)

# 2. Define risk categories based on discharge
def assess_risk(discharge):
    if discharge < 10:
        return 'Низкий риск'
    elif 10 <= discharge < 50:
        return 'Средний риск'
    else:
        return 'Высокий риск'

# 3. Add risk category to the GeoDataFrame
gdf_hydroposts['risk'] = gdf_hydroposts['discharge'].apply(assess_risk)

# 4. Create a map and add hydroposts with different colors based on risk level
m = folium.Map(location=[gdf_hydroposts['latitude'].mean(), gdf_hydroposts['longitude'].mean()], zoom_start=10)
for _, row in gdf_hydroposts.iterrows():
    color = 'green' if row['risk'] == 'Низкий риск' else ('yellow' if row['risk'] == 'Средний риск' else 'red')
    folium.CircleMarker(location=[row['latitude'], row['longitude']], radius=5, color=color).add_to(m)

# 5. Save the final map
m.save("76.html")