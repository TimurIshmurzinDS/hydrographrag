import pandas as pd
import folium

# Шаг 1: Сбор данных (примерные данные)
data = {
    'river': ['Sarykan River', 'Aksu River'],
    'current_water_level': [1.2, 0.8],  # Уровни воды в метрах
    'required_water_level_for_irrigation': [1.0, 1.0]  # Требуемые уровни воды для орошения в метрах
}

# Шаг 2: Обработка данных
df = pd.DataFrame(data)

# Шаг 3: Определение требований к уровню воды (уже определено в DataFrame)
# Шаг 4: Анализ данных
df['sufficient_for_irrigation'] = df['current_water_level'] >= df['required_water_level_for_irrigation']

# Координаты рек для визуализации на карте
river_coordinates = {
    'Sarykan River': [42.8536, 79.1016],  # Примерные координаты
    'Aksu River': [42.8656, 79.1116]     # Примерные координаты
}

# Шаг 5: Визуализация результатов
m = folium.Map(location=[42.8596, 79.1066], zoom_start=13)  # Центральная точка карты

for index, row in df.iterrows():
    river_name = row['river']
    current_level = row['current_water_level']
    required_level = row['required_water_level_for_irrigation']
    sufficient = row['sufficient_for_irrigation']
    
    coordinates = river_coordinates[river_name]
    
    if sufficient:
        color = 'green'
        popup_text = f"{river_name}: Уровень воды {current_level} м (достаточно для орошения)"
    else:
        color = 'red'
        popup_text = f"{river_name}: Уровень воды {current_level} м (недостаточно для орошения, требуется минимум {required_level} м)"
    
    folium.Marker(
        location=coordinates,
        popup=popup_text,
        icon=folium.Icon(color=color)
    ).add_to(m)

# Сохранение карты
m.save("106.html")