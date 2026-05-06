import pandas as pd
from folium import Map, Marker
from folium.plugins import HeatMap

# Сбор данных о местоположении оборудования мониторинга и его статусе.
data = {
    'location': ['55.1234, 36.5678', '54.9012, 37.2345', '55.6789, 36.0123'],
    'status': [1, 0, 1]  # 1 - работающее оборудование, 0 - неработающее
}

df = pd.DataFrame(data)

# Создание географической карты с указанием местоположения оборудования мониторинга.
m = Map(location=[55.5, 36.5], zoom_start=10)
for index, row in df.iterrows():
    if row['status'] == 1:
        Marker([row['location'].split(',')[0], row['location'].split(',')[1]], popup='Работает').add_to(m)
    else:
        Marker([row['location'].split(',')[0], row['location'].split(',')[1]], popup='Не работает').add_to(m)

# Анализ данных для выявления сбоев в работе оборудования мониторинга.
sboi = df[df['status'] == 0]

if not sboi.empty:
    print('Найдены сбои в работе оборудования мониторинга:')
    for index, row in sboi.iterrows():
        print(f'Оборудование находится по адресу: {row["location"]}')
else:
    print('Сбоев в работе оборудования мониторинга не найдено.')

# Сохранение карты в файл.
m.save("142.html")