import requests
import folium
from folium.plugins import TimestampedGeoJson

# Функция для получения данных о уровне воды в Uzyn Kargaly River
def get_water_level_data():
    url = "https://api.example.com/water-level?river=UzynKargaly"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        raise Exception("Failed to fetch water level data")

# Функция для анализа данных и определения состояния реки
def analyze_water_level(data):
    levels = [item['level'] for item in data]
    avg_level = sum(levels) / len(levels)
    min_level = min(levels)
    max_level = max(levels)

    if avg_level < 10:
        return "низкое"
    elif avg_level > 20:
        return "высокое"
    else:
        return "нормальное"

# Функция для создания рецепта пирога
def create_recipe(water_level_state):
    if water_level_state == "низкое":
        recipe = {
            "title": "Пирог с низким уровнем воды",
            "ingredients": ["мука", "сахар", "масло", "яйца", "вода"],
            "instructions": [
                "1. Разогрейте духовку до 180°C.",
                "2. Натрите муку и добавьте сахар, масло и яйца.",
                "3. Добавьте воду и хорошо перемешайте.",
                "4. Выложите тесто на противень и выпекайте 30 минут."
            ]
        }
    elif water_level_state == "высокое":
        recipe = {
            "title": "Пирог с высоким уровнем воды",
            "ingredients": ["мука", "сахар", "масло", "яйца", "вода", "чайный лист"],
            "instructions": [
                "1. Разогрейте духовку до 200°C.",
                "2. Натрите муку и добавьте сахар, масло и яйца.",
                "3. Добавьте воду и чайный лист, хорошо перемешайте.",
                "4. Выложите тесто на противень и выпекайте 35 минут."
            ]
        }
    else:
        recipe = {
            "title": "Пирог с нормальным уровнем воды",
            "ingredients": ["мука", "сахар", "масло", "яйца", "вода"],
            "instructions": [
                "1. Разогрейте духовку до 180°C.",
                "2. Натрите муку и добавьте сахар, масло и яйца.",
                "3. Добавьте воду и хорошо перемешайте.",
                "4. Выложите тесто на противень и выпекайте 30 минут."
            ]
        }
    return recipe

# Функция для визуализации данных на карте
def visualize_water_level(data):
    m = folium.Map(location=[data[0]['latitude'], data[0]['longitude']], zoom_start=12)
    
    water_levels = []
    for item in data:
        water_levels.append({
            "type": "Feature",
            "geometry": {
                "type": "Point",
                "coordinates": [item['longitude'], item['latitude']]
            },
            "properties": {
                "time": item['timestamp'],
                "level": item['level']
            }
        })
    
    TimestampedGeoJson(water_levels, period="PT1H", add_last_point=True).add_to(m)
    
    m.save("211.html")

# Основной код
if __name__ == "__main__":
    data = get_water_level_data()
    water_level_state = analyze_water_level(data)
    recipe = create_recipe(water_level_state)
    print(f"### Рецепт пирога: {recipe['title']}")
    for ingredient in recipe['ingredients']:
        print(f"- {ingredient}")
    print("\n".join(recipe['instructions']))
    
    visualize_water_level(data)