import folium
from folium.plugins import HeatMap

# Сбор данных о притоках реки Тентек (предположительно, данные хранятся в файле CSV)
import pandas as pd
df = pd.read_csv('tentek_river_data.csv')

# Создание географической модели разветвления притоков
# Предполагается, что координаты точек хранятся в столбцах 'lat' и 'lon'
model = folium.Map(location=[df['lat'].mean(), df['lon'].mean()], zoom_start=10)

# Преобразование модели в форму пирога
# Используем функцию, которая преобразует географическую модель в форму пирога
def create_pie_form(model):
    # Создаем новую карту для визуализации формы пирога
    pie_map = folium.Map(location=[model.location_lat, model.location_lon], zoom_start=10)
    
    # Добавляем слой с данными о притоках на форму пирога
    heat_data = [(row['lat'], row['lon']) for index, row in df.iterrows()]
    HeatMap(heat_data, radius=20).add_to(pie_map)
    
    return pie_map

pie_form = create_pie_form(model)

# Визуализация результата на карте
pie_form.save("242.html")