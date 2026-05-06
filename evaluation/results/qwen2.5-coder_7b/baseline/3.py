import pandas as pd
import folium
from geopandas import GeoDataFrame

# Загрузка данных
data = pd.read_csv('water_level_data.csv')

# Фильтрация данных для Talgar River
talgar_data = data[data['river_name'] == 'Talgar River']

# Нахождение последнего показателя уровня воды
last_water_level = talgar_data.iloc[-1]['water_level']
last_date = talgar_data.iloc[-1]['date']

print(f"Последний показатель уровня воды на реке Talgar River: {last_water_level} м")
print(f"Дата фиксации: {last_date}")

# Создание GeoDataFrame для визуализации
geometry = [talgar_data.iloc[-1]['geometry']]
gdf = GeoDataFrame(talgar_data.iloc[-1:], geometry=geometry)

# Создание карты
m = folium.Map(location=[gdf.geometry.y.mean(), gdf.geometry.x.mean()], zoom_start=10)

# Добавление маркера с последним уровнем воды
folium.Marker(
    location=[gdf.geometry.y.values[0], gdf.geometry.x.values[0]],
    popup=f"Последний уровень воды: {last_water_level} м<br>Дата: {last_date}",
    icon=folium.Icon(color='red', icon='info-sign')
).add_to(m)

# Сохранение карты
m.save("3.html")