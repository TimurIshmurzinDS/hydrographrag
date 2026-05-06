import pandas as pd
import folium

# Пример данных (замените на реальные данные)
data = {
    'Year': [2013, 2014, 2015, 2016, 2017, 2018, 2019, 2020, 2021, 2022],
    'Bayankol': [100, 105, 110, 115, 120, 125, 130, 135, 140, 145],
    'Shilik': [80, 85, 90, 95, 100, 105, 110, 115, 120, 125]
}

# Создание DataFrame
df = pd.DataFrame(data)

# Вычисление среднего расхода воды для каждого ручья
mean_bayankol = df['Bayankol'].mean()
mean_shilik = df['Shilik'].mean()

print(f"Средний расход воды в Bayankol за последние 10 лет: {mean_bayankol}")
print(f"Средний расход воды в Shilik за последние 10 лет: {mean_shilik}")

# Создание карты
m = folium.Map(location=[52.37, 94.6], zoom_start=6)

# Добавление маркеров с средними значениями расхода воды
folium.Marker([52.37, 94.6], popup=f"Средний расход воды в Bayankol: {mean_bayankol} м³/с", icon=folium.Icon(color='blue')).add_to(m)
folium.Marker([52.38, 94.61], popup=f"Средний расход воды в Shilik: {mean_shilik} м³/с", icon=folium.Icon(color='red')).add_to(m)

# Сохранение карты
m.save("121.html")