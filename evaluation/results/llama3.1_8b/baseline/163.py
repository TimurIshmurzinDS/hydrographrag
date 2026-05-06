import pandas as pd
from folium import Map, Marker, CircleMarker, Polygon, PolyLine
from folium.plugins import HeatMap

# Сбор и геообработка данных
data = {
    'river': ['Sarykan River', 'Shyzhyn River'],
    'length': [100, 120],
    'width': [5, 6],
    'speed': [1.2, 1.5]
}

df = pd.DataFrame(data)

# Создание модели рисков весеннего половодья
def calculate_risk(length, width, speed):
    return length * width * speed

risks = df.apply(lambda row: calculate_risk(row['length'], row['width'], row['speed']), axis=1)

# Анализ данных и прогнозирование рисков
df['risk'] = risks

# Визуализация результатов на карте
m = Map(location=[50.0, 70.0], zoom_start=6)
for index, row in df.iterrows():
    Marker([row['width'], row['length']], popup=f'Река: {row["river"]}, Риск: {row["risk"]}').add_to(m)

# Сохранение карты в файл
m.save("163.html")