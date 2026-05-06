import pandas as pd
import matplotlib.pyplot as plt
import folium

# Загрузите данные о уровнях воды реки Кыши Алматы за несколько лет.
data = pd.read_csv('kishi_almaty_water_levels.csv')

# Найдите пиковый уровень воды и средний многолетний показатель.
max_water_level = data['water_level'].max()
avg_water_level = data['water_level'].mean()

# Визуализируйте эти данные с помощью Matplotlib.
plt.figure(figsize=(10, 5))
data.plot(x='date', y='water_level')
plt.title('Water Levels on Kishi Almaty River')
plt.xlabel('Date')
plt.ylabel('Water Level (m)')
plt.axhline(y=max_water_level, color='r', linestyle='--', label='Max Water Level')
plt.axhline(y=avg_water_level, color='g', linestyle='--', label='Average Water Level')
plt.legend()
plt.show()

# Создайте интерактивную карту с помощью Folium.
m = folium.Map(location=[43.256891, 77.026539], zoom_start=12) # Координаты реки Кыши Алматы

folium.Marker([43.256891, 77.026539], popup=f'Max Water Level: {max_water_level}m\nAverage Water Level: {avg_water_level}m').add_to(m)

# Сохраните карту как HTML-файл.
m.save("122.html")