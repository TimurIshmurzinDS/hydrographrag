import pandas as pd
from shapely.geometry import Point, Polygon
from folium import Map, Marker, CircleMarker, Circle, PolyLine, FeatureGroup, GeoJson
from folium.plugins import HeatMap
import geopandas as gpd
import matplotlib.pyplot as plt

# Данные о расходе воды в сельском хозяйстве (предположим, это данные для области Омской)
water_demand_data = pd.DataFrame({
    'geometry': [Polygon([(55.0, 73.5), (56.0, 73.5), (56.0, 74.5), (55.0, 74.5)]),
                  Polygon([(54.0, 72.5), (55.0, 72.5), (55.0, 73.5), (54.0, 73.5)])],
    'water_demand': [10000, 15000]
})

# Данные о объемах воды в реках Курте и Лепсе
river_data = pd.DataFrame({
    'geometry': [Polygon([(53.0, 72.0), (54.0, 72.0), (54.0, 73.0), (53.0, 73.0)]),
                  Polygon([(52.0, 71.0), (53.0, 71.0), (53.0, 72.0), (52.0, 72.0)])],
    'water_volume': [50000, 30000]
})

# Геообработка для определения площади сельскохозяйственных угодий
gdf = gpd.GeoDataFrame(water_demand_data, geometry='geometry')
river_gdf = gpd.GeoDataFrame(river_data, geometry='geometry')

# Сравнение потребности в воде с доступным объемом воды
for index, row in water_demand_data.iterrows():
    for river_index, river_row in river_data.iterrows():
        intersection_area = row['geometry'].intersection(river_row['geometry']).area
        if intersection_area > 0:
            print(f'Площадь сельскохозяйственных угодий, которые могут быть обеспечены водой из реки {river_row["geometry"].name}: {intersection_area}')

# Визуализация на карте с помощью folium
m = Map(location=[55.5, 73.0], zoom_start=10)

for index, row in water_demand_data.iterrows():
    Marker(row['geometry'].centroid.coords[0][::-1], popup='Сельскохозяйственные угодья').add_to(m)
    
for index, row in river_data.iterrows():
    CircleMarker(row['geometry'].centroid.coords[0][::-1], radius=10000).add_to(m)

m.save("120.html")