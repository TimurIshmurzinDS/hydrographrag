import folium
import pandas as pd
import numpy as np

def solve_hydrology_task():
    # 1. Имитация данных (в реальном сценарии данные загружаются из API или БД)
    # Координаты реки Prokhodnaya (условные)
    river_coords = [
        [56.123, 60.456], 
        [56.130, 60.460], 
        [56.145, 60.475], 
        [56.160, 60.490], 
        [56.180, 60.510]
    ]
    station_coords = [56.145, 60.475] # Точка замера
    
    # Текущий расход воды (м3/с)
    current_discharge = 45.5 
    
    # Исторические данные весенних паводков за последние 10 лет (м3/с)
    historical_spring_data = {
        'year': list(range(2014, 2024)),
        'discharge': [32.1, 38.5, 41.0, 29.8, 35.2, 44.1, 37.8, 33.4, 36.7, 39.2]
    }
    df_hist = pd.DataFrame(historical_spring_data)
    
    # 2. Аналитические расчеты
    avg_hist_discharge = df_hist['discharge'].mean()
    diff_abs = current_discharge - avg_hist_discharge
    diff_pct = (diff_abs / avg_hist_discharge) * 100
    
    # Определение статуса и цвета
    if diff_pct > 15:
        status = "Высокий уровень (Паводок)"
        color = 'red'
    elif diff_pct < -15:
        status = "Низкий уровень"
        color = 'blue'
    else:
        status = "В пределах нормы"
        color = 'green'

    # 3. Визуализация на карте
    # Создаем карту, центрированную на станции
    m = folium.Map(location=station_coords, zoom_start=12, tiles='OpenStreetMap')
    
    # Рисуем русло реки
    folium.PolyLine(
        locations=river_coords, 
        color='blue', 
        weight=5, 
        opacity=0.7, 
        tooltip="Prokhodnaya River"
    ).add_to(m)
    
    # Создаем текст для всплывающего окна
    popup_text = (
        f"<b>Станция мониторинга: Prokhodnaya River</b><br>"
        f"Текущий расход: {current_discharge} м³/с<br>"
        f"Средний исторический (весна): {avg_hist_discharge:.2f} м³/с<br>"
        f"Отклонение: {diff_abs:.2f} м³/с ({diff_pct:.2f}%)<br>"
        f"<b>Статус: {status}</b>"
    )
    
    # Добавляем маркер станции
    folium.CircleMarker(
        location=station_coords,
        radius=8,
        color=color,
        fill=True,
        fill_color=color,
        fill_opacity=0.8,
        popup=folium.Popup(popup_text, max_width=300)
    ).add_to(m)
    
    # Сохранение карты
    m.save("87.html")
    print("Анализ завершен. Карта сохранена в файл 87.html")
    print(f"Результат: Текущий расход {current_discharge} м3/с, Средний {avg_hist_discharge:.2f} м3/с. Статус: {status}")

if __name__ == "__main__":
    solve_hydrology_task()