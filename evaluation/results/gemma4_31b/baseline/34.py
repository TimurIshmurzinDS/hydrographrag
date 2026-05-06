import folium
import pandas as pd
import random

# 1. Подготовка данных
# Координаты реки Лепси (приблизительные точки вдоль русла в Алматинской области)
# В реальном проекте здесь будет загрузка из CSV или базы данных ГИС
data = {
    'station_id': [1, 2, 3, 4, 5, 6],
    'name': ['Верхнее течение', 'Участок А', 'Среднее течение', 'Участок Б', 'Нижнее течение', 'Устье'],
    'lat': [43.25, 43.18, 43.10, 43.02, 42.95, 42.88],
    'lon': [78.50, 78.65, 78.80, 78.95, 79.10, 79.25],
    'pH': [7.2, 7.5, 8.1, 8.4, 7.8, 7.6],
    'BOD5': [1.2, 2.5, 4.8, 6.1, 3.2, 2.8], # Биологическое потребление кислорода
    'Nitrates': [5.0, 12.0, 25.0, 40.0, 15.0, 10.0], # мг/л
    'Pollution_Level': ['Low', 'Low', 'Medium', 'High', 'Medium', 'Low']
}

df = pd.DataFrame(data)

# Функция для определения цвета маркера в зависимости от уровня загрязнения
def get_color(level):
    if level == 'Low':
        return 'green'
    elif level == 'Medium':
        return 'orange'
    elif level == 'High':
        return 'red'
    return 'blue'

# 2. Создание карты
# Центрируем карту на среднем течении реки Лепси
m = folium.Map(location=[43.05, 78.85], zoom_start=8, tiles='OpenStreetMap')

# Добавление линии, имитирующей русло реки
river_coords = df[['lat', 'lon']].values.tolist()
folium.PolyLine(river_coords, color="blue", weight=3, opacity=0.7, tooltip="Русло реки Лепси").add_to(m)

# 3. Добавление точек мониторинга на карту
for index, row in df.iterrows():
    # Создание HTML-контента для всплывающего окна
    popup_text = f"""
    <div style='font-family: Arial; width: 200px;'>
        <h4>Станция: {row['name']}</h4>
        <b>pH:</b> {row['pH']}<br>
        <b>БПК₅:</b> {row['BOD5']} мг/л<br>
        <b>Нитраты:</b> {row['Nitrates']} мг/л<br>
        <hr>
        <b>Статус:</b> <span style='color:{get_color(row['Pollution_Level'])}; font-weight:bold;'>
        {row['Pollution_Level']}</span>
    </div>
    """
    
    folium.CircleMarker(
        location=[row['lat'], row['lon']],
        radius=8,
        popup=folium.Popup(popup_text, max_width=250),
        color=get_color(row['Pollution_Level']),
        fill=True,
        fill_color=get_color(row['Pollution_Level']),
        fill_opacity=0.7
    ).add_to(m)

# 4. Сохранение результата
m.save("34.html")

print("Карта показателей загрязнения реки Лепси успешно создана и сохранена в файл 34.html")