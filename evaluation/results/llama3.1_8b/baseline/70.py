import geopandas as gpd
from folium import Map, Marker
import pandas as pd

# Загрузим данные о гидрологических постах и их критических уровнях.
data = {
    'name': ['Пост 1', 'Пост 2', 'Пост 3'],
    'critical_level': [10, 20, 30],
    'geometry': [
        gpd.points_from_xy([75.0, 46.5], [45.0, 55.0]),
        gpd.points_from_xy([76.0, 47.0], [50.0, 60.0]),
        gpd.points_from_xy([77.0, 48.0], [55.0, 65.0])
    ]
}
df = pd.DataFrame(data)

# Привяжем данные к географической карте.
gdf = gpd.GeoDataFrame(df, geometry='geometry')

# Создадим слой на карте для отображения критических уровней.
m = Map(location=[47.5, 76.0], zoom_start=10)
critical_layer = folium.FeatureGroup(name='Критические уровни')
for index, row in gdf.iterrows():
    if row['critical_level'] > 20:
        marker = Marker(row.geometry.coords[0], popup=row.name + ': ' + str(row.critical_level))
        critical_layer.add_child(marker)

# Определим гидрологические посты с критическими уровнями и добавим их в слой.
critical_posts = gdf[gdf['critical_level'] > 20]
for index, row in critical_posts.iterrows():
    marker = Marker(row.geometry.coords[0], popup=row.name + ': ' + str(row.critical_level))
    critical_layer.add_child(marker)

# Добавим слой на карту.
m.add_child(critical_layer)
m.save("70.html")