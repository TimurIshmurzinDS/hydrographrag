import geopandas as gpd
import folium
from shapely import wkt

# Загрузка данных о водном бассейне
basin_data = gpd.read_file(r"data/basin_data.shp")
basin_data = basin_data.to_crs('EPSG:4326')

# Инициализация карты с центром в бассейне реки Лепси
centroid = basin_data.geometry.centroid.iloc[0]
m = folium.Map(location=[centroid.y, centroid.x], tiles='CartoDB positron', zoom_start=10)

# Добавление границ водного бассейна на карту
folium.GeoJson(basin_data.to_json(), name="Basin", style_function=lambda x: {'fillColor': 'green', 'color': 'darkgreen', 'fillOpacity': 0.2}).add_to(m)

# Предположим, что у нас есть координаты точек измерений качества воды в формате WKT
measurements_wkt = [
    "POINT (37.618421 55.755826)",
    "POINT (37.620421 55.757826)",
    "POINT (37.622421 55.759826)"
]

# Преобразование WKT в геометрические объекты
measurements = [{'geometry': wkt.loads(wkt_str)} for wkt_str in measurements_wkt]
measurements_gdf = gpd.GeoDataFrame(measurements, crs='EPSG:4326')

# Добавление точек измерений на карту
for _, row in measurements_gdf.iterrows():
    folium.CircleMarker(
        location=[row.geometry.y, row.geometry.x],
        radius=5,
        color='blue',
        fill=True,
        fill_color='blue'
    ).add_to(m)

# Сохранение карты в файл
m.save("42.html")