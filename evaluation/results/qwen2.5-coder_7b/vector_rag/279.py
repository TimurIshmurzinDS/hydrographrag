import geopandas as gpd
import folium
from shapely import wkt

# Загрузка shapefile и конвертация в CRS 'EPSG:4326'
basin_data = gpd.read_file(r"data/basin_data.shp")
basin_data = basin_data.to_crs('EPSG:4326')

# Создание карты с центром на centroid shapefile
centroid = basin_data.geometry.centroid[0]
m = folium.Map(location=[centroid.y, centroid.x], zoom_start=10, tiles='CartoDB positron')

# Добавление бассейна на карту
folium.GeoJson(basin_data.to_json(), style_function=lambda x: {
    'fillColor': 'green',
    'color': 'darkgreen',
    'fillOpacity': 0.2
}).add_to(m)

# Пример данных о недвижимости (замените на реальные данные)
property_data = [
    {'locatedInRegion': 'Санкт-Петербург', 'price': 1500000, 'area': 80},
    {'locatedInRegion': 'Москва', 'price': 2500000, 'area': 120},
    {'locatedInRegion': 'Санкт-Петербург', 'price': 1800000, 'area': 90},
    {'locatedInRegion': 'Москва', 'price': 3000000, 'area': 150}
]

# Добавление точек недвижимости на карту
for prop in property_data:
    folium.Marker([prop['latitude'], prop['longitude']], popup=f"Price: {prop['price']}, Area: {prop['area']}").add_to(m)

# Сохранение карты в файл
m.save("279.html")