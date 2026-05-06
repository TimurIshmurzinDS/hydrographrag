import geopandas as gpd
import folium
from shapely import wkt

# Загрузка данных о бассейне
basin_gdf = gpd.read_file(r"data/basin_data.shp")
basin_gdf = basin_gdf.to_crs('EPSG:4326')

# Инициализация карты с центром в центроиде бассейна
centroid = basin_gdf.geometry.centroid.iloc[0]
m = folium.Map(location=[centroid.y, centroid.x], tiles='CartoDB positron', zoom_start=10)

# Добавление границ бассейна на карту
folium.GeoJson(basin_gdf.to_json(), name="Basin", style_function=lambda x: {'fillColor': 'green', 'color': 'darkgreen', 'fillOpacity': 0.2}).add_to(m)

# Пример данных о уровнях воды (заменить на реальные данные)
water_data = [
    {"name": "Река1", "coordinates": wkt.loads("POINT(37.6173 55.7558)"), "Water_Classification": "критический"},
    {"name": "Река2", "coordinates": wkt.loads("POINT(37.6204 55.7540)"), "Water_Classification": "нормальный"},
    {"name": "Река3", "coordinates": wkt.loads("POINT(37.6189 55.7532)"), "Water_Classification": "критический"}
]

# Добавление маркеров на карту для рек с критическим уровнем воды
for entry in water_data:
    if entry["Water_Classification"] == "критический":
        folium.Marker(
            location=[entry["coordinates"].y, entry["coordinates"].x],
            popup=entry["name"],
            icon=folium.Icon(color='red')
        ).add_to(m)

# Сохранение карты в файл
m.save("141.html")