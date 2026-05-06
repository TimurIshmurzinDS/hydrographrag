import geopandas as gpd
import folium
from shapely import wkt

# Загрузка данных из shapefile и преобразование CRS
basin_data = gpd.read_file(r"data/basin_data.shp")
basin_data = basin_data.to_crs('EPSG:4326')

# Инициализация карты с центром в бассейне реки Каркара
centroid = basin_data.geometry.centroid.iloc[0]
m = folium.Map(location=[centroid.y, centroid.x], tiles='CartoDB positron', zoom_start=10)

# Добавление водного бассейна на карту
folium.GeoJson(basin_data.to_json(), name="Basin", style_function=lambda x: {'fillColor': 'green', 'color': 'darkgreen', 'fillOpacity': 0.2}).add_to(m)

# Пример данных о расходе воды (Water_consumption_Valuem³s) для реки Каркара
# Данные представлены в виде списка словарей с датами и значениями расхода воды
water_data = [
    {'date': '2010-01-01', 'value': 5.2},
    {'date': '2010-06-30', 'value': 7.8},
    {'date': '2011-01-01', 'value': 4.9},
    {'date': '2011-06-30', 'value': 7.5},
    # Добавьте остальные данные за период с 2010 по 2020 годы
]

# Визуализация данных о расходе воды на карте (пример)
for data in water_data:
    folium.Marker(
        location=[centroid.y, centroid.x], 
        popup=f"Дата: {data['date']}, Расход воды: {data['value']} м³/с",
        icon=folium.Icon(color='blue')
    ).add_to(m)

# Сохранение карты в файл
m.save("48.html")