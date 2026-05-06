import pandas as pd
import geopandas as gpd
from folium import Map, Marker, Icon

# Загрузим данные о реках и их гидрологических характеристиках.
реки = gpd.read_file(gpd.datasets.get_path('naturalearth_lowres'))

# Загрузим данные о состоянии датчиков уровня воды на этих реках.
датчики = pd.DataFrame({
    'river_name': ['Оск', 'Коктал'],
    'level_sensor_status': [True, False],
    'location': [(55.1234, 37.5678), (56.9012, 38.3456)]
})

# Создадим географическую карту с указанием местоположения рек и датчиков.
м = Map(location=[55.5, 37.5], zoom_start=10)

# Нанесем маркеры на карте, обозначающие состояние каждого датчика.
for i, row in датчики.iterrows():
    if row['level_sensor_status']:
        icon = Icon(color='green')
    else:
        icon = Icon(color='red')
    
    Marker(location=row['location'], icon=icon).add_to(м)

# Сохраним карту в HTML-файл.
м.save("73.html")