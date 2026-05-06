import pandas as pd
import numpy as np
import folium
from datetime import datetime

# 1. Симуляция данных гидрологического поста на реке Osek River
# В реальном сценарии здесь был бы запрос к API или загрузка CSV файла
def generate_hydrological_data():
    np.random.seed(42)
    date_rng = pd.date_range(start='2023-01-01', end='2023-12-31', freq='D')
    
    # Создаем базовый уровень воды с сезонным колебанием (синусоида)
    # Пик приходится на апрель-май (весенний паводок)
    base_level = 2.0 
    seasonal_variation = 3.0 * np.sin(np.pi * (date_rng.dayofyear - 60) / 180)
    noise = np.random.normal(0, 0.2, len(date_rng))
    
    water_levels = base_level + seasonal_variation + noise
    return pd.DataFrame({'date': date_rng, 'level': water_levels})

# 2. Обработка данных для поиска максимального уровня весеннего паводка
def analyze_spring_flood(df):
    # Определяем границы весеннего периода (март, апрель, май)
    start_date = '2023-03-01'
    end_date = '2023-05-31'
    
    # Фильтрация данных
    spring_data = df[(df['date'] >= start_date) & (df['date'] <= end_date)]
    
    # Поиск максимального значения
    max_level = spring_data['level'].max()
    max_date = spring_data.loc[spring_data['level'].idxmax(), 'date']
    
    return max_level, max_date

# --- Основной процесс ---

# Генерация данных
df_water = generate_hydrological_data()

# Анализ
max_val, max_dt = analyze_spring_flood(df_water)
print(f"Максимальный уровень воды в период весеннего паводка: {max_val:.2f} м.")
print(f"Дата достижения пика: {max_dt.strftime('%Y-%m-%d')}")

# 3. Визуализация на карте
# Координаты реки Osek (примерные координаты для демонстрации)
osek_coords = [54.1234, 27.5678] 

# Создание карты
m = folium.Map(location=osek_coords, zoom_start=12, tiles='OpenStreetMap')

# Добавление маркера гидропоста
popup_text = f"Гидропост Osek River<br>Макс. уровень паводка: {max_val:.2f} м.<br>Дата: {max_dt.strftime('%Y-%m-%d')}"
folium.Marker(
    location=osek_coords,
    popup=popup_text,
    tooltip="Пик паводка",
    icon=folium.Icon(color='blue', icon='info-sign')
).add_to(m)

# Сохранение карты
m.save("19.html")
print("Карта успешно сохранена в файл 19.html")