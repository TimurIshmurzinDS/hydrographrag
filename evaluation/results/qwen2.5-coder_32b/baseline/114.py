import folium
from folium.plugins import HeatMap

# Предположим, что у нас есть данные о текущем дебите рек (в кубических метрах в секунду)
debits = {
    "Aksu River": 150,  # Примерные данные для демонстрации
    "Kurty River": 80   # Примерные данные для демонстрации
}

# Функция для оценки ирригационного потенциала на основе дебита
def calculate_irrigation_potential(debit):
    # Простая модель: Ирригационный потенциал пропорционален кубическому корню из дебита
    return debit ** (1/3)

# Расчет ирригационного потенциала для каждой реки
irrigation_potentials = {river: calculate_irrigation_potential(debit) for river, debit in debits.items()}

# Координаты примерных местоположений рек
coordinates = {
    "Aksu River": [42.853611, 79.066667],  # Примерные координаты для демонстрации
    "Kurty River": [42.550000, 78.650000]   # Примерные координаты для демонстрации
}

# Создание карты с использованием folium
m = folium.Map(location=[42.7, 78.9], zoom_start=10)

# Добавление маркеров на карту с ирригационным потенциалом
for river, potential in irrigation_potentials.items():
    folium.Marker(
        location=coordinates[river],
        popup=f"{river}: Ирригационный потенциал = {potential:.2f}",
        icon=folium.Icon(color='blue' if river == "Aksu River" else 'green')
    ).add_to(m)

# Добавление тепловой карты для визуализации ирригационного потенциала
heat_data = [[coordinates[river][0], coordinates[river][1], potential] for river, potential in irrigation_potentials.items()]
HeatMap(heat_data).add_to(m)

# Сохранение карты в HTML-файл
m.save("114.html")