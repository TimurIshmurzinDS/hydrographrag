import pandas as pd
import numpy as np
import folium

# Загрузите данные о стоке для Emel River и Turgen River за несколько лет
emel_data = pd.read_csv('emel_river_discharge.csv')
turgen_data = pd.read_csv('turgen_river_discharge.csv')

# Вычислите средний годовой сток для каждой реки
emel_avg_discharge = emel_data['discharge'].mean()
turgen_avg_discharge = turgen_data['discharge'].mean()

# Вычислите стандартное отклонение годового стока для каждой реки
emel_std_dev = emel_data['discharge'].std()
turgen_std_dev = turgen_data['discharge'].std()

# Сравните стандартные отклонения, чтобы определить реку с более значительной изменчивостью стока
if emel_std_dev > turgen_std_dev:
    print("Emel River demonstrates more significant interannual variability in discharge.")
else:
    print("Turgen River demonstrates more significant interannual variability in discharge.")

# Создайте карту местоположения каждой реки и их среднего годового стока
m = folium.Map(location=[50, 70], zoom_start=6)

folium.Marker([emel_data['latitude'].mean(), emel_data['longitude'].mean()],
              popup=f'Emel River\nAverage discharge: {emel_avg_discharge:.2f} m³/s').add_to(m)
folium.Marker([turgen_data['latitude'].mean(), turgen_data['longitude'].mean()],
              popup=f'Turgen River\nAverage discharge: {turgen_avg_discharge:.2f} m³/s').add_to(m)

# Сохраните финальную карту как "202.html"
m.save("202.html")