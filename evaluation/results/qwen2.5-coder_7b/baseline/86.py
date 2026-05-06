import folium
from folium.plugins import MarkerCluster

# Пример данных о текущем уровне воды и предсказанных значениях для каждой реки
data = {
    "Karaoy River": {"current_level": 10, "predicted_level": 15},
    "Temirlik River": {"current_level": 8, "predicted_level": 12},
    "Turgen River": {"current_level": 7, "predicted_level": 9}
}

# Создание карты
m = folium.Map(location=[40.7128, -74.0060], zoom_start=5)

# Создание маркера для каждой реки
for river, levels in data.items():
    current_level = levels["current_level"]
    predicted_level = levels["predicted_level"]
    
    # Определение цвета на основе уровня воды
    if predicted_level > 12:
        color = 'red'
    elif predicted_level > 10:
        color = 'orange'
    else:
        color = 'green'
    
    # Добавление маркера на карту
    folium.Marker(
        location=[40.7128, -74.0060],  # Пример координат для каждой реки
        popup=f"{river}: Current Level {current_level}, Predicted Level {predicted_level}",
        icon=folium.Icon(color=color)
    ).add_to(m)

# Сохранение карты в файл
m.save("86.html")