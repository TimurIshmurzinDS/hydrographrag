import folium
from folium.plugins import MarkerCluster

# Пример данных о текущих уровнях воды в реках Sarykan River и Aksu River
water_levels = {
    "Sarykan River": 10,  # Уровень воды в метрах
    "Aksu River": 8     # Уровень воды в метрах
}

# Минимальные уровни воды для орошения (в метрах)
min_water_levels = {
    "Sarykan River": 12,
    "Aksu River": 10
}

# Создание карты
m = folium.Map(location=[43.5, 76], zoom_start=8)

# Добавление маркеров с уровнями воды и их состоянием
for river, level in water_levels.items():
    min_level = min_water_levels[river]
    if level >= min_level:
        color = 'green'
        tooltip = f"{river}: Уровень воды {level} м (Достаточно)"
    else:
        color = 'red'
        tooltip = f"{river}: Уровень воды {level} м (Недостаточно)"

    folium.Marker(
        location=[43.5, 76],  # Пример координат для каждой реки
        popup=tooltip,
        icon=folium.Icon(color=color, icon='info-sign')
    ).add_to(m)

# Сохранение карты
m.save("106.html")