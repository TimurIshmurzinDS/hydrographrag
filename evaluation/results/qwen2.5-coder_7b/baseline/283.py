import pandas as pd
import folium

# Пример данных: загрузка двух временных рядов из CSV файлов
df1 = pd.read_csv('time_series_1.csv', parse_dates=['date'], index_col='date')
df2 = pd.read_csv('time_series_2.csv', parse_dates=['date'], index_col='date')

# Убедитесь, что индексы совпадают
if not df1.index.equals(df2.index):
    raise ValueError("Индексы временных рядов не совпадают")

# Сравнение данных
comparison_results = {
    'mean_diff': (df1.mean() - df2.mean()).abs(),
    'std_dev_diff': (df1.std() - df2.std()).abs(),
    'correlation': df1.corrwith(df2)
}

# Визуализация на карте
m = folium.Map(location=[df1.index[0].latitude, df1.index[0].longitude], zoom_start=5)

for idx, row in df1.iterrows():
    folium.Marker(
        location=[row['latitude'], row['longitude']],
        popup=f"Time Series 1: {row['value']}, Time Series 2: {df2.loc[idx]['value']}",
        icon=folium.Icon(color='red' if row['value'] > df2.loc[idx]['value'] else 'green')
    ).add_to(m)

m.save("283.html")