import pandas as pd
import folium

# Шаг 1: Сбор данных
# Предположим, что у нас есть CSV файлы с данными о датчиках на реках Аягоз и Токыраун.
# Формат данных: id_датчика, долгота, широта, время_последнего_обслуживания, состояние (0 - нормально, 1 - требуется обслуживание)

data_ayagoz = pd.read_csv('sensors_ayagoz.csv')
data_tokyraun = pd.read_csv('sensors_tokyraun.csv')

# Объединим данные в один DataFrame для удобства анализа
data = pd.concat([data_ayagoz, data_tokyraun], ignore_index=True)

# Шаг 2: Анализ данных
# Определим датчики, требующие обслуживания (состояние == 1)
sensors_to_service = data[data['состояние'] == 1]

# Шаг 3: Визуализация результатов
# Создадим карту с помощью folium
m = folium.Map(location=[42.8746, 74.5903], zoom_start=10)  # Координаты примерного центра региона

# Добавим маркеры для датчиков, требующих обслуживания
for index, row in sensors_to_service.iterrows():
    folium.Marker(
        location=[row['широта'], row['долгота']],
        popup=f"Датчик {row['id_датчика']}: Требуется обслуживание",
        icon=folium.Icon(color='red')
    ).add_to(m)

# Сохранение карты в HTML файл
m.save("146.html")