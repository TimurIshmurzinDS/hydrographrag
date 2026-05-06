import pandas as pd
import folium

# Загрузка данных о расходе воды
data_tekes = pd.read_csv('tekess.csv')
data_bayankol = pd.read_csv('bayankol.csv')

# Подготовка данных к анализу
data_tekes['date'] = pd.to_datetime(data_tekes['date'])
data_bayankol['date'] = pd.to_datetime(data_bayankol['date'])

# Рассчет среднего значения расхода воды за последние 5 лет для каждой реки
tekess_avg_flow = data_tekes.groupby('date')['flow'].mean().tail(5).mean()
bayankol_avg_flow = data_bayankol.groupby('date')['flow'].mean().tail(5).mean()

# Рассчет процентного увеличения расхода воды по сравнению со средним значением для каждой реки
tekess_percent_increase = ((data_tekes['flow'] - tekess_avg_flow) / tekess_avg_flow) * 100
bayankol_percent_increase = ((data_bayankol['flow'] - bayankol_avg_flow) / bayankol_avg_flow) * 100

# Сравнение процентных увеличений для обоих рек и определение, какая из них показала наибольшее увеличение
max_increase = max(tekess_percent_increase.max(), bayankol_percent_increase.max())

if tekess_percent_increase.max() > bayankol_percent_increase.max():
    river_with_max_increase = 'Tekes River'
else:
    river_with_max_increase = 'Bayankol River'

# Создание карты с результатами
m = folium.Map(location=[43.5, 79], zoom_start=6)

folium.Marker([43.5, 79], popup=f'Река с наибольшим увеличением расхода воды: {river_with_max_increase}').add_to(m)
folium.Marker([43.2, 78], popup=f'Процентное увеличение расхода воды для Tekes River: {tekess_percent_increase.max()}%').add_to(m)
folium.Marker([43.8, 80], popup=f'Процентное увеличение расхода воды для Bayankol River: {bayankol_percent_increase.max()}%').add_to(m)

m.save("125.html")