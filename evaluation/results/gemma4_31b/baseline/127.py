import pandas as pd
import numpy as np
import folium

def solve_sharyn_flood_analysis():
    # 1. Симуляция исторических данных об уровне воды в реке Шарын
    # В реальном сценарии здесь был бы импорт из CSV или API гидропоста
    np.random.seed(42)
    dates = pd.date_range(start="2010-01-01", end="2023-12-31", freq='M')
    
    # Генерируем уровни воды с учетом сезонности (паводки весной)
    # Базовый уровень + сезонная синусоида + случайный шум + редкие экстремальные пики
    base_level = 2.5
    seasonal_variation = 1.5 * np.sin(np.arange(len(dates)) * (2 * np.pi / 12))
    noise = np.random.normal(0, 0.5, len(dates))
    
    # Добавляем несколько экстремальных паводковых значений
    extreme_events = np.zeros(len(dates))
    extreme_indices = [15, 82, 140] # Случайные индексы для пиков
    for idx in extreme_indices:
        extreme_events[idx] = np.random.uniform(3.0, 5.0)
        
    water_levels = base_level + seasonal_variation + noise + extreme_events
    
    df = pd.DataFrame({'date': dates, 'level': water_levels})

    # 2. Расчет статистических показателей
    max_level = df['level'].max()
    mean_level = df['level'].mean()
    difference = max_level - mean_level

    print(f"Максимальный уровень паводка: {max_level:.2f} м")
    print(f"Средний исторический уровень: {mean_level:.2f} м")
    print(f"Разница: {difference:.2f} м")

    # 3. Геопространственная визуализация
    # Координаты реки Шарын (примерная точка в Казахстане)
    sharyn_coords = [43.25, 79.15] 
    
    # Создание карты
    m = folium.Map(location=sharyn_coords, zoom_start=8, tiles='OpenStreetMap')

    # Создание текста для всплывающего окна
    popup_text = (
        f"<b>Река Шарын (Мониторинговый пост)</b><br>"
        f"Макс. уровень: {max_level:.2f} м<br>"
        f"Средний уровень: {mean_level:.2f} м<br>"
        f"<b>Разница: {difference:.2f} м</b>"
    )

    # Добавление маркера на карту
    folium.Marker(
        location=sharyn_coords,
        popup=folium.Popup(popup_text, max_width=300),
        tooltip="Точка замера уровня воды",
        icon=folium.Icon(color='blue', icon='info-sign')
    ).add_to(m)

    # Сохранение карты
    m.save("127.html")
    print("Карта успешно сохранена в файл 127.html")

if __name__ == "__main__":
    solve_sharyn_flood_analysis()