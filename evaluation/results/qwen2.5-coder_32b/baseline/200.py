import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import zscore
import folium

# Шаг 1: Сбор данных
# Предположим, что у нас есть CSV-файл с историческими данными о уровне воды и дождевых осадках.
data = pd.read_csv('kishi_osek_water_level_precipitation.csv', parse_dates=['date'])

# Шаг 2: Обработка данных
# Удаление пропусков и аномалий
data.dropna(inplace=True)
z_scores = zscore(data['water_level'])
abs_z_scores = np.abs(z_scores)
filtered_entries = (abs_z_scores < 3)  # Оставляем только те записи, где значение z-score меньше 3
data = data[filtered_entries]

# Шаг 3: Определение экстремальных значений
# Используем метод Z-оценки для определения экстремальных значений
threshold = 2.5  # Пороговое значение Z-оценки для экстремальных событий
extremes = data[np.abs(z_scores) > threshold]

# Шаг 4: Сравнение текущих показателей с историческими данными
# Предположим, что у нас есть текущие данные о уровне воды и дождевых осадках.
current_data = pd.DataFrame({
    'date': [pd.Timestamp.now()],
    'water_level': [150],  # Пример значения уровня воды
    'precipitation': [20]   # Пример значения дождевых осадков
})

# Проверка текущих данных на экстремальность
current_z_score = zscore([current_data['water_level'].iloc[0]])[0]
if abs(current_z_score) > threshold:
    current_extreme = True
else:
    current_extreme = False

print("Текущие данные экстремальные:", current_extreme)

# Шаг 5: Визуализация результатов
# Создание карты с помощью folium
m = folium.Map(location=[41.3279, 69.2807], zoom_start=10)  # Координаты примерного местоположения реки Kishi Osek

# Добавление маркеров для экстремальных событий
for _, row in extremes.iterrows():
    folium.Marker(
        location=[41.3279, 69.2807],  # Координаты примерного местоположения реки Kishi Osek
        popup=f"Дата: {row['date']}, Уровень воды: {row['water_level']}",
        icon=folium.Icon(color='red')
    ).add_to(m)

# Добавление маркера для текущих данных, если они экстремальные
if current_extreme:
    folium.Marker(
        location=[41.3279, 69.2807],  # Координаты примерного местоположения реки Kishi Osek
        popup=f"Дата: {current_data['date'].iloc[0]}, Уровень воды: {current_data['water_level'].iloc[0]}",
        icon=folium.Icon(color='blue')
    ).add_to(m)

# Сохранение карты в файл
m.save("200.html")

# Визуализация данных на графике (опционально)
plt.figure(figsize=(14, 7))
plt.plot(data['date'], data['water_level'], label='Уровень воды')
plt.scatter(extremes['date'], extremes['water_level'], color='red', label='Экстремальные события')
if current_extreme:
    plt.scatter(current_data['date'], current_data['water_level'], color='blue', label='Текущие данные (экстремальные)')
else:
    plt.scatter(current_data['date'], current_data['water_level'], color='green', label='Текущие данные')

plt.xlabel('Дата')
plt.ylabel('Уровень воды')
plt.title('Уровень воды в реке Kishi Osek с экстремальными событиями')
plt.legend()
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()