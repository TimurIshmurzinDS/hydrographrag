import geopandas as gpd
import folium
from shapely import wkt

# Загрузка данных бассейна из shapefile
basin_gdf = gpd.read_file(r"data/basin_data.shp")
basin_gdf = basin_gdf.to_crs('EPSG:4326')

# Инициализация карты с центром в бассейне реки Эмель
centroid = basin_gdf.geometry.centroid.iloc[0]
m = folium.Map(location=[centroid.y, centroid.x], tiles='CartoDB positron', zoom_start=10)

# Добавление бассейна на карту
folium.GeoJson(basin_gdf.to_json(), name="Basin", style_function=lambda x: {'fillColor': 'green', 'color': 'darkgreen', 'fillOpacity': 0.2}).add_to(m)

# Если есть координаты (WKT), создаем список словарей
observations = [
    {"name": "Sarykan River Confluence", "geometry": wkt.loads("POINT(75.3456 41.1234)"), "description": "Приток реки Сарыкан в бассейн реки Эмель"},
    {"name": "Observation Point", "geometry": wkt.loads("POINT(75.3500 41.1280)"), "description": "Точка наблюдения на расстоянии 0.2 км выше соединения с рекой Осек"}
]

# Добавление точек наблюдений на карту
for obs in observations:
    folium.Marker(
        location=[obs["geometry"].y, obs["geometry"].x],
        popup=folium.Popup(f"<b>{obs['name']}</b><br>{obs['description']}", max_width=300),
        icon=folium.Icon(color='blue')
    ).add_to(m)

# Сохранение карты в HTML файл
m.save("168.html")