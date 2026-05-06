import geopandas as gpd
import folium
from shapely import wkt

# Загрузка shapefile и преобразование в CRS 'EPSG:4326'
basin_gdf = gpd.read_file(r"data/basin_data.shp")
basin_gdf = basin_gdf.to_crs('EPSG:4326')

# Инициализация карты folium
centroid = basin_gdf.geometry.centroid.iloc[0]
m = folium.Map(location=[centroid.y, centroid.x], tiles='CartoDB positron', zoom_start=10)

# Добавление бассейна на карту
folium.GeoJson(basin_gdf.to_json(), name="Basin", style_function=lambda x: {'fillColor': 'green', 'color': 'darkgreen', 'fillOpacity': 0.2}).add_to(m)

# Пример данных временных рядов (заменить на реальные данные)
import pandas as pd

data1 = {
    'resultTime': pd.date_range(start='2023-01-01', periods=10, freq='D'),
    'Date_water_level_Value': [150.2, 151.0, 149.8, 150.5, 151.2, 150.7, 150.3, 150.6, 151.1, 150.9]
}

data2 = {
    'resultTime': pd.date_range(start='2023-01-01', periods=10, freq='D'),
    'Date_water_level_Value': [148.5, 149.0, 147.8, 148.5, 149.2, 148.7, 148.3, 148.6, 149.1, 148.9]
}

# Создание DataFrame
df1 = pd.DataFrame(data1)
df2 = pd.DataFrame(data2)

# Сравнение временных рядов с использованием корреляции
correlation = df1['Date_water_level_Value'].corr(df2['Date_water_level_Value'])
print(f"Корреляция между временными рядами: {correlation}")

# Построение графиков для визуального сравнения
import matplotlib.pyplot as plt

plt.figure(figsize=(10, 5))
plt.plot(df1['resultTime'], df1['Date_water_level_Value'], label='Временной ряд 1')
plt.plot(df2['resultTime'], df2['Date_water_level_Value'], label='Временной ряд 2')
plt.xlabel('Дата')
plt.ylabel('Уровень воды')
plt.title('Сравнение двух временных рядов уровней воды')
plt.legend()
plt.show()

# Сохранение карты
m.save("283.html")