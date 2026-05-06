import pandas as pd
import folium

# Пример данных (замените на реальные данные)
data = {
    'date': ['2023-06-01', '2023-06-02', '2023-06-03', '2023-06-04', '2023-06-05'],
    'Baskan_River': [10, 15, 20, 25, 30],
    'Prokhodnaya_River': [8, 12, 17, 22, 27]
}

# Создание DataFrame
df = pd.DataFrame(data)
df['date'] = pd.to_datetime(df['date'])

# Определение периода пика половодья (например, максимальный уровень на обеих реках)
peak_period = df[(df['Baskan_River'] == df['Baskan_River'].max()) & 
                 (df['Prokhodnaya_River'] == df['Prokhodnaya_River'].max())]

# Вычисление среднего расхода воды в период пика половодья
mean_Baskan = peak_period['Baskan_River'].mean()
mean_Prokhodnaya = peak_period['Prokhodnaya_River'].mean()

print(f"Средний расход на Baskan River в период пика половодья: {mean_Baskan}")
print(f"Средний расход на Prokhodnaya River в период пика половодья: {mean_Prokhodnaya}")

# Визуализация данных на карте
m = folium.Map(location=[50, 30], zoom_start=6)

folium.Marker([50, 30], popup='Baskan River', icon=folium.Icon(color='blue')).add_to(m)
folium.Marker([51, 31], popup='Prokhodnaya River', icon=folium.Icon(color='red')).add_to(m)

# Сохранение карты
m.save("89.html")