import geopandas as gpd
import folium
from shapely import wkt

# Загрузка данных о бассейне
basin_data = gpd.read_file(r"data/basin_data.shp")
basin_data = basin_data.to_crs('EPSG:4326')

# Инициализация карты с центром в бассейне реки Каркара
centroid = basin_data.geometry.centroid.iloc[0]
m = folium.Map(location=[centroid.y, centroid.x], tiles='CartoDB positron', zoom_start=10)

# Добавление бассейна на карту
folium.GeoJson(basin_data.to_json(), name="Basin", style_function=lambda x: {'fillColor': 'green', 'color': 'darkgreen', 'fillOpacity': 0.2}).add_to(m)

# Пример данных о уровнях воды и осадках (заменить на реальные данные)
water_level_data = [
    {"Date_water_level_Value": "2018-01-01", "Water_level_Valuecm": 150},
    {"Date_water_level_Value": "2018-02-01", "Water_level_Valuecm": 160},
    # Добавить остальные данные за период с 2018 по 2023 годы
]

# Пример данных о осадках (заменить на реальные данные)
precipitation_data = [
    {"Date_water_level_Value": "2018-01-01", "Precipitation_cm": 5},
    {"Date_water_level_Value": "2018-02-01", "Precipitation_cm": 10},
    # Добавить остальные данные за период с 2018 по 2023 годы
]

# Сохранение карты в файл
m.save("60.html")