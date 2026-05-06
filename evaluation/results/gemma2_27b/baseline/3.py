import pandas as pd
import folium

# Замените 'путь_к_данным.csv' на фактический путь к файлу с данными
data = pd.read_csv('путь_к_данным.csv')

# Фильтруем данные по реке Talgar River
talgar_data = data[data['River'] == 'Talgar River']

# Сортируем данные по дате и времени в обратном порядке
talgar_data = talgar_data.sort_values(by=['Date', 'Time'], ascending=False)

# Получаем последний показатель уровня воды
last_water_level = talgar_data['Water Level'].iloc[0]

print(f"Последний зафиксированный уровень воды на реке Talgar River: {last_water_level}")

# Визуализация (если требуется)
m = folium.Map(location=[43.25, 76.9], zoom_start=10)  # Замените координаты на координаты реки Talgar River

folium.Marker([43.25, 76.9], popup=f"Последний уровень: {last_water_level}").add_to(m)
m.save("3.html")