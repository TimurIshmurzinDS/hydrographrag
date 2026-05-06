import geopandas as gpd
import folium
from shapely import wkt

# Загрузка границы ручья из контекста (пример данных)
basin_data = {
    "geometry": [wkt.loads("POLYGON((0 0, 1 0, 1 1, 0 1, 0 0))")]
}

# Создание GeoDataFrame для границы ручья
basin_gdf = gpd.GeoDataFrame(basin_data)
basin_gdf.crs = 'EPSG:4326'

# Координаты WKT для русел рек Шынжалы и Талгар (пример данных)
shynzhaly_rusel_wkt = "POINT(0.5 0.5)"
talgar_rusel_wkt = "POINT(0.7 0.3)"

# Создание GeoDataFrame для русел
rusels_gdf = gpd.GeoDataFrame({
    'name': ['Shynzhaly Rusel', 'Talgar Rusel'],
    'geometry': [wkt.loads(shynzhaly_rusel_wkt), wkt.loads(talgar_rusel_wkt)]
})
rusels_gdf.crs = 'EPSG:4326'

# Создание карты
m = folium.Map(location=basin_gdf.geometry.centroid.iloc[0].coords[0], zoom_start=10, tiles='CartoDB positron')

# Добавление границ ручья на карту
folium.GeoJson(basin_gdf.to_json(), style_function=lambda x: {'fillColor': 'green', 'color': 'darkgreen', 'fillOpacity': 0.2}).add_to(m)

# Добавление русел на карту
for idx, row in rusels_gdf.iterrows():
    folium.Marker(location=row.geometry.coords[0], popup=row['name']).add_to(m)

# Вычисление пересечения русел
intersection = rusels_gdf.geometry.intersection(rusels_gdf.geometry)
if not intersection.is_empty:
    folium.CircleMarker(location=intersection.centroid.coords[0], radius=5, color='red', fill=True, fill_color='red').add_to(m)

# Сохранение карты
m.save("169.html")