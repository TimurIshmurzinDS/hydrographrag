import pandas as pd
import numpy as np
import folium

# Сбор данных
data = pd.read_csv('historical_data.csv')

# Подготовка данных
data = data.drop_duplicates()
data = data.fillna(method='ffill')

# Определение стратегий трейдинга
strategies = ['strategy1', 'strategy2', 'strategy3']
for strategy in strategies:
    # Пример определения стратегии с использованием скользящих средних
    data[strategy] = data['close'].rolling(window=50).mean() - data['close'].rolling(window=200).mean()

# Вычисление прибыли/убытка
for strategy in strategies:
    data[strategy + '_profit'] = np.where(data[strategy] > 0, data['close'].pct_change(), 0)

# Визуализация результатов
m = folium.Map(location=[40.7128, -74.0060], zoom_start=13)
for strategy in strategies:
    profit = data[strategy + '_profit'].mean()
    folium.CircleMarker(
        location=[data['latitude'], data['longitude']],
        radius=np.abs(profit),
        color='blue',
        fill=True,
        fill_opacity=0.5
    ).add_to(m)

# Сохранение карты
m.save("285.html")