import folium
import numpy as np
import pandas as pd
from folium.plugins import HeatMap

def solve_gis_crypto_task():
    # 1. Координаты реки Бутак (примерный центр бассейна в Казахстане)
    # Примечание: Точные координаты могут варьироваться, берем репрезентативную точку
    center_lat, center_lon = 48.5, 72.0 
    
    # 2. Симуляция геопространственных данных (анализ пригодности земель)
    # Создаем сетку точек вокруг реки для анализа
    np.random.seed(42)
    num_points = 100
    lats = center_lat + np.random.uniform(-0.5, 0.5, num_points)
    lons = center_lon + np.random.uniform(-0.5, 0.5, num_points)
    
    # Симулируем "Индекс пригодности" (Suitability Index) от 0 до 1
    # Чем ближе к центру (реке), тем выше индекс
    suitability = []
    for lat, lon in zip(lats, lons):
        dist = np.sqrt((lat - center_lat)**2 + (lon - center_lon)**2)
        score = np.exp(-dist * 2) * np.random.uniform(0.7, 1.0)
        suitability.append(score)
    
    df = pd.DataFrame({'lat': lats, 'lon': lons, 'score': suitability})
    
    # 3. Определение лучшей криптовалюты на основе анализа
    avg_suitability = df['score'].mean()
    total_area_potential = avg_suitability * num_points # Условный показатель масштаба
    
    if total_area_potential > 50:
        # Высокий потенциал -> Крупные инвестиции -> BTC
        recommended_crypto = "Bitcoin (BTC)"
        reason = "Высокий масштаб проекта требует максимальной ликвидности и сохранения стоимости."
    elif total_area_potential > 30:
        # Средний потенциал -> Технологический подход -> ETH
        recommended_crypto = "Ethereum (ETH)"
        reason = "Оптимально для внедрения смарт-контрактов в управление агро-логистикой."
    else:
        # Низкий/локальный потенциал -> Стабильность -> USDT
        recommended_crypto = "Tether (USDT)"
        reason = "Минимизация рисков волатильности при малых объемах инвестиций."

    # 4. Визуализация на карте
    m = folium.Map(location=[center_lat, center_lon], zoom_start=8, tiles='OpenStreetMap')
    
    # Добавляем тепловую карту пригодности земель
    heat_data = [[row['lat'], row['lon'], row['score']] for index, row in df.iterrows()]
    HeatMap(heat_data, radius=15, blur=20, gradient={0.4: 'blue', 0.65: 'lime', 1: 'red'}).add_to(m)
    
    # Добавляем маркер с итоговым решением
    info_text = (
        f"<b>Анализ бассейна реки Бутак</b><br>"
        f"Средний индекс пригодности: {avg_suitability:.2f}<br>"
        f"Рекомендуемая криптовалюта: <span style='color:green;'>{recommended_crypto}</span><br>"
        f"Обоснование: {reason}"
    )
    
    folium.Marker(
        [center_lat, center_lon], 
        popup=folium.Popup(info_text, max_width=300),
        tooltip="Результат моделирования",
        icon=folium.Icon(color='green', icon='leaf')
    ).add_to(m)
    
    # Сохранение карты
    m.save("268.html")
    print(f"Modeling complete. Recommended Crypto: {recommended_crypto}. Map saved as 268.html")

if __name__ == "__main__":
    solve_gis_crypto_task()