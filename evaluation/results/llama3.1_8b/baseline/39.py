import pandas as pd
from folium import Map, Marker

# Сбор данных
data = {
    'регион': ['Иллирийский'],
    'площадь_бассейна': [100000],  # в квадратных километрах
    'количество_населения': [50000],
    'площадь_посевов': [20000],  # в гектарах
    'вода_на_1_гектар': [1000]  # в кубических метров
}

df = pd.DataFrame(data)

# Определение потребности в воде
def calculate_water_need(area, water_per_ha):
    return area * water_per_ha

# Расчет объема воды
water_volume = df['площадь_бассейна'].values[0] * df['вода_на_1_гектар'].values[0]

print(f'Объем воды, используемый для полива: {water_volume} кубических метров')

# Визуализация на карте
m = Map(location=[45.5, 30], zoom_start=6)
Marker(location=[45.5, 30], popup='Река Или').add_to(m)

# Сохранение карты в файл
m.save("39.html")