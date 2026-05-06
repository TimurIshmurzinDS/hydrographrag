import geopandas as gpd
import pandas as pd
import folium

# 1. Load posts data (assuming it's in GeoJSON format)
posts_gdf = gpd.read_file('posts.geojson')

# 2. Load critical flood level data (assuming it's in CSV format with 'post_id' and 'critical_level' columns)
critical_levels_df = pd.read_csv('critical_levels.csv')

# 3. Load current water flow data (assuming it's in CSV format with 'post_id' and 'current_flow' columns)
current_flow_df = pd.read_csv('current_flow.csv')

# 4. Merge datasets on 'post_id'
merged_data = pd.merge(posts_gdf, critical_levels_df, on='post_id')
merged_data = pd.merge(merged_data, current_flow_df, on='post_id')

# 5. Compare current flow with critical level
merged_data['exceeds_critical_level'] = merged_data['current_flow'] > merged_data['critical_level']

# 6. Filter posts where current flow exceeds critical level
exceeding_posts_gdf = merged_data[merged_data['exceeds_critical_level']].copy()

# 7. Visualize results on map using folium
m = folium.Map(location=[41.0082, 67.1524], zoom_start=8)  # Set initial location and zoom level

for _, row in exceeding_posts_gdf.iterrows():
    folium.CircleMarker(
        location=(row.geometry.y, row.geometry.x),
        radius=5,
        color='red',
        fill=True,
        fill_color='red'
    ).add_to(m)

# Save the map as HTML file
m.save("82.html")