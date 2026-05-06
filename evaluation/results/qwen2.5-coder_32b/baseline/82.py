import pandas as pd
import folium

# Предположим, что у нас есть DataFrame с данными о постах наблюдения
# Пример данных:
data = {
    'post_id': [1, 2, 3, 4],
    'latitude': [50.123, 50.456, 50.789, 51.012],
    'longitude': [30.123, 30.456, 30.789, 31.012],
    'discharge': [150, 200, 250, 300]  # Расход воды в кубических метрах в секунду
}

# Создаем DataFrame из данных
df = pd.DataFrame(data)

# Критическая отметка паводка (в кубических метрах в секунду)
critical_discharge = 220

# Проверяем, превышает ли расход воды критическую отметку
df['is_flood'] = df['discharge'] > critical_discharge

# Создаем карту с помощью folium
m = folium.Map(location=[50.6, 30.6], zoom_start=10)

# Добавляем маркеры на карту
for index, row in df.iterrows():
    if row['is_flood']:
        color = 'red'  # Красный цвет для постов с превышением критической отметки
    else:
        color = 'blue'  # Синий цвет для остальных постов
    
    folium.Marker(
        location=[row['latitude'], row['longitude']],
        popup=f"Пост {row['post_id']}: Расход {row['discharge']} м³/с",
        icon=folium.Icon(color=color)
    ).add_to(m)

# Сохраняем карту в файл
m.save("82.html")