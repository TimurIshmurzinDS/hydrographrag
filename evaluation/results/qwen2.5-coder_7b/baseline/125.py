import pandas as pd
import folium

# Пример данных (замените на реальные данные)
data = {
    'Date': pd.date_range(start='1/1/2018', periods=5*365, freq='D'),
    'Tekes_River': [100, 105, 110, 115, 120] * 365,
    'Bayankol_River': [200, 205, 210, 215, 220] * 365
}

# Создание DataFrame
df = pd.DataFrame(data)

# Преобразование даты в формат datetime
df['Date'] = pd.to_datetime(df['Date'])

# Вычисление среднего значения за последние 5 лет для каждой реки
mean_tekes = df['Tekes_River'].mean()
mean_bayankol = df['Bayankol_River'].mean()

# Рассчет изменения по сравнению со средним значением
df['Change_Tekes'] = (df['Tekes_River'] - mean_tekes) / mean_tekes * 100
df['Change_Bayankol'] = (df['Bayankol_River'] - mean_bayankol) / mean_bayankol * 100

# Определение максимального изменения
max_change_tekes = df['Change_Tekes'].max()
max_change_bayankol = df['Change_Bayankol'].max()

# Вывод результатов
print(f"Максимальное изменение расхода воды для Tekes River: {max_change_tekes:.2f}%")
print(f"Максимальное изменение расхода воды для Bayankol River: {max_change_bayankol:.2f}%")

# Создание карты с отметками
m = folium.Map(location=[50, 10], zoom_start=4)

folium.Marker([50, 10], popup='Tekes River', icon=folium.Icon(color='blue')).add_to(m)
folium.Marker([50.5, 10.5], popup='Bayankol River', icon=folium.Icon(color='red')).add_to(m)

# Сохранение карты
m.save("125.html")