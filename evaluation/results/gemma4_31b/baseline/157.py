import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import folium
from folium import plugins

def simulate_river_runoff(river_name, base_precip, runoff_coeff):
    """
    Симуляция сезонного стока на основе типичных климатических данных 
    для горных рек Казахстана (снеговое питание).
    """
    months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
    
    # Типичный профиль осадков (условно)
    precip_pattern = np.array([40, 35, 50, 60, 70, 50, 40, 45, 55, 60, 50, 45]) 
    # Температурный профиль (влияет на снеготаяние)
    temp_pattern = np.array([-10, -5, 2, 10, 18, 22, 25, 23, 15, 8, 0, -7])
    
    # Расчет стока: 
    # Зимой сток минимален (вода в снегу), весной-летом пик (таяние + дожди)
    runoff = []
    snow_accumulation = 0
    
    for i in range(12):
        if temp_pattern[i] < 0:
            snow_accumulation += precip_pattern[i] * 0.8
            current_q = (precip_pattern[i] * 0.1) * runoff_coeff # Минимальный базовый сток
        else:
            # Таяние снега + текущие осадки
            melt = snow_accumulation * 0.4 if temp_pattern[i] > 5 else snow_accumulation * 0.1
            snow_accumulation -= melt
            current_q = (precip_pattern[i] + melt) * runoff_coeff
        
        runoff.append(current_q)
        
    return np.array(runoff), months

# Параметры для рек
rivers_data = {
    "Shilik River": {"precip": 600, "coeff": 0.45, "coords": [43.2, 78.5]},
    "Shyzhyn River": {"precip": 500, "coeff": 0.38, "coords": [43.1, 78.8]}
}

results = {}

# Расчеты
plt.figure(figsize=(10, 6))
for name, params in rivers_data.items():
    q_values, months = simulate_river_runoff(name, params['precip'], params['coeff'])
    amplitude = np.max(q_values) - np.min(q_values)
    results[name] = {"amplitude": amplitude, "flow": q_values}
    plt.plot(months, q_values, label=f"{name} (Amp: {amplitude:.2f})", marker='o')

plt.title("Прогнозируемый сезонный сток рек")
plt.xlabel("Месяц")
plt.ylabel("Условный объем стока (м³/с)")
plt.legend()
plt.grid(True)
plt.savefig("runoff_plot.png")
plt.show()

# Вывод результатов в консоль
for river, data in results.items():
    print(f"Река: {river} | Прогнозируемая амплитуда стока: {data['amplitude']:.2f} ед.")

# --- Визуализация на карте ---
# Создаем карту, центрированную в регионе
m = folium.Map(location=[43.15, 78.65], zoom_start=9, tiles='OpenStreetMap')

for name, params in rivers_data.items():
    # Добавляем маркер реки
    folium.Marker(
        location=params['coords'],
        popup=f"{name} - Amp: {results[name]['amplitude']:.2f}",
        icon=folium.Icon(color='blue', icon='info-sign')
    ).add_to(m)
    
    # Имитация зоны водосбора (окружность)
    folium.Circle(
        location=params['coords'],
        radius=20000, # 20 км
        color='blue',
        fill=True,
        fill_opacity=0.2,
        popup=f"Бассейн реки {name}"
    ).add_to(m)

# Сохранение карты
m.save("157.html")
print("Карта сохранена как 157.html")