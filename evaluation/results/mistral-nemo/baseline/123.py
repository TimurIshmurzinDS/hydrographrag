import pandas as pd
from statsmodels.tsa.seasonal import seasonal_decompose
import folium

# Загрузим данные о стоке рек Kurty и Sharyn в формате временного ряда.
kurty_data = pd.read_csv('kurty_river_discharge.csv', parse_dates=['date'], index_col='date')
sharyn_data = pd.read_csv('sharyn_river_discharge.csv', parse_dates=['date'], index_col='date')

# Вычислим тренд для каждого из этих рядов данных.
kurty_trend = seasonal_decompose(kurty_data['discharge']).trend
sharyn_trend = seasonal_decompose(sharyn_data['discharge']).trend

# Сравним эти тренды, чтобы определить, совпадают ли они.
if kurty_trend.equals(sharyn_trend):
    print("Тренды совпадают.")
else:
    print("Тренды не совпадают.")

# Визуализируем данные на карте с помощью библиотеки folium.
m = folium.Map(location=[50, 60], zoom_start=4)

folium.Choropleth(
    geo_data='world_countries.json',
    data=kurty_data,
    columns=['date', 'discharge'],
    key_on='feature.properties.name',
    fill_color='YlGnBu',
    fill_opacity=0.7,
    line_opacity=0.8,
    highlight=True
).add_to(m)

folium.LayerControl().add_to(m)

# Сохраним карту в формате HTML.
m.save("123.html")