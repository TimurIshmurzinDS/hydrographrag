import folium
import pandas as pd

def calculate_flood_risk(current_discharge, critical_discharge):
    """
    Рассчитывает индекс риска наводнения и определяет категорию.
    """
    fri = current_discharge / critical_discharge
    
    if fri < 0.6:
        risk_level = "Низкий"
        color = "green"
    elif 0.6 <= fri < 1.0:
        risk_level = "Средний"
        color = "orange"
    else:
        risk_level = "Высокий"
        color = "red"
        
    return fri, risk_level, color

# --- Исходные данные ---
# Координаты реки Prokhodnaya River (симуляция геометрии)
river_coords = [
    [55.1234, 37.4567],
    [55.1250, 37.4600],
    [55.1300, 37.4650],
    [55.1350, 37.4700],
    [55.1400, 37.4750],
    [55.1450, 37.4800],
    [55.1500, 37.4850]
]

# Гидрологические параметры
current_q = 115.0  # Текущий расход в м3/с
critical_q = 100.0 # Критический порог расхода в м3/с

# Расчет риска
fri_value, risk_cat, risk_color = calculate_flood_risk(current_q, critical_q)

print(f"Текущий расход: {current_q} м3/с")
print(f"Критический расход: {critical_q} м3/с")
print(f"Индекс риска (FRI): {fri_value:.2f}")
print(f"Уровень риска: {risk_cat}")

# --- Визуализация на карте ---
# Создание карты, центрированной на реке
m = folium.Map(location=[55.135, 37.47], zoom_start=13, tiles="CartoDB positron")

# Отрисовка русла реки с цветом в зависимости от риска
folium.PolyLine(
    locations=river_coords, 
    color=risk_color, 
    weight=6, 
    opacity=0.8, 
    tooltip=f"Река Prokhodnaya: Риск {risk_cat}"
).add_to(m)

# Добавление маркера гидропоста
folium.CircleMarker(
    location=river_coords[0], 
    radius=7, 
    color='blue', 
    fill=True, 
    fill_color='blue', 
    popup=f"Гидропост: Q={current_q} м3/с"
).add_to(m)

# Добавление информационной панели (текстовый элемент)
info_text = f"<b>Анализ риска наводнения</b><br>Река: Prokhodnaya River<br>FRI: {fri_value:.2f}<br>Статус: {risk_cat}"
folium.Popup(info_text).add_to(m) # Note: Popup usually needs a trigger, but we can use a marker for the legend

# Создаем отдельный маркер-легенду
folium.Marker(
    location=[55.120, 37.450],
    icon=folium.Icon(color='gray', icon='info-sign'),
    popup=folium.Popup(info_text, max_width=200)
).add_to(m)

# Сохранение карты
m.save("30.html")
print("Карта успешно сохранена в файл 30.html")