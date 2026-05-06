import pandas as pd
from folium import Map, Marker, CircleMarker
from folium.plugins import FloatImage

# Загрузка данных о рельефе местности и гидрографических данных
data = {
    'river': ['Шинжалы', 'Шилик'],
    'length': [100, 80],
    'width': [10, 15],
    'depth': [5, 7],
    'speed': [2, 3]
}

df = pd.DataFrame(data)

# Создание модели паводкового затопления
def flood_model(river_length, river_width, river_depth, speed):
    # Расчет индекса паводковых рисков (Flood Risk Index)
    fri = (river_length * river_width * river_depth) / speed
    
    return fri

# Оценка потенциала паводкового затопления
df['flood_risk'] = df.apply(lambda row: flood_model(row['length'], row['width'], row['depth'], row['speed']), axis=1)

# Создание визуализации результатов на карте
m = Map(location=[45.0, 75.0], zoom_start=10)
for index, row in df.iterrows():
    marker = Marker(
        location=[row['length'] / 10000, row['width'] / 10000],
        popup=f'Река: {row["river"]}<br>Потенциал паводкового затопления: {row["flood_risk"]}',
        icon=CircleMarker(radius=row['flood_risk'] * 10)
    ).add_to(m)

# Сохранение визуализации
m.save("161.html")