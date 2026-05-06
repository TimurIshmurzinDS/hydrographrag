import pandas as pd
from folium import Map, Marker
import numpy as np

# Загрузка данных о речных долинах
lepsy_data = pd.read_csv('lepsy.csv')
shilik_data = pd.read_csv('shilik.csv')

# Объединение данных
data = pd.concat([lepsy_data, shilik_data])

# Расчет индекса стока
def calculate_index_stoke(data):
    data['P'] = np.random.randint(100, 500) # Сумма осадков (пусть будет случайное число)
    data['R'] = np.random.randint(50, 200) # Сумма испарения (пусть будет случайное число)
    data['E'] = np.random.randint(20, 100) # Сумма эвапотранспирации (пусть будет случайное число)
    
    data['S'] = (data['P'] - data['R']) / data['E']
    return data

# Оценка сезонного стока
def evaluate_seasonal_flow(data):
    seasonal_flow = data.groupby('river')['S'].mean()
    return seasonal_flow

# Визуализация результатов на карте
m = Map(location=[50.0, 70.0], zoom_start=6)
for index, row in data.iterrows():
    marker = Marker(location=[row['lat'], row['lon']], popup=row['river'])
    m.add_child(marker)

# Сохранение карты в файл
m.save("152.html")

# Вывод результатов оценки сезонного стока
seasonal_flow = evaluate_seasonal_flow(data)
print(seasonal_flow)