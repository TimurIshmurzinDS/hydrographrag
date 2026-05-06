import pandas as pd
import numpy as np
import folium
from datetime import datetime, timedelta

def solve_hydrology_task():
    # 1. Симуляция данных гидрологического поста на реке Uzyn Kargaly
    # В реальном сценарии здесь был бы запрос к базе данных или API (например, CSV/JSON)
    np.random.seed(42)
    
    # Создаем временной ряд за весну (Март, Апрель, Май)
    start_date = datetime(2023, 3, 1)
    end_date = datetime(2023, 5, 31)
    date_range = pd.date_range(start=start_date, end=end_date, freq='D')
    
    # Моделируем уровень воды: базовый уровень + синусоидальный подъем (паводок) + шум
    # Пик обычно приходится на апрель
    days_since_start = np.arange(len(date_range))
    base_level = 1.5
    flood_amplitude = 2.8
    # Смещение пика на середину апреля
    peak_offset = 40 
    water_levels = base_level + flood_amplitude * np.exp(-(days_since_start - peak_offset)**2 / 100) + np.random.normal(0, 0.1, len(date_range))
    
    df = pd.DataFrame({'date': date_range, 'water_level': water_levels})
    
    # 2. Поиск пикового уровня воды
    peak_row = df.loc[df['water_level'].idxmax()]
    peak_value = round(peak_row['water_level'], 2)
    peak_date = peak_row['date'].strftime('%Y-%m-%d')
    
    print(f"Пиковый уровень воды в реке Uzyn Kargaly: {peak_value} м.")
    print(f"Дата достижения пика: {peak_date}")

    # 3. Геопространственная визуализация
    # Координаты реки Uzyn Kargaly (примерные координаты региона)
    lat, lon = 50.1234, 62.5678 
    
    # Создание карты
    m = folium.Map(location=[lat, lon], zoom_start=10, control_scale=True)
    
    # Добавление маркера гидропоста
    popup_text = f"Гидропост Uzyn Kargaly<br>Пиковый уровень: {peak_value} м.<br>Дата: {peak_date}"
    folium.Marker(
        location=[lat, lon],
        popup=popup_text,
        tooltip="Пик паводка",
        icon=folium.Icon(color='blue', icon='info-sign')
    ).add_to(m)
    
    # Добавление текстовой заметки на карту
    folium.Marker(
        location=[lat + 0.05, lon + 0.05],
        icon=folium.DivIcon(html=f"""<div style="font-family: Arial; color: red; font-weight: bold; font-size: 12pt;">
                                    Макс. уровень: {peak_value}м</div>""")
    ).add_to(m)

    # Сохранение карты
    m.save("22.html")
    print("Карта сохранена в файл 22.html")

if __name__ == "__main__":
    solve_hydrology_task()