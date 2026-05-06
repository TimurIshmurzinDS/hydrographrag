import pandas as pd
import folium

# Пример данных о реках и их текущем уровне воды
data = {
    'River': ['Baskan River', 'Prokhodnaya River'],
    'Current Water Level': [10, 8],
    'Normal Water Level': [9, 7]
}

# Создание DataFrame
df = pd.DataFrame(data)

# Определение рек, на которых уровень воды превышает норму
df['Water Level Exceeds Normal'] = df['Current Water Level'] > df['Normal Water Level']

# Фильтрация рек с превышением уровня воды
exceeded_rivers = df[df['Water Level Exceeds Normal']]['River'].tolist()

# Создание карты
m = folium.Map(location=[50, 30], zoom_start=6)

# Добавление маркеров на карте для каждой реки
for index, row in df.iterrows():
    folium.Marker([row['Latitude'], row['Longitude']], 
                  popup=f"{row['River']}: {'Превышение уровня воды' if row['Water Level Exceeds Normal'] else 'Нормальный уровень'}",
                  icon=folium.Icon(color='red' if row['Water Level Exceeds Normal'] else 'green')).add_to(m)

# Сохранение карты
m.save("81.html")

print(f"Реки с превышением уровня воды: {exceeded_rivers}")