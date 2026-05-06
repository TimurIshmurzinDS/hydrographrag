import geopandas as gpd
import folium

# Загружаем данные о координатах рек Шынжалы и Талгар
shynjaly = gpd.read_file('shynjaly.geojson')
talgar = gpd.read_file('talgar.geojson')

# Создаем GeoDataFrame для каждой реки
gdf_shynjaly = gpd.GeoDataFrame(shynjaly)
gdf_talgar = gpd.GeoDataFrame(talgar)

# Выполняем пространственное пересечение между двумя GeoDataFrame
intersection = gpd.sjoin(gdf_shynjaly, gdf_talgar, how='intersection', predicate='intersects')

# Создаем карту и добавляем результаты пересечения на нее
m = folium.Map(location=[43.2, 70], zoom_start=8)
folium.GeoJson(intersection[['geometry']]).add_to(m)

# Сохраняем карту как "169.html"
m.save("169.html")