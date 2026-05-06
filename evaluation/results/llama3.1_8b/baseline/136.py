import pandas as pd
from folium import Map, Marker, Icon

# Сбор данных о датчиках уровня воды и их статусе
data = {
    'id': [1, 2, 3],
    'name': ['Датчик 1', 'Датчик 2', 'Датчик 3'],
    'location': [(55.7558, 37.6173), (59.9386, 30.3357), (60.0500, 30.3500)],
    'status': ['нормальный', 'превышение', 'неисправен']
}

df = pd.DataFrame(data)

# Создание географической карты региона
m = Map(location=[55.7558, 37.6173], zoom_start=10)

# Обработка данных для определения статуса каждого датчика
for index, row in df.iterrows():
    if row['status'] == 'нормальный':
        icon_color = 'green'
    elif row['status'] == 'превышение':
        icon_color = 'red'
    else:
        icon_color = 'yellow'

    # Визуализация результатов на географической карте
    Marker(
        location=row['location'],
        icon=Icon(color=icon_color, prefix='fa'),
        popup=f'Датчик {row["name"]}: {row["status"]}'
    ).add_to(m)

# Сохранение карты в файл
m.save("136.html")