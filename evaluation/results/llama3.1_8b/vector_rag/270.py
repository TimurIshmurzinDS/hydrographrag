import geopandas as gpd
import folium
from shapely import wkt

# Загрузка shapefile с данными о реке Талгар
gdf = gpd.read_file(r"data/basin_data.shp").to_crs('EPSG:4326')

# Создание карты с центром в середине области
m = folium.Map(location=gdf.centroid.iloc[0], zoom_start=10, tiles='CartoDB positron')

# Добавление области на карту
folium.GeoJson(gdf.to_json(), name='basin').add_to(m)

# Создание списка координат (WKT) для расчета индекса NDVI
wkt_coords = [
    {'type': 'Point', 'coordinates': [76.2345, 43.1234]},
    {'type': 'Point', 'coordinates': [76.3456, 43.4567]}
]

# Расчет индекса NDVI на основе уровня воды в реке Талгар
ndvi_values = []
for i in range(len(wkt_coords)):
    ndvi_value = (wkt_coords[i]['coordinates'][0] + wkt_coords[i]['coordinates'][1]) / 2 * gdf['Water_level_Value'].iloc[0]
    ndvi_values.append(ndvi_value)

# Добавление индекса NDVI на карту
folium.Marker([gdf.centroid.iloc[0].y, gdf.centroid.iloc[0].x], popup='NDVI: ' + str(ndvi_values[0])).add_to(m)
folium.Marker([gdf.centroid.iloc[1].y, gdf.centroid.iloc[1].x], popup='NDVI: ' + str(ndvi_values[1])).add_to(m)

# Сохранение карты в файл
m.save("270.html")