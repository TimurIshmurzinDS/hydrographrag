import geopandas as gpd
import folium
from shapely import wkt

# Загрузка shapefile с границами бассейна (только для визуализации)
basin_data = gpd.read_file(r"data/basin_data.shp")
basin_data = basin_data.to_crs('EPSG:4326')

# Создание карты
centroid = basin_data.geometry.centroid[0]
m = folium.Map(location=[centroid.y, centroid.x], zoom_start=10, tiles='CartoDB positron')

# Добавление границ бассейна на карту
folium.GeoJson(basin_data.to_json(), style_function=lambda x: {'fillColor': 'green', 'color': 'darkgreen', 'fillOpacity': 0.2}).add_to(m)

# Пример данных уровня воды для реки Dos River (замените на реальные данные)
dos_river_water_levels = [
    {"date": "2015-01-01", "water_level": 10},
    {"date": "2015-02-01", "water_level": 12},
    {"date": "2015-03-01", "water_level": 14},
    # Добавьте больше данных
]

# Пример данных уровня воды для реки Lepsy River (замените на реальные данные)
lepsy_river_water_levels = [
    {"date": "2023-01-01", "water_level": 8},
    {"date": "2023-02-01", "water_level": 10},
    {"date": "2023-03-01", "water_level": 12},
    # Добавьте больше данных
]

# Прогнозирование уровня воды для реки Lepsy River на 2025 год (пример с использованием простого метода)
from sklearn.linear_model import LinearRegression
import pandas as pd

dos_river_df = pd.DataFrame(dos_river_water_levels)
lepsy_river_df = pd.DataFrame(lepsy_river_water_levels)

# Прогнозирование для реки Lepsy River на 2025 год (пример с использованием простого метода)
model = LinearRegression()
model.fit(pd.to_datetime(dos_river_df['date']).map(dt.datetime.timestamp).values.reshape(-1, 1), dos_river_df['water_level'])
predicted_date = pd.Timestamp('2025-01-01')
predicted_water_level = model.predict([[predicted_date.timestamp()]])[0]

# Добавление прогнозируемого уровня воды на карту для реки Lepsy River
folium.Marker([centroid.y, centroid.x], popup=f"Прогнозируемый уровень воды в Lepsy River на 2025 год: {predicted_water_level}").add_to(m)

# Сохранение карты
m.save("124.html")