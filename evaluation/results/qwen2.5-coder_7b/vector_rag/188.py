import geopandas as gpd
import folium
from shapely import wkt

# Загрузка данных о бассейнах
basin_data = r"data/basin_data.shp"
gdf = gpd.read_file(basin_data)
gdf = gdf.to_crs('EPSG:4326')

# Создание карты с центром в centroid бассейна
centroid = gdf.geometry.centroid[0]
m = folium.Map(location=[centroid.y, centroid.x], zoom_start=10, tiles='CartoDB positron')

# Добавление бассейна на карту
folium.GeoJson(gdf.to_json(), style_function=lambda x: {
    'fillColor': 'green',
    'color': 'darkgreen',
    'fillOpacity': 0.2
}).add_to(m)

# Пример данных о качестве воды и типах водных организмов для Шарын и Уржар (замените на реальные данные)
water_quality_sharyn = "II"
organisms_sharyn = ["Рыба", "Моллюски"]
water_quality_urzhar = "III"
organisms_urzhar = ["Рыба", "Моллюски", "Водяные растения"]

# Добавление информации о состоянии бассейна на карту
folium.Marker(
    location=[centroid.y, centroid.x],
    popup=f"Шарын: Качество воды - {water_quality_sharyn}, Виды организмов - {', '.join(organisms_sharyn)}",
    icon=folium.Icon(color='green')
).add_to(m)

folium.Marker(
    location=[centroid.y, centroid.x],
    popup=f"Уржар: Качество воды - {water_quality_urzhar}, Виды организмов - {', '.join(organisms_urzhar)}",
    icon=folium.Icon(color='blue')
).add_to(m)

# Сохранение карты
m.save("188.html")