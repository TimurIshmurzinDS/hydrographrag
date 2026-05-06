import geopandas as gpd
import folium
from shapely import wkt

# Загрузка данных о водном бассейне
basin_data = gpd.read_file(r"data/basin_data.shp")
basin_data = basin_data.to_crs('EPSG:4326')

# Инициализация карты с центром в центроиде водного бассейна
centroid = basin_data.geometry.centroid.iloc[0]
m = folium.Map(location=[centroid.y, centroid.x], tiles='CartoDB positron', zoom_start=12)

# Добавление границ водного бассейна на карту
folium.GeoJson(basin_data.to_json(), name="Basin", style_function=lambda x: {'fillColor': 'green', 'color': 'darkgreen', 'fillOpacity': 0.2}).add_to(m)

# Пример координат ручья Терисбутак и других водных объектов (WKT)
water_features = [
    {"name": "Terisbuthak Creek", "geometry": wkt.loads("LINESTRING(34.123 56.789, 34.124 56.790)"), "type": "HY_HydroFeature"},
    # Добавьте другие водные объекты по мере необходимости
]

# Добавление водных объектов на карту
for feature in water_features:
    folium.GeoJson(feature["geometry"], name=feature["name"]).add_to(m)

# Сохранение карты в файл
m.save("170.html")