import geopandas as gpd
from geopy.distance import geodesic

# Загрузить данные о реках
dos = gpd.read_file("dos.shp")
emel = gpd.read_file("emel.shp")

# Найти координаты устья Доса и начала Емеля
dos_mouth = dos.loc[dos["name"] == "Дос"].geometry.iloc[0].coords[0]  
emel_source = emel.loc[emel["name"] == "Емель"].geometry.iloc[0].coords[0]

# Вычислить расстояние
distance = geodesic(dos_mouth, emel_source).km

print(f"Расстояние между устьем реки Дос и началом реки Емель: {distance:.2f} км")

# Визуализация (необязательно)
import folium

m = folium.Map(location=[dos_mouth[1], dos_mouth[0]], zoom_start=8)

folium.GeoJson("dos.shp").add_to(m)
folium.GeoJson("emel.shp").add_to(m)

folium.Marker(location=dos_mouth, popup="Устье реки Дос").add_to(m)
folium.Marker(location=emel_source, popup="Начало реки Емель").add_to(m)

m.save("92.html")