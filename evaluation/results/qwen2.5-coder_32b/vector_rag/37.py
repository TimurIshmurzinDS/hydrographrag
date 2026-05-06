import geopandas as gpd
import folium
from shapely import wkt

# Загрузка данных о водном бассейне
basin_data = gpd.read_file(r"data/basin_data.shp")
basin_data = basin_data.to_crs('EPSG:4326')

# Инициализация карты с центром в точке, соответствующей центроиду водного бассейна
centroid = basin_data.geometry.centroid.iloc[0]
m = folium.Map(location=[centroid.y, centroid.x], tiles='CartoDB positron', zoom_start=12)

# Добавление границы водного бассейна на карту
folium.GeoJson(basin_data.to_json(), name="Basin", style_function=lambda x: {'fillColor': 'green', 'color': 'darkgreen', 'fillOpacity': 0.2}).add_to(m)

# Пример данных о точках измерений уровня воды и потребления (WKT)
measurements = [
    {"geometry": wkt.loads("POINT(37.618421 55.755826)"), "Water_level_Value": 150, "Date_water_level_Value": "2023-01-01"},
    {"geometry": wkt.loads("POINT(37.619421 55.756826)"), "Water_consumption_Valuem³s": 100, "Date_water_level_Value": "2023-01-01"}
]

# Добавление точек измерений на карту
for measurement in measurements:
    folium.Marker(
        location=[measurement["geometry"].y, measurement["geometry"].x],
        popup=f"Water Level: {measurement.get('Water_level_Value', 'N/A')} mm\nWater Consumption: {measurement.get('Water_consumption_Valuem³s', 'N/A')} m³/s"
    ).add_to(m)

# Сохранение карты в файл
m.save("37.html")