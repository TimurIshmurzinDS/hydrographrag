import geopandas as gpd
import folium
from shapely import wkt

# Загрузить shapefile с внешними границами бассейна
gdf = gpd.read_file(r"data/basin_data.shp").to_crs('EPSG:4326')

# Создать карту с центром в середине бассейна и параметрами tiles='CartoDB positron'
m = folium.Map(location=gdf.centroid.coords[0], zoom_start=10, tiles='CartoDB positron')

# Добавить бассейн на карту
folium.GeoJson(gdf.to_json(), name='basin').add_to(m)

# Создать список словарей с координатами точки наблюдения
point_coords = [
    {
        'type': 'Feature',
        'geometry': wkt.loads('POINT(47.123456 69.901234)'),
        'properties': {'name': 'Точка наблюдения'}
    }
]

# Добавить точку на карту
folium.Marker([point_coords[0]['geometry']['coordinates'][1], point_coords[0]['geometry']['coordinates'][0]], 
              icon=folium.Icon(color='blue')).add_to(m)

# Сохранить карту в файл
m.save("267.html")