import geopandas as gpd
import folium
from shapely import wkt

# Загрузка данных о водном бассейне из shapefile
basin_data = gpd.read_file(r"data/basin_data.shp")
basin_data = basin_data.to_crs('EPSG:4326')

# Инициализация карты с центром в полигоне бассейна
centroid = basin_data.geometry.centroid.iloc[0]
m = folium.Map(location=[centroid.y, centroid.x], tiles='CartoDB positron', zoom_start=10)

# Добавление границ водного бассейна на карту
folium.GeoJson(basin_data.to_json(), name="Basin", style_function=lambda x: {'fillColor': 'green', 'color': 'darkgreen', 'fillOpacity': 0.2}).add_to(m)

# Пример данных о расходе воды (заменить на реальные данные)
water_consumption_data = [
    {"month": "2020-01", "value_m3": 5000},
    {"month": "2020-02", "value_m3": 6000},
    # ... остальные месяцы 2020 года
    {"month": "2023-01", "value_m3": 5500},
    {"month": "2023-02", "value_m3": 6500},
    # ... остальные месяцы 2023 года
]

# Преобразование данных в DataFrame для анализа
import pandas as pd

df = pd.DataFrame(water_consumption_data)
df['month'] = pd.to_datetime(df['month'])
df.set_index('month', inplace=True)

# Визуализация временных рядов расхода воды
import matplotlib.pyplot as plt

plt.figure(figsize=(14, 7))
plt.plot(df[df.index.year == 2020], label='2020')
plt.plot(df[df.index.year == 2023], label='2023')
plt.title('Ежемесячный расход воды в реке Сарыкан (2020 и 2023)')
plt.xlabel('Месяц')
plt.ylabel('Расход воды, м³')
plt.legend()
plt.grid(True)
plt.show()

# Сохранение карты
m.save("58.html")