import pandas as pd
import folium
from datetime import datetime

# Пример данных (замените на реальные данные)
data = {
    'date': ['2019-06-01', '2019-07-01', '2019-08-01', '2019-12-01', '2019-01-01', '2019-02-01'],
    'flow': [100, 150, 200, 300, 400, 500]
}

# Преобразование данных в DataFrame
df = pd.DataFrame(data)
df['date'] = pd.to_datetime(df['date'])

# Разделение данных на летние и зимние периоды
df['season'] = df['date'].dt.month.apply(lambda x: 'Лето' if 6 <= x <= 8 else 'Зима')

# Вычисление среднего расхода воды для каждого периода
mean_flow_summer = df[df['season'] == 'Лето']['flow'].mean()
mean_flow_winter = df[df['season'] == 'Зима']['flow'].mean()

print(f"Средний расход воды в летнем периоде: {mean_flow_summer}")
print(f"Средний расход воды в зимнем периоде: {mean_flow_winter}")

# Визуализация данных на карте
m = folium.Map(location=[50.46, 30.52], zoom_start=10)

folium.Marker([50.46, 30.52], popup='Kurty River').add_to(m)

# Добавление меток для среднего расхода воды
folium.CircleMarker(
    location=[50.46, 30.52],
    radius=10,
    color='red',
    fill=True,
    fill_color='red',
    popup=f'Средний расход воды в летнем периоде: {mean_flow_summer}',
    tooltip='Лето'
).add_to(m)

folium.CircleMarker(
    location=[50.46, 30.52],
    radius=10,
    color='blue',
    fill=True,
    fill_color='blue',
    popup=f'Средний расход воды в зимнем периоде: {mean_flow_winter}',
    tooltip='Зима'
).add_to(m)

# Сохранение карты
m.save("51.html")