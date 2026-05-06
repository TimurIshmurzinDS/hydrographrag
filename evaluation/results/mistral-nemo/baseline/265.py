import geopandas as gpd
import pandas as pd
from shapely.geometry import Point, LineString
import numpy as np
import folium

# Load data
river_emel = gpd.read_file('river_emel.shp')
pollution_sources = pd.read_csv('pollution_sources.csv')

# Create a map centered on the river Emel
m = folium.Map(location=[51.7098, 34.6236], zoom_start=10)

# Add river Emel to the map
river_emel_geom = river_emel['geometry'].iloc[0]
folium.GeoJson(river_emel_geom).add_to(m)

# Add pollution sources to the map
for index, row in pollution_sources.iterrows():
    geometry = Point(row['longitude'], row['latitude'])
    folium.Marker(geometry, popup=row['source']).add_to(m)

# Model pollution spread (simplified example)
pollution_spread = LineString([(34.6236, 51.7098), (34.6543, 51.7234), (34.6850, 51.7456)])
folium.GeoJson(pollution_spread).add_to(m)

# Evaluate environmental impact (simplified example)
impact = np.random.randint(1, 10, size=len(river_emel))
river_emel['impact'] = impact
river_emel_exploded = river_emel.explode().reset_index(drop=True)
for _, row in river_emel_exploded.iterrows():
    folium.CircleMarker(location=[row.geometry.y, row.geometry.x], radius=5,
                        color='red' if row['impact'] > 5 else 'green',
                        fill_color='red' if row['impact'] > 5 else 'green').add_to(m)

# Save the map
m.save("265.html")