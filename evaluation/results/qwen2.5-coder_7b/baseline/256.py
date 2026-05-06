import folium
from geopandas import GeoDataFrame, read_file
from shapely.geometry import Point

# Пример данных о реке Талгар (замените на реальные данные)
river_talgar = {
    "name": "Талгар",
    "geometry": Point(43.123456, 70.987654)  # Координаты примера
}

# Создание GeoDataFrame для реки Талгар
gdf_river_talgar = GeoDataFrame([river_talgar], crs="EPSG:4326")

# Определение области интереса (AOI)
aoi = gdf_river_talgar.geometry.buffer(1000)  # Буфер в 1 километр

# Пример данных о доступности воды (замените на реальные данные)
water_accessibility_data = {
    "name": ["Пункт 1", "Пункт 2"],
    "geometry": [Point(43.123, 70.987), Point(43.125, 70.986)],
    "water_volume": [500, 300]  # Объем воды в литрах
}

# Создание GeoDataFrame для доступности воды
gdf_water_accessibility = GeoDataFrame(water_accessibility_data, crs="EPSG:4326")

# Фильтрация данных о доступности воды внутри AOI
filtered_water_accessibility = gdf_water_accessibility[gdf_water_accessibility.geometry.within(aoi)]

# Создание карты
m = folium.Map(location=[river_talgar["geometry"].y, river_talgar["geometry"].x], zoom_start=12)

# Добавление реки Талгар на карту
folium.GeoJson(gdf_river_talgar).add_to(m)

# Добавление точек доступности воды на карту
for idx, row in filtered_water_accessibility.iterrows():
    folium.Marker(
        location=[row["geometry"].y, row["geometry"].x],
        popup=f"Пункт {idx + 1}: Объем воды - {row['water_volume']} л",
        icon=folium.Icon(color="green", icon="info-sign")
    ).add_to(m)

# Сохранение карты
m.save("256.html")

print("Карта сохранена как '256.html'")