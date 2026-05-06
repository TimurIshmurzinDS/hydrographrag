import pandas as pd
import folium
from folium.plugins import MarkerCluster

# Предположим, что у нас есть CSV-файл с данными о реке Шынжалы
# Структура файла: latitude, longitude, pH, temperature, dissolved_oxygen

# Шаг 1: Загрузка данных
data = pd.read_csv('shynzhaly_data.csv')

# Шаг 2: Подготовка данных (пример очистки)
data.dropna(inplace=True)  # Удаление строк с пропущенными значениями

# Шаг 3: Анализ данных (вычисление статистических показателей)
stats = data.describe()
print(stats)

# Шаг 4: Визуализация данных на карте
m = folium.Map(location=[data['latitude'].mean(), data['longitude'].mean()], zoom_start=10)

marker_cluster = MarkerCluster().add_to(m)

for _, row in data.iterrows():
    popup_text = f"pH: {row['pH']}, Температура: {row['temperature']}°C, Кислород растворенный: {row['dissolved_oxygen']} mg/L"
    folium.Marker(
        location=[row['latitude'], row['longitude']],
        popup=popup_text
    ).add_to(marker_cluster)

# Шаг 5: Сохранение карты в файл
m.save("44.html")