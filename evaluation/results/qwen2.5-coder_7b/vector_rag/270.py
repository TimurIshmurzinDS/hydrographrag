import geopandas as gpd
import folium
from shapely import wkt

# Загрузка shapefile с границами бассина
basin_data = gpd.read_file(r"data/basin_data.shp")
basin_data = basin_data.to_crs('EPSG:4326')

# Создание карты
centroid = basin_data.geometry.centroid[0]
m = folium.Map(location=[centroid.y, centroid.x], zoom_start=10, tiles='CartoDB positron')

# Добавление границ бассина на карту
folium.GeoJson(basin_data.to_json(), style_function=lambda x: {
    'fillColor': 'green',
    'color': 'darkgreen',
    'fillOpacity': 0.2
}).add_to(m)

# Пример данных уровня воды в реке Талгар (в см)
water_level_values = [
    {'date': '2023-10-01', 'value_cm': 5},
    {'date': '2023-10-02', 'value_cm': 15},
    {'date': '2023-10-03', 'value_cm': 10}
]

# Порог для определения NDVI
threshold = 10

# Расчет NDVI на основе уровня воды в реке Талгар
ndvi_values = []
for value in water_level_values:
    if value['value_cm'] > threshold:
        ndvi = (value['value_cm'] - threshold) / (2 * threshold)
    else:
        ndvi = -(threshold - value['value_cm']) / (2 * threshold)
    ndvi_values.append({'date': value['date'], 'ndvi': ndvi})

# Добавление точек на карту с расчетом NDVI
for ndvi_value in ndvi_values:
    folium.Marker(
        location=[centroid.y, centroid.x],
        popup=f"Date: {ndvi_value['date']}, NDVI: {ndvi_value['ndvi']:.2f}",
        icon=folium.Icon(color='red' if ndvi_value['ndvi'] < 0 else 'green')
    ).add_to(m)

# Сохранение карты
m.save("270.html")