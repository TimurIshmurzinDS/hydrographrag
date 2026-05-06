import pandas as pd
import folium

# Пример данных: расход воды в реке Karkara River за последние два десятилетия (в миллилитрах)
data = {
    'Year': [2010, 2011, 2012, 2013, 2014, 2015, 2016, 2017, 2018, 2019, 2020, 2021, 2022],
    'Flow': [1000, 1050, 1100, 1150, 1200, 1250, 1300, 1350, 1400, 1450, 1500, 1550, 1600]
}

# Создание DataFrame
df = pd.DataFrame(data)

# Вычисление среднего расхода воды за последние два десятилетия
mean_flow_last_decade = df['Flow'].tail(10).mean()
mean_flow_prev_decade = df['Flow'].head(10).mean()

# Рассчет разницы в расходе воды
flow_difference = mean_flow_last_decade - mean_flow_prev_decade

print(f"Средний расход воды за последние десятилетия: {mean_flow_last_decade:.2f} мл")
print(f"Средний расход воды за предыдущее десятилетие: {mean_flow_prev_decade:.2f} мл")
print(f"Разница в расходе воды: {flow_difference:.2f} мл")

# Визуализация данных на карте
m = folium.Map(location=[40.7128, 35.1695], zoom_start=5)

folium.Marker([40.7128, 35.1695], popup='Karkara River').add_to(m)

# Сохранение карты
m.save("54.html")