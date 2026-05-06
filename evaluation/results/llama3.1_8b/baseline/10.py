import pandas as pd
import geopandas as gpd
from folium import Map, Marker, Icon
from folium.plugins import HeatMap

# Загрузите данные о местоположении датчиков и их статусах в DataFrame.
data = {
    'id': [1, 2, 3],
    'location': [(46.5, 77.0), (46.6, 77.1), (46.7, 77.2)],
    'status': ['good', 'bad', 'good']
}
df = pd.DataFrame(data)

# Создайте слой геометрии для отображения местоположений датчиков на карте.
gdf = gpd.GeoDataFrame(df, geometry=gpd.points_from_xy(df.location.map(lambda x: x[1]), df.location.map(lambda x: x[0])))

# Настройте карту и добавьте слой данных для отображения статуса датчиков.
m = Map(location=[46.6, 77.1], zoom_start=10)
for index, row in gdf.iterrows():
    if row['status'] == 'good':
        icon = Icon(color='green')
    else:
        icon = Icon(color='red')
    Marker(row.geometry, icon=icon).add_to(m)

# Сохраните карту в файл.
m.save("10.html")