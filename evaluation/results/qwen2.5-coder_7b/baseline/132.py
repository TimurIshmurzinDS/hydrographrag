import pandas as pd
import folium

# Загрузка данных (пример)
data_lepsy = pd.read_csv('lepsy_data.csv')
data_tekes = pd.read_csv('tekes_data.csv')

# Предположим, что данные имеют следующую структуру:
# data['year'] - год
# data['flow'] - уровень стока

# Найдем год с самым высоким уровнем стока для каждой из рек
max_flow_lepsy = data_lepsy.loc[data_lepsy['flow'].idxmax()]
max_flow_tekes = data_tekes.loc[data_tekes['flow'].idxmax()]

print(f"Год с самым высоким уровнем стока в Lepsy River: {max_flow_lepsy['year']}")
print(f"Год с самым высоким уровнем стока в Tekes River: {max_flow_tekes['year']}")

# Визуализация данных на карте
m = folium.Map(location=[60.17, 24.93], zoom_start=8)

folium.Marker(
    location=[60.17, 24.93],
    popup=f"Год с самым высоким уровнем стока в Lepsy River: {max_flow_lepsy['year']}",
    icon=folium.Icon(color='red', icon='info-sign')
).add_to(m)

folium.Marker(
    location=[61.75, 24.93],
    popup=f"Год с самым высоким уровнем стока в Tekes River: {max_flow_tekes['year']}",
    icon=folium.Icon(color='blue', icon='info-sign')
).add_to(m)

m.save("132.html")