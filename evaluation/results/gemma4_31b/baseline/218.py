import numpy as np
import folium
from folium.plugins import MarkerCluster

def calculate_jupiter_gravity_impact():
    # 1. Константы и координаты
    # Координаты реки Баскан (примерная центральная точка)
    baskan_coords = [45.35, 33.50] 
    
    # Гравитационная постоянная G (м^3 кг^-1 с^-2)
    G = 6.67430e-11
    # Масса Юпитера (кг)
    M_jupiter = 1.898e27
    # Масса гипотетического объема воды в реке (кг) - например, 1 кубический метр
    M_water = 1000 
    
    # Среднее расстояние от Земли до Юпитера (метры)
    # Варьируется от 588 млн км до 968 млн км
    dist_min = 588e9
    dist_max = 968e9
    
    # Симулируем текущее расстояние (для примера возьмем среднее с небольшим шумом)
    current_dist = np.random.uniform(dist_min, dist_max)
    
    # 2. Расчет силы гравитации (Закон Ньютона)
    force = G * (M_jupiter * M_water) / (current_dist**2)
    
    # 3. Гипотетическая модель изменения уровня воды (Delta h)
    # В реальности это значение будет стремиться к нулю, 
    # но для моделирования введем коэффициент чувствительности
    sensitivity_coeff = 1e-12 
    delta_h = force * sensitivity_coeff
    
    # Базовый уровень воды в реке (условные метры)
    base_level = 2.5 
    final_level = base_level + delta_h
    
    return {
        "coords": baskan_coords,
        "force": force,
        "delta_h": delta_h,
        "final_level": final_level,
        "distance": current_dist
    }

def create_gis_map(data):
    # Создание карты вокруг реки Баскан
    m = folium.Map(location=data["coords"], zoom_start=10, tiles="OpenStreetMap")
    
    # Добавление маркера с данными
    popup_text = (
        f"<b>Река Баскан: Гравитационный мониторинг</b><br>"
        f"Расстояние до Юпитера: {data['distance']:.2e} м<br>"
        f"Сила притяжения: {data['force']:.2e} Н<br>"
        f"Влияние на уровень: {data['delta_h']:.2e} м<br>"
        f"Итоговый уровень: {data['final_level']:.6f} м"
    )
    
    folium.Marker(
        location=data["coords"],
        popup=folium.Popup(popup_text, max_width=300),
        icon=folium.Icon(color="blue", icon="info-sign")
    ).add_to(m)
    
    # Добавление нескольких точек вдоль русла для имитации сети датчиков
    offsets = [[0.1, 0.1], [0.2, -0.1], [-0.1, 0.2], [0.05, -0.2]]
    cluster = MarkerCluster().add_to(m)
    
    for off in offsets:
        point = [data["coords"][0] + off[0], data["coords"][1] + off[1]]
        folium.CircleMarker(
            location=point,
            radius=5,
            color="red",
            fill=True,
            popup=f"Датчик уровня: {data['final_level']:.6f} м"
        ).add_to(cluster)

    # Сохранение карты
    m.save("218.html")
    print("Map has been saved as 218.html")

if __name__ == "__main__":
    # Выполнение моделирования
    result_data = calculate_jupiter_gravity_impact()
    
    # Визуализация
    create_gis_map(result_data)
    
    print(f"Расчет завершен.")
    print(f"Текущий уровень воды с учетом Юпитера: {result_data['final_level']:.10f} м")