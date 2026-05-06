import geopandas as gpd
import folium
from shapely import wkt

# Загрузка данных о водном бассейне
basin_data = gpd.read_file(r"data/basin_data.shp")
basin_data = basin_data.to_crs('EPSG:4326')

# Создание карты с центром в центроиде водного бассейна
centroid = basin_data.geometry.centroid.iloc[0]
m = folium.Map(location=[centroid.y, centroid.x], tiles='CartoDB positron', zoom_start=10)

# Добавление границ водного бассейна на карту
folium.GeoJson(basin_data.to_json(), name="Basin", style_function=lambda x: {'fillColor': 'green', 'color': 'darkgreen', 'fillOpacity': 0.2}).add_to(m)

# Предположительные координаты постов наблюдений (WKT)
# В реальном сценарии эти данные должны быть получены из надежного источника
observation_points_wkt = [
    "POINT(69.15 40.35)",
    "POINT(69.20 40.40)",
    "POINT(69.25 40.45)",
    "POINT(69.30 40.50)"
]

# Преобразование WKT в геометрические объекты и создание DataFrame
observation_points = [wkt.loads(point) for point in observation_points_wkt]
observation_df = gpd.GeoDataFrame(geometry=observation_points, crs='EPSG:4326')

# Пример данных о расходе воды для постов наблюдений (в кубических метрах в секунду)
discharge_data = [10.5, 12.3, 9.8, 11.7]
observation_df['discharge'] = discharge_data

# Добавление маркеров на карту с информацией о расходе воды
for _, row in observation_df.iterrows():
    folium.Marker(
        location=[row.geometry.y, row.geometry.x],
        popup=f"Расход воды: {row.discharge} м³/с",
        icon=folium.Icon(color='blue')
    ).add_to(m)

# Сохранение карты в HTML файл
m.save("78.html")