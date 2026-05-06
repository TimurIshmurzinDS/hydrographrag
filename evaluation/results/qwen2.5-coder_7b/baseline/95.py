import geopandas as gpd
from shapely.geometry import Point
import folium

# Загрузка данных о реках
ulken_almaty = gpd.read_file('ulken_almaty.shp')
shyzyn = gpd.read_file('shyzyn.shp')

# Определение притока реки Улькен Алматы
def find_sources(river, all_rivers):
    sources = []
    for other_river in all_rivers:
        if not river.geometry.equals(other_river.geometry) and river.geometry.within(other_river.geometry):
            sources.append(other_river)
    return sources

ulken_almaty_sources = find_sources(ulken_almaty, ulken_almaty)

# Определение притока реки Шыжын
shyzyn_sources = find_sources(shyzyn, shyzyn)

# Проверка связи между реками через систему притоков
def are_connected(river1, river2):
    sources_river1 = find_sources(river1, ulken_almaty)
    sources_river2 = find_sources(river2, shyzyn)
    
    for source in sources_river1:
        if source in sources_river2:
            return True
    return False

connected = are_connected(ulken_almaty, shyzyn)

# Визуализация на карте
m = folium.Map(location=[43.05, 76.98], zoom_start=10)

folium.GeoJson(ulken_almaty.geometry).add_to(m)
folium.GeoJson(shyzyn.geometry).add_to(m)

if connected:
    folium.Marker([43.05, 76.98], popup='Связь между реками Улькен Алматы и Шыжын').add_to(m)
else:
    folium.Marker([43.05, 76.98], popup='Реки не связаны через притоки').add_to(m)

m.save("95.html")