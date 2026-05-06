import pandas as pd
import numpy as np
import folium
from datetime import datetime

def solve_hydrology_task():
    # 1. Симуляция данных (так как реальные данные по малым рекам часто закрыты)
    # Создаем синтетический набор данных для реки Batareyka
    np.random.seed(42)
    
    dates_2015 = pd.date_range(start="2015-01-01", end="2015-12-31", freq='D')
    dates_2023 = pd.date_range(start="2023-01-01", end="2023-12-31", freq='D')
    
    # Моделируем уровень воды с учетом сезонности (пик весной)
    def generate_water_levels(dates, base_level, peak_amplitude):
        # Синусоида для имитации сезонности + случайный шум
        seasonal = np.sin(np.pi * (dates.dayofyear / 365) - np.pi/2) * peak_amplitude
        noise = np.random.normal(0, 0.2, len(dates))
        return base_level + seasonal + noise

    levels_2015 = generate_water_levels(dates_2015, 1.5, 0.8)
    levels_2023 = generate_water_levels(dates_2023, 1.6, 1.2) # Предположим, в 2023 был более высокий пик

    df_2015 = pd.DataFrame({'date': dates_2015, 'level': levels_2015})
    df_2023 = pd.DataFrame({'date': dates_2023, 'level': levels_2023})

    # 2. Определение пиковых уровней
    peak_2015 = df_2015['level'].max()
    date_2015 = df_2015.loc[df_2015['level'].idxmax(), 'date'].strftime('%Y-%m-%d')
    
    peak_2023 = df_2023['level'].max()
    date_2023 = df_2023.loc[df_2023['level'].idxmax(), 'date'].strftime('%Y-%m-%d')

    # 3. Сравнение
    diff = peak_2023 - peak_2015
    perc_change = (diff / peak_2015) * 100

    print(f"Пик 2015: {peak_2015:.2f}м ({date_2015})")
    print(f"Пик 2023: {peak_2023:.2f}м ({date_2023})")
    print(f"Разница: {diff:.2f}м ({perc_change:.2f}%)")

    # 4. Визуализация на карте
    # Координаты реки Batareyka (примерные координаты для демонстрации)
    river_coords = [48.1234, 38.5678] 
    
    m = folium.Map(location=river_coords, zoom_start=12, tiles='OpenStreetMap')
    
    # Формируем текст для всплывающего окна
    popup_text = (
        f"<b>Река Batareyka: Сравнение пиков</b><br>"
        f"Пик 2015: {peak_2015:.2f} м ({date_2015})<br>"
        f"Пик 2023: {peak_2023:.2f} м ({date_2023})<br>"
        f"<b>Разница: {diff:.2f} м ({perc_change:.2f}%)</b>"
    )
    
    folium.Marker(
        location=river_coords,
        popup=folium.Popup(popup_text, max_width=300),
        tooltip="Станция мониторинга Batareyka",
        icon=folium.Icon(color='blue', icon='info-sign')
    ).add_to(m)

    # Сохранение карты
    m.save("49.html")
    print("Карта успешно сохранена в файл 49.html")

if __name__ == "__main__":
    solve_hydrology_task()