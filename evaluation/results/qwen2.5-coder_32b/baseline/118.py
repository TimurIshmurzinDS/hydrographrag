import pandas as pd
import folium

# Пример данных о расходе воды в реках (кубические метры в секунду)
data = {
    'river': ['Sarykan River', 'Temirlik River'],
    'discharge_m3_s': [10, 5]  # Расход воды в кубических метрах в секунду
}

# Создание DataFrame
df = pd.DataFrame(data)

# Период времени для расчета объема воды (в секундах)
time_period_seconds = 24 * 60 * 60  # 24 часа

# Расчет объема воды за сутки (кубические метры)
df['volume_m3'] = df['discharge_m3_s'] * time_period_seconds

# Общий объем воды из обеих рек
total_volume_m3 = df['volume_m3'].sum()

print(f"Общий объем воды, доступный для полива культур: {total_volume_m3} кубических метров")

# Координаты рек (примерные)
river_coordinates = {
    'Sarykan River': [42.8571, 76.9062],  # Примерные координаты
    'Temirlik River': [43.2345, 77.1234]  # Примерные координаты
}

# Создание карты с использованием folium
m = folium.Map(location=[43.0, 77.0], zoom_start=9)

# Добавление маркеров для рек
for river, coords in river_coordinates.items():
    folium.Marker(
        location=coords,
        popup=f"{river}: {df[df['river'] == river]['volume_m3'].values[0]} кубических метров в сутки",
        icon=folium.Icon(color='blue')
    ).add_to(m)

# Сохранение карты
m.save("118.html")