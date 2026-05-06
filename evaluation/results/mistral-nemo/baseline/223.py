import pandas as pd
from geopandas import GeoDataFrame
from shapely.geometry import Point
import folium

# Step 1: Collect data
water_level_data = pd.read_csv('water_level_data.csv')
gold_price_data = pd.read_csv('gold_price_data.csv')

# Step 2: Geocoding
bayankol_river_coords = (47.95, 86.3) # Example coordinates for Bayankol River
river_point = Point(bayankol_river_coords[0], bayankol_river_coords[1])
gdf = GeoDataFrame({'geometry': [river_point]}, index=[0])

# Step 3: Spatial interpolation (using IDW method as an example)
from pyinterp import IDW
interpolator = IDW(z=water_level_data['water_level'], x=water_level_data['longitude'], y=water_level_data['latitude'])
predicted_water_levels = interpolator.predict(gdf)

# Step 4: Correlation analysis (using pandas' corr method as an example)
correlation = water_level_data['water_level'].corr(gold_price_data['gold_price'])

# Step 5: Determine investment points based on correlation results

# Step 6: Visualization using folium
m = folium.Map(location=bayankol_river_coords, zoom_start=10)

for idx, row in gdf.iterrows():
    folium.CircleMarker(
        location=(row.geometry.y, row.geometry.x),
        radius=5,
        color='blue',
        fill=True,
        fill_opacity=0.5
    ).add_to(m)

m.save("223.html")