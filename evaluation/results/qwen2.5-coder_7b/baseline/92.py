import geopandas as gpd
from shapely.geometry import Point, LineString
import folium

# Загрузка данных о реках Дос и Емель (пример данных)
data = {
    'name': ['Дос', 'Емель'],
    'geometry': [
        LineString([(10.5, 48.2), (11.3, 47.9), (12.1, 47.6)]),
        LineString([(13.5, 48.8), (14.2, 48.5), (15.0, 48.2)])
    ]
}

# Создание GeoDataFrame
gdf = gpd.GeoDataFrame(data)

# Определение устья и начала рек
source_point_dos = Point(gdf.loc[gdf['name'] == 'Дос', 'geometry'].iloc[0].coords[0])
target_point_emel = Point(gdf.loc[gdf['name'] == 'Емель', 'geometry'].iloc[0].coords[-1])

# Вычисление расстояния
distance_km = source_point_dos.distance(target_point_emel) / 1000

print(f"Расстояние между устьем реки Дос и началом реки Емель: {distance_km:.2f} километров")

# Визуализация на карте
m = folium.Map(location=[48.5, 13], zoom_start=6)

folium.Marker([source_point_dos.y, source_point_dos.x], popup='Устье реки Дос', icon=folium.Icon(color='red')).add_to(m)
folium.Marker([target_point_emel.y, target_point_emel.x], popup='Начало реки Емель', icon=folium.Icon(color='blue')).add_to(m)

# Сохранение карты
m.save("92.html")