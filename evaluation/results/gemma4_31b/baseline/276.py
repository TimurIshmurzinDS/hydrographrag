import numpy as np
import folium
from folium.plugins import HeatMap

def simulate_rabbit_population():
    # --- Параметры симуляции ---
    grid_size = 15  # Размер сетки 15x15
    time_steps = 50 # Количество итераций (дней/месяцев)
    growth_rate = 0.3 # Коэффициент прироста (r)
    diffusion_rate = 0.1 # Коэффициент миграции
    food_to_capacity_scale = 10 # Коэффициент пересчета корма в макс. популяцию
    
    # Координаты центра области (например, лесной массив)
    start_lat, start_lon = 55.75, 37.61 
    cell_size = 0.01 # Размер одной ячейки в градусах
    
    # 1. Создание карты корма (случайное распределение с градиентом)
    # Создаем матрицу, где значения имитируют наличие растительности
    food_map = np.random.uniform(1, 10, (grid_size, grid_size))
    # Добавим "богатую" зону в центре для наглядности
    food_map[5:10, 5:10] += 15 
    
    # 2. Инициализация популяции
    # Начинаем с небольшой группы кроликов в центре
    pop_map = np.zeros((grid_size, grid_size))
    pop_map[7, 7] = 10.0 
    
    # 3. Цикл моделирования
    for t in range(time_steps):
        new_pop_map = np.copy(pop_map)
        
        for i in range(grid_size):
            for j in range(grid_size):
                # Текущая популяция и емкость среды (зависит от корма)
                N = pop_map[i, j]
                K = food_map[i, j] * food_to_capacity_scale
                
                # Логистический рост
                growth = growth_rate * N * (1 - N / K) if K > 0 else 0
                
                # Диффузия (миграция в соседние ячейки)
                migration = 0
                neighbors = []
                if i > 0: neighbors.append((i-1, j))
                if i < grid_size-1: neighbors.append((i+1, j))
                if j > 0: neighbors.append((i, j-1))
                if j < grid_size-1: neighbors.append((i, j+1))
                
                for ni, nj in neighbors:
                    # Кролики перемещаются туда, где плотность ниже
                    diff = (pop_map[i, j] - pop_map[ni, nj]) * diffusion_rate
                    migration -= diff
                
                new_pop_map[i, j] += growth + migration
        
        # Ограничение: популяция не может быть отрицательной
        pop_map = np.maximum(0, new_pop_map)

    # 4. Визуализация на карте Folium
    m = folium.Map(location=[start_lat, start_lon], zoom_start=12, tiles='OpenStreetMap')
    
    # Подготовка данных для HeatMap или CircleMarkers
    heat_data = []
    for i in range(grid_size):
        for j in range(grid_size):
            lat = start_lat + (i * cell_size)
            lon = start_lon + (j * cell_size)
            val = pop_map[i, j]
            
            # Добавляем точку для тепловой карты (lat, lon, weight)
            heat_data.append([lat, lon, val])
            
            # Добавляем круговые маркеры для детального отображения
            if val > 1:
                folium.CircleMarker(
                    location=[lat, lon],
                    radius=val/2, 
                    color='green',
                    fill=True,
                    fill_color='lime',
                    popup=f"Pop: {int(val)} | Food: {int(food_map[i,j])}"
                ).add_to(m)

    # Добавляем слой тепловой карты для визуализации плотности
    HeatMap(heat_data).add_to(m)
    
    # Сохранение результата
    m.save("276.html")
    print("Simulation complete. Map saved as 276.html")

if __name__ == "__main__":
    simulate_rabbit_population()