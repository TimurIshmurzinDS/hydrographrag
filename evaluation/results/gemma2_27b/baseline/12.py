import pandas as pd
import folium
from folium.plugins import TimeSliderChoropleth

# Загрузка данных с сенсора (замените на фактический путь к файлу)
data = pd.read_csv("sensor_data.csv")

# Преобразование даты в формат datetime
data['timestamp'] = pd.to_datetime(data['timestamp'])

# Создание карты
m = folium.Map(location=[55.75, 37.62], zoom_start=12)  # Замените на координаты сенсора

# Визуализация данных на карте с помощью TimeSliderChoropleth
time_slider = TimeSliderChoropleth(
    data,
    date_column='timestamp',
    value_column='water_level',  # Замените на название столбца с уровнем воды
    location_column=['latitude', 'longitude'],  # Замените на названия столбцов с координатами
)

time_slider.add_to(m)

# Сохранение карты
m.save("12.html")