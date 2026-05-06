import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import folium

# Предположим, что данные находятся в CSV файлах с колонками: 'timestamp', 'water_level', 'river', 'latitude', 'longitude'
data_ili = pd.read_csv('data_ili.csv', parse_dates=['timestamp'])
data_karatal = pd.read_csv('data_karatal.csv', parse_dates=['timestamp'])

# Объединение данных в один DataFrame
data = pd.concat([data_ili, data_karatal], ignore_index=True)

# Предварительная обработка данных: удаление пропусков и аномалий
data.dropna(inplace=True)
data = data[(data['water_level'] > 0) & (data['water_level'] < 100)]  # Примерный фильтр для аномалий

# Анализ стабильности: вычисление стандартного отклонения и коэффициента вариации
stability_analysis = data.groupby('river')['water_level'].agg(['std', 'mean']).reset_index()
stability_analysis['cv'] = stability_analysis['std'] / stability_analysis['mean']

print(stability_analysis)

# Визуализация временных рядов
plt.figure(figsize=(14, 7))
for river in data['river'].unique():
    plt.plot(data[data['river'] == river]['timestamp'], 
             data[data['river'] == river]['water_level'], 
             label=river)
plt.xlabel('Время')
plt.ylabel('Уровень воды')
plt.title('Температурные ряды уровня воды для рек Или и Каратал')
plt.legend()
plt.grid(True)
plt.savefig("water_levels_timeseries.png")
plt.show()

# Создание карты с местоположением датчиков
m = folium.Map(location=[42.8746, 74.5910], zoom_start=10)  # Координаты Бишкека

for _, row in data.iterrows():
    folium.Marker(
        location=[row['latitude'], row['longitude']],
        popup=f"Река: {row['river']}, Уровень воды: {row['water_level']} м"
    ).add_to(m)

m.save("150.html")