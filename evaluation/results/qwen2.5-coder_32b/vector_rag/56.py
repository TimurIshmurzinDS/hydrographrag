import geopandas as gpd
import folium
from shapely import wkt

# Загрузка данных о бассейне
basin_data = gpd.read_file(r"data/basin_data.shp")
basin_data = basin_data.to_crs('EPSG:4326')

# Инициализация карты с центром в бассейне реки Dos River
centroid = basin_data.geometry.centroid.iloc[0]
m = folium.Map(location=[centroid.y, centroid.x], tiles='CartoDB positron', zoom_start=10)

# Добавление бассейна на карту
folium.GeoJson(basin_data.to_json(), name="Basin", style_function=lambda x: {'fillColor': 'green', 'color': 'darkgreen', 'fillOpacity': 0.2}).add_to(m)

# Пример данных о водном уровне (для демонстрации)
water_level_data = [
    {"date": "2018-01-01", "value": 150, "geometry": wkt.loads("POINT(69.345 40.789)")},
    {"date": "2018-02-01", "value": 155, "geometry": wkt.loads("POINT(69.345 40.789)")},
    # Добавьте остальные данные о водном уровне здесь
]

# Добавление точек наблюдения на карту
for obs in water_level_data:
    folium.CircleMarker(
        location=[obs['geometry'].y, obs['geometry'].x],
        radius=5,
        popup=f"Date: {obs['date']}, Water Level: {obs['value']} m",
        color='blue',
        fill=True,
        fill_color='blue'
    ).add_to(m)

# Сохранение карты
m.save("56.html")