import pandas as pd
import numpy as np
import folium
from folium.plugins import MarkerCluster

# 1. Симуляция данных (так как реальные данные датчиков Сарыкана закрыты)
# Координаты района реки Сарыкан (примерные)
SARYKAN_CENTER = [44.5, 68.0] 

def generate_mock_data():
    # Создаем список датчиков в районе реки Сарыкан
    np.random.seed(42)
    sensors_data = {
        'sensor_id': [f'SN_{i}' for i in range(1, 16)],
        'river_name': ['Sarykan', 'Sarykan', 'Sarykan', 'Tributary_A', 'Tributary_A', 
                       'Sarykan', 'Sarykan', 'Tributary_B', 'Tributary_B', 'Sarykan',
                       'Sarykan', 'Tributary_C', 'Tributary_C', 'Sarykan', 'Sarykan'],
        'lat': np.random.uniform(44.3, 44.7, 15),
        'lon': np.random.uniform(67.8, 68.2, 15),
        'current_level': np.random.uniform(1.0, 5.0, 15),
        'hist_mean': [2.5] * 15,
        'hist_std': [0.5] * 15
    }
    
    df = pd.DataFrame(sensors_data)
    
    # Искусственно создаем аномалии для демонстрации
    # Датчик 3 и 12 имеют критический подъем уровня воды
    df.loc[2, 'current_level'] = 8.2 
    df.loc[11, 'current_level'] = 7.9
    
    return df

# 2. Функция обнаружения аномалий (Z-score)
def detect_anomalies(df, threshold=2.0):
    """
    Вычисляет Z-score и помечает аномальные показатели.
    """
    df['z_score'] = (df['current_level'] - df['hist_mean']) / df['hist_std']
    df['is_anomaly'] = df['z_score'].abs() > threshold
    return df

# 3. Основной процесс моделирования
def main():
    # Загрузка данных
    df_sensors = generate_mock_data()
    
    # Анализ аномалий
    df_analyzed = detect_anomalies(df_sensors)
    
    # Выявление рек с аномалиями
    anomalous_rivers = df_analyzed[df_analyzed['is_anomaly']]['river_name'].unique()
    print(f"Обнаружены аномалии на следующих реках: {', '.join(anomalous_rivers)}")

    # 4. Визуализация на карте
    m = folium.Map(location=SARYKAN_CENTER, zoom_start=9, tiles='CartoDB positron')
    
    # Добавляем кластеры для датчиков
    marker_cluster = MarkerCluster().add_to(m)
    
    for idx, row in df_analyzed.iterrows():
        color = 'red' if row['is_anomaly'] else 'green'
        status = 'ANOMALY' if row['is_anomaly'] else 'NORMAL'
        
        popup_text = (
            f"Sensor: {row['sensor_id']}<br>"
            f"River: {row['river_name']}<br>"
            f"Level: {row['current_level']:.2f}m<br>"
            f"Status: {status}"
        )
        
        folium.CircleMarker(
            location=[row['lat'], row['lon']],
            radius=7,
            popup=popup_text,
            color=color,
            fill=True,
            fill_color=color,
            fill_opacity=0.7
        ).add_to(marker_cluster)

    # Сохранение карты
    m.save("139.html")
    print("Карта успешно сохранена в файл 139.html")

if __name__ == "__main__":
    main()