import pandas as pd
from folium import Map, Marker
import matplotlib.pyplot as plt

# Загрузите данные о стоке для реки Лепсы и Текеса в формате CSV
lepsy_data = pd.read_csv('lepsy_flow.csv')
tekis_data = pd.read_csv('tekis_flow.csv')

# Проанализируйте данные, чтобы найти год с самым высоким уровнем стока для каждой реки
max_lepsy_year = lepsy_data['year'].loc[lepsy_data['flow'].idxmax()]
max_tekis_year = tekis_data['year'].loc[tekis_data['flow'].idxmax()]

# Сравните эти два года и определите, какой из них имеет самый высокий уровень стока
if lepsy_data.loc[lepsy_data['year'] == max_lepsy_year, 'flow'].values[0] > tekis_data.loc[tekis_data['year'] == max_tekis_year, 'flow'].values[0]:
    max_flow_year = max_lepsy_year
else:
    max_flow_year = max_tekis_year

# Визуализируйте результаты на карте с помощью библиотеки Folium
m = Map(location=[55.5, 60], zoom_start=6)
Marker(location=[55.5, 60], popup=f'Год с самым высоким уровнем стока: {max_flow_year}').add_to(m)

# Сохраните карту в файл
m.save("132.html")

# Визуализируйте данные о стоке для обоих рек на графике
plt.figure(figsize=(10, 6))
plt.plot(lepsy_data['year'], lepsy_data['flow'], label='Река Лепсы')
plt.plot(tekis_data['year'], tekis_data['flow'], label='Река Текес')
plt.xlabel('Год')
plt.ylabel('Уровень стока')
plt.title('Сравнение уровня стока в реках Лепсы и Текеса')
plt.legend()
plt.show()

print(f'Год с самым высоким уровнем стока: {max_flow_year}')