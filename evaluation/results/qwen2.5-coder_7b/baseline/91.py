import geopandas as gpd
import folium

# Загрузка данных о реке Уржар и ее притоках (пример использования shapefile)
gdf = gpd.read_file('path_to_your_shapefile.shp')

# Фильтрация данных для получения только притков реки Уржар
urzhar_streams = gdf[gdf['name'] == 'Уржар']

# Извлечение координат притков
stream_coordinates = urzhar_streams.geometry.apply(lambda geom: geom.centroid.xy)

# Создание карты с использованием folium
m = folium.Map(location=[urzhar_streams.geometry.centroid.y.mean(), urzhar_streams.geometry.centroid.x.mean()], zoom_start=12)

# Добавление маркеров для каждого притока
for coord in stream_coordinates:
    folium.Marker([coord[1][0], coord[0][0]], popup='Приток реки Уржар').add_to(m)

# Сохранение карты в файл
m.save("91.html")