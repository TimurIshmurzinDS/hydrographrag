import pandas as pd
from folium import Map, Marker, CircleMarker
import geopandas as gpd

# Шаг 1: Подготовка данных
# Для примера мы будем использовать геометрию реки Батареке в виде GeoJSON-файла.
river_geometry = {
    "type": "Feature",
    "geometry": {
        "type": "LineString",
        "coordinates": [
            [37.623, 53.913],
            [37.625, 53.915],
            [37.627, 53.917]
        ]
    },
    "properties": {}
}

# Шаг 2: Создание модели мониторинга
# Для примера мы будем использовать простую модель, которая учитывает только уровень воды.
water_level_data = pd.DataFrame({
    'location': ['Батареке'],
    'level': [10.5]
})

# Шаг 3: Визуализация результатов на карте
m = Map(location=[53.915, 37.625], zoom_start=12)

for index, row in water_level_data.iterrows():
    if row['level'] > 10:
        marker = Marker(
            location=[row['location'].latitude, row['location'].longitude],
            popup=f"Уровень воды: {row['level']} м",
            icon=CircleMarker(color='red', radius=5)
        ).add_to(m)

gdf = gpd.GeoDataFrame.from_features([river_geometry])
m.add_child(gdf)

# Сохранение карты в HTML-файл
m.save("14.html")