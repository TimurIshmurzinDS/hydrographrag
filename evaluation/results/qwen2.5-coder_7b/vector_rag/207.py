import geopandas as gpd
import folium
from shapely import wkt

# Загрузка shapefile с границами бассейна
basin_data = gpd.read_file(r"data/basin_data.shp")
basin_data = basin_data.to_crs('EPSG:4326')

# Создание карты
centroid = basin_data.geometry.centroid[0]
m = folium.Map(location=[centroid.y, centroid.x], zoom_start=10, tiles='CartoDB positron')

# Добавление границ бассейна на карту
folium.GeoJson(basin_data.to_json(), style_function=lambda x: {
    'fillColor': 'green',
    'color': 'darkgreen',
    'fillOpacity': 0.2
}).add_to(m)

# Пример данных о межених (замените на реальные данные)
emel_river_extremes = [0.5, 1.2, 0.8, 1.5, 0.9]  # Максимальные уровни в метрах
turgen_river_extremes = [0.6, 1.3, 0.7, 1.4, 1.0]

# Построение временных рядов и выявление экстремальных значений
import pandas as pd

emel_df = pd.DataFrame(emel_river_extremes, columns=['extreme_level'])
turgen_df = pd.DataFrame(turgen_river_extremes, columns=['extreme_level'])

# Добавление меток времени (например, год)
emel_df['year'] = range(2013, 2018)
turgen_df['year'] = range(2013, 2018)

# Сравнение частоты экстремальных межени
import matplotlib.pyplot as plt

plt.figure(figsize=(10, 5))
plt.plot(emel_df['year'], emel_df['extreme_level'], label='Emel River')
plt.plot(turgen_df['year'], turgen_df['extreme_level'], label='Turgen River')
plt.xlabel('Year')
plt.ylabel('Extreme Level (m)')
plt.title('Comparison of Extreme Flood Levels in Emel and Turgen Rivers')
plt.legend()
plt.show()

# Сохранение карты
m.save("207.html")