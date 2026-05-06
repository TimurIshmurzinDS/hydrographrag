import geopandas as gpd
import folium
from folium.plugins import MarkerCluster

# Загрузка данных о реках (пример данных)
data = {
    'name': ['Karaoy River', 'Baskan River', 'Temirlik River'],
    'geometry': [
        {'type': 'LineString', 'coordinates': [(39.12, 45.67), (38.90, 45.89)]},
        {'type': 'LineString', 'coordinates': [(40.12, 46.67), (40.90, 46.89)]},
        {'type': 'LineString', 'coordinates': [(41.12, 47.67), (41.90, 47.89)]}
    ]
}

# Создание GeoDataFrame
gdf = gpd.GeoDataFrame(data, geometry='geometry')

# Функция для проверки риска затопления (пример)
def check_flood_risk(river_name):
    # Здесь можно добавить логику для проверки текущего риска затопления
    # Например, запрос к API погоды или анализ данных о текущем состоянии воды
    return "Low"  # Пример возврата риска

# Добавление столбца с риском затопления
gdf['flood_risk'] = gdf['name'].apply(check_flood_risk)

# Создание карты
m = folium.Map(location=[40, 46], zoom_start=5)

# Визуализация рек и их риска затопления
marker_cluster = MarkerCluster().add_to(m)
for idx, row in gdf.iterrows():
    folium.Marker(
        location=row.geometry.centroid.coords[0],
        popup=f"{row['name']} - Risk: {row['flood_risk']}",
        icon=folium.Icon(color='blue', icon='water')
    ).add_to(marker_cluster)

# Сохранение карты
m.save("90.html")