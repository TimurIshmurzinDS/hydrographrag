import pandas as pd
import folium

# Загрузка данных о уровнях воды (замените на фактический путь к файлу)
data = pd.read_csv("uzyn_kargaly_water_levels.csv")

# Преобразование даты в формат datetime
data['Date'] = pd.to_datetime(data['Date'])

# Фильтрация данных по периоду весеннего паводка (замените на фактические даты)
spring_flood_data = data[(data['Date'] >= '2023-03-15') & (data['Date'] <= '2023-05-15')]

# Вычисление максимального уровня воды
max_water_level = spring_flood_data['Water Level'].max()

print(f"Пиковый уровень воды в реке Uzyn Kargaly River во время весеннего паводка: {max_water_level} метров")

# Визуализация (необязательно)
m = folium.Map(location=[43.25, 70.8], zoom_start=10)  # Замените на координаты реки Uzyn Kargaly River

folium.Marker([43.25, 70.8], popup=f"Максимальный уровень: {max_water_level} м").add_to(m)

m.save("22.html")