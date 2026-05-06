import folium
from folium.plugins import HeatMap

# Пример данных: текущий расход воды и критические значения
current_flow = 150  # Текущий расход воды в реке (м³/с)
critical_flows = [100, 200, 300]  # Критические значения расхода воды (м³/с)

# Расчет индекса риска
risk_index = sum(1 for cf in critical_flows if current_flow > cf) / len(critical_flows)

# Создание карты
m = folium.Map(location=[50.45, 30.52], zoom_start=12)

# Добавление маркера с индексом риска
folium.Marker(
    location=[50.45, 30.52],
    popup=f"Индекс риска наводнения: {risk_index:.2f}",
    icon=folium.Icon(color='red', icon='info-sign')
).add_to(m)

# Сохранение карты
m.save("30.html")