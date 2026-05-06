import folium
import pandas as pd

# 1. Подготовка данных
def prepare_data():
    # Загрузка данных о высоте реки, количестве осадков и местоположении населенных пунктов
    river_heights = pd.read_csv('river_heights.csv')
    rainfall_data = pd.read_csv('rainfall_data.csv')
    settlements = pd.read_csv('settlements.csv')

    # Объединение данных о высоте реки и количестве осадков по названию реки
    data = pd.merge(river_heights, rainfall_data, on='river_name')

    return data, settlements

# 2. Определение риска наводнений
def calculate_risk(data):
    # Рассчитать среднюю высоту реки и количество осадков за определенный период времени для каждой реки
    mean_height = data['height'].mean()
    mean_rainfall = data['rainfall'].mean()

    # Использовать формулу риска наводнений, основанную на средней высоте реки и количестве осадков,
    # чтобы получить индекс риска наводнений для каждой реки
    risk_index = mean_height * mean_rainfall

    return risk_index

# 3. Визуализация результатов
def visualize_results(data, settlements, risk_index):
    # Создать карту с помощью библиотеки `folium`, отображающую местоположение рек,
    # населенных пунктов вдоль рек и индекс риска наводнений
    m = folium.Map(location=[43.2641, 72.5729], zoom_start=8)

    # Отобразить реки на карте
    for _, row in data.iterrows():
        folium.PolyLine(locations=[(row['lat'], row['lon'])], weight=2, color='blue').add_to(m)

    # Отобразить населенные пункты вдоль рек на карте
    for _, row in settlements.iterrows():
        folium.Marker([row['lat'], row['lon']], popup=f'Населенный пункт: {row["name"]}\nИндекс риска наводнений: {risk_index}').add_to(m)

    # Сохранить финальную карту как "151.html"
    m.save("151.html")

# Основной код
data, settlements = prepare_data()
risk_index = calculate_risk(data)
visualize_results(data, settlements, risk_index)