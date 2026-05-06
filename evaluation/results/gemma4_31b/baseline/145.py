import pandas as pd
import folium
import random

# =============================================================================
# 1. Симуляция базы данных (Mock Data)
# =============================================================================
def get_sensor_data():
    """
    Имитация получения данных из БД. 
    В реальном сценарии здесь будет запрос к PostgreSQL/PostGIS или API.
    """
    rivers = {
        "Волга": [50.0, 45.0],
        "Лена": [65.0, 120.0],
        "Енисей": [60.0, 90.0],
        "Обь": [55.0, 80.0],
        "Амур": [52.0, 130.0]
    }
    
    data = []
    sensor_id = 1
    for river, coords in rivers.items():
        # Создаем по 3-5 датчиков для каждой реки
        for i in range(random.randint(3, 6)):
            status = random.choices(["Active", "Inactive"], weights=[0.9, 0.1])[0]
            current_val = round(random.uniform(1.0, 10.0), 2)
            threshold = 7.0
            
            data.append({
                "sensor_id": sensor_id,
                "river_name": river,
                "lat": coords[0] + random.uniform(-2, 2),
                "lon": coords[1] + random.uniform(-5, 5),
                "value": current_val,
                "threshold": threshold,
                "status": status
            })
            sensor_id += 1
            
    return pd.DataFrame(data)

# =============================================================================
# 2. Логика анализа состояния
# =============================================================================
def analyze_status(row):
    if row['status'] == 'Inactive':
        return 'Error', 'red'
    if row['value'] > row['threshold']:
        return 'Critical', 'red'
    if row['value'] > row['threshold'] * 0.8:
        return 'Warning', 'orange'
    return 'Normal', 'green'

# =============================================================================
# 3. Основной процесс моделирования
# =============================================================================
def main():
    # Загрузка данных
    df = get_sensor_data()
    
    # Применяем анализ состояния
    df[['state', 'color']] = df.apply(
        lambda row: pd.Series(analyze_status(row)), axis=1
    )
    
    # --- Вывод общей статистики ---
    total_sensors = len(df)
    active_sensors = len(df[df['status'] == 'Active'])
    critical_sensors = len(df[df['state'] == 'Critical'])
    
    print("--- Общий обзор состояния датчиков ---")
    print(f"Всего датчиков в базе: {total_sensors}")
    print(f"Активных датчиков: {active_sensors}")
    print(f"Датчиков в критическом состоянии: {critical_sensors}")
    print(f"Доля работоспособности: {(active_sensors/total_sensors)*100:.2f}%")
    print("--------------------------------------")

    # --- Визуализация на карте ---
    # Центрируем карту по средним координатам всех датчиков
    m = folium.Map(location=[df['lat'].mean(), df['lon'].mean()], zoom_start=3)
    
    for _, row in df.iterrows():
        popup_text = (
            f"<b>Река:</b> {row['river_name']}<br>"
            f"<b>ID:</b> {row['sensor_id']}<br>"
            f"<b>Значение:</b> {row['value']} (Порог: {row['threshold']})<br>"
            f"<b>Статус:</b> {row['status']}<br>"
            f"<b>Состояние:</b> {row['state']}"
        )
        
        folium.CircleMarker(
            location=[row['lat'], row['lon']],
            radius=7,
            popup=popup_text,
            color=row['color'],
            fill=True,
            fill_color=row['color'],
            fill_opacity=0.7
        ).add_to(m)
    
    # Сохранение карты строго в файл 145.html
    m.save("145.html")
    print("Карта успешно сохранена в файл 145.html")

if __name__ == "__main__":
    main()