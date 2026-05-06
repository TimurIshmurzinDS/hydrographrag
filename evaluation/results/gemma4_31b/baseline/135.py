import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import folium
from folium.plugins import MarkerCluster

# 1. Симуляция исторических данных (так как реальные данные требуют доступа к гидрологическим архивам)
# Создаем временной ряд за 20 лет (2003-2022) для летнего периода
np.random.seed(42)
years = np.arange(2003, 2023)
# Средний расход воды (м3/с), с добавлением случайных колебаний и засушливых провалов
shilik_flow = np.random.normal(loc=15, scale=4, size=len(years))
sharyn_flow = np.random.normal(loc=10, scale=3, size=len(years))

# Искусственно создаем периоды засухи для наглядности сравнения
drought_years = [2008, 2012, 2015, 2018, 2021]
for yr_idx, yr in enumerate(years):
    if yr in drought_years:
        shilik_flow[yr_idx] *= 0.5  # Резкое падение стока
        sharyn_flow[yr_idx] *= 0.4  # Еще более резкое падение

df = pd.DataFrame({
    'Year': years,
    'Shilik': shilik_flow,
    'Sharyn': sharyn_flow
})

# 2. Анализ засух
def analyze_drought(series):
    mean = series.mean()
    std = series.std()
    threshold = mean - std  # Порог засухи: 1 стандартное отклонение ниже среднего
    drought_mask = series < threshold
    return drought_mask, threshold

shilik_droughts, shilik_thresh = analyze_drought(df['Shilik'])
sharyn_droughts, sharyn_thresh = analyze_drought(df['Sharyn'])

df['Shilik_Drought'] = shilik_droughts
df['Sharyn_Drought'] = sharyn_droughts

# Сводная статистика
shilik_count = df['Shilik_Drought'].sum()
sharyn_count = df['Sharyn_Drought'].sum()

print(f"Количество лет летней засухи: Шилик = {shilik_count}, Шарын = {sharyn_count}")

# 3. Визуализация временных рядов
plt.figure(figsize=(12, 6))
plt.plot(df['Year'], df['Shilik'], label='Shilik River', color='blue', marker='o')
plt.plot(df['Year'], df['Sharyn'], label='Sharyn River', color='green', marker='s')
plt.axhline(y=shilik_thresh, color='blue', linestyle='--', alpha=0.5, label='Shilik Threshold')
plt.axhline(y=sharyn_thresh, color='green', linestyle='--', alpha=0.5, label='Sharyn Threshold')
plt.title("Comparison of Summer River Discharge (Historical)")
plt.xlabel("Year")
plt.ylabel("Flow Rate (m3/s)")
plt.legend()
plt.grid(True)
plt.savefig("drought_analysis.png")
plt.close()

# 4. Геопространственная визуализация (Folium)
# Приблизительные координаты рек в Казахстане
locations = {
    "Shilik River": [44.5, 78.5, shilik_count],
    "Sharyn River": [43.8, 80.2, sharyn_count]
}

# Создание карты
m = folium.Map(location=[44.1, 79.3], zoom_start=6, tiles='OpenStreetMap')

for river, data in locations.items():
    lat, lon, count = data
    color = 'red' if count > 5 else 'orange'
    
    folium.CircleMarker(
        location=[lat, lon],
        radius=10,
        popup=f"<b>{river}</b><br>Drought Years: {count}",
        color=color,
        fill=True,
        fill_color=color
    ).add_to(m)
    
    # Добавляем текстовую метку
    folium.Marker(
        location=[lat, lon],
        icon=folium.DivIcon(html=f'<div style="font-family: Arial; color: black; font-weight: bold;">{river}</div>')
    ).add_to(m)

# Сохранение карты строго в файл 135.html
m.save("135.html")

print("Analysis complete. Map saved as 135.html and plot as drought_analysis.png")