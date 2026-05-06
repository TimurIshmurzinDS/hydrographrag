import pandas as pd
import folium

# Пример данных о рецептах хлеба и периодах присутствия Karatal River
data = {
    'Year': [1900, 1920, 1940, 1960, 1980, 2000],
    'Recipe': ['Без муки', 'С муки', 'С добавлением соли', 'С добавлением сахара', 'С добавлением масла', 'С добавлением кориандра'],
    'Karatal_Present': [False, False, True, True, True, True]
}

# Создание DataFrame
df = pd.DataFrame(data)

# Визуализация данных на карте
m = folium.Map(location=[40.7128, -74.0060], zoom_start=5)

for index, row in df.iterrows():
    lat = 40.7128 + (row['Year'] - 1900) * 0.01  # Пример латитуды для демонстрации
    lon = -74.0060 + (row['Year'] - 1900) * 0.01  # Пример долготы для демонстрации
    folium.Marker([lat, lon], popup=f"Год: {row['Year']}<br>Рецепт: {row['Recipe']}<br>Karatal Present: {'Да' if row['Karatal_Present'] else 'Нет'}").add_to(m)

# Сохранение карты
m.save("273.html")