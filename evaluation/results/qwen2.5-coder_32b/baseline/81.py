import folium
import pandas as pd

# Пример данных о текущих уровнях воды (в метрах над устьем)
data = {
    'River': ['Baskan River', 'Prokhodnaya River'],
    'Current_Water_Level': [2.5, 3.0]  # Примерные значения
}

# Нормативные уровни воды для рек (в метрах над устьем)
normative_levels = {
    'Baskan River': 2.0,
    'Prokhodnaya River': 2.8
}

# Создание DataFrame из данных
df = pd.DataFrame(data)

# Определение рек с повышенным уровнем воды
exceeding_rivers = df[df['Current_Water_Level'] > df['River'].map(normative_levels)]

# Координаты рек (примерные значения)
coordinates = {
    'Baskan River': [56.123, 94.789],
    'Prokhodnaya River': [56.456, 95.012]
}

# Создание карты
m = folium.Map(location=[56.290, 94.950], zoom_start=10)

# Добавление маркеров для рек с повышенным уровнем воды
for index, row in exceeding_rivers.iterrows():
    river_name = row['River']
    level = row['Current_Water_Level']
    normative_level = normative_levels[river_name]
    folium.Marker(
        location=coordinates[river_name],
        popup=f"{river_name}: Уровень воды {level}м (Норма: {normative_level}м)",
        icon=folium.Icon(color='red')
    ).add_to(m)

# Сохранение карты в файл
m.save("81.html")