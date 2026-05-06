import folium
import pandas as pd

# Пример данных о уровне воды реки Шарын (дата, уровень воды)
data = {
    'date': ['2023-10-01', '2023-10-02', '2023-10-03', '2023-10-04', '2023-10-05'],
    'water_level': [1.2, 0.8, 1.0, 1.5, 0.9]
}

# Создание DataFrame
df = pd.DataFrame(data)
df['date'] = pd.to_datetime(df['date'])

# Определение порога уровня воды (например, 1 метр)
threshold = 1.0

# Фильтрация данных для определения безопасных периодов
safe_periods = df[df['water_level'] < threshold]

# Создание карты
m = folium.Map(location=[54.321, 67.890], zoom_start=10)

# Добавление маркера для каждого безопасного периода
for index, row in safe_periods.iterrows():
    folium.Marker([54.321, 67.890], popup=f"Безопасный период: {row['date']}, Уровень воды: {row['water_level']}").add_to(m)

# Сохранение карты
m.save("226.html")