import geopandas as gpd
from shapely.geometry import Polygon, LineString
import folium

# Шаг 1: Получение данных о рее Тентек и её притоках из OpenStreetMap
url = "https://overpass-api.de/api/interpreter"
query = """
[out:json];
(
    way["name"="Тентек"](54.3,20.6,54.7,21.0);
    relation["name"="Тентек"](54.3,20.6,54.7,21.0);
    way["waterway"~"river|stream"]->.r;
    (._;>;);
);
out geom;
"""
import requests
response = requests.get(url, params={'data': query})
data = response.json()

# Преобразование данных в GeoDataFrame
gdf = gpd.GeoDataFrame.from_features(data['elements'])

# Фильтрация только линий (рек и притоков)
rivers_gdf = gdf[gdf['type'] == 'way'].copy()
rivers_gdf['geometry'] = rivers_gdf['geometry'].apply(lambda x: LineString(x['coordinates']))

# Шаг 2: Визуализация данных с использованием folium
m = folium.Map(location=[54.5, 20.8], zoom_start=10)

for _, row in rivers_gdf.iterrows():
    folium.PolyLine(locations=row['geometry'].coords, color="blue", weight=2.5, opacity=1).add_to(m)

# Шаг 3: Создание формы пирога на основе разветвления рек
def create_pie_shape(rivers_gdf):
    # Простое приближение формы пирога как объединения всех линий в многоугольник
    all_coords = []
    for geom in rivers_gdf['geometry']:
        all_coords.extend(geom.coords)
    
    # Создание выпуклой оболочки для получения формы пирога
    from shapely.geometry import MultiPoint, Polygon
    convex_hull = MultiPoint(all_coords).convex_hull
    
    return convex_hull

pie_shape = create_pie_shape(rivers_gdf)

# Шаг 4: Визуализация формы пирога на карте
folium.GeoJson(pie_shape, style_function=lambda x: {'fillColor': 'red', 'color': 'black'}).add_to(m)

# Сохранение карты в файл
m.save("242.html")