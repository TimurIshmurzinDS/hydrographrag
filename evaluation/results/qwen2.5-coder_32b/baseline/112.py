import folium
import pandas as pd
from shapely.geometry import Point, LineString
from geopandas import GeoDataFrame

# Пример данных о реках (координаты точек для создания линий)
data = {
    'river': ['Kurty River', 'Urzhar River', 'Byzhy River'],
    'coordinates': [
        [[48.5, 63.5], [48.6, 63.7], [48.7, 63.9]],  # Координаты для Kurty River
        [[48.2, 63.1], [48.3, 63.3], [48.4, 63.5]],  # Координаты для Urzhar River
        [[48.0, 62.9], [48.1, 63.1], [48.2, 63.3]]   # Координаты для Byzhy River
    ],
    'consumption': [500, 700, 600]  # Уровни водопотребления в кубометрах в день
}

# Создание GeoDataFrame с реками
rivers = []
for index, row in pd.DataFrame(data).iterrows():
    line = LineString([Point(coord) for coord in row['coordinates']])
    rivers.append({'river': row['river'], 'geometry': line, 'consumption': row['consumption']})

gdf_rivers = GeoDataFrame(rivers)

# Создание карты
m = folium.Map(location=[48.5, 63.5], zoom_start=10)

# Добавление рек на карту с цветовой кодировкой по уровню водопотребления
for _, row in gdf_rivers.iterrows():
    folium.PolyLine(
        locations=row['geometry'].coords,
        color='blue' if row['consumption'] < 600 else 'orange' if row['consumption'] < 700 else 'red',
        weight=5,
        popup=f"Река: {row['river']}, Уровень водопотребления: {row['consumption']} куб.м/день"
    ).add_to(m)

# Сохранение карты
m.save("112.html")