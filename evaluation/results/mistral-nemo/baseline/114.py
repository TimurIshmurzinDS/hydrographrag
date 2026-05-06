import folium
import pandas as pd

# Шаг 1: Получение данных о дебне рек Aksu River и Kurty River для заданного периода времени.
aksu_data = pd.read_csv('aksu_river_discharge.csv')
kurty_data = pd.read_csv('kurty_river_discharge.csv')

# Шаг 2: Вычисление среднего дебита для каждой реки в течение этого периода.
aksu_avg_discharge = aksu_data['discharge'].mean()
kurty_avg_discharge = kurty_data['discharge'].mean()

# Шаг 3: Определение площади территории, которую каждая река может орошать, исходя из ее среднего дебита и нормы расхода воды на единицу площади.
norm_water_usage = 0.01 # примерная норма расхода воды на единицу площади в м³/га
aksu_irrigation_potential = aksu_avg_discharge * norm_water_usage
kurty_irrigation_potential = kurty_avg_discharge * norm_water_usage

# Шаг 4: Визуализация результатов на карте с помощью библиотеки `folium`.
m = folium.Map(location=[43.25, 76.9], zoom_start=8) # примерные координаты и масштаб для демонстрации

# Добавляем реки на карту
aksu_river = [41.05, 72.8] # примерные координаты реки Aksu River
kurty_river = [43.5, 77.0] # примерные координаты реки Kurty River

folium.PolyLine(aksu_river, weight=5, color='blue', popup=f'Aksu River\nAverage discharge: {aksu_avg_discharge:.2f} m³/s\nIrrigation potential: {aksu_irrigation_potential:.2f} га').add_to(m)
folium.PolyLine(kurty_river, weight=5, color='red', popup=f'Kurty River\nAverage discharge: {kurty_avg_discharge:.2f} m³/s\nIrrigation potential: {kurty_irrigation_potential:.2f} га').add_to(m)

# Сохраняем карту в файл
m.save("114.html")