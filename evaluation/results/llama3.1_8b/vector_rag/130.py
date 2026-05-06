import geopandas as gpd
import folium
from shapely import wkt

# Загрузка данных о реках и селе из соответствующих файлов
gdf_basin = gpd.read_file(r"data/basin_data.shp")
gdf_basin.crs = 'EPSG:4326'

# Создание карты с центром в координатах центра полигона
m = folium.Map(location=gdf_basin.centroid.coords[0], zoom_start=10, tiles='CartoDB positron')

# Добавление полигона на карту
folium.GeoJson(gdf_basin.to_crs(epsg=4326).geometry.__geo_interface__,
               name='basin',
               style={'fillColor': 'green', 'color': 'darkgreen', 'fillOpacity': 0.2}).add_to(m)

# Создание списка координат точек наблюдения (сел) в формате WKT
wkt_coords = [
    {'lat': 47.123, 'lon': 88.456},
    {'lat': 47.234, 'lon': 88.567},
    {'lat': 47.345, 'lon': 88.678}
]

# Сформирование базового уровня стока для Bayankol River на основе данных Shilik River
base_level = gdf_basin[gdf_basin['name'] == 'Shilik River'].geometry.iloc[0].centroid.coords[0][1]

# Вычисление исторического отклонения стока Bayankol River относительно базового уровня
def calculate_flow_deviation(flow_data, base_level):
    deviation = []
    for flow in flow_data:
        deviation.append(flow - base_level)
    return deviation

flow_data = [10.5, 12.7, 15.2]  # примерные данные о стоке Bayankol River
deviation = calculate_flow_deviation(flow_data, base_level)

# Добавление точек наблюдения на карту
for coord in wkt_coords:
    folium.Marker([coord['lat'], coord['lon']], popup=f'Село {coord["lat"]}, {coord["lon"]}').add_to(m)

# Сохранение карты в файл
m.save("130.html")