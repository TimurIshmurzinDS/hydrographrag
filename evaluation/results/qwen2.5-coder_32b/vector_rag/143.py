import geopandas as gpd
import folium
from shapely import wkt

# Загрузка данных о бассейне
basin_data = gpd.read_file(r"data/basin_data.shp")
basin_data = basin_data.to_crs('EPSG:4326')

# Инициализация карты с центром в бассейне
centroid = basin_data.geometry.centroid.iloc[0]
m = folium.Map(location=[centroid.y, centroid.x], tiles='CartoDB positron', zoom_start=10)

# Добавление бассейна на карту
folium.GeoJson(basin_data.to_json(), name="Basin", style_function=lambda x: {'fillColor': 'green', 'color': 'darkgreen', 'fillOpacity': 0.2}).add_to(m)

# Пример данных о гидропостах (координаты и уровни воды)
hydro_posts = [
    {"name": "Karatal Post 1", "coordinates": wkt.loads("POINT(76.95 43.25)"), "water_level_cm": [150, 155, 160], "dates": ["2023-01-01", "2023-01-02", "2023-01-03"]},
    {"name": "Karatal Post 2", "coordinates": wkt.loads("POINT(76.98 43.27)"), "water_level_cm": [152, 157, 162], "dates": ["2023-01-01", "2023-01-02", "2023-01-03"]},
    {"name": "Koktal Post 1", "coordinates": wkt.loads("POINT(76.85 43.15)"), "water_level_cm": [140, 145, 150], "dates": ["2023-01-01", "2023-01-02", "2023-01-03"]},
    {"name": "Koktal Post 2", "coordinates": wkt.loads("POINT(76.88 43.17)"), "water_level_cm": [142, 147, 152], "dates": ["2023-01-01", "2023-01-02", "2023-01-03"]}
]

# Добавление маркеров гидропостов на карту
for post in hydro_posts:
    folium.Marker(
        location=[post["coordinates"].y, post["coordinates"].x],
        popup=f"{post['name']}<br>Water Levels: {', '.join(map(str, post['water_level_cm']))}<br>Dates: {', '.join(post['dates'])}",
        icon=folium.Icon(color='blue')
    ).add_to(m)

# Сохранение карты
m.save("143.html")