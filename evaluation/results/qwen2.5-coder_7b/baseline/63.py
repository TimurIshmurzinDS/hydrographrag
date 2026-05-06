import geopandas as gpd
import folium

# Загрузка данных о гидропостах (пример: из GeoJSON файла)
hydro_stations = gpd.read_file('path_to_hydro_stations.geojson')

# Пример данных о текущих уровнях воды для гидропостов
water_levels_data = {
    'station_id': [1, 2, 3],
    'current_level': [5.0, 6.5, 7.2]
}

# Преобразование данных в DataFrame
water_levels_df = pd.DataFrame(water_levels_data)

# Объединение данных о гидропостах с данными о текущих уровнях воды
merged_data = hydro_stations.merge(water_levels_df, on='station_id')

# Создание карты
m = folium.Map(location=[merged_data.geometry.centroid.y.mean(), merged_data.geometry.centroid.x.mean()], zoom_start=10)

# Добавление маркеров с текущими уровнями воды
for idx, row in merged_data.iterrows():
    folium.Marker(
        location=[row.geometry.y, row.geometry.x],
        popup=f"Гидропост {row.station_id}: Уровень воды - {row.current_level} м",
        icon=folium.Icon(color='blue', icon='info-sign')
    ).add_to(m)

# Сохранение карты
m.save("63.html")