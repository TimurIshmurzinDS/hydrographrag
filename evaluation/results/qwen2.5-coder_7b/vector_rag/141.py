import geopandas as gpd
import folium
from shapely import wkt

# Загрузка данных о реках и их текущих уровнях воды
data = {
    "Coordinates": [
        {"WKT": "POINT(10 20)", "Water_level_Value": 50, "Water_Classification": "Критический"},
        {"WKT": "POINT(30 40)", "Water_level_Value": 60, "Water_Classification": "Нормальный"},
        {"WKT": "POINT(50 60)", "Water_level_Value": 70, "Water_Classification": "Критический"}
    ]
}

# Преобразование WKT в геометрии
geometries = [wkt.loads(point["WKT"]) for point in data["Coordinates"]]
gdf = gpd.GeoDataFrame(data, geometry=geometries)

# Создание карты
centroid = gdf.geometry.centroid[0]
m = folium.Map(location=[centroid.y, centroid.x], zoom_start=10, tiles='CartoDB positron')

# Добавление границы бассейна (если необходимо)
basin_data = gpd.read_file(r"data/basin_data.shp")
basin_data.to_crs(epsg=4326, inplace=True)
folium.GeoJson(basin_data.geometry, style_function=lambda x: {'fillColor': 'green', 'color': 'darkgreen', 'fillOpacity': 0.2}).add_to(m)

# Добавление маркеров с критическими уровнями воды
for idx, row in gdf.iterrows():
    if row["Water_Classification"] == "Критический":
        folium.Marker([row.geometry.y, row.geometry.x], popup=f"Уровень воды: {row['Water_level_Value']} cm", icon=folium.Icon(color='red')).add_to(m)

# Сохранение карты
m.save("141.html")