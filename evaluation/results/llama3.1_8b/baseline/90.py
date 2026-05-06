import pandas as pd
from folium import Map, Marker
from folium.plugins import HeatMap

# Подготовка данных
data = {
    'Река': ['Караой', 'Баскан', 'Темирлик'],
    'Длина (км)': [120, 90, 80],
    'Ширина (м)': [10, 15, 12],
    'Скорость течения (м/с)': [1.5, 2.0, 1.8]
}

df = pd.DataFrame(data)

# Оценка риска затопления
def оценка_риска_затопления(длина, ширина, скорость):
    # Простая оценка риска затопления на основе длины, ширины и скорости течения
    риск = (длина * ширина * скорость) / 1000
    return риск

df['Риск затопления'] = df.apply(lambda row: оценка_риска_затопления(row['Длина (км)'], row['Ширина (м)'], row['Скорость течения (м/с)']), axis=1)

# Визуализация результатов
m = Map(location=[50.0, 70.0], zoom_start=6)
for index, row in df.iterrows():
    marker = Marker(
        location=[row['Длина (км)'] * 0.01, row['Ширина (м)'] * 0.1],
        popup=f'Река: {row["Река"]}<br>Риск затопления: {row["Риск затопления"]:.2f}',
        icon=folium.Icon(color='red')
    ).add_to(m)

m.save("90.html")