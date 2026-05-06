import folium
import pandas as pd

def solve_gis_task():
    # 1. Имитация данных о датчиках уровня воды для рек Tentek и Temirlik
    # В реальном сценарии здесь был бы запрос к API (например, requests.get(url))
    data = {
        'sensor_id': ['TENT-01', 'TENT-02', 'TEMI-01', 'TEMI-02', 'TEMI-03'],
        'river': ['Tentek River', 'Tentek River', 'Temirlik River', 'Temirlik River', 'Temirlik River'],
        'lat': [48.721, 48.550, 48.810, 48.620, 48.410],
        'lon': [68.120, 68.310, 68.550, 68.710, 68.820],
        'water_level': [1.2, 2.5, 0.8, 3.1, None], # None означает сбой датчика
        'status': ['Normal', 'Warning', 'Normal', 'Critical', 'Offline']
    }

    df = pd.DataFrame(data)

    # 2. Функция для определения цвета маркера в зависимости от статуса
    def get_color(status):
        if status == 'Normal':
            return 'green'
        elif status == 'Warning':
            return 'orange'
        elif status == 'Critical':
            return 'red'
        else:
            return 'gray' # Для Offline или ошибок

    # 3. Инициализация карты
    # Центрируем карту примерно между двумя реками в регионе Караганды
    m = folium.Map(location=[48.6, 68.4], zoom_start=8, tiles='OpenStreetMap')

    # 4. Добавление датчиков на карту
    for index, row in df.iterrows():
        # Формируем текст для всплывающего окна
        popup_text = (
            f"<b>Река:</b> {row['river']}<br>"
            f"<b>ID датчика:</b> {row['sensor_id']}<br>"
            f"<b>Уровень:</b> {row['water_level'] if row['water_level'] is not None else 'N/A'} м.<br>"
            f"<b>Состояние:</b> {row['status']}"
        )
        
        # Создаем маркер
        folium.Marker(
            location=[row['lat'], row['lon']],
            popup=folium.Popup(popup_text, max_width=300),
            icon=folium.Icon(color=get_color(row['status']), icon='info-sign')
        ).add_to(m)

    # 5. Сохранение карты
    m.save("72.html")
    print("Карта успешно создана и сохранена в файл 72.html")

if __name__ == "__main__":
    solve_gis_task()