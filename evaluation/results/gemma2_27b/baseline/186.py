import pandas as pd
import geopandas as gpd
from shapely.geometry import Point
import folium

# Загрузка данных о загрязнении реки
pollution_data = pd.read_csv("pollution_data.csv")
pollution_points = gpd.GeoDataFrame(pollution_data, geometry=gpd.points_from_xy(pollution_data["longitude"], pollution_data["latitude"]))

# Загрузка данных о местах использования воды в сельском хозяйстве
water_use_data = pd.read_csv("water_use_data.csv")
water_use_points = gpd.GeoDataFrame(water_use_data, geometry=gpd.points_from_xy(water_use_data["longitude"], water_use_data["latitude"]))

# Гидрологическая модель (например, HEC-RAS) для расчета распространения загрязняющих веществ
# ...

# Оценка концентрации загрязняющих веществ в местах использования воды
concentrations = []
for point in water_use_points:
    # Расчет концентрации на основе гидрологической модели
    concentration = # ...

    concentrations.append(concentration)

# Создание карты с Folium
m = folium.Map(location=[46, 1], zoom_start=8)

# Добавление точек загрязнения на карту
folium.GeoJson(pollution_points).add_to(m)

# Добавление точек использования воды на карту
folium.GeoJson(water_use_points).add_to(m)

# Сохранение карты
m.save("186.html")