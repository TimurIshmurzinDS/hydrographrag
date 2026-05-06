import geopandas as gpd
import folium
from shapely import wkt

# Загрузить данные о бассейне реки Или из файла data/basin_data.shp
gdf = gpd.read_file(r"data/basin_data.shp")
gdf = gdf.to_crs('EPSG:4326')

# Создать карту с использованием библиотеки Folium и добавить на нее бассейн
m = folium.Map(location=gdf.centroid.coords[0], zoom_start=10, tiles='CartoDB positron')
folium.GeoJson(gdf.to_crs('EPSG:4326').geometry.__geo_interface__, 
               name='Basin',
               style_function=lambda x: {'fillColor': 'green', 'color': 'darkgreen', 'fillOpacity': 0.2}).add_to(m)

# Если в контексте есть координаты (WKT), создать список словарей для отображения этих координат на карте
if gdf['geometry'].any():
    coordinates = []
    for i, row in gdf.iterrows():
        geometry = wkt.loads(row.geometry.wkt)
        coordinates.append({
            'type': 'Feature',
            'geometry': geometry.__geo_interface__,
            'properties': {
                'name': f'Coordinate {i}'
            }
        })
    
    folium.GeoJson(coordinates, 
                   name='Coordinates', 
                   style_function=lambda x: {'fillColor': '#ff0000', 'color': '#00ff00', 'fillOpacity': 0.2}).add_to(m)

# Сохранить карту в файл
m.save("144.html")