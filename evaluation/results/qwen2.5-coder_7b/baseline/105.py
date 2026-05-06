import geopandas as gpd
import requests
from shapely.geometry import Point
import folium

# Список названий рек
rivers = ["Улькен Алматы", "Емель", "Тентек"]

# Функция для получения координат реки из OpenStreetMap Nominatim API
def get_coordinates(river_name):
    url = f"https://nominatim.openstreetmap.org/search?q={river_name}&format=json&addressdetails=1"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        if data:
            lat = float(data[0]['lat'])
            lon = float(data[0]['lon'])
            return Point(lon, lat)
    return None

# Создаем GeoDataFrame для хранения координат рек
gdf_rivers = gpd.GeoDataFrame(columns=['river_name', 'geometry'])

# Получаем координаты и добавляем в GeoDataFrame
for river in rivers:
    coordinates = get_coordinates(river)
    if coordinates:
        gdf_rivers = gdf_rivers.append({'river_name': river, 'geometry': coordinates}, ignore_index=True)

# Определяем регион (например, Алматинская область)
region_polygon = gpd.read_file('path_to_region_shapefile.shp')  # Замените на путь к вашему shapefile региона

# Фильтруем реки, чьи координаты находятся в регионе
gdf_filtered = gdf_rivers[gdf_rivers.within(region_polygon.unary_union)]

# Создаем карту и добавляем маркеры с координатами рек
m = folium.Map(location=[43.2107, 76.9238], zoom_start=10)  # Координаты центра региона

for index, row in gdf_filtered.iterrows():
    folium.Marker([row['geometry'].y, row['geometry'].x], popup=row['river_name']).add_to(m)

# Сохраняем карту
m.save("105.html")