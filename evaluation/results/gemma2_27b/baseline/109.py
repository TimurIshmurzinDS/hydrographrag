import geopandas as gpd
from shapely.geometry import Point
from shapely.ops import nearest_points
import folium

# Загрузка данных о реках и пастбищных землях
rivers = gpd.read_file("rivers.shp")
pastures = gpd.read_file("pastures.shp")

# Расчет расстояния от пастбищных земель до рек
distances = []
for index, row in pastures.iterrows():
    point = Point(row.geometry.x, row.geometry.y)
    nearest_river = rivers.nearest(Point(row.geometry.x, row.geometry.y))
    distance = nearest_points(point, nearest_river.geometry)[0].distance(nearest_river.geometry[0])
    distances.append(distance)

# Создание растрового слоя с gradation доступности водных ресурсов
raster = gpd.GeoDataFrame({"geometry": pastures.geometry, "distance": distances})
raster["availability"] = 1 - (raster["distance"] / raster["distance"].max())

# Визуализация данных на карте
m = folium.Map(location=[rivers.centroid.y, rivers.centroid.x], zoom_start=10)
folium.GeoJson("rivers.shp").add_to(m)
folium.GeoJson("pastures.shp").add_to(m)

# Визуализация gradation доступности водных ресурсов
raster.plot(ax=m, column="availability", cmap="viridis")

m.save("109.html")