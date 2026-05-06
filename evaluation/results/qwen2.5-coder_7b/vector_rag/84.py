import geopandas as gpd
import folium
from shapely import wkt

# Загрузка данных о гидропостах и их измерениях
hydro_stations = pd.read_csv('data/hydro_stations.csv')
measurements = pd.read_csv('data/measurements.csv')

# Фильтрация данных для периода весеннего половодья (например, марта-апреля)
start_date = '2023-03-01'
end_date = '2023-04-30'
filtered_measurements = measurements[(measurements['date'] >= start_date) & (measurements['date'] <= end_date)]

# Создание карты
basin_data = gpd.read_file(r"data/basin_data.shp")
basin_data.crs = 'EPSG:4326'

centroid = basin_data.geometry.centroid[0]
m = folium.Map(location=[centroid.y, centroid.x], zoom_start=10, tiles='CartoDB positron')

# Добавление границы бассейна
folium.GeoJson(basin_data.to_json(), style_function=lambda x: {
    'fillColor': 'green',
    'color': 'darkgreen',
    'fillOpacity': 0.2
}).add_to(m)

# Добавление маркеров гидропостов и их измерений
for index, row in hydro_stations.iterrows():
    station_id = row['station_id']
    station_name = row['station_name']
    station_coords = wkt.loads(row['geometry'])
    
    # Фильтрация измерений для текущего гидропоста
    station_measurements = filtered_measurements[filtered_measurements['station_id'] == station_id]
    
    if not station_measurements.empty:
        max_flow = station_measurements['flow'].max()
        folium.Marker(
            location=[station_coords.y, station_coords.x],
            popup=f"Гидропост: {station_name}<br>Максимальный расход воды: {max_flow} м³/с",
            icon=folium.Icon(color='red', icon='info-sign')
        ).add_to(m)

# Сохранение карты
m.save("84.html")