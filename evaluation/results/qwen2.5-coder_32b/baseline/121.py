import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import folium

# Предполагается, что данные о расходе воды представлены в CSV файлах с колонками 'date' и 'discharge'
# Пример данных: date (YYYY-MM-DD), discharge (куб. м/с)

# Загрузка данных
bayankol_data = pd.read_csv('bayankol_discharge.csv', parse_dates=['date'])
shilik_data = pd.read_csv('shilik_discharge.csv', parse_dates=['date'])

# Фильтрация данных за последние 10 лет
end_date = bayankol_data['date'].max()
start_date = end_date - pd.DateOffset(years=10)

bayankol_data = bayankol_data[(bayankol_data['date'] >= start_date) & (bayankol_data['date'] <= end_date)]
shilik_data = shilik_data[(shilik_data['date'] >= start_date) & (shilik_data['date'] <= end_date)]

# Обработка данных: удаление пропусков
bayankol_data.dropna(subset=['discharge'], inplace=True)
shilik_data.dropna(subset=['discharge'], inplace=True)

# Вычисление среднего расхода воды за последние 10 лет
avg_bayankol_discharge = bayankol_data['discharge'].mean()
avg_shilik_discharge = shilik_data['discharge'].mean()

print(f"Средний расход воды в реке Bayankol River: {avg_bayankol_discharge:.2f} куб. м/с")
print(f"Средний расход воды в реке Shilik River: {avg_shilik_discharge:.2f} куб. м/с")

# Визуализация результатов
plt.figure(figsize=(10, 5))
plt.bar(['Bayankol River', 'Shilik River'], [avg_bayankol_discharge, avg_shilik_discharge], color=['blue', 'green'])
plt.title('Средний расход воды в реках за последние 10 лет')
plt.ylabel('Расход воды (куб. м/с)')
plt.show()

# Географическая визуализация
# Координаты рек: примерные значения, замените на точные, если есть
bayankol_coords = [45.2671, 89.0322]  # Примерные координаты Bayankol River
shilik_coords = [45.2671, 89.0322]    # Примерные координаты Shilik River

m = folium.Map(location=[(bayankol_coords[0] + shilik_coords[0]) / 2, (bayankol_coords[1] + shilik_coords[1]) / 2], zoom_start=10)

folium.Marker(
    location=bayankol_coords,
    popup=f"Bayankol River\nСредний расход: {avg_bayankol_discharge:.2f} куб. м/с",
    icon=folium.Icon(color='blue')
).add_to(m)

folium.Marker(
    location=shilik_coords,
    popup=f"Shilik River\nСредний расход: {avg_shilik_discharge:.2f} куб. м/с",
    icon=folium.Icon(color='green')
).add_to(m)

m.save("121.html")