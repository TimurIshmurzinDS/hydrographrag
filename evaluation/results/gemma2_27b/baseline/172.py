import geopandas as gpd
from shapely.geometry import Polygon
import rasterio
import rasterio.plot as rplot
import matplotlib.pyplot as plt
import folium

# Загрузка данных
river_network = gpd.read_file("river_network.shp")
dem = rasterio.open("dem.tif")

# Определение зоны водосбора
watershed_zone = ... # Используйте библиотеку для расчета зоны водосбора (например, "Watershed" в ArcGIS)

# Фильтрация дренажной сети внутри зоны водосбора
river_network_in_watershed = river_network[river_network.intersects(watershed_zone)]

# Расчет длины дренажной сети
total_length = sum([line.length for line in river_network_in_watershed])

# Расчет площади зоны водосбора
area = ... # Используйте библиотеку для расчета площади полигона (например, "shapely")

# Расчет плотности дренажной сети
density = total_length / area

print(f"Плотность дренажной сети: {density} км/км²")

# Визуализация на карте
m = folium.Map()
folium.GeoJson("river_network.shp").add_to(m)
folium.GeoJson("watershed_zone.shp").add_to(m)
m.save("172.html")