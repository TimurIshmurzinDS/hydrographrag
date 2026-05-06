import pandas as pd
import numpy as np
from scipy.stats import zscore
import folium

# Предположим, что у нас есть данные о потоковом расходе воды в формате CSV
# Структура данных: дата, река (Aksu или Temirlik), потоковый расход (куб. м/с)

# Загрузка данных
data = pd.read_csv('water_flow_data.csv', parse_dates=['date'])

# Разделение данных по рекам
aksu_data = data[data['river'] == 'Aksu']
temirlik_data = data[data['river'] == 'Temirlik']

# Функция для оценки риска засухи на основе Z-оценки
def assess_drought_risk(flow_data):
    # Вычисление среднего и стандартного отклонения потокового расхода
    mean_flow = flow_data['flow'].mean()
    std_dev_flow = flow_data['flow'].std()
    
    # Вычисление Z-оценки для каждого значения потокового расхода
    z_scores = (flow_data['flow'] - mean_flow) / std_dev_flow
    
    # Оценка риска засухи: если Z-оценка меньше -2, считаем это засухой
    drought_risk = np.where(z_scores < -2, 1, 0)
    
    return drought_risk

# Оценка риска засухи для каждой реки
aksu_drought_risk = assess_drought_risk(aksu_data)
temirlik_drought_risk = assess_drought_risk(temirlik_data)

# Добавление столбца с риском засухи в исходные данные
aksu_data['drought_risk'] = aksu_drought_risk
temirlik_data['drought_risk'] = temirlik_drought_risk

# Оценка общего риска для каждой реки
aksu_total_risk = aksu_drought_risk.mean()
temirlik_total_risk = temirlik_drought_risk.mean()

print(f"Риск засухи Aksu River: {aksu_total_risk:.2f}")
print(f"Риск засухи Temirlik River: {temirlik_total_risk:.2f}")

# Определение наиболее рискованной реки
if aksu_total_risk > temirlik_total_risk:
    riskier_river = "Aksu River"
else:
    riskier_river = "Temirlik River"

print(f"Более рискованная река: {riskier_river}")

# Визуализация на карте
# Предположим, что у нас есть координаты для каждой из рек и фермерских хозяйств

# Координаты рек
aksu_coords = [42.860911, 75.313374]  # Примерные координаты Aksu River
temirlik_coords = [42.858889, 75.311111]  # Примерные координаты Temirlik River

# Координаты фермерских хозяйств (пример)
farms_coords = [
    [42.860000, 75.310000],
    [42.865000, 75.315000],
    [42.859000, 75.314000]
]

# Создание карты
m = folium.Map(location=[42.860000, 75.310000], zoom_start=13)

# Добавление маркеров для рек
folium.Marker(aksu_coords, popup='Aksu River', icon=folium.Icon(color='blue')).add_to(m)
folium.Marker(temirlik_coords, popup='Temirlik River', icon=folium.Icon(color='green')).add_to(m)

# Добавление маркеров для фермерских хозяйств
for coord in farms_coords:
    folium.Marker(coord, popup='Фермерское хозяйство').add_to(m)

# Сохранение карты в HTML файл
m.save("111.html")