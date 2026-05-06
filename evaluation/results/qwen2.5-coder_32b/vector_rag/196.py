import geopandas as gpd
import folium
from shapely import wkt
import pandas as pd
import matplotlib.pyplot as plt

# Загрузка данных о бассейне
basin_data = gpd.read_file(r"data/basin_data.shp")
basin_data = basin_data.to_crs('EPSG:4326')

# Инициализация карты
centroid = basin_data.geometry.centroid.iloc[0]
m = folium.Map(location=[centroid.y, centroid.x], tiles='CartoDB positron', zoom_start=10)
folium.GeoJson(basin_data, style_function=lambda x: {'fillColor': 'green', 'color': 'darkgreen', 'fillOpacity': 0.2}).add_to(m)

# Пример данных о расходе воды (заменить на реальные данные)
data = {
    'Date': pd.date_range(start='1/1/2013', end='12/31/2022'),
    'Koksu_Water_consumption_Valuem³s': [50 + 10 * i % 12 for i in range(365*10)],
    'Emel_Water_consumption_Value': [40 + 8 * i % 12 for i in range(365*10)]
}

# Преобразование данных в DataFrame
df = pd.DataFrame(data)
df['Date'] = pd.to_datetime(df['Date'])
df.set_index('Date', inplace=True)

# Построение графиков сезонных изменений расхода воды
plt.figure(figsize=(14, 7))
plt.plot(df.index.month, df['Koksu_Water_consumption_Valuem³s'], label='Река Коксу')
plt.plot(df.index.month, df['Emel_Water_consumption_Value'], label='Река Эмел')
plt.title('Сезонные изменения расхода воды в реках Коксу и Эмел')
plt.xlabel('Месяц')
plt.ylabel('Расход воды (м³/с)')
plt.legend()
plt.grid(True)
plt.show()

# Сохранение карты
m.save("196.html")