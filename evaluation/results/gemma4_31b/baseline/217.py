import folium
import pandas as pd
import numpy as np
import random

# 1. Симуляция данных датчиков вдоль реки Малая Алматинка (Kishi Almaty River)
# Координаты примерно вдоль русла реки в Алматы
sensors_data = [
    {"id": "Sensor_1", "lat": 43.225, "lon": 77.012, "temp": 15.5, "humidity": 65},
    {"id": "Sensor_2", "lat": 43.238, "lon": 77.035, "temp": 18.2, "humidity": 58},
    {"id": "Sensor_3", "lat": 43.251, "lon": 77.058, "temp": 21.0, "humidity": 52},
    {"id": "Sensor_4", "lat": 43.265, "lon": 77.081, "temp": 23.5, "humidity": 45},
    {"id": "Sensor_5", "lat": 43.278, "lon": 77.104, "temp": 25.1, "humidity": 38},
]

df = pd.DataFrame(sensors_data)

# 2. Модель анализа условий для кактусов
def generate_cactus_instruction(temp, humidity):
    instructions = []
    
    # Анализ температуры
    if temp < 15:
        instructions.append("Критически низкая температура! Срочно перенесите кактус в помещение или используйте обогрев.")
    elif temp < 20:
        instructions.append("Температура прохладная. Рекомендуется использование мини-парника.")
    else:
        instructions.append("Температурный режим оптимален.")
        
    # Анализ влажности
    if humidity > 60:
        instructions.append("Слишком высокая влажность (влияние реки)! Полностью прекратите полив и обеспечьте максимальную вентиляцию.")
    elif humidity > 40:
        instructions.append("Влажность выше нормы. Сократите частоту полива до 1 раза в месяц.")
    else:
        instructions.append("Влажность воздуха идеальна для кактусов.")
        
    return " ".join(instructions)

# 3. Расчет общего статуса и инструкций
df['instruction'] = df.apply(lambda x: generate_cactus_instruction(x['temp'], x['humidity']), axis=1)

def get_color(row):
    if row['temp'] >= 20 and row['humidity'] <= 40:
        return 'green'
    elif row['temp'] >= 15 and row['humidity'] <= 60:
        return 'orange'
    else:
        return 'red'

df['color'] = df.apply(get_color, axis=1)

# 4. Визуализация на карте
# Центр карты - Алматы, район реки Малая Алматинка
m = folium.Map(location=[43.25, 77.05], zoom_start=12, tiles='OpenStreetMap')

for index, row in df.iterrows():
    folium.CircleMarker(
        location=[row['lat'], row['lon']],
        radius=8,
        popup=f"<b>{row['id']}</b><br>T: {row['temp']}°C, H: {row['humidity']}%<br><i>{row['instruction']}</i>",
        color=row['color'],
        fill=True,
        fill_color=row['color'],
        fill_opacity=0.7
    ).add_to(m)

# Сохранение карты
m.save("217.html")

# 5. Вывод итоговой общей инструкции на основе средних данных
avg_temp = df['temp'].mean()
avg_hum = df['humidity'].mean()
final_guide = generate_cactus_instruction(avg_temp, avg_hum)

print("--- ИНСТРУКЦИЯ ПО ВЫРАЩИВАНИЮ КАКТУСОВ (на основе данных Kishi Almaty River) ---")
print(f"Средняя температура в зоне датчиков: {avg_temp:.2f}°C")
print(f"Средняя влажность в зоне датчиков: {avg_hum:.2f}%")
print(f"Общая рекомендация: {final_guide}")
print("--------------------------------------------------------------------------------")
print("Карта с детальными инструкциями по точкам сохранена в файл 217.html")