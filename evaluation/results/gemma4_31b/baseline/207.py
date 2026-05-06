import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import folium
from datetime import datetime, timedelta

# 1. Генерация синтетических данных для двух рек
def generate_river_data(river_name, start_year=2004, end_year=2023):
    np.random.seed(42 if river_name == "Emel" else 7)
    date_rng = pd.date_range(start=f"{start_year}-01-01", end=f"{end_year}-12-31", freq='D')
    
    # Базовый расход + сезонность (синусоида) + шум
    # Emel - более крупная река, Turgen - горная, более изменчивая
    base_flow = 15 if river_name == "Emel" else 8
    amplitude = 10 if river_name == "Emel" else 6
    
    # Создаем сезонный цикл
    days = np.arange(len(date_rng))
    seasonal_pattern = base_flow + amplitude * np.sin(2 * np.pi * days / 365.25)
    noise = np.random.normal(0, 2, len(date_rng))
    
    # Добавляем случайные экстремальные падения (засухи)
    extremes = np.random.choice([0, 1], size=len(date_rng), p=[0.98, 0.02])
    seasonal_pattern[extremes == 1] *= 0.1 
    
    flow = np.maximum(0.1, seasonal_pattern + noise)
    return pd.DataFrame({'date': date_rng, 'flow': flow, 'river': river_name})

# Подготовка данных
df_emel = generate_river_data("Emel")
df_turgen = generate_river_data("Turgen")

# 2. Анализ экстремальных меженей
def analyze_low_water(df):
    mean_flow = df['flow'].mean()
    threshold = mean_flow * 0.2  # Порог экстремальной межени (20% от среднего)
    
    # Помечаем дни экстремальной межени
    df['is_extreme'] = df['flow'] < threshold
    
    # Группируем по годам и считаем количество дней
    df['year'] = df['date'].dt.year
    yearly_freq = df.groupby('year')['is_extreme'].sum()
    
    return yearly_freq, threshold

freq_emel, thresh_emel = analyze_low_water(df_emel)
freq_turgen, thresh_turgen = analyze_low_water(df_turgen)

# 3. Визуализация результатов (Графики)
plt.figure(figsize=(12, 6))
plt.plot(freq_emel.index, freq_emel.values, marker='o', label=f'Emel River (Thresh: {thresh_emel:.2f})', color='blue')
plt.plot(freq_turgen.index, freq_turgen.values, marker='s', label=f'Turgen River (Thresh: {thresh_turgen:.2f})', color='green')
plt.title("Частота дней экстремальной межени по годам (2004-2023)")
plt.xlabel("Год")
plt.ylabel("Количество дней в году")
plt.legend()
plt.grid(True, linestyle='--', alpha=0.7)
plt.savefig("low_water_analysis.png")
plt.close()

# 4. Геопространственная визуализация (Folium)
# Координаты (приблизительные для региона Алматинской области, Казахстан)
locations = {
    "Emel River": [43.5, 78.5],
    "Turgen River": [43.2, 77.5]
}

m = folium.Map(location=[43.3, 78.0], zoom_start=7, tiles='OpenStreetMap')

for river, coords in locations.items():
    # Определяем данные для попапа
    if river == "Emel River":
        total_days = freq_emel.sum()
        avg_days = freq_emel.mean()
    else:
        total_days = freq_turgen.sum()
        avg_days = freq_turgen.mean()
        
    folium.Marker(
        location=coords,
        popup=f"<b>{river}</b><br>Всего дней межени: {int(total_days)}<br>Среднее в год: {avg_days:.1f}",
        icon=folium.Icon(color='blue' if "Emel" in river else 'green', icon='info-sign')
    ).add_to(m)

# Сохранение карты строго по условию
m.save("207.html")

print("Анализ завершен. Результаты сохранены в 'low_water_analysis.png' и '207.html'.")
print(f"Средняя частота меженей Emel: {freq_emel.mean():.2f} дней/год")
print(f"Средняя частота меженей Turgen: {freq_turgen.mean():.2f} дней/год")