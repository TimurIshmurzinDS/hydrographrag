import geopandas as gpd
import folium
from shapely import wkt

# Загрузка данных о бассейне из shapefile
basin_data = gpd.read_file(r"data/basin_data.shp")
basin_data = basin_data.to_crs('EPSG:4326')

# Инициализация карты с центром в бассейне
centroid = basin_data.geometry.centroid.iloc[0]
m = folium.Map(location=[centroid.y, centroid.x], tiles='CartoDB positron', zoom_start=10)

# Добавление бассейна на карту
folium.GeoJson(basin_data.to_json(), name="Basin", style_function=lambda x: {'fillColor': 'green', 'color': 'darkgreen', 'fillOpacity': 0.2}).add_to(m)

# Предполагаемые координаты точек наблюдения (WKT)
coordinates = [
    {"name": "Kishi Almaty River", "wkt": "POINT(76.9345 42.8617)"},
    {"name": "Bayankol River", "wkt": "POINT(76.8000 42.9000)"}
]

# Преобразование координат из WKT в точки
points = [gpd.GeoSeries.from_wkt([coord["wkt"]]).iloc[0] for coord in coordinates]

# Добавление точек наблюдения на карту
for point, coord in zip(points, coordinates):
    folium.Marker(
        location=[point.y, point.x],
        popup=coord["name"],
        icon=folium.Icon(color='blue')
    ).add_to(m)

# Сохранение карты в файл
m.save("134.html")