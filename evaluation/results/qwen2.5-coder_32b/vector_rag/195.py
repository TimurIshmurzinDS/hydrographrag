import geopandas as gpd
import folium
from shapely import wkt

# Загрузка shapefile и преобразование CRS
basin = gpd.read_file(r"data/basin_data.shp")
basin = basin.to_crs('EPSG:4326')

# Инициализация карты с центром в бассейне реки Уржар
centroid = basin.geometry.centroid.iloc[0]
m = folium.Map(location=[centroid.y, centroid.x], tiles='CartoDB positron', zoom_start=10)

# Добавление бассейна на карту
folium.GeoJson(basin.to_json(), name="Basin", style_function=lambda x: {'fillColor': 'green', 'color': 'darkgreen', 'fillOpacity': 0.2}).add_to(m)

# Пример координат водопотребления (WKT)
water_consumption_points_wkt = [
    "POINT(48.35 69.12)",
    "POINT(48.37 69.15)"
]

# Преобразование WKT в GeoDataFrame
water_consumption_points = [wkt.loads(point) for point in water_consumption_points_wkt]
gdf_water_consumption = gpd.GeoDataFrame(geometry=water_consumption_points, crs='EPSG:4326')

# Добавление точек водопотребления на карту
for _, row in gdf_water_consumption.iterrows():
    folium.Marker([row.geometry.y, row.geometry.x], popup="Точка водопотребления").add_to(m)

# Сохранение карты в HTML файл
m.save("195.html")