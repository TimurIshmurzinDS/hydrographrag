import pandas as pd
from folium import Map, Marker, CircleMarker
import geopandas as gpd
from shapely.geometry import Point

# Подготовка данных
data = {
    'geometry': [Point(55.7558, 37.6173), Point(55.7559, 37.6174)],
    'тип_почвы': ['чернозем', 'луг'],
    'растительность': ['деревья', 'травы'],
    'уровень_воды': [1.2, 0.8],
    'скорость_течения': [0.5, 1.0]
}
df = pd.DataFrame(data)

# Создание модели
def оценка_устойчивости(row):
    тип_почвы = row['тип_почвы']
    растительность = row['растительность']
    уровень_воды = row['уровень_воды']
    скорость_течения = row['скорость_течения']

    if тип_почвы == 'чернозем' and растительность == 'деревья':
        устойчивость = 0.8 * уровень_воды + 0.2 * скорость_течения
    elif тип_почвы == 'луг' and растительность == 'травы':
        устойчивость = 0.9 * уровень_воды - 0.1 * скорость_течения
    else:
        устойчивость = 0.5

    return устойчивость

df['устойчивость'] = df.apply(оценка_устойчивости, axis=1)

# Визуализация результатов
m = Map(location=[55.7558, 37.6173], zoom_start=12)
for index, row in df.iterrows():
    Marker(
        location=[row['geometry'].y, row['geometry'].x],
        popup=f'Устойчивость: {row["устойчивость"]:.2f}',
        icon=CircleMarker(radius=row['устойчивость'] * 10).add_to(m)
    ).add_to(m)

m.save("184.html")