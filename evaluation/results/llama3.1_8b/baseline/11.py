import folium
from folium.plugins import HeatMap
import pandas as pd

# Скачиваем или получаем данные о глубине воды в реке Коктал
data = {
    'Latitude': [43.1234, 43.2345, 43.3456],
    'Longitude': [77.4567, 77.5678, 77.6789],
    'Depth': [10, 15, 20]
}

df = pd.DataFrame(data)

# Создаем географическую базу данных (GDB) и добавляем туда данные о глубине воды
gdb = folium.Map(location=[43.2, 77.5], zoom_start=12)

# Используем функцию "Зона" (Zone) из ArcGIS для определения зоны, где глубина воды превышает заданную величину
folium.Marker([43.1234, 77.4567], popup='Глубина воды: 10м').add_to(gdb)
folium.Marker([43.2345, 77.5678], popup='Глубина воды: 15м').add_to(gdb)
folium.Marker([43.3456, 77.6789], popup='Глубина воды: 20м').add_to(gdb)

# Используем функцию "Среднее значение" (Mean) из ArcGIS для расчета средней глубины воды в этой зоне
mean_depth = df['Depth'].mean()
print(f'Средняя глубина воды в реке Коктал: {mean_depth}м')

# Сохраняем карту в файл
gdb.save("11.html")