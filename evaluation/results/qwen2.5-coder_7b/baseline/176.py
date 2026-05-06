import geopandas as gpd
from shapely.geometry import Point, LineString
import folium

# Загрузка данных
terisbutak = gpd.read_file('path_to_terisbutak.shp')
talgar = gpd.read_file('path_to_talgar.shp')

# Создание геометрии для каждого узла русла ручья Терисбутак
terisbutak_points = terisbutak.geometry.apply(lambda geom: geom.centroid if geom.type == 'LineString' else geom)

# Инициализация карты
m = folium.Map(location=[terisbutak.geometry.centroid.y.mean(), terisbutak.geometry.centroid.x.mean()], zoom_start=12)

# Нахождение ближайшей точки от каждого узла русла ручья до реки Талгар
for point in terisbutak_points:
    distances = talgar.geometry.apply(lambda geom: point.distance(geom))
    nearest_talgar = talgar.iloc[distances.idxmin()]
    folium.Marker([point.y, point.x], popup=f"Ближайшая точка к руслу Терисбутак", icon=folium.Icon(color='red')).add_to(m)
    folium.PolyLine([[point.y, point.x], [nearest_talgar.geometry.centroid.y, nearest_talgar.geometry.centroid.x]], color='blue').add_to(m)

# Сохранение карты
m.save("176.html")