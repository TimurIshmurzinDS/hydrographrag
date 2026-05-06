import folium
import pandas as pd
import random

# 1. Симуляция данных о гидропостах на реке Temirlik River
# В реальном сценарии здесь будет запрос к API гидрологической службы или загрузка CSV/GeoJSON
data = {
    'station_id': [101, 102, 103, 104, 105],
    'station_name': ['Upper Temirlik', 'Mid-North Post', 'Central Basin', 'Lower Valley', 'Estuary Post'],
    'lat': [43.25, 43.20, 43.15, 43.10, 43.05], # Примерные координаты
    'lon': [76.50, 76.55, 76.60, 76.65, 76.70], # Примерные координаты
    'discharge_m3s': [12.5, 22.1, 35.8, 28.4, 10.2] # Текущий расход воды в м3/с
}

df = pd.DataFrame(data)

# 2. Функция для определения уровня риска и цвета маркера
def get_risk_level(discharge):
    if discharge > 30:
        return 'High', 'red'
    elif discharge > 15:
        return 'Medium', 'orange'
    else:
        return 'Low', 'green'

# 3. Создание карты
# Центрируем карту по средним координатам реки
map_center = [df['lat'].mean(), df['lon'].mean()]
m = folium.Map(location=map_center, zoom_start=10, tiles='OpenStreetMap')

# 4. Добавление постов на карту
for index, row in df.iterrows():
    risk_text, color = get_risk_level(row['discharge_m3s'])
    
    # Формирование текста для всплывающего окна
    popup_info = (
        f"<b>Station:</b> {row['station_name']}<br>"
        f"<b>Discharge:</b> {row['discharge_m3s']} m³/s<br>"
        f"<b>Flood Probability:</b> {risk_text}"
    )
    
    folium.CircleMarker(
        location=[row['lat'], row['lon']],
        radius=8,
        popup=popup_info,
        color=color,
        fill=True,
        fill_color=color,
        fill_opacity=0.7
    ).add_to(m)

# 5. Сохранение результата
m.save("78.html")

print("Analysis complete. The map has been saved as 78.html")
print("\nSummary of Water Discharge Data:")
print(df[['station_name', 'discharge_m3s']])