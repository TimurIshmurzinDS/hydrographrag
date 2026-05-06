import pandas as pd
import folium

# Предположим, что у нас есть данные о уровне воды реки Каскелен в формате CSV
# Структура данных: дата, уровень_воды (в метрах)
data = {
    'date': pd.date_range(start='1/1/2023', periods=365),
    'water_level': [1.0 + 0.5 * abs(i - 182) / 182 for i in range(365)]  # Простая модель сезонных колебаний
}

# Создаем DataFrame из данных
df = pd.DataFrame(data)

# Анализ данных: находим периоды максимального уровня воды
max_water_level = df['water_level'].max()
critical_dates = df[df['water_level'] == max_water_level]['date']

# Выводим даты с максимальным уровнем воды
print("Даты с максимальным уровнем воды:")
for date in critical_dates:
    print(date)

# Координаты реки Каскелен (примерные)
kaskelen_coords = [43.2567, 76.9285]

# Создаем карту folium
m = folium.Map(location=kaskelen_coords, zoom_start=10)

# Добавляем маркер на место реки Каскелен
folium.Marker(
    location=kaskelen_coords,
    popup='Река Каскелен',
    icon=folium.Icon(icon="info-sign")
).add_to(m)

# Сохраняем карту в файл
m.save("240.html")

print("Карта сохранена как 240.html")