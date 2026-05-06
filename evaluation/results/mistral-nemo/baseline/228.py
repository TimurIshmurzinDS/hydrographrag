import geopandas as gpd
import pandas as pd
from shapely.geometry import Point
import folium

# 1. Сбор данных о сезонных изменениях реки Аягоз
data = {
    'season': ['spring', 'summer', 'autumn', 'winter'],
    'coordinate_x': [50, 52, 54, 56],
    'coordinate_y': [30, 32, 34, 36],
    'depth': [1.5, 2.2, 1.8, 2.1],
    'flow_speed': [2.5, 3.1, 2.7, 2.9]
}
df = pd.DataFrame(data)

# 2. Создание цифровой модели рельефа (ДМР)
geometry = [Point(xy) for xy in zip(df['coordinate_x'], df['coordinate_y'])]
gdf = gpd.GeoDataFrame(df, geometry=geometry)
gdf.crs = "EPSG:4326"
gdf.to_file("river.shp")

# 3. Определение оптимального места для запуска ракеты
optimal_launch_site = (52, 32) # Примерные координаты оптимального места для запуска ракеты

# 4. Проектирование ракеты с учетом топографии местности и других условий
rocket_design = {
    'length': 10,
    'width': 5,
    'height': 3,
    'fuel_type': 'RP-1',
    'engine_type': 'RS-25'
}

# 5. Визуализация процесса на карте
m = folium.Map(location=optimal_launch_site, zoom_start=10)
folium.GeoJson("river.shp").add_to(m)
folium.Marker(optimal_launch_site, popup="Оптимальное место для запуска ракеты").add_to(m)
m.save("228.html")