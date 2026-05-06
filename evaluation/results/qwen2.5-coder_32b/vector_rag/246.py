import geopandas as gpd
import folium
from shapely import wkt

# Загрузка данных о водном бассейне и преобразование CRS
basin = gpd.read_file(r"data/basin_data.shp")
basin = basin.to_crs(epsg=4326)

# Координаты Альфа Орионис (Betelgeuse)
alpha_orionis_coords = {'name': 'Alpha Orionis', 'geometry': wkt.loads('POINT(86.944444 -7.403333)')}

# Предполагаемые координаты точки на реке Шилик (в формате WKT)
shilik_river_coords = {'name': 'Shilik River Point', 'geometry': wkt.loads('POINT(86.95 -7.41)')}  # Примерные координаты

# Создание GeoDataFrame для точек
points_gdf = gpd.GeoDataFrame([alpha_orionis_coords, shilik_river_coords], crs='EPSG:4326')

# Инициализация карты с центром в центроиде водного бассейна
centroid = basin.geometry.centroid.iloc[0]
m = folium.Map(location=[centroid.y, centroid.x], tiles='CartoDB positron', zoom_start=10)

# Добавление водного бассейна на карту
folium.GeoJson(basin.to_json(), name="Basin", style_function=lambda x: {'fillColor': 'green', 'color': 'darkgreen', 'fillOpacity': 0.2}).add_to(m)

# Добавление точек на карту
for _, point in points_gdf.iterrows():
    folium.Marker([point.geometry.y, point.geometry.x], popup=point.name).add_to(m)

# Сохранение карты в файл
m.save("246.html")