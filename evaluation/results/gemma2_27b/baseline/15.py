import geopandas as gpd
from shapely.geometry import Point
import folium

# Загрузка данных о гидрологических станциях
stations = gpd.read_file("hydrological_stations.shp") 

# Загрузка данных об уровнях воды (предполагаем, что они хранятся в столбце 'water_level')
water_levels = stations['water_level']

# Интерполяция уровней воды (пример с IDW)
from scipy.interpolate import idw
x, y = stations.geometry.x, stations.geometry.y
z = water_levels

# Создание сетки для интерполяции
xi, yi = np.mgrid[x.min():x.max():100j, y.min():y.max():100j]

# Интерполирование уровней воды на сетке
zi = idw( (x, y), z, (xi, yi) )

# Создание карты с folium
m = folium.Map(location=[stations.geometry.y.mean(), stations.geometry.x.mean()], zoom_start=12)

# Добавление гидрологических станций на карту
for idx, row in stations.iterrows():
    folium.Marker(
        location=[row.geometry.y, row.geometry.x], 
        popup=f"Уровень воды: {row['water_level']}"
    ).add_to(m)

# Визуализация интерполированных уровней воды (пример - heatmap)
from folium.plugins import HeatMap
HeatMap(zi, radius=15).add_to(m)

# Сохранение карты
m.save("15.html")