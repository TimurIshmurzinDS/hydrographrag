import geopandas as gpd
import pandas as pd
import folium

# Загрузка данных о качестве воды из базы данных
data = pd.read_sql("SELECT * FROM water_quality", con=engine)

# Фильтрация данных для рек Byzhy River и Tekeli River
byzhy_data = data[data['river'] == 'Byzhy River']
tekeli_data = data[data['river'] == 'Tekeli River']

# Вычисление средних значений экологических индикаторов для каждой реки
byzhy_avg = byzhy_data.mean()
tekeli_avg = tekeli_data.mean()

# Создание карты с помощью библиотеки folium
m = folium.Map(location=[51.5074, -0.1278], zoom_start=6)

# Добавление точек на карту для рек Byzhy River и Tekeli River
folium.Marker([byzhy_data['latitude'].mean(), byzhy_data['longitude'].mean()], popup='Byzhy River').add_to(m)
folium.Marker([tekeli_data['latitude'].mean(), tekeli_data['longitude'].mean()], popup='Tekeli River').add_to(m)

# Сохранение карты в файл HTML
m.save("119.html")