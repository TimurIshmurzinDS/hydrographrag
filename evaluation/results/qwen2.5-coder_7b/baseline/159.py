import folium
from folium.plugins import MarkerCluster
import requests

# Функция для получения прогноза погоды
def get_weather_forecast(api_key, city):
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}"
    response = requests.get(url)
    data = response.json()
    return data['main']['temp']

# Функция для определения критических уровней высоты водных стояний
def get_critical_levels():
    # Здесь можно добавить логику для получения критических уровней из базы данных или файла конфигурации
    critical_levels = {
        'Lepsy River': 100,  # Примерный уровень в метрах
        'Shynzhaly River': 80   # Примерный уровень в метрах
    }
    return critical_levels

# Функция для анализа риска перелива
def analyze_risk(current_levels, critical_levels):
    risks = {}
    for river, level in current_levels.items():
        if level > critical_levels[river]:
            risks[river] = 'Высокий риск'
        else:
            risks[river] = 'Низкий риск'
    return risks

# Основная функция для анализа и визуализации
def analyze_and_visualize():
    api_key = 'YOUR_OPENWEATHERMAP_API_KEY'  # Замените на ваш API ключ OpenWeatherMap
    cities = {
        'Lepsy River': 'Lepsy, Russia',
        'Shynzhaly River': 'Shynzhaly, Kazakhstan'
    }
    
    current_levels = {}
    for river, city in cities.items():
        temp = get_weather_forecast(api_key, city)
        # Пример: преобразуем температуру в метры (это примерный расчет)
        current_level = temp * 0.1
        current_levels[river] = current_level
    
    critical_levels = get_critical_levels()
    risks = analyze_risk(current_levels, critical_levels)
    
    # Создание карты
    m = folium.Map(location=[52.4863, 41.9021], zoom_start=7)  # Примерные координаты центра карты
    
    marker_cluster = MarkerCluster().add_to(m)
    
    for river, level in current_levels.items():
        color = 'red' if risks[river] == 'Высокий риск' else 'green'
        folium.Marker(
            location=[52.4863, 41.9021],  # Примерные координаты реки
            popup=f"{river}: Уровень {level} м, Риск: {risks[river]}",
            icon=folium.Icon(color=color)
        ).add_to(marker_cluster)
    
    m.save("159.html")

# Вызов основной функции
analyze_and_visualize()