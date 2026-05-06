import geopandas as gpd
import folium
from shapely import wkt

# Загрузка данных о реке Бызж, объеме потребления воды и урожае местных культур
data = {
    'Бызж': {'Объем потребления воды (м³)': 1000000},
    'Ургар': {'Объем потребления воды (м³)': 500000},
    'Шыжын': {'Объем потребления воды (м³)': 750000}
}

# Создание GeoDataFrame для рек
basin_data = gpd.read_file(r"data/basin_data.shp")
basin_data = basin_data.to_crs('EPSG:4326')

# Инициализация карты с центром на centroid базина и тайлами CartoDB positron
centroid = basin_data.geometry.centroid[0]
m = folium.Map(location=[centroid.y, centroid.x], zoom_start=10, tiles='CartoDB positron')

# Добавление базина на карту
folium.GeoJson(basin_data.to_json(), style_function=lambda x: {
    'fillColor': 'green',
    'color': 'darkgreen',
    'fillOpacity': 0.2
}).add_to(m)

# Визуализация данных о потреблении воды и урожае на карте
for name, values in data.items():
    folium.Marker(
        location=[centroid.y, centroid.x],
        popup=f"Река: {name}<br>Объем потребления воды: {values['Объем потребления воды (м³)']} м³",
        icon=folium.Icon(color='blue', icon='info-sign')
    ).add_to(m)

# Сохранение карты
m.save("185.html")