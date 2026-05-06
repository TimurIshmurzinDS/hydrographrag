import geopandas as gpd
from shapely.geometry import shape
import folium

# Загрузите данные о координатах русел рек в формате GeoJSON или Shapefile.
# Для примера мы будем использовать фиктивные данные.
shynzhaly = {
    "type": "FeatureCollection",
    "features": [
        {
            "type": "Feature",
            "geometry": {"type": "LineString", "coordinates": [[45.0, 60.0], [50.0, 65.0]]},
            "properties": {},
        }
    ]
}

talgar = {
    "type": "FeatureCollection",
    "features": [
        {
            "type": "Feature",
            "geometry": {"type": "LineString", "coordinates": [[55.0, 70.0], [60.0, 75.0]]},
            "properties": {},
        }
    ]
}

# Преобразуйте данные в геообъекты Shapely.
shynzhaly_gdf = gpd.GeoDataFrame.from_features(shynzhaly["features"])
talgar_gdf = gpd.GeoDataFrame.from_features(talgar["features"])

# Определите пересечение двух геометрий.
intersection_geom = shynzhaly_gdf.geometry[0].intersection(talgar_gdf.geometry[0])

# Если пересечение не пусто, то оно будет представлено в виде полигона или линии.
if intersection_geom:
    print("Пересечение существует.")
else:
    print("Пересечения нет.")

# Создайте карту с маркерами для исходных данных и результата пересечения.
m = folium.Map(location=[(shynzhaly_gdf.geometry[0].y.max() + talgar_gdf.geometry[0].y.min()) / 2, 
                         (shynzhaly_gdf.geometry[0].x.max() + talgar_gdf.geometry[0].x.min()) / 2], zoom_start=10)

# Добавьте маркеры для исходных данных.
folium.Marker([shynzhaly_gdf.geometry[0].y, shynzhaly_gdf.geometry[0].x], 
              popup="Река Шынжалы").add_to(m)
folium.Marker([talgar_gdf.geometry[0].y, talgar_gdf.geometry[0].x], 
              popup="Река Талгар").add_to(m)

# Добавьте полигон для результата пересечения.
if intersection_geom:
    folium.Polygon(intersection_geom.exterior.coords[:], color='red').add_to(m)

# Сохраните карту в файл.
m.save("169.html")