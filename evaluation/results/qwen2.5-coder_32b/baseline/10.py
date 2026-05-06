import pandas as pd
import folium

# Шаг 1: Сбор данных (пример данных)
# Предположим, что данные о датчиках представлены в виде DataFrame
data = {
    'sensor_id': [1, 2, 3],
    'latitude': [42.8657, 42.8690, 42.8723],
    'longitude': [74.5967, 74.6000, 74.6033],
    'status': ['активен', 'неактивен', 'активен']
}

# Создание DataFrame
sensors_df = pd.DataFrame(data)

# Шаг 2: Подготовка данных (уже выполнено в предыдущем шаге)

# Шаг 3: Визуализация на карте с использованием folium

# Создание карты, центрированной по средним координатам датчиков
map_center = [sensors_df['latitude'].mean(), sensors_df['longitude'].mean()]
m = folium.Map(location=map_center, zoom_start=13)

# Добавление маркеров на карту для каждого датчика
for index, row in sensors_df.iterrows():
    if row['status'] == 'активен':
        icon_color = 'green'
    else:
        icon_color = 'red'
    
    folium.Marker(
        location=[row['latitude'], row['longitude']],
        popup=f"Датчик {row['sensor_id']} - Статус: {row['status']}",
        icon=folium.Icon(color=icon_color)
    ).add_to(m)

# Шаг 4: Сохранение карты в HTML-файл
m.save("10.html")