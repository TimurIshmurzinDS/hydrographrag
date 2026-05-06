import geopandas as gpd
import folium
from shapely import wkt

# Загрузка данных о бассейне из shape-файла
basin_data = gpd.read_file(r"data/basin_data.shp")
basin_data.crs = 'EPSG:4326'

# Создание карты с центром в середине бассейна и использованием слоя CartoDB positron
m = folium.Map(location=[basin_data.centroid.y, basin_data.centroid.x], zoom_start=10, tiles='CartoDB positron')

# Добавление бассейна на карту с прозрачностью 20%
folium.GeoJson(basin_data.to_crs(epsg=3857).geometry.apply(lambda x: x.wkt),
                name='Бассейн',
                style_function=lambda x: {'fillColor': 'green', 'color': 'darkgreen', 'fillOpacity': 0.2}).add_to(m)

# Создание списка словарей для последних зафиксированных уровней воды
water_levels = [
    {"location": "2 км выше устья реки Prokhodnoy River", "value": 10},
    {"location": "2 км выше устья реки Prokhodnoy River", "value": 12}
]

# Добавление маркеров на карту для последних зафиксированных уровней воды
for level in water_levels:
    folium.Marker([level["location"]], popup=f"Уровень воды: {level['value']}").add_to(m)

# Сохранение карты в файл
m.save("67.html")