import geopandas as gpd
import folium
from shapely import wkt

# Загрузка данных о бассейне в формате shapefile
basin_data = gpd.read_file(r"data/basin_data.shp")
basin_data.crs = 'EPSG:4326'

# Создание карты с центром в координатах центра бассейна и использованием слоя CartoDB positron
m = folium.Map(location=[basin_data.centroid.y, basin_data.centroid.x], tiles='CartoDB positron')

# Добавление бассейна на карту в виде GeoJson с определенным цветом и прозрачностью
folium.GeoJson(data=basin_data.to_crs(epsg=4326).to_json(), name='basin').add_to(m)

# Создание списка словарей для координат (WKT)
wkt_coords = [
    {
        'lat': 55.123456,
        'lon': 37.654321
    },
    {
        'lat': 55.987654,
        'lon': 38.765432
    }
]

# Добавление координат на карту в виде маркеров
for coord in wkt_coords:
    folium.Marker([coord['lat'], coord['lon']], icon=folium.Icon(color='red')).add_to(m)

# Сохранение карты в файл с именем "265.html"
m.save("265.html")