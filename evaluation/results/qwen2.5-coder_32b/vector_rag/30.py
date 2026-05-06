import geopandas as gpd
import folium
from shapely import wkt

# Загрузка данных о бассейне реки Прокходная из shapefile
basin_data = gpd.read_file(r"data/basin_data.shp")
basin_data = basin_data.to_crs('EPSG:4326')

# Инициализация карты с центром в бассейне реки Прокходная
centroid = basin_data.geometry.centroid.iloc[0]
m = folium.Map(location=[centroid.y, centroid.x], tiles='CartoDB positron', zoom_start=10)

# Добавление бассейна на карту
folium.GeoJson(basin_data.to_json(), name="Basin", style_function=lambda x: {'fillColor': 'green', 'color': 'darkgreen', 'fillOpacity': 0.2}).add_to(m)

# Предположим, что у нас есть координаты точки наблюдения в формате WKT
observation_point_wkt = "POINT(37.618423 55.755814)"  # Примерные координаты для иллюстрации
observation_point = gpd.GeoSeries([wkt.loads(observation_point_wkt)], crs='EPSG:4326')

# Добавление точки наблюдения на карту
folium.Marker(location=[observation_point.y.iloc[0], observation_point.x.iloc[0]], popup="Точка наблюдения").add_to(m)

# Предположим, что текущий расход воды в реке Прокходная составляет 12 м³/с
current_discharge = 12  # м³/с

# Критическое значение расхода воды для начала риска наводнения
critical_discharge = 10  # м³/с

# Расчет индекса риска наводнения
if current_discharge > critical_discharge:
    flood_risk_index = "Высокий"
else:
    flood_risk_index = "Низкий"

# Добавление информации о текущем расходе воды и индексе риска на карту
folium.Marker(location=[observation_point.y.iloc[0], observation_point.x.iloc[0]], popup=f"Текущий расход: {current_discharge} м³/с\nИндекс риска наводнения: {flood_risk_index}").add_to(m)

# Сохранение карты в файл
m.save("30.html")