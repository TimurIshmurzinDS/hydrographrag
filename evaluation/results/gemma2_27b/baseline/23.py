import geopandas as gpd
from shapely.geometry import Polygon
import folium

# Загрузка данных ЦМР (предполагается, что файл в формате shapefile)
dmr = gpd.read_file("path/to/dmr.shp")

# Загрузка данных о гидрологических параметрах (например, из CSV файла)
hydrology_data = pd.read_csv("path/to/hydrology_data.csv")

# Гидрологическое моделирование (используя HEC-RAS или аналогичную модель)
# ... (код моделирования не представлен, так как зависит от конкретной модели)

# Определение зон затопления на основе результатов гидрологического моделирования
flood_zones = gpd.GeoDataFrame(geometry=[Polygon([(x1, y1), (x2, y2), ..., (xn, yn)])]) # Заменить на реальные координаты

# Визуализация результатов на карте Folium
m = folium.Map(location=[latitude, longitude], zoom_start=12)

# Добавление слоев ЦМР и зон затопления на карту
folium.GeoJson(dmr).add_to(m)
folium.GeoJson(flood_zones, style_function=lambda feature: {
    'fillColor': 'blue' if feature['properties']['risk'] == 'low' else 'yellow' if feature['properties']['risk'] == 'medium' else 'red',
    'fillOpacity': 0.5
}).add_to(m)

# Сохранение карты в HTML файл
m.save("23.html")