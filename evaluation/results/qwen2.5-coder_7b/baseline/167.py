import geopandas as gpd
from shapely.geometry import LineString
import folium

# Загрузка данных о речных ветвях (пример: из Shapefile)
gdf = gpd.read_file('path_to_your_shapefile.shp')

# Фильтрация данных для получения только тех ветвей, которые соединяют реку Текес и реку Тентек
tekes = gdf[gdf['name'] == 'Текес']
tentek = gdf[gdf['name'] == 'Тентек']

# Соединение ветвей между рекой Текес и рекой Тентек (пример: простое соединение)
# Здесь предполагается, что у вас есть точные координаты начала и конца каждой ветви
tekes_coords = tekes.geometry[0].coords
tentek_coords = tentek.geometry[0].coords

# Создание линии, соединяющей начало реки Текес с концом реки Тентек
combined_line = LineString(tekes_coords + list(tentek_coords)[::-1])

# Создание GeoDataFrame для отображения на карте
combined_gdf = gpd.GeoDataFrame(geometry=[combined_line], crs=gdf.crs)

# Визуализация на карте с использованием folium
m = folium.Map(location=[tekes.geometry[0].centroid.y, tekes.geometry[0].centroid.x], zoom_start=12)

folium.GeoJson(combined_gdf.to_json(), style_function=lambda x: {'color': 'blue'}).add_to(m)
tekes.plot(ax=m.get_root().children[0].children[0], color='red')
tentek.plot(ax=m.get_root().children[0].children[0], color='green')

# Сохранение карты
m.save("167.html")

# Расчет протяженности линии
total_length = combined_line.length
print(f"Общая протяженность речной сети: {total_length} м")