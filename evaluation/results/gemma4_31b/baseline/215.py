import folium
import numpy as np
import pandas as pd
import hashlib
import random
from datetime import datetime

def simulate_water_levels(points_count, time_steps=24):
    """Симуляция колебаний уровня воды в разных точках реки"""
    data = []
    for i in range(points_count):
        base_level = random.uniform(2.0, 5.0)
        for t in range(time_steps):
            # Добавляем случайное колебание (шум)
            fluctuation = np.sin(t * 0.5) + random.uniform(-0.5, 0.5)
            level = base_level + fluctuation
            data.append({'point_id': i, 'timestamp': t, 'level': level})
    return pd.DataFrame(data)

def mock_mine(point_id, water_level, difficulty_prefix="00"):
    """
    Имитация майнинга: поиск хеша, начинающегося с определенного префикса.
    Сложность (префикс) зависит от волатильности (в данной упрощенной модели фиксирована).
    """
    nonce = 0
    while True:
        input_str = f"{point_id}-{water_level}-{nonce}"
        hash_result = hashlib.sha256(input_str.encode()).hexdigest()
        if hash_result.startswith(difficulty_prefix):
            return nonce, hash_result
        nonce += 1
        if nonce > 10000: # Ограничение для предотвращения бесконечного цикла в симуляции
            return None, None

def run_mining_simulation():
    # Координаты реки Баянкол (приблизительная аппроксимация для демонстрации)
    # В реальном проекте здесь будет GeoJSON или Shapefile
    bayankol_coords = [
        [44.123, 68.456], [44.150, 68.500], [44.180, 68.550], 
        [44.210, 68.600], [44.250, 68.680], [44.300, 68.750]
    ]
    
    num_points = len(bayankol_coords)
    water_data = simulate_water_levels(num_points)
    
    results = []
    
    for pid in range(num_points):
        point_levels = water_data[water_data['point_id'] == pid]['level'].values
        # Вычисляем волатильность (стандартное отклонение)
        volatility = np.std(point_levels)
        
        # Определяем сложность на основе волатильности: 
        # чем выше волатильность, тем легче "майнить" (меньше нулей в префиксе)
        difficulty = "0" if volatility > 0.8 else "00"
        
        coins_mined = 0
        for level in point_levels:
            nonce, h = mock_mine(pid, level, difficulty)
            if nonce is not None:
                coins_mined += 1
        
        results.append({
            'coord': bayankol_coords[pid],
            'coins': coins_mined,
            'volatility': volatility
        })
    
    return results

def create_gis_map(results):
    # Создаем карту, центрированную на среднем значении координат
    m = folium.Map(location=[44.2, 68.6], zoom_start=9, tiles='CartoDB dark_matter')
    
    # Рисуем линию реки
    coords_list = [r['coord'] for r in results]
    folium.PolyLine(coords_list, color="blue", weight=3, opacity=0.7, tooltip="Bayankol River").add_to(m)
    
    # Добавляем маркеры с результатами майнинга
    for res in results:
        # Цвет маркера зависит от количества добытых монет
        color = 'green' if res['coins'] > 15 else 'yellow' if res['coins'] > 5 else 'red'
        
        folium.CircleMarker(
            location=res['coord'],
            radius=res['coins'] * 0.5 + 5, # Размер зависит от прибыли
            color=color,
            fill=True,
            fill_color=color,
            popup=f"Coins Mined: {res['coins']}<br>Volatility: {res['volatility']:.2f}"
        ).add_to(m)
    
    m.save("215.html")
    print("Map has been saved as 215.html")

if __name__ == "__main__":
    print("Starting Hydro-Mining Simulation...")
    mining_results = run_mining_simulation()
    create_gis_map(mining_results)
    print("Simulation complete.")