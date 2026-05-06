import geopandas as gpd
import folium
from shapely import wkt

# Загрузка данных о бассейне
basin_data = gpd.read_file(r"data/basin_data.shp")
basin_data = basin_data.to_crs(epsg=4326)

# Инициализация карты с центроидом бассейна
centroid = basin_data.geometry.centroid.iloc[0]
m = folium.Map(location=[centroid.y, centroid.x], tiles='CartoDB positron', zoom_start=10)

# Добавление границ бассейна на карту
folium.GeoJson(basin_data.to_json(), name="Basin", style_function=lambda x: {'fillColor': 'green', 'color': 'darkgreen', 'fillOpacity': 0.2}).add_to(m)

# Пример данных о уровнях воды для рек Tentek River и Temirlik River
water_level_data = [
    {"name": "Tentek River", "coordinates": wkt.loads("POINT(45.123 40.456)"), "date": "2023-10-01", "level_cm": 150},
    {"name": "Temirlik River", "coordinates": wkt.loads("POINT(45.789 40.123)"), "date": "2023-10-01", "level_cm": 160}
]

# Добавление точек измерений уровня воды на карту
for data in water_level_data:
    folium.Marker(
        location=[data['coordinates'].y, data['coordinates'].x],
        popup=f"Река: {data['name']}, Дата: {data['date']}, Уровень воды: {data['level_cm']} см",
        icon=folium.Icon(color='blue')
    ).add_to(m)

# Сохранение карты в файл
m.save("72.html")