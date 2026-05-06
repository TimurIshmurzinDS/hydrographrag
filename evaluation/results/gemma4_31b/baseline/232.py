import numpy as np
import folium
import math

def get_kaskelen_water_level():
    """
    Имитация получения данных с датчика уровня воды в р. Каскелен.
    Возвращает значение в метрах.
    """
    # В реальности здесь был бы запрос к API гидрологической службы
    return np.random.uniform(0.5, 5.0)

def calculate_moon_trajectory(water_level):
    """
    Расчет параметров траектории на основе уровня воды.
    Используется упрощенная модель Гомановского перелета.
    """
    # Константы
    MU_EARTH = 3.986004418e14  # Гравитационный параметр Земли (м^3/с^2)
    R_EARTH = 6371000          # Радиус Земли (м)
    R_LEO = 6571000            # Радиус низкой околоземной орбиты (R_earth + 200км)
    R_MOON = 384400000         # Среднее расстояние до Луны (м)

    # 1. Расчет LRI (Launch Readiness Index)
    # Предположим, идеальный уровень воды для запуска - 2.5 метра
    ideal_level = 2.5
    lri = 1.0 / (1.0 + abs(water_level - ideal_level))
    
    # 2. Расчет скорости для Гомановского перелета
    # Скорость на LEO
    v_leo = math.sqrt(MU_EARTH / R_LEO)
    
    # Скорость в перигее переходного эллипса
    v_perigee = math.sqrt(MU_EARTH * (2/R_LEO - 2/(R_LEO + R_MOON)))
    
    # Необходимый импульс (Delta-V)
    delta_v = v_perigee - v_leo
    
    # Вносим "абсурдную" зависимость от уровня воды в итоговый расчет
    # Если LRI низкий, добавляем "поправку на нестабильность"
    final_delta_v = delta_v * (1 + (1 - lri) * 0.01)
    
    return final_delta_v, lri

def main():
    # Координаты реки Каскелен (примерные)
    kaskelen_coords = [43.23, 77.15]
    
    # Получаем данные
    water_level = get_kaskelen_water_level()
    delta_v, lri = calculate_moon_trajectory(water_level)
    
    print(f"--- Данные мониторинга р. Каскелен ---")
    print(f"Текущий уровень воды: {water_level:.2f} м")
    print(f"Индекс готовности к запуску (LRI): {lri:.4f}")
    print(f"Расчетная Delta-V для полета на Луну: {delta_v:.2f} м/с")
    
    # Визуализация на карте
    # Создаем карту, центрированную на Каскелене
    m = folium.Map(location=kaskelen_coords, zoom_start=10, tiles="CartoDB positron")
    
    # Маркер уровня воды
    folium.Marker(
        location=kaskelen_coords,
        popup=f"Датчик р. Каскелен\nУровень: {water_level:.2f}м\nLRI: {lri:.2f}",
        tooltip="Точка замера воды",
        icon=folium.Icon(color="blue", icon="info-sign")
    ).add_to(m)
    
    # Гипотетическая точка запуска (рядом)
    launch_site = [43.25, 77.20]
    folium.Marker(
        location=launch_site,
        popup=f"Космодром 'Каскелен-1'\nТребуемая Delta-V: {delta_v:.2f} м/с",
        tooltip="Точка старта",
        icon=folium.Icon(color="red", icon="rocket")
    ).add_to(m)
    
    # Рисуем линию "связи" между рекой и космодромом
    folium.PolyLine([kaskelen_coords, launch_site], color="green", weight=2.5, opacity=0.8).add_to(m)
    
    # Сохранение карты
    m.save("232.html")
    print("\nКарта сохранена в файл 232.html")

if __name__ == "__main__":
    main()