import pandas as pd
import folium

# Подготовка данных (предположим, что данные хранятся в DataFrame)
data = {
    'river_name': ['Sharyn River'],
    'max_flood_level': [10.5],
    'historical_mean_level': [8.2]
}
df = pd.DataFrame(data)

# Обработка данных
max_flood_level = df['max_flood_level'].values[0]
historical_mean_level = df['historical_mean_level'].values[0]

difference = max_flood_level - historical_mean_level

print(f"Разница между максимальным зафиксированным уровнем паводка и его историческим средним значением: {difference}")

# Визуализация результатов на карте
m = folium.Map(location=[43.5, 76.0], zoom_start=10)
folium.Marker([43.5, 76.0], popup=f"Разница между максимальным зафиксированным уровнем паводка и его историческим средним значением: {difference}").add_to(m)

m.save("127.html")