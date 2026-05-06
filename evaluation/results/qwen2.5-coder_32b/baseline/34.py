import pandas as pd
import folium

# Шаг 1: Сбор данных (примерные данные)
data = {
    'latitude': [56.32, 56.34, 56.36],
    'longitude': [44.01, 44.03, 44.05],
    'oxygen_level': [8.5, 7.9, 8.2],  # Уровень кислорода в мг/л
    'pollutant_concentration': [0.05, 0.10, 0.08]  # Концентрация загрязняющих веществ в мг/л
}

# Создание DataFrame
df = pd.DataFrame(data)

# Шаг 2: Подготовка данных (примерная обработка)
# Удаление пропущенных значений, если они есть
df.dropna(inplace=True)

# Шаг 3: Анализ данных (вычисление средних показателей)
average_oxygen_level = df['oxygen_level'].mean()
average_pollutant_concentration = df['pollutant_concentration'].mean()

print(f"Средний уровень кислорода: {average_oxygen_level} мг/л")
print(f"Средняя концентрация загрязняющих веществ: {average_pollutant_concentration} мг/л")

# Шаг 4: Визуализация данных
# Создание карты с центром в средних координатах точек измерений
map_center = [df['latitude'].mean(), df['longitude'].mean()]
m = folium.Map(location=map_center, zoom_start=12)

# Добавление маркеров на карту
for index, row in df.iterrows():
    popup_text = f"Уровень кислорода: {row['oxygen_level']} мг/л\nКонцентрация загрязняющих веществ: {row['pollutant_concentration']} мг/л"
    folium.Marker(
        location=[row['latitude'], row['longitude']],
        popup=popup_text,
        icon=folium.Icon(color='red')
    ).add_to(m)

# Сохранение карты в файл
m.save("34.html")