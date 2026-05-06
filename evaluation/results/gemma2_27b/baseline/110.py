import pandas as pd
import geopandas as gpd
from shapely.geometry import Point
import folium

# Загрузка данных о расходе воды (замените на ваши данные)
water_data = pd.read_csv("water_discharge.csv")
water_data["geometry"] = [Point(x, y) for x, y in zip(water_data["longitude"], water_data["latitude"])]
water_data = gpd.GeoDataFrame(water_data, geometry="geometry", crs="EPSG:4326")

# Загрузка данных о урожайности (замените на ваши данные)
yield_data = pd.read_csv("yield_data.csv")
yield_data["geometry"] = [Point(x, y) for x, y in zip(yield_data["longitude"], yield_data["latitude"])]
yield_data = gpd.GeoDataFrame(yield_data, geometry="geometry", crs="EPSG:4326")

# Пространственный анализ (замените на ваши функции анализа)
def analyze_water_yield(water_data, yield_data):
    # ... ваш код для пространственного анализа и статистического анализа

# Выполнение анализа
analyze_water_yield(water_data, yield_data)

# Визуализация результатов (замените на ваши функции визуализации)
m = folium.Map(location=[43.25, 78.0], zoom_start=8)
folium.GeoJson(water_data).add_to(m)
folium.GeoJson(yield_data).add_to(m)

# Сохранение карты
m.save("110.html")