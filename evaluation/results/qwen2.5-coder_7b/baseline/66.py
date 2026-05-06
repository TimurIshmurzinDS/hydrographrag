import geopandas as gpd
from shapely.geometry import Point, LineString
import folium

# Загрузка данных о реке Temirlik River (пример данных)
temirlik_river = gpd.GeoDataFrame({
    'geometry': [LineString([(0, 0), (1, 1), (2, 2)]), LineString([(3, 3), (4, 4), (5, 5)])]
}, crs="EPSG:4326")

# Пример данных о местоположении оборудования
equipment_points = gpd.GeoDataFrame({
    'geometry': [Point(0.5, 0.5), Point(1.5, 1.5), Point(4.5, 4.5)]
}, crs="EPSG:4326")

# Проверка, находится ли оборудование на реке
equipment_on_river = gpd.sjoin(equipment_points, temirlik_river, how='left', op='within')

# Визуализация результатов
m = folium.Map(location=[temirlik_river.geometry.centroid.y.mean(), temirlik_river.geometry.centroid.x.mean()], zoom_start=10)

folium.GeoJson(temirlik_river.to_json()).add_to(m)
folium.GeoJson(equipment_points.to_json()).add_to(m)

# Добавление маркеров для оборудования на реке
for idx, row in equipment_on_river.iterrows():
    folium.Marker([row['geometry'].y, row['geometry'].x], popup=f"Equipment at {idx}").add_to(m)

m.save("66.html")