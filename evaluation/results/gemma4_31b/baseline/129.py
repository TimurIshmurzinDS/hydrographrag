import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import folium
from datetime import datetime

# 1. Симуляция данных (так как реальные данные требуют доступа к API гидропостов)
# Создаем синтетический набор данных за последние 5 лет (2019-2023)
np.random.seed(42)
years = np.arange(2019, 2024)
months = ['January', 'February', 'March', 'April', 'May', 'June', 
          'July', 'August', 'September', 'October', 'November', 'December']

data_list = []
for year in years:
    for month_idx, month in enumerate(months):
        # Весеннее половодье (март, апрель, май) - индексы 2, 3, 4
        is_spring = 2 <= month_idx <= 4
        
        # Генерация расхода воды: весной значения значительно выше
        # Kurty River: средний расход в половодье выше
        kurty_flow = np.random.uniform(50, 100) if is_spring else np.random.uniform(5, 20)
        # Tekes River: более стабильный, но чуть меньший расход
        tekes_flow = np.random.uniform(30, 70) if is_spring else np.random.uniform(8, 25)
        
        data_list.append({
            'Year': year,
            'Month': month,
            'Month_Idx': month_idx,
            'Kurty_River': kurty_flow,
            'Tekes_River': tekes_flow
        })

df = pd.DataFrame(data_list)

# 2. Фильтрация данных за период весеннего половодья (март-май)
spring_df = df[df['Month_Idx'].isin([2, 3, 4])]

# Расчет средних показателей по годам
annual_spring_avg = spring_df.groupby('Year')[['Kurty_River', 'Tekes_River']].mean()

print("Средний расход воды в период половодья (м3/с):")
print(annual_spring_avg)

# 3. Визуализация графиков
plt.figure(figsize=(12, 6))
plt.plot(annual_spring_avg.index, annual_spring_avg['Kurty_River'], marker='o', label='Kurty River', color='blue', linewidth=2)
plt.plot(annual_spring_avg.index, annual_spring_avg['Tekes_River'], marker='s', label='Tekes River', color='green', linewidth=2)
plt.title('Сравнение среднего расхода воды в период весеннего половодья (2019-2023)')
plt.xlabel('Год')
plt.ylabel('Расход воды (м3/с)')
plt.xticks(years)
plt.grid(True, linestyle='--', alpha=0.7)
plt.legend()
plt.savefig("discharge_comparison.png")
plt.close()

# 4. Геопространственная визуализация (Folium)
# Приблизительные координаты рек в регионе (Казахстан/Центральная Азия)
locations = {
    "Kurty River": [43.5, 79.5, annual_spring_avg['Kurty_River'].mean()],
    "Tekes River": [44.0, 81.0, annual_spring_avg['Tekes_River'].mean()]
}

# Создание карты
m = folium.Map(location=[43.75, 80.25], zoom_start=7, tiles='OpenStreetMap')

for river, info in locations.items():
    lat, lon, avg_flow = info
    folium.Marker(
        location=[lat, lon],
        popup=f"<b>{river}</b><br>Средний расход (весна): {avg_flow:.2f} м3/с",
        tooltip=river,
        icon=folium.Icon(color='blue' if 'Kurty' in river else 'green', icon='info-sign')
    ).add_to(m)

# Добавление текстового описания на карту
folium.Popup(
    f"Анализ половодья 2019-2023:<br>Kurty Avg: {annual_spring_avg['Kurty_River'].mean():.2f} m3/s<br>Tekes Avg: {annual_spring_avg['Tekes_River'].mean():.2f} m3/s"
).add_to(m)

# Сохранение карты
m.save("129.html")

print("\nProcessing complete. Map saved as 129.html and plot as discharge_comparison.png")