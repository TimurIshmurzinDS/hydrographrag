import geopandas as gpd
import folium
from shapely import wkt
import pandas as pd
import matplotlib.pyplot as plt

# Загрузка границы бассейна (пример данных)
basin_data = gpd.read_file(r"data/basin_data.shp")
basin_data = basin_data.to_crs('EPSG:4326')

# Создание карты с границами бассейна
centroid = basin_data.geometry.centroid[0]
m = folium.Map(location=[centroid.y, centroid.x], zoom_start=10, tiles='CartoDB positron')

# Добавление границы бассейна на карту
folium.GeoJson(basin_data.to_json(), style_function=lambda x: {
    'fillColor': 'green',
    'color': 'darkgreen',
    'fillOpacity': 0.2
}).add_to(m)

# Пример данных о расходе воды (замените на реальные данные)
water_consumption_2020 = pd.DataFrame({
    'Date': pd.date_range(start='1/1/2020', end='12/31/2020', freq='M'),
    'Water_consumption_Value': [100, 150, 200, 250, 300, 350, 400, 450, 500, 550, 600, 650]
})

water_consumption_2023 = pd.DataFrame({
    'Date': pd.date_range(start='1/1/2023', end='12/31/2023', freq='M'),
    'Water_consumption_Value': [120, 170, 220, 270, 320, 370, 420, 470, 520, 570, 620, 670]
})

# Визуализация данных
plt.figure(figsize=(12, 6))

plt.plot(water_consumption_2020['Date'], water_consumption_2020['Water_consumption_Value'], label='2020', marker='o')
plt.plot(water_consumption_2023['Date'], water_consumption_2023['Water_consumption_Value'], label='2023', marker='o')

plt.xlabel('Месяц')
plt.ylabel('Расход воды (м³)')
plt.title('Ежемесячные показатели расхода воды в реке Sarykan River за 2020 и 2023 годы')
plt.legend()
plt.grid(True)

# Сохранение графика
plt.savefig("water_consumption_comparison.png")

# Сохранение карты
m.save("58.html")