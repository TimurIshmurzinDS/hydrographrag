import pandas as pd
import folium

# 1. Имитация базы данных гидрологических постов
# В реальном сценарии здесь будет загрузка из GeoJSON, Shapefile или SQL БД
data = {
    'station_id': [101, 102, 103, 104, 105, 106],
    'river': ['Karaoy River', 'Karaoy River', 'Karaoy River', 'Other River', 'Karaoy River', 'Other River'],
    'lat': [43.123, 43.250, 43.380, 43.500, 43.510, 43.600],
    'lon': [77.100, 77.200, 77.300, 77.400, 77.450, 77.500],
    'current_discharge': [12.5, 45.2, 28.0, 10.0, 62.1, 5.0], # м3/с
    'critical_threshold': [15.0, 40.0, 30.0, 12.0, 50.0, 8.0]  # м3/с
}

df = pd.DataFrame(data)

# 2. Фильтрация постов на реке Karaoy River
karaoy_stations = df[df['river'] == 'Karaoy River'].copy()

# 3. Проверка превышения критической отметки паводка
def check_flood(row):
    if row['current_discharge'] > row['critical_threshold']:
        return 'CRITICAL'
    return 'NORMAL'

karaoy_stations['status'] = karaoy_stations.apply(check_flood, axis=1)

# 4. Визуализация на карте
# Центрируем карту по средним координатам реки Karaoy
center_lat = karaoy_stations['lat'].mean()
center_lon = karaoy_stations['lon'].mean()
m = folium.Map(location=[center_lat, center_lon], zoom_start=10)

for index, row in karaoy_stations.iterrows():
    # Определяем цвет маркера в зависимости от статуса
    color = 'red' if row['status'] == 'CRITICAL' else 'green'
    
    # Формируем текст для всплывающего окна
    popup_text = (
        f"Станция: {row['station_id']}<br>"
        f"Расход: {row['current_discharge']} м3/с<br>"
        f"Порог: {row['critical_threshold']} м3/с<br>"
        f"Статус: {'⚠️ ПРЕВЫШЕНИЕ' if row['status'] == 'CRITICAL' else '✅ Норма'}"
    )
    
    folium.Marker(
        location=[row['lat'], row['lon']],
        popup=folium.Popup(popup_text, max_width=300),
        icon=folium.Icon(color=color, icon='info-sign')
    ).add_to(m)

# Сохранение карты строго в файл 82.html
m.save("82.html")

print("Анализ завершен. Карта сохранена в файл 82.html")
print(karaoy_stations[['station_id', 'current_discharge', 'critical_threshold', 'status']])