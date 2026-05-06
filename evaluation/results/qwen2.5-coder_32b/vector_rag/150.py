import geopandas as gpd
import folium
from shapely import wkt

# Загрузка данных о бассейне
basin_data = gpd.read_file(r"data/basin_data.shp")
basin_data = basin_data.to_crs('EPSG:4326')

# Инициализация карты с центром в бассейне реки
centroid = basin_data.geometry.centroid.iloc[0]
m = folium.Map(location=[centroid.y, centroid.x], tiles='CartoDB positron', zoom_start=10)

# Добавление границ бассейна на карту
folium.GeoJson(basin_data.to_json(), name="Basin", style_function=lambda x: {'fillColor': 'green', 'color': 'darkgreen', 'fillOpacity': 0.2}).add_to(m)

# Пример данных по уровням воды для реки Каратал (в реальности данные должны быть загружены из источника)
water_level_data_karatal = [
    {'Date_water_level_Value': '2023-01-01', 'Water_level_Valuecm': 150},
    {'Date_water_level_Value': '2023-01-02', 'Water_level_Valuecm': 152},
    {'Date_water_level_Value': '2023-01-03', 'Water_level_Valuecm': 148},
    # Добавьте больше данных по необходимости
]

# Пример данных по уровням воды для реки Или (в реальности данные должны быть загружены из источника)
water_level_data_ili = [
    {'Date_water_level_Value': '2023-01-01', 'Water_level_Valuecm': 200},
    {'Date_water_level_Value': '2023-01-02', 'Water_level_Valuecm': 205},
    {'Date_water_level_Value': '2023-01-03', 'Water_level_Valuecm': 198},
    # Добавьте больше данных по необходимости
]

# Преобразование дат в формат datetime для анализа временных рядов
import pandas as pd

df_karatal = pd.DataFrame(water_level_data_karatal)
df_ili = pd.DataFrame(water_level_data_ili)

df_karatal['Date_water_level_Value'] = pd.to_datetime(df_karatal['Date_water_level_Value'])
df_ili['Date_water_level_Value'] = pd.to_datetime(df_ili['Date_water_level_Value'])

# Анализ стабильности показаний датчиков уровня воды
import matplotlib.pyplot as plt

plt.figure(figsize=(14, 7))

plt.subplot(2, 1, 1)
plt.plot(df_karatal['Date_water_level_Value'], df_karatal['Water_level_Valuecm'], marker='o')
plt.title('Уровень воды реки Каратал')
plt.xlabel('Дата')
plt.ylabel('Уровень воды (см)')
plt.grid(True)

plt.subplot(2, 1, 2)
plt.plot(df_ili['Date_water_level_Value'], df_ili['Water_level_Valuecm'], marker='o', color='orange')
plt.title('Уровень воды реки Или')
plt.xlabel('Дата')
plt.ylabel('Уровень воды (см)')
plt.grid(True)

plt.tight_layout()
plt.show()

# Сохранение карты
m.save("150.html")