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

# Пример данных о расходе воды (в реальном сценарии данные должны быть загружены из источника)
water_data = [
    {"river": "Koktal River", "date": "2023-01-01", "Water_consumption_Valuem³s": 5.0},
    {"river": "Koktal River", "date": "2023-07-01", "Water_consumption_Valuem³s": 20.0},
    {"river": "Baskan River", "date": "2023-01-01", "Water_consumption_Valuem³s": 4.0},
    {"river": "Baskan River", "date": "2023-07-01", "Water_consumption_Valuem³s": 18.0}
]

# Преобразование данных в GeoDataFrame для визуализации
gdf_water_data = gpd.GeoDataFrame(water_data, geometry=[wkt.loads("POINT (0 0)")]*len(water_data))  # Примерные координаты

# Добавление маркеров на карту с информацией о расходе воды
for _, row in gdf_water_data.iterrows():
    folium.Marker(
        location=(centroid.y, centroid.x),  # Используем центр бассейна для примера
        popup=f"Река: {row['river']}, Дата: {row['date']}, Расход воды: {row['Water_consumption_Valuem³s']} м³/с",
        icon=folium.Icon(color='blue')
    ).add_to(m)

# Сохранение карты
m.save("85.html")