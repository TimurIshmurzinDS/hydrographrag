import geopandas as gpd
import pandas as pd
import numpy as np
from shapely.geometry import Point
import folium

# 1. Подготовка данных
data = {
    'geometry': [Point(xy) for xy in zip(longitudes, latitudes)],
    'elevation': elevations,
    'precipitation': precipitations,
    # другие гидрологические параметры...
}
gdf = gpd.GeoDataFrame(data)

# 2. Определение зон риска наводнений
risk_zones = gdf[gdf['elevation'] < threshold_elevation]

# 3. Моделирование экстремальных осадков
extreme_precipitation = model_climate(gdf['precipitation'])

# 4. Анализ воздействия экстремальных осадков
risk_zones['flood_risk'] = extreme_precipitation * risk_zones['elevation']

# 5. Визуализация результатов
m = folium.Map(location=[avg_lat, avg_lon], zoom_start=10)

folium.GeoJson(risk_zones[['geometry', 'flood_risk']].to_json(), name='Risk Zones').add_to(m)
folium.LayerControl().add_to(m)

m.save("209.html")