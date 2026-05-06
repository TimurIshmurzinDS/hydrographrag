import folium
from folium.plugins import HeatMap

# Топография русла реки Дос (пример данных)
river_data = [
    [56.01, 84.92],
    [56.02, 84.93],
    [56.03, 84.94],
    [56.04, 84.95],
    [56.05, 84.96]
]

# Создание карты
m = folium.Map(location=[56.03, 84.94], zoom_start=12)

# Добавление теплового слоя для топографии русла
HeatMap(river_data).add_to(m)

# Сохранение карты
m.save("244.html")

print("Карта сохранена как '244.html'")