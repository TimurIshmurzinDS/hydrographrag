import folium
import pandas as pd
import numpy as np
from datetime import datetime, timedelta

# 1. Подготовка синтетических данных для моделирования
# В реальном сценарии здесь будет загрузка CSV или запрос к API гидромета
def generate_flood_data():
    # Координаты примерного расположения реки Uzyn Kargaly (Центральный Казахстан)
    # Приблизительные точки для визуализации русла
    river_coords = [
        [49.12, 67.50], [49.15, 67.60], [49.20, 67.75], 
        [49.25, 67.90], [49.30, 68.10], [49.35, 68.30]
    ]
    
    # Создаем временной ряд для весеннего периода (Март - Май)
    dates = pd.date_range(start="2023-03-01", end="2023-05-31")
    
    # Моделируем кривую паводка: низкий старт -> резкий пик в апреле -> спад
    # Формула имитирует колоколообразную кривую паводка
    days = np.arange(len(dates))
    peak_day = 35  # Примерно середина апреля
    discharge_values = 2.0 + 15.0 * np.exp(-(days - peak_day)**2 / (2 * 10**2))
    
    df = pd.DataFrame({'Date': dates, 'Discharge': discharge_values})
    return river_coords, df

# 2. Основная функция моделирования и визуализации
def main():
    river_coords, flood_df = generate_flood_data()
    
    # Определяем ключевые значения для вывода
    max_q = flood_df['Discharge'].max()
    avg_q = flood_df['Discharge'].mean()
    peak_date = flood_df.loc[flood_df['Discharge'].idxmax(), 'Date'].strftime('%Y-%m-%d')

    print(f"Анализ весеннего паводка реки Uzyn Kargaly:")
    print(f"Пиковый расход воды: {max_q:.2f} м3/с (Дата: {peak_date})")
    print(f"Средний расход за период: {avg_q:.2f} м3/с")
    print("-" * 30)
    print("Значения расхода по датам (выборка):")
    print(flood_df.iloc[::10].to_string(index=False))

    # 3. Создание карты
    # Центрируем карту по средней точке реки
    center_lat = np.mean([c[0] for c in river_coords])
    center_lon = np.mean([c[1] for c in river_coords])
    m = folium.Map(location=[center_lat, center_lon], zoom_start=9, tiles='OpenStreetMap')

    # Отрисовка русла реки
    folium.PolyLine(
        locations=river_coords, 
        color='blue', 
        weight=5, 
        opacity=0.7, 
        tooltip="Русло реки Uzyn Kargaly"
    ).add_to(m)

    # Добавление точек замера (гидропостов)
    # Для примера поставим посты в начале, середине и конце русла
    stations = [
        {"name": "Верхний пост", "coord": river_coords[0], "q": f"{max_q*0.6:.2f} м3/с"},
        {"name": "Средний пост", "coord": river_coords[3], "q": f"{max_q*0.8:.2f} м3/с"},
        {"name": "Нижний пост", "coord": river_coords[-1], "q": f"{max_q:.2f} м3/с"},
    ]

    for station in stations:
        folium.CircleMarker(
            location=station["coord"],
            radius=8,
            color='red',
            fill=True,
            fill_color='red',
            popup=f"Станция: {station['name']}<br>Пиковый расход: {station['q']}",
            tooltip=station["name"]
        ).add_to(m)

    # Сохранение карты
    m.save("29.html")
    print("\nКарта с результатами моделирования сохранена в файл '29.html'")

if __name__ == "__main__":
    main()