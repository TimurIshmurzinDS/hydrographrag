import geopandas as gpd
import folium
from shapely import wkt

# Загрузка shapefile с границами бассейна (только для визуализации)
basin_data = gpd.read_file(r"data/basin_data.shp")
basin_data = basin_data.to_crs('EPSG:4326')

# Инициализация карты
centroid = basin_data.geometry.centroid[0]
m = folium.Map(location=[centroid.y, centroid.x], zoom_start=10, tiles='CartoDB positron')

# Добавление границ бассейна на карту
folium.GeoJson(basin_data.to_json(), style_function=lambda x: {'fillColor': 'green', 'color': 'darkgreen', 'fillOpacity': 0.2}).add_to(m)

# Пример данных оHistorical water levels для Koksu River (замените на реальные данные)
water_level_data = [
    {"Date": "2018-01-01", "Water_level_Value": 45},
    {"Date": "2018-02-01", "Water_level_Value": 50},
    {"Date": "2018-03-01", "Water_level_Value": 55},
    # Добавьте больше данных по необходимости
]

# Преобразование данных в DataFrame
import pandas as pd
df = pd.DataFrame(water_level_data)
df['Date'] = pd.to_datetime(df['Date'])
df.set_index('Date', inplace=True)

# Построение временного ряда
folium.PolyLine(locations=[(row['Water_level_Value'], i) for i, row in df.iterrows()], color='blue').add_to(m)

# Расчет статистических характеристик
mean_water_level = df['Water_level_Value'].mean()
std_water_level = df['Water_level_Value'].std()

# Определение порога 50-летнего паводка (пример: вероятность превышения среднего значения)
threshold_50_year_flood = mean_water_level + std_water_level

# Визуализация порога на карте
folium.Marker([threshold_50_year_flood, 1], popup=f"50-летний паводок: {threshold_50_year_flood}").add_to(m)

# Сохранение карты
m.save("203.html")