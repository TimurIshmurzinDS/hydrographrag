import geopandas as gpd
from shapely import wkt

# Загрузка данных о бассейне из shape-файла
basin_data = gpd.read_file(r"data/basin_data.shp")
basin_data.crs = 'EPSG:4326'

# Создание карты с центром в середине бассейна и использованием слоя CartoDB positron
m = folium.Map(location=basin_data.centroid, zoom_start=10, tiles='CartoDB positron')

# Добавление бассейна на карту
folium.GeoJson(basin_data.to_crs(epsg=3857).geometry.apply(lambda x: x.wkt),
               name='Basin',
               style_function=lambda x: {'fillColor': 'green', 'color': 'darkgreen', 'fillOpacity': 0.2}).add_to(m)

# Создание списка словарей с координатами (WKT)
coordinates = [
    {
        "type": "Feature",
        "geometry": wkt.loads("POINT(48.6784 35.0331)"),
        "properties": {}
    },
    {
        "type": "Feature",
        "geometry": wkt.loads("POINT(48.6792 35.0345)"),
        "properties": {}
    }
]

# Добавление координат на карту
folium.GeoJson(coordinates, name='Coordinates').add_to(m)

# Сохранение карты в файл
m.save("127.html")