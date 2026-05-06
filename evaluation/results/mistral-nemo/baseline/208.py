import pandas as pd
import matplotlib.pyplot as plt
import folium

# 1. Подготовка данных
data_koksu = pd.read_csv('koksu_river_data.csv')
data_byzhy = pd.read_csv('byzhy_river_data.csv')

# 2. Очистка данных
data_koksu.dropna(inplace=True)
data_byzhy.dropna(inplace=True)

# 3. Агрегация данных
data_koksu_agg = data_koksu.groupby(data_koksu['date'].dt.year)['water_level'].mean().reset_index()
data_byzhy_agg = data_byzhy.groupby(data_byzhy['date'].dt.year)['water_level'].mean().reset_index()

# 4. Визуализация тренда
plt.figure(figsize=(10,5))
plt.plot(data_koksu_agg['date'], data_koksu_agg['water_level'], label='Koksu River')
plt.plot(data_byzhy_agg['date'], data_byzhy_agg['water_level'], label='Byzhy River')
plt.xlabel('Year')
plt.ylabel('Average Minimum Water Level (m)')
plt.title('10-year trend of minimum water levels in Koksu and Byzhy Rivers')
plt.legend()
plt.grid(True)
plt.show()

# 5. Картографирование данных
m = folium.Map(location=[data_koksu['latitude'].mean(), data_koksu['longitude'].mean()], zoom_start=8)

folium.Marker([data_koksu['latitude'].mean(), data_koksu['longitude'].mean()], popup='Koksu River').add_to(m)
folium.Marker([data_byzhy['latitude'].mean(), data_byzhy['longitude'].mean()], popup='Byzhy River').add_to(m)

# 6. Сохранение результатов
plt.savefig('water_level_trend.png')
m.save("208.html")