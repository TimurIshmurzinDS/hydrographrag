import geopandas as gpd
import folium
from shapely import wkt

# Загрузка shapefile с данными о гидропостах
gdf = gpd.read_file(r"data/hydropower_stations.shp")
gdf.crs = 'EPSG:4326'

# Создание карты
centroid = gdf.geometry.centroid[0]
m = folium.Map(location=[centroid.y, centroid.x], zoom_start=10, tiles='CartoDB positron')

# Добавление границы бассейна на карту
basin_data = gpd.read_file(r"data/basin_data.shp")
basin_data.crs = 'EPSG:4326'
folium.GeoJson(basin_data.to_json(), style_function=lambda x: {'fillColor': 'green', 'color': 'darkgreen', 'fillOpacity': 0.2}).add_to(m)

# Фильтрация данных для гидропостов на реке Karaoy River
karaoy_stations = gdf[gdf['River'] == 'Karaoy']

# Оценка риска паводка (пример: если расход воды превышает 1000 м³/с, риск увеличивается)
for idx, row in karaoy_stations.iterrows():
    water_consumption = row['Water_consumption_Valuem³s']
    if water_consumption > 1000:
        folium.Marker([row.geometry.y, row.geometry.x], popup=f"Гидропост: {row['Name']}, Риск паводка: Высокий", icon=folium.Icon(color='red')).add_to(m)
    else:
        folium.Marker([row.geometry.y, row.geometry.x], popup=f"Гидропост: {row['Name']}, Риск паводка: Низкий", icon=folium.Icon(color='green')).add_to(m)

# Сохранение карты
m.save("76.html")