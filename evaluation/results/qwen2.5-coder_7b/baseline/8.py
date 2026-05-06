import pandas as pd
import folium

# Пример данных о местоположении датчиков (широта, долгота)
data = {
    'latitude': [43.210, 43.215, 43.220, 43.225],
    'longitude': [76.890, 76.895, 76.900, 76.905]
}

# Создаем DataFrame
df = pd.DataFrame(data)

# Создаем карту с центром в Ulken Almaty River
m = folium.Map(location=[43.2175, 76.8975], zoom_start=12)

# Добавляем маркеры для каждого датчика
for index, row in df.iterrows():
    folium.Marker([row['latitude'], row['longitude']], popup=f"Датчик {index+1}").add_to(m)

# Сохраняем карту в файл
m.save("8.html")

print("Карта сохранена как 8.html")