import pandas as pd
from folium import Map, Marker
from folium.plugins import HeatMap

# Загрузите данные о сельскохозяйственных угодьях в виде геометрических объектов (геометрии)
agriculture_data = pd.read_csv('агрокультура.csv')

# Загрузите данные о качестве воды в реке Лепси
water_quality_data = pd.read_csv('качество_воды.csv')

# Объедините данные о сельскохозяйственных угодьях и качестве воды
merged_data = pd.merge(agriculture_data, water_quality_data, on='id')

# Оцените влияние каждого типа сельскохозяйственных угодий на качество воды
correlation_matrix = merged_data.corr()
print(correlation_matrix)

# Создайте интерактивную карту с помощью библиотеки Folium
m = Map(location=[55.8, 28.2], zoom_start=10)
heat_map = HeatMap(merged_data[['x', 'y']].values, radius=5, blur=3, max_val=1000)

# Добавьте маркеры для каждого типа сельскохозяйственных угодий
for index, row in merged_data.iterrows():
    Marker(location=[row['x'], row['y']], popup=row['тип_угодья']).add_to(m)

# Добавьте слой с тепловой картой
m.add_child(heat_map)

# Сохраните карту в файл
m.save("42.html")