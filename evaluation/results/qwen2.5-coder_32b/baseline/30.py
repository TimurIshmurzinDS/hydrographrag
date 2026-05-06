import folium

# Шаг 1: Сбор данных (примерные данные для демонстрации)
current_discharge = 250  # текущий расход воды в м3/с

# Шаг 2: Определение критических значений
normal_discharge = 150   # нормативный уровень расхода воды в м3/с
critical_discharge = 400 # критический уровень расхода воды в м3/с

# Шаг 3: Расчет индекса риска
def calculate_flood_risk_index(current, normal, critical):
    if current <= normal:
        return 0.0
    elif current > normal and current < critical:
        return (current - normal) / (critical - normal)
    else:
        return 1.0

flood_risk_index = calculate_flood_risk_index(current_discharge, normal_discharge, critical_discharge)

# Шаг 4: Визуализация результатов
# Координаты реки Prokhodnaya River (примерные координаты)
latitude = 56.3270
longitude = 44.0028

m = folium.Map(location=[latitude, longitude], zoom_start=12)

# Добавление маркера с индексом риска
folium.Marker(
    [latitude, longitude],
    popup=f"Индекс риска наводнения: {flood_risk_index:.2f}",
    icon=folium.Icon(color='red' if flood_risk_index >= 0.8 else 'blue')
).add_to(m)

# Сохранение карты в файл
m.save("30.html")

print(f"Индекс риска наводнения: {flood_risk_index:.2f}")