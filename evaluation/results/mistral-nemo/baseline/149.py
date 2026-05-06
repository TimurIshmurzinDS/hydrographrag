import pandas as pd
import folium

# Загружаем данные о положении датчиков и информации о сигнале
data = pd.read_csv('sensor_data.csv')

# Функция для проверки наличия периода отсутствия сигнала
def check_signal_loss(sensor_id, start_time, end_time):
    sensor_data = data[data['sensor_id'] == sensor_id]
    signal_loss = sensor_data[(sensor_data['time'] >= start_time) & (sensor_data['time'] <= end_time)]['signal'].isnull().sum()
    return signal_loss > 0

# Анализируем данные о сигнале от датчиков на реках Лепсы и Киши Осек
Lepsa_signal_loss = check_signal_loss('Lepsa', '2022-01-01', '2022-12-31')
Osek_signal_loss = check_signal_loss('Osek', '2022-01-01', '2022-12-31')

# Создаем карту с результатами
m = folium.Map(location=[54.6873, 23.8103], zoom_start=8)

if Lepsa_signal_loss:
    folium.Marker([54.6873, 23.8103], popup='Отсутствие сигнала на реке Лепсы').add_to(m)
else:
    folium.Marker([54.6873, 23.8103], popup='Наличие сигнала на реке Лепсы').add_to(m)

if Osek_signal_loss:
    folium.Marker([54.6873, 23.8103], popup='Отсутствие сигнала на реке Киши Осек').add_to(m)
else:
    folium.Marker([54.6873, 23.8103], popup='Наличие сигнала на реке Киши Осек').add_to(m)

# Сохраняем карту в файл
m.save("149.html")