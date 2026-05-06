import folium
from branca.element import Template, MacroElement

# Шаг 1: Анализ геологических условий (простая модель)
geological_data = {
    'water_sources': [(48.7396, 2.3072)],  # Примерные координаты реки Талгар на Земле
    'minerals': [(48.7450, 2.3100)]
}

# Шаг 2: Создание модели почвы (простая модель)
soil_model = {
    'composition': {'sand': 60, 'clay': 20, 'organic_matter': 20},
    'pH': 7.0
}

# Шаг 3: Моделирование климата (простая модель)
climate_data = {
    'temperature': -50,  # Средняя температура на поверхности Марса
    'sunlight_hours': 12   # Среднее количество часов солнечного света в сутки
}

# Шаг 4: Оптимизация водоснабжения (простая модель)
water_supply = {
    'source_distance': 50,  # Расстояние до источника воды в км
    'irrigation_system_efficiency': 0.8  # Эффективность системы полива
}

# Шаг 5: Моделирование роста картофеля (простая модель)
potato_growth_model = {
    'growth_rate': 1.2,  # Коэффициент роста в день
    'harvest_period': 90  # Срок созревания культуры в днях
}

# Шаг 6: Визуализация результатов на карте
m = folium.Map(location=[48.7396, 2.3072], zoom_start=13)

# Добавление маркеров для источников воды и минералов
for coord in geological_data['water_sources']:
    folium.Marker(coord, popup='Источник воды').add_to(m)
    
for coord in geological_data['minerals']:
    folium.Marker(coord, popup='Минеральные включения').add_to(m)

# Добавление информации о модели почвы
soil_info = f"Состав почвы: {soil_model['composition']}\n pH: {soil_model['pH']}"
folium.Marker([48.7396, 2.3072], popup=soil_info).add_to(m)

# Добавление информации о климате
climate_info = f"Температура: {climate_data['temperature']} °C\n Солнечное освещение: {climate_data['sunlight_hours']} ч/сутки"
folium.Marker([48.7396, 2.3072], popup=climate_info).add_to(m)

# Добавление информации о водоснабжении
water_supply_info = f"Расстояние до источника: {water_supply['source_distance']} км\n Эффективность системы полива: {water_supply['irrigation_system_efficiency']}"
folium.Marker([48.7396, 2.3072], popup=water_supply_info).add_to(m)

# Добавление информации о модели роста картофеля
potato_growth_info = f"Коэффициент роста: {potato_growth_model['growth_rate']}\n Срок созревания: {potato_growth_model['harvest_period']} дней"
folium.Marker([48.7396, 2.3072], popup=potato_growth_info).add_to(m)

# Сохранение карты
m.save("263.html")